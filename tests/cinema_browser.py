"""Dedicated TV acceptance tests; real hosted data, no provider fixtures."""
import os
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.connect_over_cdp(os.getenv('STREAMSCOUT_CDP','http://127.0.0.1:19223'))
 c=b.new_context(viewport={'width':1920,'height':1080}); page=c.new_page()
 page.goto('http://127.0.0.1:8000/tv/?client=webos',wait_until='domcontentloaded')
 page.wait_for_selector('#tv-root',timeout=5000)
 page.wait_for_selector('.tv-tile',timeout=15000)
 tiles=page.locator('.tv-row').first.locator('.tv-tile'); tiles.first.focus()
 page.wait_for_timeout(350)
 left=page.locator('#tv-stage').bounding_box()
 assert page.locator('#tv-menu').bounding_box()['x']+page.locator('#tv-menu').bounding_box()['width']<=0
 page.keyboard.press('ArrowLeft'); page.wait_for_timeout(350)
 assert page.evaluate('document.activeElement.matches("#tv-menu button")')
 assert page.locator('#tv-stage').bounding_box()==left
 page.keyboard.press('ArrowRight'); assert tiles.first.evaluate('e=>e===document.activeElement')
 for _ in range(tiles.count()+3): page.keyboard.press('ArrowRight')
 assert tiles.last.evaluate('e=>e===document.activeElement')
 key=page.evaluate('document.activeElement.dataset.key')
 page.keyboard.press('Enter'); page.wait_for_selector('#tv-details:not([hidden])')
 assert page.evaluate('document.activeElement.matches("#tv-details button")')
 page.keyboard.press('Escape'); assert page.evaluate('document.activeElement.dataset.key')==key
 page.wait_for_timeout(250)
 assert page.locator('#tv-title').inner_text()==tiles.last.locator('.tv-caption').inner_text()
 assert page.locator('#tv-backdrop .tv-art').bounding_box()['height']>=page.locator('#tv-hero').bounding_box()['height']*.9
 page.screenshot(path='/home/hermes/.hermes/cache/scratch/streamscout-cinema-1080.png')
 c.close(); b.close()
print('TV menu hide/layout stability, boundaries and details focus restoration passed')
