'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const src=fs.readFileSync(require('node:path').join(__dirname,'../market.js'),'utf8'),context=vm.createContext({});vm.runInContext(src.slice(src.indexOf('function routingTerm('),src.indexOf('function paint(')),context);
const match=context.routingTerm;
assert(match('我需要ssh连接设备','ssh'));assert(match('查看黄历宜忌','黄历'));assert(!match('planet','plan'));assert(match('planet plan','plan'));assert(match('inspect robot.step','.step'));assert(!match('unrelated',''));assert(match('literal c++','c++'));assert(!match('anything','.*'));console.log('PASS store routing keyword boundaries, CJK, extensions, literal regex characters');
