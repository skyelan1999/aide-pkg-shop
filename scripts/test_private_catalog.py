import copy,hashlib,json,unittest,zipfile
from verify_catalog import ROOT,validate_private
from routing import metadata
class PrivateCatalogTest(unittest.TestCase):
 def test_commercial_preparation_has_no_distribution(self):
  catalog=json.loads((ROOT/'catalog.json').read_text())
  for ident in ('pjplan',):
   item=json.loads((ROOT/'listings'/f'{ident}.json').read_text());validate_private(item)
   self.assertEqual(item['commerce']['status'],'coming_soon')
   self.assertEqual(item['commerce']['publicKeys'],{})
   self.assertTrue(item['source'].startswith('https://github.com/skyelan1999/'))
   self.assertFalse(any(k in item for k in ('package','sha256','bytes','downloadURL')))
   self.assertNotIn('purchaseURL',item['commerce'])
   self.assertEqual([x for x in catalog['privateListings'] if x['id']==ident],[dict(item,routing=metadata(item))])
 def test_compare_exposes_only_licensed_thin_client(self):
  item=json.loads((ROOT/'listings/compare.json').read_text())
  catalog=json.loads((ROOT/'catalog.json').read_text())
  self.assertEqual([x for x in catalog['plugins'] if x['id']=='compare'],[item])
  self.assertFalse(any(x['id']=='compare' for x in catalog['privateListings']))
  self.assertEqual(item['distribution'],'public')
  self.assertIs(item['activationRequired'],True)
  self.assertNotIn('commerce',item)
  self.assertTrue(item['license'].startswith('Proprietary'))
  self.assertTrue(item['source'].startswith('https://github.com/skyelan1999/aide-commercial-downloads/releases/'))
  pkg=ROOT/item['package']
  self.assertEqual(hashlib.sha256(pkg.read_bytes()).hexdigest(),item['sha256'])
  with zipfile.ZipFile(pkg) as z:
   self.assertEqual(set(z.namelist()), {'LICENSE','README.md','THIRD-PARTY-NOTICES.md','compare-source.cjs','index.js','manifest.json','offline-adapter.cjs','workbench.html'})
   manifest=json.loads(z.read('manifest.json'))
   self.assertEqual(manifest['license'],'Proprietary')
   self.assertEqual(manifest['version'],item['version'])
   self.assertIs(manifest['commercial']['offlineLicense'],True)
   self.assertIs(manifest['settingsSchema']['properties']['offlineMacDockerWorkspace']['default'],False)
 def test_rejects_public_package_unconfigured_sale_and_unsafe_checkout(self):
  p=json.loads((ROOT/'listings/pjplan.json').read_text())
  for field,value in [('package','packages/pjplan/secret.zip'),('sha256','a'*64),('bytes',1),('commerce',{'status':'available','model':'perpetual-major'}),('commerce',{'status':'coming_soon','model':'perpetual-major','purchaseURL':'javascript:alert(1)'})]:
   bad=copy.deepcopy(p);bad[field]=value
   with self.assertRaises(AssertionError):validate_private(bad)
if __name__=='__main__':unittest.main()
