const {test}=require('node:test');const assert=require('node:assert/strict');
const config=require('../app/config.js');
test('server addresses preserve subpath and set TV mode',()=>{assert.equal(config.serverUrl('http://192.168.1.2:8000'), 'http://192.168.1.2:8000/');assert.equal(config.serverUrl('https://tv.example/scout/'),'https://tv.example/scout/');});
test('reject unsafe schemes, credentials and non-server paths',()=>{for(const v of ['file:///etc/passwd','javascript:alert(1)','https://user:secret@example.com','https://example.com/?x=1','https://example.com/#hi',''])assert.throws(()=>config.serverUrl(v));});
test('target contains explicit client marker and no injected HTML',()=>{const u=new URL(config.target('http://192.168.1.2:8000','file:///app/index.html'));assert.equal(u.searchParams.get('client'),'webos');assert.equal(u.searchParams.get('launcher'),'file:///app/index.html');});
