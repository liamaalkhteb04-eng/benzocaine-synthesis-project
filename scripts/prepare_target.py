"""Verify a target against public PubChem and local RDKit, without AI calls."""
import argparse
from pathlib import Path
import urllib.request
from urllib.parse import quote
from _runtime import ROOT,load,save,digest

def main():
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors
    p=argparse.ArgumentParser();p.add_argument('--input',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    target=load(a.input);mol=Chem.MolFromSmiles(target['smiles']);assert mol is not None
    formula=rdMolDescriptors.CalcMolFormula(mol);assert formula==target['expected_formula']
    result={'target_id':target['target_id'],'canonical_smiles':Chem.MolToSmiles(mol),'formula':formula,'formal_charge':Chem.GetFormalCharge(mol),'input_sha256':digest(a.input),'rdkit_identity_check':'passed','pubchem_status':'not_verified'}
    url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+quote(target['name'])+'/property/MolecularFormula,CanonicalSMILES,InChIKey/JSON'
    result['source_url']=url
    try:
        import json
        with urllib.request.urlopen(url,timeout=30) as r:raw=json.loads(r.read())
        save(a.output.with_name('pubchem.raw.json'),raw)
        record=raw['PropertyTable']['Properties'][0];smi=record.get('ConnectivitySMILES',record.get('CanonicalSMILES',record.get('SMILES')))
        assert record['CID']==target['pubchem_cid'] and record['MolecularFormula']==formula
        assert Chem.MolToSmiles(Chem.MolFromSmiles(smi))==Chem.MolToSmiles(mol)
        result.update(pubchem_status='matched',pubchem_cid=record['CID'],inchi_key=record.get('InChIKey'))
    except Exception as e:result['pubchem_failure']=type(e).__name__
    save(a.output,result);print(result['rdkit_identity_check'],result['pubchem_status'])

if __name__=='__main__':main()
