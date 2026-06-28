---
tags: []
aliases: []
created: 2026-06-27
---
# Forge Dashboard Template Summary

Source: `HermesTemplates/forge-dashboard-template.html`

Key tokens:
- Work Sans + JetBrains Mono
- surface: `#0b1120`, panel: `#121724`, panel-hi: `#1a2030`
- sidebar width driven by `--sidebar-width`, glass panels use linear gradient from panel-hi to panel
- system status chips, schedule chips, log table with sticky header
- settings cards with bordered inputs and accent actions

Reuse notes:
- `.glass-panel` becomes `LiquidGlassPanel`
- `.fx-status` chips become `StatusPill`
- `.fx-sched` becomes module/tag chips
- `.fx-logscroll` patterns map to `ActivityFeed`

---
#core-systems #dashboard #zakos

