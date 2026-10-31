# 0.4.16 — TV sport-family artwork, regression category tests, ambient debug

Local release prep only: do not overwrite/publish 0.4.15, parent owns deploy. This release introduces:

- Correct family/alias fallback for artwork in football/soccer, hockey, NCAA soccer, MLS, generic cases; real coverage for events like Mechelen/Genk, non-NFL American football, others. No more blank cards for these categories.
- Extensive browser and regression test coverage for hero and card art on real and stub data (test_tv_startup_browser.py, startup_live.py, new parametric category cases).
- All shelves/DOM/focus and performance criteria unchanged; no extraneous category wallpapering; Home has true-visual fallback when photo absent (not blank motif, not logo-only unless intended).
- Mirrors all prior 0.4.15 docs on catalog/artwork byte/audit. No new images added; asset hashes/manifest identical.
- Bump package, appinfo, config, build tokens, asset queries strictly to 0.4.16; nested/root Homebrew catalogs rewritten (not published/deployed). No overwrite of 0.4.15.

Verification:
- Passes all tests: tv_startup_browser, startup_live, cinema_browser etc. on real and stub data (Playwright isolated Chromium, AGENT_BROWSER_EXECUTABLE_PATH).
- All TV asset bytes and normalized permissions confirmed against backend.
- Full pre-existing audit/usage/warning context in release-0.4.15.md applies unchanged for artwork, legal, and device proof (still unverified on physical LG).
