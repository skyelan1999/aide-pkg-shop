#!/usr/bin/env python3
"""Build deterministic official packages from an explicit Aide Git commit; no user registry/cache."""
import argparse, hashlib, io, json, re, subprocess, tempfile, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
 'creation': ['office','sqlite','propeller-aero','skill','plugin-authoring'],
 'workspace': ['archive-tools','markdown-history','environment-guide','terminal','browser-control','computer-control'],
 'communication': ['comm-serial','comm-ssh','comm-tcp','comm-udp'],
 'planning': ['goal','plan','todo','feedback','subagent','workflow'],
 'utilities': ['current-time','lunar-calendar'],
}
CATEGORY = {p:g for g,ps in GROUPS.items() for p in ps}
PERMISSIONS = {
 'creation':'可向 Aide 提交文件、命令或引用管理提案；相关操作沿用现有授权。',
 'workspace':'可能访问已授权文件或调用主机控制能力；浏览器和电脑控制另需宿主授权。',
 'communication':'可连接用户指定的设备或远程主机；需自行配置连接和凭据。',
 'planning':'注册任务协调工具；真实任务执行和管理操作沿用 Aide 权限。',
 'utilities':'读取日期、时间或本地算法数据；以详情和源码为准。',
}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--aide',type=Path,required=True);ap.add_argument('--ref',required=True);o=ap.parse_args()
 def git(*args):return subprocess.check_output(['git','-C',str(o.aide),*args])
 commit=git('rev-parse',o.ref+'^{commit}').decode().strip();host=git('show',commit+':internal/server/plugin_host.js').decode()
 items=[]
 with tempfile.TemporaryDirectory(prefix='aide-market-') as temp:
  for ident,category in CATEGORY.items():
   prefix='plugins/'+ident+'/';names=git('ls-tree','-r','--name-only',commit,'--',prefix).decode().splitlines()
   if not names:continue
   files={name[len(prefix):]:git('show',commit+':'+name) for name in names}
   manifest=json.loads(files['manifest.json']);assert manifest['id']==ident and manifest['main']=='index.js'
   # Use exactly the same standalone-entry validation as the existing installer.
   entry=Path(temp)/'index.js';entry.write_bytes(files['index.js'])
   validation=json.loads(subprocess.check_output(['node','-e',host,'validate',str(entry)]))
   if not validation.get('ok'):raise ValueError((ident,validation))
   files.setdefault('LICENSE',git('show',commit+':LICENSE'))
   buffer=io.BytesIO()
   with zipfile.ZipFile(buffer,'w') as z:
    for name in sorted(files):
     assert '..' not in Path(name).parts and not name.startswith('/')
     info=zipfile.ZipInfo(name,(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,files[name])
   raw=buffer.getvalue();assert len(raw)<=24*1024*1024
   digest=hashlib.sha256(raw).hexdigest();package='packages/'+ident+'/'+manifest['version']+'-'+digest[:12]+'.zip'
   dest=ROOT/package;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
   dependencies=[]
   if 'package.json' in files:
    dependencies=[name+' '+version for name,version in json.loads(files['package.json']).get('dependencies',{}).items()]
   if ident=='browser-control':dependencies.append('Aide 浏览器运行环境；Safari 模式需要宿主桥接')
   if ident=='computer-control':dependencies.append('Aide Computer Bridge 与操作系统屏幕录制/辅助功能权限')
   if ident=='office':dependencies.append('Aide Office Python 运行环境')
   if ident=='skill':dependencies.append('需要包含 skill_library 原生执行器的 Aide 源码构建（192b80f3 及后续）；旧版仅上传 ZIP 不足以启用')
   if ident=='plugin-authoring':dependencies.append('需要 Aide 原生 manage_plugins / manage_references 管理执行器；管理动作遵守角色开关与人工确认')
   readme=files.get('README.md',b'').decode('utf-8',errors='replace')[:16000]
   item=dict(id=ident,kind='plugin',name=manifest['name'],description=manifest.get('description',''),version=manifest['version'],author='Aide',category=category,icon=category,package=package,sha256=digest,bytes=len(raw),minAideVersion='0.1.17.0 RC2',platforms=['windows','macos','linux'],dependencies=dependencies,permissions=PERMISSIONS[category],trustNotice='Node 插件在宿主中执行；目录审核和摘要校验不等于权限沙箱。安装会注册并启用插件。',features=['skill-library-v1'] if ident=='skill' else ['plugin-authoring-v1'] if ident=='plugin-authoring' else [],source='https://github.com/skyelan1999/aide/tree/'+commit+'/'+prefix.rstrip('/'),license='MIT',readme=readme,screenshots=[],changelog='官方目录首批收录；打包源码固定为 '+commit[:8]+'。')
   items.append(item)
 catalog=dict(schemaVersion=1,title='Aide 官方插件市场',sourceCommit=commit,plugins=items)
 (ROOT/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(dict(plugins=len(items),sourceCommit=commit,bytes=sum(x['bytes'] for x in items))))
if __name__=='__main__':main()
