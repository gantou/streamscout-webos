# 0.4.15 — TV artwork, bounded shelves and ambient shuffle

Local release preparation only. No commit, push, deployment, upload or publication was performed.

## Changes

- Synchronize the hosted backend TV frontend and packaged `app/tv` bytes; bump TV asset queries and launcher build token to 0.4.15.
- Ship 39 baseline RGB JPEGs (36 new, three optimized legacy files), totaling 10,375,199 JPEG bytes. Each is at most 1920 pixels on its long edge and 300,000 bytes. There are 38 action-suitable photos; the retained Justin Jefferson static pregame image remains in the manifest for compatibility but is excluded from ambient and action artwork selection.
- Include image-specific Commons sources, creator/licence credits, source SHA-1, output SHA-256, dimensions, modification notices and action context in `app/tv/assets/manifest.json`. These are resized/recompressed derivatives, not unchanged originals. CC BY/CC BY-SA obligations remain applicable; no athlete publicity, trademark or endorsement clearance is claimed.
- Match sports artwork within its league and label unmatched fallback art illustrative rather than implying it depicts the playing teams.
- Bound large catalogs to eight mounted cards per resident shelf, preserve logical navigation through the full collection, avoid unchanged shelf/hero reconstruction, and render initial content without waiting for score requests.
- Shuffle the ambient deck separately on each opening. When enough eligible images exist, the new first image avoids both the previous opening image and the previous last-displayed image. Rotate every 25 seconds; retain moving clock, five-minute exit, remote dismissal and focus restoration. Native OLED screensaver settings remain unchanged.

## Verification

Executed locally:

```sh
# /opt/data/streamscout
STREAMSCOUT_CHROMIUM="$AGENT_BROWSER_EXECUTABLE_PATH" uv run pytest -q
uv run --with pillow python scripts/verify_tv_artwork.py
node --test tests/playback.test.cjs

# /opt/data/streamscout-webos
npm test
npm run build
python3 tools/verify_release.py --update-catalogs
python3 tools/verify_release.py
```

Backend full suite: **190 passed**, with one existing Starlette/httpx deprecation warning. This includes real installed Chromium browser tests, seven ambient openings with alternating rotated/immediate closes, ineligible-photo exclusion, and large-catalog performance/navigation tests. webOS Node tests: **5 passed**. Backend playback Node tests: **13 passed**. Offline artwork provenance/bytes validation: **39 photos verified**.

`tools/verify_release.py` inspects actual `data.tar.gz` members, checks every packaged application file against source bytes, compares the complete backend/webOS TV file sets, verifies all 39 image hashes, enforces directory 755/file 644 payload modes, and checks version/hash/size across both nested manifests and the bare-root JSON catalog. It also checks that `docs/release-0.4.14.md` still equals its committed bytes.

Prepared artifact: `dist/com.gantou.streamscout_0.4.15_all.ipk`, **10,416,834 bytes**, SHA-256 `48d02b9e5980fa452139e688ee414125aa2288255e2762f3d2965df9018dcaf1`. Actual payload: nine directories at 755, 52 files at 644; all 51 application files match audited sources byte-for-byte (the additional file is package metadata). LG's default JS minification initially prevented exact byte parity; `tools/build.py` now restores original application bytes while normalizing the payload. Rerun catalog update and verification after any rebuild because archive timestamps can change the hash.

## Not verified

Physical LG installation, hosted userscript injection, Magic Remote, suspend/resume and advancing live video remain unverified. Local/browser success is not physical-TV compatibility. No publication URLs have been fetched for this unpublished version. The exact requested Edwards dunk / Melo competitive three-pointer / Jefferson spectacular catch set is not claimed.
