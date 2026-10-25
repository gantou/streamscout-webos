# StreamScout for webOS

TV client for [StreamScout](https://github.com/gantou/streamscout). The FastAPI server retains discovery, scores, profiles, recording and relaying. This repository owns the LG launcher, setup and remote adaptations. No backend fork or root service.

## First build (0.1.0)

- Packaged full-screen launcher, app icon, remembered server address and automatic reconnect on launch.
- Top-level hosted StreamScout UI; no iframe (server CSP forbids framing).
- `webOSUserScripts/userScript.js` enables TV mode, maps LG Back (461) and media controls, adds Change server and a connection retry screen.
- Existing HLS.js/native fallback is reused unchanged. **Native-first playback tuning is not implemented yet.**
- TV screensaver defaults are preserved. No elevated privileges or firmware modifications.

## Build

```sh
npm ci --ignore-scripts
npm test
npm run build
```

Output: `dist/com.gantou.streamscout_0.1.0_all.ipk`.

## Install / test

With an already-configured LG/webOS CLI target:

```sh
npx ares-install --device YOUR_TV dist/com.gantou.streamscout_0.1.0_all.ipk
npx ares-launch --device YOUR_TV com.gantou.streamscout
```

On first launch enter your **TV-accessible** server URL, not localhost. Settings → Change StreamScout server returns to setup. Home-level Back hands control back to webOS.

In Homebrew Channel → Settings → Add repository, enter:

```
https://raw.githubusercontent.com/gantou/streamscout-webos/main/homebrew/repo.json
```

Refresh the store, select StreamScout and install. The catalog and manifest are hosted in this public repository; the IPK downloads from GitHub Releases. Your StreamScout backend remains LAN-only.

## Verification and limitations

`npm test` checks URL validation. `tests/browser_smoke.py` uses Playwright from the backend environment, connects the launcher to the real running server and tests TV mode/Back mapping with simulated userscript injection. Run:

```sh
cd ../streamscout
uv run python ../streamscout-webos/tests/browser_smoke.py
```

The official LG packager produced the IPK. Real G3 installation, userscript injection, Magic Remote, suspend/resume and advancing live video **have not been tested on the physical TV**. Browser tests are not proof of those. Latest firmware is not an exact runtime version; collect the installed webOS version before declaring compatibility.

Launcher health fetch uses no-cors for cross-origin reachability, not HTTP health validation; the hosted page polls and validates health same-origin after launch. Keep the backend trusted-LAN only. Subpath URLs are preserved in setup, but the existing backend uses root-relative API routes and therefore requires root hosting/proxy rewriting.

The LG CLI ships vulnerable pinned/bundled build-time dependencies reported by npm audit. They are not included in the TV IPK. Do not use CLI development servers on untrusted networks. Recheck audit when upgrading the CLI.

References: [LG hosted apps](https://webostv.developer.lge.com/develop/getting-started/web-app-types), [LG Back button](https://webostv.developer.lge.com/develop/guides/back-button), [webOS userscripts](https://www.webosbrew.org/pages/web-development), [Homebrew Channel](https://github.com/webosbrew/webos-homebrew-channel/).
