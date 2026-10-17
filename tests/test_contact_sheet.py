"""联系表尺寸、分页和拒绝无效输入的回归。"""
import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[1]/'skills/photocraft-batch-image-delivery/scripts/contact_sheet.py'
s=importlib.util.spec_from_file_location('contact_sheet',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class ContactSheet(unittest.TestCase):
    def test_pages_keep_explicit_order(self):
        locations=m.grid(7);self.assertEqual([p[0] for p in locations],[0]*6+[1]);self.assertEqual(locations[0][1:],locations[6][1:])
    def test_aspect_and_no_upscale(self):
        wide=m.placement('wide.png',1000,200,120,84,240,200)
        self.assertAlmostEqual(wide['scale'],20.8);self.assertEqual(wide['center'],[120,84])
        self.assertEqual(m.placement('small.png',20,20,120,84,240,200)['scale'],100)
        tall=m.placement('tall.png',200,1000,120,84,240,200);self.assertAlmostEqual(tall['scale'],13.6)
    def test_invalid_inputs_rejected(self):
        for params in [(0,), (201,), (1,0), (1,5), (1,3,4), (1,3,2,20)]:
            with self.subTest(params=params),self.assertRaises(ValueError):m.grid(*params)
if __name__=='__main__':unittest.main()
