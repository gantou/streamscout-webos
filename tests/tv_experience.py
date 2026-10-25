"""Integration checks on the real hosted UI with simulated LG injection."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp(os.getenv('STREAMSCOUT_CDP','http://127.0.0.1:19223'))
    ctx=b.new_context(viewport={'width':1920,'height':1080})
    page=ctx.new_page(); errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:8000/?client=webos')
    page.evaluate((ROOT/'app/webOSUserScripts/userScript.js').read_text())
    page.wait_for_selector('body.webos-app')
    page.evaluate("document.querySelector('#watch').hidden=false")
    page.wait_for_selector('body.webos-watching')
    print('Player bounds:',page.locator('#player').bounding_box())
    assert page.locator('#player').bounding_box()=={'x':0,'y':0,'width':1920,'height':1080}
    assert not page.locator('#player').evaluate('e=>e.controls')
    assert page.locator('#webos-toggle').is_visible()
    page.evaluate("document.querySelector('#player').dispatchEvent(new Event('playing'))")
    page.wait_for_function("()=>document.body.classList.contains('webos-controls-hidden')",timeout=7000)
    page.keyboard.press('ArrowUp')
    assert not page.locator('body').evaluate("e=>e.classList.contains('webos-controls-hidden')")
    page.evaluate("document.querySelector('#player').dispatchEvent(new Event('pause'))")
    page.wait_for_timeout(3500)
    assert page.locator('#webos-toggle').is_visible()
    page.screenshot(path='/home/hermes/.hermes/cache/scratch/streamscout-webos-player.png')
    page.locator('#close-player').click()
    page.wait_for_function("()=>!document.body.classList.contains('webos-watching')")
    assert page.locator('#primary-nav').is_visible()
    page.screenshot(path='/home/hermes/.hermes/cache/scratch/streamscout-webos-browse.png')
    assert not errors,errors
    ctx.close(); b.close()
print('TV viewport player, controls auto-hide/wake/pause, exit to browsing passed')
