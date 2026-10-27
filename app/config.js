(function(root){'use strict';
function serverUrl(value){var u=new URL(String(value).trim());if(!/^https?:$/.test(u.protocol)||u.username||u.password||u.search||u.hash)throw new Error('Enter an HTTP or HTTPS server address without credentials, query or fragment.');if(!u.pathname.endsWith('/'))u.pathname+='/';return u.href;}
function target(value,launcher){var u=new URL('tv/',serverUrl(value));u.searchParams.set('client','webos');u.searchParams.set('launcher',launcher);u.searchParams.set('build','0.4.8');return u.href;}
var config={serverUrl:serverUrl,target:target};if(typeof module!=='undefined')module.exports=config;else root.ScoutConfig=config;
})(typeof window!=='undefined'?window:globalThis);
