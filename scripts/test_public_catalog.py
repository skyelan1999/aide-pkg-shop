import hashlib,json,re,subprocess,tempfile,unittest
from pathlib import Path
from build_catalog import load_listings

class PublicListingTest(unittest.TestCase):
 def listing(self,**changes):
  return dict(id='example',kind='plugin',distribution='public',package='packages/example/1.0.0-test.zip',sha256='a'*64,bytes=123,**changes)
 def load(self,item):
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory);(p/'example.json').write_text(json.dumps(item));return load_listings(p)
 def test_public_screenshots_remain_compatible_with_existing_hosts(self):
  root=Path(__file__).resolve().parents[1]
  provenance=json.loads((root/'screenshots/provenance.json').read_text())
  expected={image['path']:image for source in provenance['sources'] for image in source['images']}
  found=set()
  for item in load_listings():
   for url in item.get('screenshots',[]):
    match=re.fullmatch(r'https://raw[.]githubusercontent[.]com/skyelan1999/aide-pkg-shop/([a-f0-9]{40})/(screenshots/[^?#]+)',url)
    self.assertIsNotNone(match, 'older hosts only accept official shop screenshots')
    commit,path=match.groups();record=expected[path]
    raw=subprocess.check_output(['git','show',commit+':'+path],cwd=root)
    self.assertEqual(hashlib.sha256(raw).hexdigest(),record['sha256'])
    self.assertEqual(len(raw),record['bytes']);found.add(path)
  self.assertEqual(found,set(expected))
 def test_public_listing_survives_catalog_rebuild(self):
  item=self.listing();self.assertEqual(self.load(item),[item])
 def test_rejects_private_payloads_collisions_and_unsafe_public_paths(self):
  for field,value in [('distribution','private'),('id','office'),('package','packages/example/../../secret.zip'),('sha256','invalid'),('bytes',0),('commerce',{'status':'available'})]:
   item=self.listing();item[field]=value
   with self.assertRaises(AssertionError):self.load(item)
if __name__=='__main__':unittest.main()
