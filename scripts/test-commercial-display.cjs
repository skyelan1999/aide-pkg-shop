'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const src=fs.readFileSync(path.join(__dirname,'../market.js'),'utf8');
const context=vm.createContext({URL});
vm.runInContext(src.slice(src.indexOf('function safeResource('),src.indexOf('function routingTerm(')),context);
const item=JSON.parse(fs.readFileSync(path.join(__dirname,'../listings/pp-customer.json'),'utf8'));
assert.equal(item.activationRequired,true);assert.equal(item.distribution,'public');assert(!item.commerce);
assert(item.license.includes('需离线激活'));assert(item.description.includes('business@sklastu.com'));
for(const id of ['professional-project','pp-leadership','pp-customer']){
 const licensed=JSON.parse(fs.readFileSync(path.join(__dirname,'../listings/'+id+'.json'),'utf8'));
 assert.equal(licensed.distribution,'public',id);assert.equal(licensed.activationRequired,true,id);assert(!licensed.commerce,id);
 assert(licensed.name.includes('商业版'),id);assert(!licensed.name.includes('筹备'),id);assert(!licensed.features.includes('private-plugin-v1'),id);
 assert(licensed.readme.includes('.plicense')&&licensed.readme.includes('.prequest'),id);
 assert(licensed.resources.length>0&&licensed.resources.every(r=>context.safeResource(r)),id);
 assert(licensed.description.includes('business@sklastu.com'),id);
}
const resource=item.resources[0];assert(context.safeResource(resource));
for(const url of ['http://github.com/skyelan1999/aide-pkg-shop/releases/download/v1/a.zip','https://github.com.evil.test/skyelan1999/aide-pkg-shop/releases/download/v1/a.zip','https://user:pass@github.com/skyelan1999/aide-pkg-shop/releases/download/v1/a.zip','https://github.com/another/repo/releases/download/v1/a.zip',resource.url+'?token=secret',resource.url+'#fragment','javascript:alert(1)','https://github.com:444/skyelan1999/aide-pkg-shop/releases/download/v1/a.zip'])assert(!context.safeResource({...resource,url}),url);
for(const changes of [{sha256:'invalid'},{bytes:0},{bytes:1.5},{bytes:300*1024*1024}])assert(!context.safeResource({...resource,...changes}));
assert(!src.includes('个免费'));assert(src.includes("p.activationRequired?'发行说明 ↗':'查看源码 ↗'"));
console.log('PASS licensed public listing, quotation contact and constrained component links');
