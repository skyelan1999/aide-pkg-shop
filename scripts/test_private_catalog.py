import copy,json,unittest
from verify_catalog import ROOT,validate_private
class PrivateCatalogTest(unittest.TestCase):
 def test_prelaunch(self):validate_private(json.loads((ROOT/'listings/pjplan.json').read_text()))
 def test_rejects_public_package_unconfigured_sale_and_unsafe_checkout(self):
  p=json.loads((ROOT/'listings/pjplan.json').read_text())
  for field,value in [('package','packages/pjplan/secret.zip'),('sha256','a'*64),('bytes',1),('commerce',{'status':'available','model':'perpetual-major'}),('commerce',{'status':'coming_soon','model':'perpetual-major','purchaseURL':'javascript:alert(1)'})]:
   bad=copy.deepcopy(p);bad[field]=value
   with self.assertRaises(AssertionError):validate_private(bad)
if __name__=='__main__':unittest.main()
