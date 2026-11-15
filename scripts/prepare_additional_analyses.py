"""Plan analyses from real selected reactions. No QM, EPI, GUI or LLM execution."""
import argparse
from pathlib import Path
import shutil
from _runtime import ROOT,load,save,digest

def main():
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors
    p=argparse.ArgumentParser();p.add_argument('--run-dir',type=Path,required=True);a=p.parse_args();run=a.run_dir.resolve();e=load(run/'report-evidence.json')
    smarts={'nitro':'[N+](=O)[O-]','primary_aryl_amine':'[NX3;H2][c]','carboxylic_acid':'[CX3](=O)[OX2H1]','ester':'[CX3](=O)[OX2][#6]','amide':'[CX3](=O)[NX3]','aryl_bromide':'[c][Br]'}
    patterns={k:Chem.MolFromSmarts(v) for k,v in smarts.items()}
    observations=[];inventory={}
    for step in e['steps']:
        parts=[]
        for role,smiles in [('precursor',s) for s in step['precursor_smiles']]+[('product',step['product_smiles'])]:
            mol=Chem.MolFromSmiles(smiles);canonical=Chem.MolToSmiles(mol)
            counts={k:len(mol.GetSubstructMatches(v)) for k,v in patterns.items()}
            parts.append({'role':role,'smiles':smiles,'functional_group_counts':counts})
            inventory.setdefault(canonical,{'smiles':canonical,'formula':rdMolDescriptors.CalcMolFormula(mol),'formal_charge':Chem.GetFormalCharge(mol),'occurrences':[]})['occurrences'].append({'route_id':step['route_id'],'step_id':step['step_id'],'role':role})
        cond=step['conditions'];top=cond['candidates'][0] if cond and cond['candidates'] else None
        if top:
            for slot in ['catalyst1','solvent1','solvent2','reagent1','reagent2']:
                if top[slot]:
                    mol=Chem.MolFromSmiles(top[slot])
                    if mol:
                        key=Chem.MolToSmiles(mol);inventory.setdefault(key,{'smiles':key,'formula':rdMolDescriptors.CalcMolFormula(mol),'formal_charge':Chem.GetFormalCharge(mol),'occurrences':[]})['occurrences'].append({'route_id':step['route_id'],'step_id':step['step_id'],'role':slot})
        observations.append({'route_id':step['route_id'],'step_id':step['step_id'],'depends_on':step.get('depends_on',[]),'structures':parts,'rank1_conditions':top,'yield_percent':step['yield_prediction']['yield_percent'] if step['yield_prediction'] else None,'status':'observations_only_not_experimental_validation'})
    save(run/'structural-observations.json',{'artifact_type':'RDKit_2D_structural_counts_not_new_model_predictions','smarts':smarts,'source_evidence_sha256':digest(run/'report-evidence.json'),'steps':observations})
    save(run/'analysis-material-inventory.json',{'status':'prepared_from_actual_structures_and_rank1_condition_slots','materials':list(inventory.values()),'property_values':None,'three_dimensional_coordinates_generated':False})
    versions={name:{'path':shutil.which(name),'execution_tested':False} for name in ['opencode','pi','feynman','mopac','MPBPWIN','DiscoveryStudio']}
    save(ROOT/'plans/tool-status.json',{'tools':versions,'additional_install_search_reference':'Previous read-only audit in the preserved test project; no tools were installed in this task','installations_performed':0,'new_paid_calls':0,'additional_tools_executed':False})
    plan={'status':'prepared_not_executed','target':e['target'],'source_run':str(run),'source_evidence_sha256':digest(run/'report-evidence.json'),'skill_sha256':digest(ROOT/'skill/synthesis_report_skill.md'),'selected_routes':e['selected_route_ids'],'materials_file':str(run/'analysis-material-inventory.json'),'analyses':{
      'harness_comparison':{'requires':['OpenCode','pi','Feynman','verified Solar provider compatibility'],'same':['skill bytes/hash','frozen input and evidence','Solar snapshot','temperature','max_tokens','tool allowlist'],'settings':{k:e['report_plan'][k] for k in ['model','temperature','max_tokens']},'separate_modes':['fresh_generation','revision_generation','document_rebuild_without_model_call','shared_script_workflow_orchestration'],'record_differences':['wrapper prompts','message roles','tool schema','effective parameters','retries','compaction','auxiliary calls','returned model','usage','latency','errors'],'planned_repetitions_after_budget_approval':3,'executed_repetitions':0},
      'mopac':{'requires':['MOPAC executable','approved 3D conformer preparation','charge/multiplicity/method/solvent/convergence settings'],'molecules':'Target plus organic precursors of report-selected steps. Use materials_file; choose manageable subset after chemical review.','outputs':['original input/out/arc','convergence/gradient and frequency status','actual geometry/charges/dipole/orbital results'],'caveats':['No Pd/Cu surface catalysis validation by isolated organic molecule PM7','Do not rank unlike molecular formulas by raw energy','No yield, reaction rate or activation-barrier proof']},
      'epi_suite':{'requires':['EPI Suite/MPBPWIN','verified chemical forms','temperature/pressure/composition or explicitly sourced conditional scenario'],'materials':'Reactants/intermediates/product and actual rank-1 solvent/reagent slots; distinguish ionic/metal/nonorganic entries with applicability checks','outputs':['raw estimated BP/MP/vapor pressure','separate measured database data','method/units/reference conditions'],'blocker':'Parrot supplies no temperature/time/equivalents; do not invent them','caveats':['Pure-substance MP/BP does not establish solution phase or reaction impossibility','Keep decomposition, protonation, solubility and pressure limitations']},
      'discovery_studio':{'requires':['Discovery Studio Visualizer','traceable 3D structures and atom indices','multiple conformers and recorded approach orientations'],'focus':'Use actual ester-forming step if present for carbonyl/oxygen approach; primary nitro reduction on a metal catalyst is not represented by a simple two-molecule approach picture','outputs':['structure hashes','original screenshots/session records','actual distances/angles and steric observations'],'caveats':['Not a transition state','Not dynamics or yield validation']}
    },'maximum_final_report_pages':e['report_plan']['maximum_pages_including_references'],'final_author':'Solar Pro 4','report_generation_performed':False,'paid_calls_authorized':False,'installations_authorized':False}
    save(ROOT/'plans/additional-analyses.json',plan)
    print('Prepared material inventory and four analysis plans from',len(e['steps']),'actual steps')

if __name__=='__main__':main()
