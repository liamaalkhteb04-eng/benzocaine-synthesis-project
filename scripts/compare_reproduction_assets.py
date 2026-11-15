"""Compare saved AiZynthFinder assets/config and historical benzocaine runs.
Read-only on all input evidence; writes only a new JSON validation artifact.
"""
import argparse, hashlib, json
from pathlib import Path


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def canonical_config(value):
    if isinstance(value,dict): return {k:canonical_config(v) for k,v in value.items()}
    if isinstance(value,list): return [canonical_config(v) for v in value]
    if isinstance(value,str) and (('\\' in value) or (len(value)>2 and value[1]==':')):
        return value.replace('\\','/').replace('//','/').lower()
    return value


def by_basename(mapping):
    return {Path(k.replace('\\','/')).name: v for k,v in mapping.items()}


def selected_routes(obj):
    return [{k:r.get(k) for k in ('route_id','is_solved','scores','metadata')} | {
        'steps':[{k:s.get(k) for k in ('step_id','depends_on','reaction_smiles','precursor_smiles','product_smiles','precursor_stock_flags','metadata')} for s in r.get('steps',[])]
    } for r in obj.get('predictions') or []]


def selected_conditions(obj):
    out=[]
    for item in obj.get('predictions') or []:
        out.append({k:item.get(k) for k in ('reaction_smiles','canonical_reaction_smiles','steps')} | {
            'candidates':[{k:c.get(k) for k in ('rank','catalyst1','catalyst2','solvent1','solvent2','reagent1','reagent2','sequence_score')} for c in item.get('candidates',[])]
        })
    return out


