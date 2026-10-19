import json,tempfile,unittest
from pathlib import Path
from build_catalog import load_listings

class PublicListingTest(unittest.TestCase):
 def listing(self,**changes):
  return dict(id='example',kind='plugin',distribution='public',package='packages/example/1.0.0-test.zip',sha256='a'*64,bytes=123,**changes)
 def load(self,item):
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory);(p/'example.json').write_text(json.dumps(item));return load_listings(p)
 def test_public_listing_survives_catalog_rebuild(self):
  item=self.listing();self.assertEqual(self.load(item),[item])
 def test_rejects_private_payloads_collisions_and_unsafe_public_paths(self):
  for field,value in [('distribution','private'),('id','office'),('package','packages/example/../../secret.zip'),('sha256','invalid'),('bytes',0),('commerce',{'status':'available'})]:
   item=self.listing();item[field]=value
   with self.assertRaises(AssertionError):self.load(item)
if __name__=='__main__':unittest.main()
