"""Real TV playback through the actual live Kick Watch action."""
import os,time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.connect_over_cdp(os.getenv('STREAMSCOUT_CDP','http://127.0.0.1:19223'))
 ctx=b.new_context(viewport={'width':1920,'height':1080});page=ctx.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8000/tv/?client=webos')
 page.wait_for_selector('.tv-tile[data-key^="kick:"]',timeout=45000)
 page.locator('.tv-tile[data-key^="kick:"]').first.focus();page.keyboard.press('Enter');page.keyboard.press('Enter')
 page.wait_for_selector('#tv-player:not([hidden])')
 deadline=time.monotonic()+70
 while time.monotonic()<deadline:
  state=page.locator('#tv-video').evaluate('v=>({time:v.currentTime,ready:v.readyState,width:v.videoWidth,height:v.videoHeight})')
  if state['time']>8 and state['ready']>=2:break
  page.wait_for_timeout(1000)
 else:raise AssertionError({'state':state,'status':page.locator('#tv-play-status').inner_text()})
 print('Real advancing TV playback:',state)
 page.wait_for_timeout(3500)
 assert page.locator('body').evaluate('b=>b.classList.contains("controls-hidden")')
 page.keyboard.press('ArrowUp');assert not page.locator('body').evaluate('b=>b.classList.contains("controls-hidden")')
 page.keyboard.press('Escape');assert page.locator('#tv-player').is_hidden();assert page.locator('#tv-details').is_visible()
 page.keyboard.press('Escape');assert page.evaluate('document.activeElement.matches(".tv-tile")')
 assert not errors,errors
 ctx.close();b.close()
print('TV real Watch, controls wake and Back unwind passed')