def selected_yields(obj):
    return [{k:x.get(k) for k in ('route_id','step_id','reaction_smiles','raw_value','yield_percent','raw_output_scale','yield_status','within_physical_bounds','applicability','conditions_in_input')} for x in obj.get('predictions') or []]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(); root=a.project_root.resolve()
    base_routes=root/'results/benzocaine-live-20261031-03'
    representative=root/'results/benzocaine-live-20261031-04'
    replay=root/'submission/github-ready-20261104/results/benzocaine-live-repro-20261105-01'
    b3=load(base_routes/'routes.json'); b4=load(representative/'routes.json'); rr=load(replay/'routes.json')
    v_old=load(replay/'reproduction-validation.json')
    c4=load(representative/'conditions-parrot.json'); cr=load(replay/'conditions-parrot.json')
    y4=load(representative/'yields-rxn_yields.json'); yr=load(replay/'yields-rxn_yields.json')
    hist_assets=by_basename(b3.get('asset_sha256') or {})
    replay_assets=by_basename(rr.get('asset_sha256') or {})
    required_assets=('uspto_model.onnx','uspto_templates.csv.gz')
    per_asset={name:{'historical_sha256':hist_assets.get(name),'rerun_sha256':replay_assets.get(name),'same':bool(hist_assets.get(name) and hist_assets.get(name)==replay_assets.get(name))} for name in required_assets}
    hstock=b3.get('derived_stock_provenance') or {}; rstock=rr.get('derived_stock_provenance') or {}
    bucket_map_same=hstock.get('files')==rstock.get('files') and len(hstock.get('files') or {})==26
    source_same=bool(hstock.get('source_sha256') and hstock.get('source_sha256')==rstock.get('source_sha256'))
    cfg_same=canonical_config(b3.get('configuration'))==canonical_config(rr.get('configuration'))
    cfg_hash_same=b3.get('configuration_sha256')==rr.get('configuration_sha256')
    checks={
      'run_relationship_routes_03_equals_representative_04_file_sha':sha(base_routes/'routes.json')==sha(representative/'routes.json'),
      'route_run_03_success':b3.get('status')=='success' and b3.get('inference_executed') is True,
      'representative_04_conditions_success':c4.get('status')=='success' and c4.get('inference_executed') is True,
      'representative_04_yields_success':y4.get('status')=='success' and y4.get('inference_executed') is True,
      'rerun_routes_success':rr.get('status')=='success' and rr.get('inference_executed') is True,
      'rerun_conditions_success':cr.get('status')=='success' and cr.get('inference_executed') is True,
      'rerun_yields_success':yr.get('status')=='success' and yr.get('inference_executed') is True,
      'model_hashes_match':all(per_asset[x]['same'] for x in required_assets),
      'prior_false_hash_flags_reconciled_against_raw_evidence':(v_old.get('comparison_to_historical_benzocaine',{}).get('model_and_stock_hashes_same') is False and v_old.get('comparison_to_historical_benzocaine',{}).get('model_and_template_hashes_same') is False and all(per_asset[x]['same'] for x in required_assets) and source_same and bucket_map_same),
      'stock_source_hash_matches':source_same,
      'all_26_stock_bucket_hashes_match':bucket_map_same,
      'semantic_configuration_matches_after_path_separator_normalization':cfg_same,
      'configuration_json_byte_hashes_differ':not cfg_hash_same,
      'route_predictions_match':selected_routes(b3)==selected_routes(rr),
      'conditions_match_representative_run_04':selected_conditions(c4)==selected_conditions(cr),
      'yields_match_representative_run_04':selected_yields(y4)==selected_yields(yr),
    }
    out={
      'schema_version':'1.0','status':'passed' if all(checks.values()) else 'failed',
      'verification_scope':'offline_comparison_of_saved_run_evidence_only_no_inference',
      'historical_route_run_id':'benzocaine-live-20261031-03',
      'historical_representative_run_id':'benzocaine-live-20261031-04',
      'rerun_id':'benzocaine-live-repro-20261105-01',
      'relationship':{
        'route_reference':'-03 is the original AiZynthFinder route run. Its routes.json SHA-256 is byte-identical to the routes.json copied into representative bundle -04.',
        'representative_bundle':'-04 is the earlier representative result bundle; it contains successful Parrot conditions and Yield-BERT outputs, while its route artifact is reused from -03.',
        'comparison_basis':'Compare route assets and route predictions from -03 to rerun; compare Parrot conditions and Yield-BERT outputs from representative -04 to rerun. The -03 conditions file is failed and is not used as the successful condition reference.'
      },
      'source_files':{
        'historical_routes_json':{'path':str(base_routes/'routes.json'),'sha256':sha(base_routes/'routes.json')},
        'representative_routes_json':{'path':str(representative/'routes.json'),'sha256':sha(representative/'routes.json')},
        'rerun_routes_json':{'path':str(replay/'routes.json'),'sha256':sha(replay/'routes.json')},
        'prior_validation_json':{'path':str(replay/'reproduction-validation.json'),'sha256':sha(replay/'reproduction-validation.json')},
        'representative_conditions_json':{'path':str(representative/'conditions-parrot.json'),'sha256':sha(representative/'conditions-parrot.json')},
        'rerun_conditions_json':{'path':str(replay/'conditions-parrot.json'),'sha256':sha(replay/'conditions-parrot.json')},
        'representative_yields_json':{'path':str(representative/'yields-rxn_yields.json'),'sha256':sha(representative/'yields-rxn_yields.json')},
        'rerun_yields_json':{'path':str(replay/'yields-rxn_yields.json'),'sha256':sha(replay/'yields-rxn_yields.json')},
      },
      'asset_comparison':{
        'model_and_reaction_template_archives':per_asset,
        'zinc_source':{'historical_sha256':hstock.get('source_sha256'),'rerun_sha256':rstock.get('source_sha256'),'same':source_same},
        'derived_stock_buckets':{'count_historical':len(hstock.get('files') or {}),'count_rerun':len(rstock.get('files') or {}),'all_file_sha256_and_size_entries_same':bucket_map_same},
        'aizynthfinder_code_module':{'historical_sha256':b3.get('finder_source_sha256'),'rerun_sha256':rr.get('finder_source_sha256'),'same':b3.get('finder_source_sha256')==rr.get('finder_source_sha256')},
      },
      'configuration_comparison':{
        'historical_materialized_config_sha256':b3.get('configuration_sha256'),
        'rerun_materialized_config_sha256':rr.get('configuration_sha256'),
        'byte_hash_same':cfg_hash_same,
        'recorded_configuration_object_same_after_path_separator_normalization':cfg_same,
        'historical_config_template_sha256':b3.get('configuration_template_sha256'),
        'rerun_config_template_sha256':rr.get('configuration_template_sha256'),
        'config_template_hash_comparable':bool(b3.get('configuration_template_sha256')),
        'cause_of_byte_hash_difference':'unresolved; historical temporary materialized configuration source file was not retained',
      },
      'prior_validation_conflict':{
        'prior_false_model_and_stock_hashes_same':v_old.get('comparison_to_historical_benzocaine',{}).get('model_and_stock_hashes_same'),
        'prior_false_model_and_template_hashes_same':v_old.get('comparison_to_historical_benzocaine',{}).get('model_and_template_hashes_same'),
        'prior_free_text_says_asset_hashes_match':'model/template hashes match' in v_old.get('comparison_to_historical_benzocaine',{}).get('performance_difference_interpretation',''),
        'recomputed_model_and_reaction_template_hashes_same':checks['model_hashes_match'],
        'recomputed_stock_source_and_all_bucket_hashes_same':source_same and bucket_map_same,
        'false_fields_are_inconsistent_with_raw_hashes':not v_old.get('comparison_to_historical_benzocaine',{}).get('model_and_template_hashes_same',True) and checks['model_hashes_match'] and bucket_map_same,
        'corrected_interpretation':'model, USPTO reaction-template archive and stock hashes match; configuration JSON byte hashes differ while recorded configuration objects match after path separator normalization',
        'original_validation_record_preserved':True,
      },
      'checks':checks,
      'interpretation_limits':['Identical outputs and identical assets are separate claims and checked separately.','Config JSON hashes differ; semantic configuration is equal only after normalizing path separators.','No cause for the historical config byte-hash difference is asserted.','No fresh model inference was run.'],
    }
    out['status']='passed' if all(checks.values()) else 'failed'
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':out['status'],'checks':checks},ensure_ascii=False,indent=2))
    return 0 if out['status']=='passed' else 1

if __name__=='__main__': raise SystemExit(main())
