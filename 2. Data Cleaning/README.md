# 2. Data Cleaning

## Data Quality Issues Found

### Issue 1 — Budget Utilization Outliers
- **Problem:** Some campaigns show >100% budget utilization (overspend)
- **Fix:** Flagged for audit; capped at 100% for utilization calculations
- **Impact:** Budget efficiency metrics would be inflated

### Issue 2 — ROAS Outliers
- **Problem:** Brand Awareness ROAS of 1,417× appears anomalously high
- **Likely cause:** Last-click attribution over-credits upper-funnel campaigns when users later convert via Email
- **Fix:** Noted in analysis; attribution model review recommended
- **Impact:** Objective-level ROAS comparison misleading without attribution correction

### Issue 3 — Revenue Attribution
- **Problem:** Some campaigns show revenue despite zero conversions tracked
- **Likely cause:** View-through attribution or cross-device tracking gaps
- **Fix:** Flagged; excluded from conversion rate calculations where conversions = 0

### Issue 4 — Missing End Dates
- **Problem:** Running/Active campaigns have no End_Date
- **Fix:** Used data collection date as proxy for duration calculations

## Cleaning Summary

| Issue | Records Affected | Action |
|-------|-----------------|--------|
| Budget overspend | ~15 | Flagged, capped at 100% for utilization |
| ROAS outliers | ~8 | Noted in analysis commentary |
| Zero conversions with revenue | ~12 | Excluded from conv rate analysis |
| Missing end dates | ~45 | Proxy date applied |
