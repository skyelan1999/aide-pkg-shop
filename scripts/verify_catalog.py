#!/usr/bin/env python3
"""Verify every catalog package and assemble only public site files for Pages."""
import hashlib, io, json, shutil, stat, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 d=json.loads((ROOT/'catalog.json').read_text());assert d['schemaVersion']==1
 assert 0<len(d['plugins'])<=200;seen=set();total=0
 for p in d['plugins']:
  assert p['id'] not in seen;seen.add(p['id']);assert p['kind']=='plugin'
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
 out=ROOT/'public';out.mkdir(exist_ok=True)
 for filename in ['index.html','market.css','market.js','favicon.svg','catalog.json']:
  shutil.copyfile(ROOT/filename,out/filename)
 for p in d['plugins']:
  target=out/p['package'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/p['package'],target)
 (out/'.nojekyll').write_text('')
 print(f'PASS {len(seen)} official packages, {total} bytes; public site assembled')
if __name__=='__main__':main()
