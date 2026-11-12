# 0.4.17 — Canonical Crew TV shelves

Adds persisted Crew catalogs to Home, Live and Sports, grouped by canonical category. Source choices submit exact catalog/item/source IDs to the existing bounded Crew Watch endpoint. Removed navigation routes are excluded, and stale/scheduled/unverified states remain explicit. Resolver support remains partial; channel visibility does not establish playable coverage.

Browser regression covers empty discovery caches, canonical cards, removal filtering, Watch request IDs, provider errors and Back. Existing TV startup/CSP regressions pass. Launcher token and hosted asset queries bumped; backend and packaged TV bytes synchronized. Physical LG remote/playback confirmation remains outstanding.
