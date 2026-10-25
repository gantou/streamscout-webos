"""Run with StreamScout's Playwright environment; no TV claimed."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.connect_over_cdp(os.getenv('STREAMSCOUT_CDP','http://127.0.0.1:19223'))
    ctx=browser.new_context(viewport={'width':1920,'height':1080})
    page=ctx.new_page(); errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    def asset(route):
        path=route.request.url.split('launcher.test/')[1].split('?')[0]
        route.fulfill(path=str(ROOT/'app'/(path or 'index.html')))
    page.route('http://launcher.test/**',asset)
    page.goto('http://launcher.test/?setup=1')
    page.locator('#server').fill('file:///etc/passwd')
    page.locator('#connect').click()
    assert 'Could not connect' in page.locator('#status').inner_text()
    page.locator('#server').fill('http://127.0.0.1:8000')
    page.screenshot(path='/home/hermes/.hermes/cache/scratch/streamscout-webos-setup.png')
    page.locator('#connect').click()
    page.wait_for_url('http://127.0.0.1:8000/?client=webos*')
    # Simulate webOSUserScripts injection; Chromium does not inject this itself.
    page.evaluate((ROOT/'app/webOSUserScripts/userScript.js').read_text())
    assert page.locator('body').evaluate("e=>e.classList.contains('tv-mode')")
    page.locator('#primary-nav [data-view=settings]').click()
    page.evaluate("window.dispatchEvent(new KeyboardEvent('keydown',{keyCode:461,bubbles:true,cancelable:true}))")
    assert page.locator('#primary-nav [data-view=home]').get_attribute('aria-pressed')=='true'
    page.evaluate("window.__back=0;window.PalmSystem={platformBack:()=>window.__back++};window.dispatchEvent(new KeyboardEvent('keydown',{keyCode:461,bubbles:true,cancelable:true}))")
    assert page.evaluate('window.__back')==1
    assert not errors, errors
    ctx.close();browser.close()
print('Launcher validation, real-server connection, TV mode and LG Back mapping passed')
