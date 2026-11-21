"""Join actual outputs by (route_id, step_id) and check multi-step dependencies."""
import argparse
from pathlib import Path
from _runtime import ROOT,load,save,digest,local_artifact

MODELS={
 'aizynthfinder':'https://github.com/MolecularAI/aizynthfinder',
 'synthex':'https://github.com/schwallergroup/synthex',
 'askcos':'https://gitlab.com/mlpds_mit/askcosv2/context_recommender',
 'parrot':'https://github.com/wangxr0526/Parrot',
 'rxn_yields':'https://github.com/rxn4chemistry/rxn_yields',
 'drfp':'https://github.com/reymond-group/drfp'}

def join_steps(routes,conditions,yields,target_smiles):
    from rdkit import Chem
    def canonical(s):
        mol=Chem.MolFromSmiles(s)
        if mol is None:raise ValueError('Invalid model structure')
        return Chem.MolToSmiles(mol)
    target=canonical(target_smiles);lookup={};route_info=[]
    for route in routes.get('predictions') or []:
        seen={};steps=route['steps']
        if not steps:raise ValueError('A stock-only result is not a synthesis route')
        for step in steps:
            key=(route['route_id'],step['step_id'])
            if key in lookup:raise ValueError('Duplicate route/step identifier')
            canonical(step['product_smiles'])
            precursors=[canonical(s) for s in step['precursor_smiles']]
            if step['reaction_smiles']!='.'.join(step['precursor_smiles'])+'>>'+step['product_smiles']:raise ValueError('Reaction representation mismatch')
            for dependency in step.get('depends_on',[]):
                if dependency not in seen or canonical(seen[dependency]['product_smiles']) not in precursors:raise ValueError('Dependency does not supply a precursor or is out of order')
            seen[step['step_id']]=step
            lookup[key]={'route_id':key[0],**step,'conditions':None,'yield_prediction':None}
        if canonical(steps[-1]['product_smiles'])!=target:raise ValueError('Route does not end at the requested target')
        route_info.append({'route_id':route['route_id'],'step_count':len(steps),'scores':route.get('scores'),'is_solved':route.get('is_solved'),'overall_yield_percent':None,'overall_yield_reason':'No experimentally validated overall yield; branching and independently predicted steps are not combined.'})
    matched=set()
    for row in conditions.get('predictions') or []:
        for location in row['steps']:
            key=(location['route_id'],location['step_id'])
            if key not in lookup or row['reaction_smiles']!=lookup[key]['reaction_smiles'] or key in matched:raise ValueError('Condition join mismatch, duplicate or extra step')
            matched.add(key);lookup[key]['conditions']={k:v for k,v in row.items() if k!='steps'}
    if conditions.get('status')=='success' and matched!=set(lookup):raise ValueError('Missing actual condition outputs')
    yielded=set()
    for row in yields.get('predictions') or []:
        key=(row['route_id'],row['step_id'])
        if key not in lookup or row['reaction_smiles']!=lookup[key]['reaction_smiles'] or key in yielded:raise ValueError('Yield join mismatch, duplicate or extra step')
        yielded.add(key);lookup[key]['yield_prediction']=row
    if yields.get('status')=='success' and yielded!=set(lookup):raise ValueError('Missing actual yield outputs')
    return route_info,list(lookup.values())

