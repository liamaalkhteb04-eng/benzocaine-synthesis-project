"""Structural unit fixtures only; never saved or represented as model predictions."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from predict_routes import normalize_trees
from build_evidence import join_steps

class StepGraphTests(unittest.TestCase):
    def setUp(self):
        def leaf(s):return {'smiles':s,'in_stock':True}
        def product(s,precursors):return {'smiles':s,'in_stock':False,'children':[{'children':precursors}]}
        tree=product('CCOC(C)=O',[product('CCO',[leaf('C=C')]),product('CC(=O)O',[leaf('CC=O')])])
        self.routes={'status':'success','predictions':normalize_trees([tree])}
        self.steps=self.routes['predictions'][0]['steps']
        self.cond={'status':'success','predictions':[{'reaction_smiles':s['reaction_smiles'],'steps':[{'route_id':'route-01','step_id':s['step_id']}],'candidates':[]} for s in reversed(self.steps)]}
        self.yd={'status':'success','predictions':[{'route_id':'route-01','step_id':s['step_id'],'reaction_smiles':s['reaction_smiles'],'yield_percent':None} for s in self.steps]}
    def test_branch_dependencies_and_reordered_conditions(self):
        self.assertEqual(self.steps[-1]['depends_on'],['step-01','step-02'])
        info,rows=join_steps(self.routes,self.cond,self.yd,'CCOC(C)=O')
        self.assertEqual(info[0]['step_count'],3)
        for row in rows:self.assertEqual(row['reaction_smiles'],row['conditions']['reaction_smiles'])
    def test_wrong_reaction_rejected(self):
        bad=copy.deepcopy(self.cond);bad['predictions'][0]['reaction_smiles']='C>>O'
        with self.assertRaises(ValueError):join_steps(self.routes,bad,self.yd,'CCOC(C)=O')
    def test_missing_step_rejected(self):
        bad=copy.deepcopy(self.yd);bad['predictions'].pop()
        with self.assertRaises(ValueError):join_steps(self.routes,self.cond,bad,'CCOC(C)=O')
    def test_invalid_dependency_rejected(self):
        bad=copy.deepcopy(self.routes);bad['predictions'][0]['steps'][-1]['depends_on']=['step-99']
        with self.assertRaises(ValueError):join_steps(bad,self.cond,self.yd,'CCOC(C)=O')

if __name__=='__main__':unittest.main()
