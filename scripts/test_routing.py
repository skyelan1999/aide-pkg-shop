import copy,json,unittest
from routing import ROOT,build_index,metadata
class RoutingTest(unittest.TestCase):
 def test_new_listing_gets_index_without_host_change(self):
  p=dict(id='new-cad',name='新CAD',version='1.0.0',description='文件建模')
  c=dict(sourceCommit='a'*40,plugins=[p]);d=build_index(c)
  self.assertEqual(d['plugins'][0]['routing']['keywords'],['new-cad','新cad'])
  self.assertEqual(c['plugins'][0]['routing'],d['plugins'][0]['routing'])
 def test_known_extensions_and_aliases(self):
  self.assertIn('ssh',metadata(dict(id='terminal',name='终端'))['keywords'])
  self.assertIn('.docx',metadata(dict(id='office',name='Office'))['extensions'])
 def test_rejects_unbounded_or_executable_metadata(self):
  for r in [dict(keywords=['a']*33,summary=''),dict(keywords=['a','A'],summary=''),dict(keywords=['a'],summary='',script='run'),dict(keywords=['a'],summary='',extensions=['../../a']),dict(keywords=['a\n'],summary='')]:
   with self.assertRaises(AssertionError):metadata(dict(id='test',routing=r))
 def test_checked_in_index_is_complete_and_current(self):
  c=json.loads((ROOT/'catalog.json').read_text());self.assertEqual(json.loads((ROOT/'routing.json').read_text()),build_index(c))
if __name__=='__main__':unittest.main()
