# Hermes Dashboard Template Summary

Source: `HermesTemplates/hermes-dashboard-template.html`

Key tokens:
- bg: `#15151F`, panel: `rgba(31,31,43,0.55)`, border: `rgba(255,255,255,0.105)`
- text: `#F4F4F8`, muted: `#8A8A9B`, heading: `Inter Tight`, mono: `JetBrains Mono`
- blur: `34px`, nav height: `88px`
- top nav: fixed, three-column grid, glass tabs, status pill with pulse dot
- overview tabs: radar + ops grid + throughput + feed + board/content/schedule panels
- motion: slide-in feed, jitter/decimal counters, pulse dots, sparkline

Reuse notes:
- `.glass` panel is the base for all v3 surfaces
- `.top-nav` becomes the v3 `TopBar`/shell
- `.tabs` maps directly to the Overview/Agents/Tasks tabs
