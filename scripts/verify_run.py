"""Verify actual source hashes, step joins, yield normalization and every figure."""
import argparse
from pathlib import Path
import math
from PIL import Image
from _runtime import ROOT,load,save,digest,local_artifact
from build_evidence import join_steps
from audit_parrot_slots import verify_run as verify_parrot_slots

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-dir',type=Path,required=True);a=p.parse_args();run=a.run_dir.resolve()
    routes=load(run/'routes.json');cond=load(run/'conditions-parrot.json');yd=load(run/'yields-rxn_yields.json');target=load(run/'input.json')
    slot_audit=verify_parrot_slots(run)
    assert slot_audit["status"]=="passed", slot_audit["errors"]
    for result in [routes,cond,yd]:assert result['status']=='success' and result['inference_executed']
    info,steps=join_steps(routes,cond,yd,target['smiles']);meta=yd['checkpoint_metadata']
    for s in steps:
        y=s['yield_prediction'];expected=100*(y['raw_value']*meta['training_yield_std']+meta['training_yield_mean'])
        assert math.isclose(y['yield_percent'],expected,abs_tol=1e-12)
        assert y['conditions_in_input'] is False
    figures=load(run/'figures/manifest.json')['figures'];assert len(figures)==len(steps)
    expected_keys={(s['route_id'],s['step_id']) for s in steps}
    assert {(f['route_id'],f['step_id']) for f in figures}==expected_keys
    for f in figures:
        assert f['status']=='success';path=local_artifact(f['image_path'],run/'figures');assert digest(path)==f['sha256']
        with Image.open(path) as im:im.verify()
    for n,sha in load(run/'manifest.json')['files'].items():assert digest(run/n)==sha,n
    if (run/'reused-evidence.json').exists():
        for group in load(run/'reused-evidence.json').values():
            for n,sha in group['files'].items():assert digest(run/n)==sha,n
    save(run/'verification.json',{'status':'passed','routes':len(info),'steps':len(steps),'multi_step_routes':sum(r['step_count']>1 for r in info),'unique_condition_reactions':len(cond['predictions']),'condition_step_mappings':sum(len(c['steps']) for c in cond['predictions']),'yield_step_outputs':len(yd['predictions']),'reaction_figures':len(figures),'truncated_yield_inputs':sum(y['input_truncated'] for y in yd['predictions']),'out_of_bounds_yields':sum(y['within_physical_bounds'] is False for y in yd['predictions']),'parrot_slot_audit':slot_audit,'scope':'Actual output integrity, slot mapping, and joins; no experimental/target-domain accuracy validation'})
    print('Verified real route/step/condition/yield/image provenance:',len(info),len(steps))

if __name__=='__main__':main()

