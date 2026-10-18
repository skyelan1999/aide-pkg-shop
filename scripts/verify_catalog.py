#!/usr/bin/env python3
"""Verify every catalog package and assemble only public site files for Pages."""
import base64, hashlib, io, json, shutil, stat, subprocess, zipfile
from urllib.parse import urlsplit
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def validate_private(p):
 assert p.get('distribution')=='private'
 assert not any(p.get(k) for k in ('package','sha256','bytes'))
 assert not (ROOT/'packages'/p['id']).exists(), 'private packages must never enter the public repository'
 c=p['commerce'];assert c['status'] in ('coming_soon','available') and c['model']=='perpetual-major'
 assert len(c.get('publicKeys',{}))<=8
 for key in c.get('publicKeys',{}).values():assert len(base64.b64decode(key,validate=True))==32
 if c['status']=='available':assert c.get('publicKeys'), 'publisher keys required before sale'
 if c.get('purchaseURL'):
  u=urlsplit(c['purchaseURL']);assert u.scheme=='https' and u.hostname and not u.username and not u.password and not u.fragment

def main():
 d=json.loads((ROOT/'catalog.json').read_text());assert d['schemaVersion']==1
 items=d['plugins']+d.get('privateListings',[])
 assert all(p.get('distribution','public')=='public' for p in d['plugins'])
 assert all(p.get('distribution')=='private' for p in d.get('privateListings',[]))
 assert 0<len(items)<=200;seen=set();total=0
 for p in items:
  assert p['id'] not in seen;seen.add(p['id']);assert p['kind']=='plugin'
  if p.get('distribution')=='private':
   validate_private(p)
   continue
  assert p.get('distribution','public')=='public' and not p.get('commerce')
  name=p['package'];assert name.startswith('packages/'+p['id']+'/') and '..' not in Path(name).parts and '\\' not in name
  raw=(ROOT/name).read_bytes();assert len(raw)==p['bytes'] and len(raw)<=24*1024*1024
  assert hashlib.sha256(raw).hexdigest()==p['sha256']
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   assert z.testzip() is None and len(z.infolist())<=256
   expanded=0
   for entry in z.infolist():
    assert not entry.filename.startswith('/') and '..' not in Path(entry.filename).parts and not stat.S_ISLNK(entry.external_attr>>16)
    expanded+=entry.file_size
   assert expanded<=64*1024*1024
   m=json.loads(z.read('manifest.json'));assert m['id']==p['id'] and m['version']==p['version'];assert m['main'] in z.namelist()
  total+=len(raw)
 private_ids=[p['id'].lower() for p in items if p.get('distribution')=='private']
 for name in subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0'):
  lower=name.lower()
  assert not lower.endswith(('.pem','.key','.license.json')), 'private keys/customer licenses must not enter marketplace: '+name
  assert not (lower.endswith('.zip') and any(ident in lower for ident in private_ids)), 'private ZIP must not enter public repository: '+name
 out=ROOT/'public';out.mkdir(exist_ok=True)
 # Generated output only: remove stale package copies before publishing a new catalog.
 if (out/'packages').exists():shutil.rmtree(out/'packages')
 for filename in ['index.html','market.css','market.js','favicon.svg','catalog.json']:
  shutil.copyfile(ROOT/filename,out/filename)
 for p in items:
  if p.get('distribution')=='private':continue
  target=out/p['package'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/p['package'],target)
 (out/'.nojekyll').write_text('')
 print(f'PASS {len(seen)} listings, {len(seen)-len(private_ids)} public packages, {len(private_ids)} private listings, {total} public bytes; public site assembled')
if __name__=='__main__':main()
