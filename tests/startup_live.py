"""Live hosted TV startup and remote smoke (not physical LG verification)."""
import os
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(os.getenv('STREAMSCOUT_CDP', 'http://127.0.0.1:19223'))
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto('http://127.0.0.1:8000/tv/?client=webos&build=0.4.5', wait_until='domcontentloaded')
    page.wait_for_selector('.tv-tile', timeout=60000)
    assert page.locator('.hero-copy').evaluate('e=>getComputedStyle(e).position') == 'absolute'
    assert page.locator('#tv-notice').is_hidden()
    tiles = page.locator('.tv-row').first.locator('.tv-tile')
    tiles.first.focus()
    page.keyboard.press('ArrowLeft')
    assert page.evaluate('document.activeElement.matches("#tv-menu button")')
    page.keyboard.press('ArrowRight')
    assert tiles.first.evaluate('e=>e===document.activeElement')
    page.keyboard.press('Enter')
    page.wait_for_selector('#tv-details:not([hidden])')
    page.keyboard.press('Escape')
    assert tiles.first.evaluate('e=>e===document.activeElement')
    page.wait_for_timeout(1100)
    assert page.locator('#tv-title').inner_text() == tiles.first.locator('.tv-caption').inner_text()
    assert not errors, errors
    page.screenshot(path='/home/hermes/.hermes/cache/scratch/streamscout-fixed-tv.png')
    print('Live startup: shelves rendered, CSS positioned, menu/Back/details focus passed; tiles:', page.locator('.tv-tile').count())
    context.close()
    browser.close()
