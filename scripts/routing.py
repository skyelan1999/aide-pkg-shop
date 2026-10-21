"""Bounded capability metadata; data only, no executable routing rules."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALIASES={
 'terminal':['终端','ssh','tcp','udp','串口','serial','设备调试','中继'],
 'almanac':['黄历','农历','阴历','宜忌','节气','万年历'],
 'current-time':['当前时间','现在几点','时区','clock','time'],
 'lunar-calendar':['农历','阴历','节气'],
 'office':['word','excel','powerpoint','docx','xlsx','pptx','办公文档'],
 'archive-tools':['压缩','解压','zip','tar','archive'],
 'sqlite':['sqlite','数据库','sql'],
 'browser-control':['浏览器','网页','browser','网页自动化'],
 'computer-control':['电脑控制','桌面控制','鼠标','键盘'],
 'skill':['技能','skill'], 'goal':['目标','goal'], 'plan':['计划','plan'],
 'todo':['待办','todo'], 'feedback':['反馈','feedback'],
 'workflow':['工作流','workflow'],'subagent':['子代理','subagent'],
 'environment-guide':['环境指南','环境配置','环境激活'],
 'markdown-history':['markdown历史','版本历史','历史版本'],
 'plugin-authoring':['插件开发','编写插件','安装插件'],
}
EXTENSIONS={'office':['.docx','.xlsx','.pptx'],'sqlite':['.sqlite','.db'],'archive-tools':['.zip','.tar','.gz']}
def metadata(p):
 ident=p['id'];raw=p.get('routing')
 if raw is None:
  words=[ident,p.get('name',ident)]+ALIASES.get(ident.lower(),[])
  words=list(dict.fromkeys(w.strip().lower() for w in words if w.strip()))
  raw=dict(keywords=words[:32],extensions=EXTENSIONS.get(ident.lower(),[]),summary=p.get('description','')[:240])
 assert isinstance(raw,dict) and set(raw)<= {'keywords','extensions','summary'}
 words=raw.get('keywords');assert isinstance(words,list) and 1<=len(words)<=32
 seen=set()
 for w in words:
  assert isinstance(w,str) and w==w.strip() and 0<len(w.encode())<=96 and not any(c in w for c in '\r\n\0')
  assert w.lower() not in seen;seen.add(w.lower())
 extensions=raw.get('extensions',[]);assert isinstance(extensions,list) and len(extensions)<=16
 for e in extensions:assert isinstance(e,str) and re.fullmatch(r'\.[a-z0-9][a-z0-9_+.-]{0,23}',e) and '..' not in e
 assert isinstance(raw.get('summary'),str) and len(raw['summary'].encode())<=1024
 return raw

def build_index(catalog):
 entries=[]
 for p in catalog['plugins']+catalog.get('privateListings',[]):
  p['routing']=metadata(p)
  entries.append(dict(id=p['id'],name=p['name'],version=p['version'],distribution=p.get('distribution','public'),routing=p['routing']))
 return dict(schemaVersion=1,sourceCommit=catalog['sourceCommit'],plugins=entries)
def write(catalog,root=ROOT):
 index=build_index(catalog)
 (root/'routing.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
 return index
if __name__=='__main__':
 p=ROOT/'catalog.json';catalog=json.loads(p.read_text());write(catalog);p.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
