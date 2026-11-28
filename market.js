(() => {
'use strict';
const $=id=>document.getElementById(id),node=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;};
const english=document.documentElement.lang==='en',base=document.body.dataset.base||'';
const categories=english?{all:'All plugins',creation:'Creation & professional',workspace:'Workspace',communication:'Communication',planning:'Planning & collaboration',utilities:'Utilities'}:{all:'全部插件',creation:'创作与专业',workspace:'工作空间',communication:'连接与通信',planning:'规划与协作',utilities:'日常工具'};
const paths={creation:'M12 3v18M3 12h18M5 5l14 14M19 5L5 19',workspace:'M3 7h7l2 2h9v11H3ZM3 7V4h7l2 3',communication:'M8 3v5m8-5v5M6 8h12v3a6 6 0 0 1-12 0ZM12 17v4',planning:'M8 5h13M8 12h13M8 19h13M3 5h1M3 12h1M3 19h1',utilities:'M12 3v3m0 12v3M3 12h3m12 0h3M8 8l8 8m0-8-8 8'};
let items=[],translations={},category='all',busy=false,lastFocus=null;
function icon(p){const e=node('span','plugin-icon');e.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="'+(paths[p.category]||paths.creation)+'"/></svg>';return e;}
function safePackage(p){return /^packages\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_.-]+\.zip$/.test(p.package)&&!p.package.includes('..')&&/^[a-f0-9]{64}$/.test(p.sha256)&&p.bytes>0&&p.bytes<=24*1024*1024;}
function privateListing(p){return p.distribution==='private'&&!p.package&&!p.sha256&&!p.bytes&&p.commerce&&['coming_soon','available'].includes(p.commerce.status);}
function safeSource(p){try{const u=new URL(p.source);return u.protocol==='https:'&&u.hostname==='github.com'&&u.pathname.startsWith('/skyelan1999/');}catch{return false;}}
function safeResource(r){try{const u=new URL(r.url);return u.origin==='https://github.com'&&!u.username&&!u.password&&!u.search&&!u.hash&&/^\/skyelan1999\/aide-commercial-downloads\/releases\/download\/[a-zA-Z0-9_.-]+\/[a-zA-Z0-9_.-]+\.zip$/.test(u.pathname)&&/^[a-f0-9]{64}$/.test(r.sha256)&&Number.isSafeInteger(r.bytes)&&r.bytes>0&&r.bytes<=256*1024*1024;}catch{return false;}}
function routingTerm(query,term){
 term=String(term||'').toLowerCase();if(!term)return false;
 if(/[^\x00-\x7f]/.test(term)||term.startsWith('.'))return query.includes(term);
 const escaped=term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');return new RegExp('(^|[^a-z0-9_])'+escaped+'($|[^a-z0-9_])').test(query);
}
function translated(p){
 if(!english)return p;
 const t=translations[p.id]||{},view={...p};
 for(const key of ['name','description','permissions','trustNotice','license'])if(typeof t[key]==='string'&&t[key])view[key]=t[key];
 if(Array.isArray(t.dependencies)&&t.dependencies.every(x=>typeof x==='string'))view.dependencies=t.dependencies;
 if(Array.isArray(t.resourceTitles)&&t.resourceTitles.every(x=>typeof x==='string'))view.resources=(p.resources||[]).map((r,i)=>({...r,title:t.resourceTitles[i]||r.title}));
 if(p.commerce&&typeof t.priceLabel==='string'&&t.priceLabel)view.commerce={...p.commerce,priceLabel:t.priceLabel};
 return view;
}
function paint(){const q=$('search').value.toLowerCase().trim(),matched=items.filter(p=>{const view=translated(p),haystack=(p.name+' '+p.id+' '+p.description+' '+view.name+' '+view.description+' '+(p.routing?.keywords||[]).join(' ')).toLowerCase();return(category==='all'||p.category===category)&&(!q||haystack.includes(q)||(p.routing?.keywords||[]).some(k=>routingTerm(q,k)));});$('grid').replaceChildren();for(const p of matched){const view=translated(p),card=node('article','card'),head=node('div','card-head'),names=node('div');names.append(node('h3','',view.name),node('span','official',(english?'Aide Official · ':'Aide 官方 · ')+(categories[p.category]||(english?'Plugin':'插件'))));head.append(icon(p),names);const foot=node('div','card-foot'),more=node('button','',english?'View details ↗':'查看详情 ↗');more.onclick=()=>details(p);let delivery;if(privateListing(p))delivery=p.commerce.status==='coming_soon'?(english?'Commercial preview':'商业筹备中'):view.commerce.priceLabel;else delivery=(p.activationRequired?(english?'Offline activation required · ':'需离线激活 · '):'')+Math.ceil(p.bytes/1024)+' KB';foot.append(node('span','','v'+p.version+' · '+delivery),more);card.append(head,node('p','',view.description),foot);$('grid').append(card);}$('status').textContent=matched.length?'':(english?'No matching plugins. Try another keyword.':'没有匹配的插件，试试其他关键词。');}
function details(p){
 lastFocus=document.activeElement;const view=translated(p),body=$('detail-body');body.replaceChildren(icon(p));const title=node('h2','',view.name);title.id='detail-title';body.append(title,node('p','',view.description));
 const labels=english?{version:'Version',platforms:'Platforms',minimum:'Minimum Aide',dependencies:'Dependencies',license:'License',permissions:'Permissions',delivery:'Delivery'}:{version:'版本',platforms:'适用平台',minimum:'最低版本',dependencies:'运行依赖',license:'许可证',permissions:'权限说明',delivery:'交付方式'};
 const fallback=english?'Uses the Aide built-in runtime':'使用 Aide 内置运行环境',privateDelivery=english?'Private delivery · Package not public':'私有交付 · 安装包不公开';
 const dl=node('dl');for(const [k,v]of [[labels.version,p.version],[labels.platforms,(p.platforms||[]).join(' / ')],[labels.minimum,p.minAideVersion],[labels.dependencies,(view.dependencies||[]).join(english?' ':'；')||fallback],[labels.license,view.license],[labels.permissions,view.permissions],[privateListing(p)?labels.delivery:'SHA-256',privateListing(p)?privateDelivery:p.sha256]])dl.append(node('dt','',k),node('dd','',v));body.append(dl,node('p','',view.trustNotice));
 if(english){
  const original=[p.readme,p.changelog].filter(Boolean).join('\n\n---\n\n');
  if(original){body.append(node('p','original-note','Publisher README and changelog are preserved in their original Chinese to avoid altering technical or licensing terms.'));const d=node('details'),s=node('summary','','Original README and changelog (Chinese)');d.append(s,node('pre','',original));body.append(d);}
 }else{
  if(p.readme){const d=node('details'),s=node('summary','','阅读使用说明');d.append(s,node('pre','',p.readme));body.append(d);}body.append(node('p','',p.changelog));
 }
 if(privateListing(p)){
  const c=view.commerce,price=c.priceLabel||(english?'Price to be announced':'价格待公布'),availability=c.status==='coming_soon'?(english?'Commercial edition in preparation; not yet available for sale.':'商业版本筹备中，尚未开放销售。'):(english?'After purchase, the publisher privately delivers the package and signed license. Authorize installation in the Aide market details.':'购买后由发布者私下交付安装包和签名许可证，在 Aide 市场详情中授权安装。'),licenseNote=english?'One purchase permanently covers the purchased version; major-version upgrades require separate authorization.':'一次购买可永久使用已购版本；大版本升级单独授权。';body.append(node('p','',price),node('p','',availability),node('p','',licenseNote));
  if(c.status==='available'&&c.purchaseURL){try{const u=new URL(c.purchaseURL);if(u.protocol==='https:'&&!u.username&&!u.password){const buy=node('a','primary',english?'Purchase ↗':'前往购买 ↗');buy.href=u.href;buy.target='_blank';buy.rel='noopener noreferrer';body.append(buy);}}catch{}}
  $('details').showModal();return;
 }
 const actions=node('div','detail-actions'),download=node('button','primary',english?'Download plugin ZIP':'下载插件 ZIP'),source=node('a','',english?(p.activationRequired?'Release notes ↗':'View source ↗'):(p.activationRequired?'发行说明 ↗':'查看源码 ↗')),status=node('p','download-status');status.setAttribute('role','status');source.href=p.source;source.target='_blank';source.rel='noopener noreferrer';download.disabled=!safePackage(p);
 download.onclick=async()=>{if(busy)return;busy=true;download.disabled=true;status.textContent=english?'Downloading and verifying…':'正在下载并校验…';try{const r=await fetch(base+p.package);if(!r.ok)throw Error((english?'Download failed: HTTP ':'下载失败：HTTP ')+r.status);if(Number(r.headers.get('Content-Length'))>p.bytes)throw Error(english?'Unexpected download size':'下载大小异常');const data=await r.arrayBuffer();if(data.byteLength!==p.bytes)throw Error(english?'Incomplete download':'下载不完整');const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',data))).map(b=>b.toString(16).padStart(2,'0')).join('');if(hash!==p.sha256)throw Error(english?'Verification failed; file not saved':'校验失败，文件未保存');const url=URL.createObjectURL(new Blob([data],{type:'application/zip'})),a=node('a');a.href=url;a.download='aide-pkg-'+p.id+'-v'+p.version+'.zip';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);status.textContent=english?'Verified. Install the ZIP in Aide under “Plugins → Upload”.':'校验通过。下载后在 Aide「插件 → 上传」安装。';}catch(e){status.textContent=e.message;}finally{busy=false;download.disabled=false;}};
 actions.append(download,source);body.append(actions,status);for(const r of view.resources||[]){if(!safeResource(r))continue;const a=node('a','',r.title+' ↗');a.href=r.url;a.target='_blank';a.rel='noopener noreferrer';const block=node('div','resource');block.append(a,node('p','',Math.ceil(r.bytes/1024/1024)+(english?' MB · Follow the usage instructions after download':' MB · 下载后按使用说明配置')),node('p','download-status','SHA-256: '+r.sha256));body.append(block);}$('details').showModal();
}
$('close').onclick=()=>$('details').close();$('details').addEventListener('close',()=>lastFocus?.focus());$('search').oninput=paint;
for(const [id,label]of Object.entries(categories)){const b=node('button','',label);b.setAttribute('aria-pressed',String(id===category));b.onclick=()=>{category=id;for(const e of $('categories').children)e.setAttribute('aria-pressed',String(e===b));paint();};$('categories').append(b);}
async function load(){
 try{
  const r=await fetch(base+'catalog.json');if(!r.ok)throw Error(english?'Catalog unavailable':'目录暂不可用');const d=await r.json();if(d.schemaVersion!==1||!Array.isArray(d.plugins)||d.plugins.length+(d.privateListings||[]).length>200)throw Error(english?'Invalid catalog format':'目录格式错误');items=[...d.plugins,...(d.privateListings||[])].filter(p=>p.kind==='plugin'&&(privateListing(p)||safePackage(p))&&safeSource(p));
  if(english){const er=await fetch(base+'catalog-en.json');if(!er.ok)throw Error('English catalog unavailable');const ed=await er.json();if(ed.schemaVersion!==1||!ed.plugins||typeof ed.plugins!=='object'||Array.isArray(ed.plugins))throw Error('Invalid English catalog format');translations=ed.plugins;const ids=new Set(items.map(p=>p.id));if(Object.keys(translations).some(id=>!ids.has(id))||items.some(p=>typeof translations[p.id]?.name!=='string'||typeof translations[p.id]?.description!=='string'))throw Error('English catalog mismatch');}
  const publicCount=items.filter(p=>!privateListing(p)).length,privateCount=items.filter(privateListing).length;$('count').textContent=english?items.length+' plugins · '+publicCount+' public downloads · '+privateCount+' private-delivery '+(privateCount===1?'listing':'listings'):items.length+' 个插件 · '+publicCount+' 个公开下载 · '+privateCount+' 个私下交付条目';paint();
 }catch(e){$('status').textContent=e.message+(english?' Please refresh later.':'，请稍后刷新。');$('count').textContent=english?'Catalog failed to load':'目录加载失败';}
}
load();
})();
