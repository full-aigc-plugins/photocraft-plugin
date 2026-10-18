import importlib.util
from pathlib import Path
import unittest
P=Path(__file__).resolve().parents[1]/'scripts/repair_plan.py'
class RepairPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('repair_plan',P);cls.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.m)
    def data(self):return {'width':256,'height':192,'protected':[[100,100,140,140]],'strokes':[{'kind':'heal','points':[[80,40],[84,42]],'source':[60,40],'size':6}]}
    def test_methods(self):
        p=self.m.build_plan(self.data());self.assertEqual(p['steps'][0]['command'],'layer.duplicate');self.assertEqual(p['steps'][1]['command'],'paint.healingBrush');self.assertEqual(p['steps'][1]['params']['source'],[60,40]);self.assertFalse(p['countsAsNewScene'])
    def test_crossing_protected_region(self):
        d=self.data();d['strokes'][0]['points']=[[80,120],[160,120]]
        with self.assertRaises(ValueError):self.m.build_plan(d)
    def test_brush_radius(self):
        d=self.data();d['strokes'][0]['points']=[[98,120]]
        with self.assertRaises(ValueError):self.m.build_plan(d)
    def test_edge(self):
        d=self.data();d['strokes'][0]['points']=[[1,40]]
        with self.assertRaises(ValueError):self.m.build_plan(d)
    def test_source_sweep(self):
        d=self.data();d['strokes'][0].update(points=[[80,40],[84,42]],source=[98,120])
        with self.assertRaises(ValueError):self.m.build_plan(d)
    def test_bad_numeric(self):
        for value in [True,float('nan'),float('inf'),0,100001]:
            d=self.data();d['width']=value
            with self.assertRaises(ValueError):self.m.build_plan(d)
    def test_spot(self):
        d=self.data();d['strokes']=[{'kind':'spot','points':[[40,30]],'size':5}];p=self.m.build_plan(d);self.assertEqual(p['steps'][1]['params']['type'],'proximityMatch');self.assertNotIn('source',p['steps'][1]['params'])
if __name__=='__main__':unittest.main()