def build(run):
    target=load(run/'input.json');routes=load(run/'routes.json');conditions=load(run/'conditions-parrot.json');yields=load(run/'yields-rxn_yields.json')
    route_info,steps=join_steps(routes,conditions,yields,target['smiles'])
    # Presentation budget, not a scientific assertion about a fixed number of routes.
    plan=load(ROOT/'configs/report-plan.json');selected=[r['route_id'] for r in route_info[:plan['max_report_routes']]]
    if plan.get('selected_route_ids'):
        selected=plan['selected_route_ids']
        if not set(selected)<={r['route_id'] for r in route_info}:raise ValueError('Unknown report route selection')
    elif selected:
        multi=next((r['route_id'] for r in route_info if r['step_count']>1),None)
        if multi and multi not in selected:selected[-1]=multi
    figures=[{'figure_id':'target','path':str((run/'target/target.png').resolve()),'caption':target['name']+' structure'}]
    manifest=load(run/'figures/manifest.json')
    for f in manifest['figures']:
        if f['status']=='success' and f['route_id'] in selected:
            figures.append({'figure_id':f['route_id']+'/'+f['step_id'],'path':str(local_artifact(f['image_path'],run/'figures')),'caption':f['route_id']+' '+f['step_id']+' predicted reaction'})
    additional=load(run/'additional-analysis-status.json') if (run/'additional-analysis-status.json').exists() else {}
    for name,analysis in additional.items():
        if analysis.get('status')=='success':
            for item in analysis.get('figures',[]):
                path=Path(item['path']);path=path if path.is_absolute() else run/path
                if not path.is_file() or digest(path)!=item['sha256']:raise ValueError('Additional analysis image must have actual matching source hash')
                figures.append({'figure_id':name+'/'+item['figure_id'],'path':str(path.resolve()),'caption':item['caption']})
    for f in figures:f['sha256']=digest(f['path'])
    refs=[{'title':target['name']+' identity','url':target['identity_reference']}]+[{'title':n,'url':u} for n,u in MODELS.items()]
    meta=yields.get('checkpoint_metadata',{})
    for title,field in [('Yield normalization code','normalization_reference'),('Training data','training_data_reference')]:
        if meta.get(field):refs.append({'title':title,'url':meta[field]})
    for i,ref in enumerate(refs,1):ref['id']=i
    limitations=[{'kind':'cross_model_limit','note':'Parrot conditions are not inputs to the yield model. Predicted yields are not experimentally validated.'},
                  {'kind':'model_applicability','note':'Target-specific accuracy and domain membership are not assessed; normalization correctness is not accuracy validation.'},
                  {'kind':'missing_conditions','note':'Temperature, time and equivalents are not supplied by the selected condition checkpoint.'},
                  {'kind':'route_limit','note':'Stock membership and template scores do not prove practical feasibility. Search excludes target from stock; agents/byproducts can be omitted.'}]
    for step in steps:
        prediction=step['yield_prediction']
        if prediction and (prediction.get('input_truncated') or prediction.get('within_physical_bounds') is False):limitations.append({'kind':'yield_quality_warning','route_id':step['route_id'],'step_id':step['step_id'],'truncated':prediction.get('input_truncated'),'within_physical_bounds':prediction.get('within_physical_bounds')})
    evidence={'schema_version':'1.0','target':target,'model_status':{'routes':routes['status'],'conditions':conditions['status'],'yields':yields['status']},'route_summary':route_info,'steps':steps,'selected_route_ids':selected,'report_steps':[s for s in steps if s['route_id'] in selected], 'report_figure_assets':figures,'required_references':refs,'limitations':limitations,'additional_analyses':additional,'report_plan':plan,'condition_results_file':'conditions-parrot.json','normalization':meta,'source_hashes':{n:digest(run/n) for n in ['input.json','routes.json','conditions-parrot.json','yields-rxn_yields.json','figures/manifest.json']}}
    return evidence

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-dir',type=Path,required=True);a=p.parse_args();run=a.run_dir.resolve()
    evidence=build(run);save(run/'report-evidence.json',evidence)
    save(run/'validation_notes.json',{'artifact_type':'deterministic_checks_not_a_Solar_report','target_id':evidence['target']['target_id'],'notes':evidence['limitations'],'applicability':'not_assessed','source_hashes':evidence['source_hashes']})
    save(run/'step-validation.json',{'status':'passed','route_count':len(evidence['route_summary']),'step_count':len(evidence['steps']),'multi_step_route_count':sum(r['step_count']>1 for r in evidence['route_summary']),'conditions_joined':sum(s['conditions'] is not None for s in evidence['steps']),'yields_joined':sum(s['yield_prediction'] is not None for s in evidence['steps']),'scope':'Exact route/step/reaction joins and topological dependency checks; not chemical feasibility validation'})
    print('Validated actual routes:',len(evidence['route_summary']),'steps:',len(evidence['steps']))

if __name__=='__main__':main()
