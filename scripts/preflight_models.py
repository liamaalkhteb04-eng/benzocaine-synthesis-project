"""Preflight an input and existing local model assets without running inference."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from _runtime import ROOT, expand_runtime_values, load, load_runtime_config


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def run_probe(python, code, args=(), extra_env=None, timeout=300):
    env=os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONIOENCODING='utf-8',
               HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',WANDB_MODE='disabled')
    for key in ('UPSTAGE_API_KEY','GEMINI_API_KEY','WANDB_API_KEY'): env.pop(key,None)
    if extra_env: env.update(extra_env)
    proc=subprocess.run([str(python),'-B','-c',code,*map(str,args)],capture_output=True,
                        text=True,encoding='utf-8',errors='replace',env=env,timeout=timeout,
                        cwd=ROOT)
    return {'exit_code':proc.returncode,'stdout':proc.stdout.strip(),
            'stderr_tail':proc.stderr[-2000:].strip() or None}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--runtime',type=Path,default=ROOT/'configs/runtime.json')
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    lock_path=ROOT/'configs/model-assets.lock.json'
    lock=load(lock_path) if lock_path.is_file() else {}
    result={'schema_version':'1.0','mode':'preflight_only_no_model_inference',
            'input':str(a.input.resolve()),'asset_lock':str(lock_path),
            'asset_lock_sha256':sha256(lock_path) if lock_path.is_file() else None,
            'checks':{},'model_calls':0}
    errors=[]
    if not lock: errors.append('missing_model_asset_lock')
    payload=load(a.input)
    smiles=payload.get('smiles'); formula=payload.get('formula') or payload.get('expected_formula')
    if not smiles or not formula: errors.append('input_requires_smiles_and_formula')
    runtime=load_runtime_config(a.runtime)
    az=runtime.get('aizynthfinder',{}); par=runtime.get('parrot',{}); yld=runtime.get('rxn_yields',{})
    for key,cfg in [('aizynthfinder',az),('parrot',par),('rxn_yields',yld)]:
        if not isinstance(cfg,dict): errors.append(f'missing_runtime_section:{key}')
    for key,cfg,required in [
        ('aizynthfinder',az,['python','model_dir','stock_buckets','config']),
        ('parrot',par,['python','repository','checkpoint','config']),
        ('rxn_yields',yld,['python','checkpoint','metadata'])]:
        for field in required:
            value=str(cfg.get(field,''))
            if not value or '${' in value: errors.append(f'unset_runtime_value:{key}.{field}')

    # Local structure/formula validation under the same RDKit runtime used by AiZynthFinder.
    ai_python=Path(az.get('python',''))
    if ai_python.is_file() and smiles and formula:
        code="import json,sys; from rdkit import Chem; from rdkit.Chem import rdMolDescriptors; m=Chem.MolFromSmiles(sys.argv[1]); assert m is not None,'invalid_smiles'; f=rdMolDescriptors.CalcMolFormula(m); assert f==sys.argv[2],f'formula_mismatch:{f}'; print(json.dumps({'canonical_smiles':Chem.MolToSmiles(m,canonical=True),'formula':f}))"
        result['checks']['input_structure']=run_probe(ai_python,code,[smiles,formula])
        if result['checks']['input_structure']['exit_code']: errors.append('input_structure_check_failed')

    # AiZynth model/template checks and exact stock-bucket provenance, all read-only.
    az_model=Path(az.get('model_dir',''))
    az_cfg=Path(az.get('config',''))
    az_stock=Path(az.get('stock_buckets',''))
    az_assets={}
    if az_cfg.is_file():
        material=expand_runtime_values(load(az_cfg),{'PROJECT_ROOT':str(ROOT),
            'AIZYNTH_MODEL_DIR':az.get('model_dir','${AIZYNTH_MODEL_DIR}'),
            'AIZYNTH_STOCK_BUCKETS':az.get('stock_buckets','${AIZYNTH_STOCK_BUCKETS}')})
        for group in material.get('expansion',{}).values():
            for item in group if isinstance(group,list) else []:
                f=Path(item)
                actual=sha256(f) if f.is_file() else None
                expected=lock.get('aizynthfinder',{}).get('files',{}).get(f.name)
                az_assets[str(f)]={'exists':f.is_file(),'sha256':actual,
                    'expected_sha256':expected,'matches_asset_lock':actual is not None and actual==expected}
                if not f.is_file(): errors.append('missing_aizynth_model_asset')
                elif actual!=expected: errors.append('aizynth_model_hash_mismatch')
        stock_manifest=az_stock/'manifest.json'
        stock_info={'path':str(az_stock),'exists':stock_manifest.is_file()}
        if stock_manifest.is_file():
            m=load(stock_manifest); stock_info.update({'status':m.get('status'),
                'manifest_sha256':sha256(stock_manifest),
                'manifest_source_path_is_machine_specific':True,
                'source_path':m.get('source_path'),
                'source_rows':m.get('source_rows'),'extracted_rows':m.get('extracted_rows'),
                'record_bytes':m.get('record_bytes'),'tables_version':m.get('tables_version')})
            if m.get('status')!='validated' or m.get('source_rows')!=m.get('extracted_rows') or m.get('record_bytes')!=28 or m.get('source_rows')!=lock.get('aizynthfinder',{}).get('stock_rows'):
                errors.append('invalid_or_incomplete_stock_manifest')
            source=Path(m.get('source_path',''))
            stock_info['source_exists']=source.is_file()
            stock_info['source_sha256_actual']=sha256(source) if source.is_file() else None
            stock_info['source_hash_matches']=source.is_file() and stock_info['source_sha256_actual']==m.get('source_sha256')
            stock_info['source_hash_matches_lock']=stock_info['source_sha256_actual']==lock.get('aizynthfinder',{}).get('stock_source_sha256')
            if not stock_info['source_hash_matches'] or not stock_info['source_hash_matches_lock']:
                errors.append('stock_source_checksum_mismatch_or_missing')
            file_errors=[]; total=0
            expected_names={f'{chr(x)}.keys' for x in range(ord('A'),ord('Z')+1)}
            if set(m.get('files',{}))!=expected_names: file_errors.append('stock_bucket_index_incomplete')
            for name,entry in m.get('files',{}).items():
                f=az_stock/name
                if not f.is_file(): file_errors.append(f'missing:{name}'); continue
                total+=f.stat().st_size
                if f.stat().st_size!=entry.get('bytes') or sha256(f)!=entry.get('sha256'):
                    file_errors.append(f'checksum_or_size_mismatch:{name}')
            stock_info['bucket_count']=len(m.get('files',{}));stock_info['bucket_bytes']=total
            stock_info['bucket_errors']=file_errors
            if file_errors: errors.append('stock_bucket_integrity_failed')
        else: errors.append('missing_stock_bucket_manifest')
        result['checks']['aizynth_assets']={'model_assets':az_assets,'stock':stock_info}
    else: errors.append('missing_aizynth_config')

    # Probe runtime imports only; do not load model weights or invoke prediction methods.
    if ai_python.is_file():
        ai_code="import onnxruntime; import numpy; import rdkit; import pandas; import tables; import importlib.metadata as md,json,sys; sys.path.insert(0,sys.argv[1]); from disk_stock import DiskInchiStock; d=DiskInchiStock(sys.argv[2]); print(json.dumps({'python':sys.version.split()[0],'packages':{n:md.version(n) for n in ['aizynthfinder','rdkit','onnxruntime','numpy','pandas','tables']},'disk_stock_rows':len(d),'bucket_files_opened':len(d.maps)}))"
        result['checks']['aizynth_runtime']=run_probe(ai_python,ai_code,[ROOT/'scripts',az_stock],timeout=300)
        if result['checks']['aizynth_runtime']['exit_code']: errors.append('aizynth_runtime_probe_failed')
        else:
            observed=json.loads(result['checks']['aizynth_runtime']['stdout'])
            expected=lock.get('aizynthfinder',{})
            mismatches=[k for k,v in expected.get('packages',{}).items() if observed.get('packages',{}).get(k)!=v]
            if observed.get('python')!=expected.get('python') or mismatches:
                errors.append('aizynth_runtime_version_mismatch:'+','.join(mismatches or ['python']))

    repo=Path(par.get('repository','')); checkpoint=Path(par.get('checkpoint','')); pypar=Path(par.get('python',''))
    repo_commit=None; repo_clean=None
    if repo.is_dir():
        revision=subprocess.run(['git','-C',str(repo),'rev-parse','HEAD'],capture_output=True,text=True,encoding='utf-8',errors='replace')
        status=subprocess.run(['git','-C',str(repo),'status','--short'],capture_output=True,text=True,encoding='utf-8',errors='replace')
        repo_commit=revision.stdout.strip() if revision.returncode==0 else None
        repo_clean=status.returncode==0 and not status.stdout.strip()
        if repo_commit!=lock.get('parrot',{}).get('repository_commit') or not repo_clean:
            errors.append('parrot_repository_revision_or_worktree_mismatch')
    par_files={name:checkpoint/name for name in ['pytorch_model.bin','config.json','model_args.json','tokenizer_config.json','special_tokens_map.json','vocab.txt']}
    par_hashes={str(f):sha256(f) for f in par_files.values() if f.is_file()}
    missing=[str(f) for f in [repo/'inference.py',*par_files.values()] if not f.is_file()]
    par_file_records={str(f):{'exists':f.is_file(),'sha256':sha256(f) if f.is_file() else None,
        'matches_asset_lock':f.is_file() and sha256(f)==lock.get('parrot',{}).get('files',{}).get(f.name)}
        for f in par_files.values()}
    result['checks']['parrot_assets']={'repository':str(repo),'repository_commit':repo_commit,
        'repository_worktree_clean':repo_clean,'checkpoint':str(checkpoint),
        'files':par_file_records,'missing':missing}
    if missing: errors.append('parrot_files_missing')
    if any(not x['matches_asset_lock'] for x in par_file_records.values()): errors.append('parrot_checkpoint_hash_mismatch')
    if pypar.is_file() and repo.is_dir():
        par_code="import importlib.metadata as md,json,sys; sys.path.insert(0,sys.argv[1]); import torch,pandas,yaml,transformers,rxnfp; from models.parrot_model import ParrotConditionPredictionModel; from rxnfp.models import SmilesTokenizer; print(json.dumps({'python':sys.version.split()[0],'packages':{n:md.version(n) for n in ['torch','transformers','rxnfp','simpletransformers']},'imports':'passed'}))"
        result['checks']['parrot_runtime']=run_probe(pypar,par_code,[repo],timeout=360)
        if result['checks']['parrot_runtime']['exit_code']: errors.append('parrot_runtime_probe_failed')
        else:
            observed=json.loads(result['checks']['parrot_runtime']['stdout'])
            expected=lock.get('parrot',{})
            mismatches=[k for k,v in expected.get('packages',{}).items() if observed.get('packages',{}).get(k)!=v]
            if observed.get('python')!=expected.get('python') or mismatches:
                errors.append('parrot_runtime_version_mismatch:'+','.join(mismatches or ['python']))

    py_yield=Path(yld.get('python','')); ycp=Path(yld.get('checkpoint','')); metadata_path=Path(yld.get('metadata',''))
    yweight=ycp/'pytorch_model.bin'
    meta=load(metadata_path) if metadata_path.is_file() else {}
    weight_sha=sha256(yweight) if yweight.is_file() else None
    yfiles={name:ycp/name for name in ['pytorch_model.bin','config.json','model_args.json','tokenizer_config.json','special_tokens_map.json','vocab.txt']}
    ymissing=[str(f) for f in yfiles.values() if not f.is_file()]
    yield_file_records={str(f):{'exists':f.is_file(),'sha256':sha256(f) if f.is_file() else None,
        'matches_asset_lock':f.is_file() and sha256(f)==lock.get('rxn_yields',{}).get('files',{}).get(f.name)}
        for f in yfiles.values()}
    result['checks']['yield_assets']={'checkpoint':str(ycp),'files':yield_file_records,
        'metadata_path':str(metadata_path),'metadata_sha256':sha256(metadata_path) if metadata_path.is_file() else None,
        'checkpoint_metadata_hash_matches':weight_sha is not None and weight_sha==meta.get('checkpoint_sha256'),
        'normalization_scale':meta.get('output_scale'),'training_data_reference':meta.get('training_data_reference'),
        'missing':ymissing}
    if ymissing: errors.append('yield_files_missing')
    if any(not x['matches_asset_lock'] for x in yield_file_records.values()): errors.append('yield_asset_hash_mismatch')
    if not result['checks']['yield_assets']['checkpoint_metadata_hash_matches']: errors.append('yield_checkpoint_hash_mismatch')
    if meta.get('output_scale')!='standardized_fraction' or meta.get('training_yield_units')!='fraction' or not meta.get('training_data_reference'):
        errors.append('yield_normalization_metadata_invalid')
    if py_yield.is_file():
        yield_code="import importlib.metadata as md,json,sys; import torch,transformers; from rxnfp.models import SmilesTokenizer; print(json.dumps({'python':sys.version.split()[0],'packages':{n:md.version(n) for n in ['torch','transformers','rxnfp']},'imports':'passed'}))"
        result['checks']['yield_runtime']=run_probe(py_yield,yield_code,timeout=360)
        if result['checks']['yield_runtime']['exit_code']: errors.append('yield_runtime_probe_failed')
        else:
            observed=json.loads(result['checks']['yield_runtime']['stdout'])
            expected=lock.get('rxn_yields',{})
            mismatches=[k for k,v in expected.get('packages',{}).items() if observed.get('packages',{}).get(k)!=v]
            if observed.get('python')!=expected.get('python') or mismatches:
                errors.append('yield_runtime_version_mismatch:'+','.join(mismatches or ['python']))

    # Ensure runtime configs point at the same adapter templates used by the package.
    for label,cfg,pathkey in [('aizynthfinder',az,'config'),('parrot',par,'config')]:
        if not Path(cfg.get(pathkey,'')).is_file(): errors.append(f'missing_{label}_adapter_config')
    route_source=(ROOT/'scripts/predict_routes.py').read_text(encoding='utf-8')
    yield_source=(ROOT/'scripts/predict_yields.py').read_text(encoding='utf-8')
    result['checks']['adapter_runtime_wiring']={
        'route_expands_runtime_model_and_stock_paths':all(x in route_source for x in ['config.get("model_dir"','config.get("stock_buckets"','expand_runtime_values(load(cfg_template)']),
        'yield_worker_gets_materialized_resolved_runtime':all(x in yield_source for x in ['save(materialized_runtime, {args.model: config})','args.input.resolve(), materialized_runtime.resolve(), raw']),
        'yield_worker_does_not_receive_raw_runtime_template':'args.input.resolve(), args.runtime.resolve(), raw' not in yield_source,
    }
    if not all(result['checks']['adapter_runtime_wiring'].values()): errors.append('adapter_runtime_wiring_check_failed')
    if errors:
        result.update(status='failed',errors=errors)
    else:
        result.update(status='passed',errors=[])
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'error_count':len(errors),'output':str(a.output.resolve()),'model_calls':0}))
    return 0 if not errors else 2

if __name__=='__main__': raise SystemExit(main())
