"""Remote-only focus regression on the hosted app with deterministic detail content."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.connect_over_cdp(os.getenv('STREAMSCOUT_CDP','http://127.0.0.1:19223'))
 c=b.new_context(viewport={'width':1920,'height':1080});page=c.new_page()
 page.goto('http://127.0.0.1:8000/?client=webos')
 page.evaluate((r/'app/webOSUserScripts/userScript.js').read_text())
 tiles=page.locator('.content-tile:visible')
 if tiles.count():
  tiles.first.focus();page.keyboard.press('Enter')
  page.wait_for_selector('#content-detail:not([hidden])')
  page.wait_for_selector('#webos-detail-hero')
  page.keyboard.press('ArrowDown')
  assert page.evaluate('document.activeElement.id')=='webos-detail-watch'
  page.screenshot(path='/home/hermes/.hermes/cache/scratch/streamscout-webos-details.png')
  page.evaluate("window.dispatchEvent(new KeyboardEvent('keydown',{keyCode:461,bubbles:true,cancelable:true}))")
  assert page.locator('#content-detail').is_hidden()
  assert page.evaluate("document.activeElement.classList.contains('content-tile')")
 page.evaluate("""()=>{let d=document.querySelector('#content-detail');d.hidden=false;document.body.classList.add('detail-open');document.querySelector('#detail-body').innerHTML='<div><button id="remote-watch">Watch</button></div><details><summary id="remote-sources">Sources</summary><button id="remote-source">Source one</button></details>';document.querySelector('#close-detail').focus();}""")
 page.keyboard.press('ArrowDown')
 assert page.evaluate('document.activeElement.id')=='webos-detail-watch',page.evaluate('document.activeElement.id')
 page.keyboard.press('ArrowDown')
 assert page.evaluate('document.activeElement.id')=='remote-watch'
 page.keyboard.press('ArrowDown')
 assert page.evaluate('document.activeElement.id')=='remote-sources'
 page.evaluate("document.activeElement.dispatchEvent(new KeyboardEvent('keydown',{keyCode:13,bubbles:true,cancelable:true}))")
 assert page.locator('#remote-source').is_visible()
 assert page.locator('#webos-detail-hero').is_visible()
 assert page.locator('#webos-detail-watch').is_visible()
 page.keyboard.press('ArrowDown');assert page.evaluate('document.activeElement.id')=='remote-source'
 page.evaluate("document.querySelector('#watch').hidden=false")
 page.wait_for_selector('body.webos-watching')
 page.keyboard.press('ArrowUp');assert page.evaluate('document.activeElement.id')=='close-player'
 page.keyboard.press('ArrowDown');assert page.evaluate('document.activeElement.id')=='webos-toggle'
 page.evaluate("document.querySelector('#watch').hidden=true;document.querySelector('#content-detail').hidden=true")
 page.locator('#primary-nav [data-view=settings]').click()
 page.locator('#settings-nav button').first.focus();page.keyboard.press('ArrowDown')
 assert page.locator('#settings-nav button').nth(1).evaluate('e=>e===document.activeElement')
 c.close();b.close()
print('Remote-only detail navigation, LG OK, player and settings focus passed')
