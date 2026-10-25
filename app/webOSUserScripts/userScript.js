// webOS injects this script into hosted pages, including remote origins.
(function(){'use strict';
var params=new URLSearchParams(location.search);if(params.get('client')!=='webos'||window.__streamscoutWebOS)return;window.__streamscoutWebOS=true;
var launcher=params.get('launcher');
try{if(launcher&&new URL(launcher).protocol!=='file:')launcher=null;}catch(e){launcher=null;}
try{localStorage.setItem('streamscout-tv','true');}catch(e){}
function configure(){configureTV();document.body.classList.add('tv-mode');var tv=document.getElementById('tv-mode');if(tv){tv.checked=true;tv.dispatchEvent(new Event('change'));}var style=document.createElement('style');style.textContent='body.tv-mode footer{display:none}#webos-connection{position:fixed;z-index:100000;inset:0;background:#0b1118;color:#eef5f8;display:flex;flex-direction:column;align-items:center;justify-content:center;font:28px Arial}#webos-connection button{padding:20px 30px;margin:20px;font-size:26px}#webos-server-settings{font-size:24px;padding:18px;margin:20px 0}';document.head.append(style);var settings=document.getElementById('settings-view');if(settings&&launcher){var b=document.createElement('button');b.id='webos-server-settings';b.textContent='Change StreamScout server';b.addEventListener('click',function(){location.href=launcher+'?setup=1';});settings.prepend(b);}var home=document.querySelector('#primary-nav [data-view=home]');if(home)home.focus();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',configure);else configure();
function video(){return document.getElementById('player');}
function configureTV(){
 document.body.classList.add('webos-app');
 var css=document.createElement('style');css.textContent=`
 body.webos-app{background:#080a0d;font-family:Arial,sans-serif}
 .webos-app header{border:0;background:transparent;padding:24px 48px}
 .webos-app #primary-nav{border:0;background:transparent;gap:24px;padding:12px 48px}
 .webos-app #primary-nav button{font-size:26px;border:0;background:transparent;padding:16px 24px}
 .webos-app #primary-nav button[aria-pressed=true]{color:#fff;background:#242830}
 .webos-app #content{padding:24px 48px}
 .webos-app .content-shelf{gap:28px;padding:16px 8px 32px}
 .webos-app .content-tile{border-radius:8px}
 .webos-app .content-tile:focus{outline:4px solid white;outline-offset:6px;transform:scale(1.025)}
 .webos-app button:focus-visible{outline:3px solid white;outline-offset:5px}
 .webos-app .manage-settings,.webos-app footer{display:none!important}
 .webos-app #watch:not([hidden]){position:fixed!important;inset:0!important;width:100vw!important;height:100vh!important;max-width:none!important;margin:0!important;padding:0!important;border:0!important;border-radius:0!important;background:#000;z-index:90000;overflow:hidden}
 .webos-app #player{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;max-height:none!important;margin:0!important;padding:0!important;border:0!important;object-fit:contain;background:#000;border-radius:0!important}
 .webos-watching header,.webos-watching #primary-nav,.webos-watching #browse-nav{visibility:hidden}
 .webos-app #watch>.section-title{position:absolute;top:0;left:0;right:0;z-index:3;padding:32px 48px;background:linear-gradient(#000c,transparent)}
 .webos-app #watch>.section-title h3{font-size:28px}
 .webos-app #watch>.actions{position:absolute;bottom:0;left:0;right:0;z-index:3;padding:40px 48px;display:flex;align-items:center;gap:24px;background:linear-gradient(transparent,#000e)}
 .webos-app #watch button{font-size:26px;padding:16px 28px;border-radius:6px}
 .webos-app #fullscreen-player,.webos-app #playback-diagnostics,.webos-app #watch>p.muted{display:none!important}
 .webos-app #playback-status{position:absolute;top:120px;left:48px;right:48px;z-index:3;font-size:26px;background:#000a;width:fit-content}
 .webos-app #playback-status:empty{display:none}
 .webos-controls-hidden #watch>.section-title,.webos-controls-hidden #watch>.actions,.webos-controls-hidden #playback-status{opacity:0;pointer-events:none}
 `;var sheet=Array.from(document.styleSheets).find(function(s){return s.href&&new URL(s.href).origin===location.origin;});if(!sheet)return;css.textContent.split('}').forEach(function(rule){if(rule.trim())sheet.insertRule(rule+'}',sheet.cssRules.length);});
 var panel=document.getElementById('watch'),v=video();if(!panel||!v)return;
 var toggle=document.createElement('button');toggle.id='webos-toggle';toggle.textContent='Play';toggle.onclick=function(){if(v.paused)v.play().catch(function(){});else v.pause();};
 panel.querySelector('.actions').prepend(toggle);v.controls=false;
 var timer,playing=false,origin=null;
 function reveal(){clearTimeout(timer);document.body.classList.remove('webos-controls-hidden');if(!panel.hidden&&playing)timer=setTimeout(function(){document.body.classList.add('webos-controls-hidden');},3000);}
 function sync(){var was=document.body.classList.contains('webos-watching');document.body.classList.toggle('webos-watching',!panel.hidden);if(!panel.hidden&&!was){origin=document.activeElement;reveal();toggle.focus({preventScroll:true});}else if(panel.hidden&&was){clearTimeout(timer);playing=false;document.body.classList.remove('webos-controls-hidden');if(origin&&origin.isConnected&&!origin.closest('[hidden]'))origin.focus({preventScroll:true});}}
 new MutationObserver(sync).observe(panel,{attributes:true,attributeFilter:['hidden']});sync();
 v.addEventListener('playing',function(){playing=true;toggle.textContent='Pause';reveal();});
 ['pause','ended','error','waiting'].forEach(function(type){v.addEventListener(type,function(){playing=false;toggle.textContent=v.paused?'Play':'Pause';reveal();});});
 window.addEventListener('keydown',function(e){if(panel.hidden)return;var hidden=document.body.classList.contains('webos-controls-hidden');reveal();if(hidden&&['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Enter'].includes(e.key)){e.preventDefault();e.stopImmediatePropagation();toggle.focus({preventScroll:true});}},true);
 panel.addEventListener('pointermove',reveal);panel.addEventListener('focusin',reveal);
}
// Capture before the hosted application's Back handlers. Translate LG 461 once.
window.addEventListener('keydown',function(e){var key=e.keyCode;if(key===461){e.preventDefault();e.stopImmediatePropagation();var watch=document.getElementById('watch'),detail=document.getElementById('content-detail'),home=document.querySelector('#primary-nav [data-view=home]');if((!watch||watch.hidden)&&(!detail||detail.hidden)&&home&&home.getAttribute('aria-pressed')==='true'){if(window.PalmSystem&&PalmSystem.platformBack)PalmSystem.platformBack();return;}document.dispatchEvent(new KeyboardEvent('keydown',{key:'BrowserBack',bubbles:true,cancelable:true}));return;}if([415,19,413,179].includes(key)){var v=video(),panel=document.getElementById('watch');if(!v||!panel||panel.hidden)return;e.preventDefault();e.stopImmediatePropagation();if(key===413){document.dispatchEvent(new KeyboardEvent('keydown',{key:'BrowserBack',bubbles:true,cancelable:true}));return;}if(key===19||(key===179&&!v.paused))v.pause();else v.play().catch(function(){});}},true);
// Do not disable the LG screensaver or request elevated privileges.
var failures=0;async function check(){if(document.hidden)return;try{var r=await fetch('/api/health',{signal:AbortSignal.timeout(8000)});if(!r.ok)throw new Error('offline');failures=0;document.getElementById('webos-connection')?.remove();}catch(e){if(++failures<2||document.getElementById('webos-connection'))return;var box=document.createElement('section');box.id='webos-connection';box.setAttribute('role','alert');var title=document.createElement('h2');title.textContent='Server unavailable';var text=document.createElement('p');text.textContent='Check your network and StreamScout server.';var retry=document.createElement('button');retry.textContent='Retry';retry.onclick=function(){location.reload();};box.append(title,text,retry);if(launcher){var change=document.createElement('button');change.textContent='Change server';change.onclick=function(){location.href=launcher+'?setup=1';};box.append(change);}document.body.append(box);retry.focus();}}
setInterval(check,15000);
})();
