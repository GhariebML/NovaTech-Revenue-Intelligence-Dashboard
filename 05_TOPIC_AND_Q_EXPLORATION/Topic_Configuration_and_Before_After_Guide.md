# Quick Chat Topic Configuration & Before/After Accuracy Guide

**Topic Name:** `NovaTech Revenue Intelligence`  
**Associated SPICE Datasets:** `novatech_crm_deals`, `novatech_marketing_campaigns`, `novatech_support_tickets`, `novatech_unified` (`novatech_account_360_summary` reference)  
**Date:** 25 November 2026

---

## 1. Semantic Layer Enrichments Applied

| Configuration Layer | Specific Changes Implemented | Accuracy Problem Solved |
|---|---|---|
| **Friendly Field Names** | Renamed `deal_value` -> `Deal Revenue (USD)`, `win_rate_flag` -> `Win Rate (%)`, `days_to_close` -> `Sales Cycle (Days)`, `campaign_roi_pct` -> `Campaign ROI (%)`, `resolution_time_days` -> `Resolution Time (Days)`. | Prevents Q from referencing cryptic underscore column names or misinterpreting `list_price` vs. `deal_value`. |
| **Business Term Synonyms** | Added *"revenue, sales, closed revenue, ACV"* to `Deal Revenue`; *"win rate, close rate"* to `Win Rate`; *"SLA, turnaround, resolution speed"* to `Resolution Time`; *"churn risk, at-risk"* to `At-Risk Flag`. | Enables VP Sarah Chen and sales managers to ask natural business questions without knowing exact column labels. |
| **Default Aggregations** | Set `Win Rate (%)`, `Response Rate (%)`, `Sales Cycle (Days)`, and `Resolution Time (Days)` to **`AVERAGE`**; `Campaign ROI (%)` to aggregate `(Sum Rev - Sum Spend)/Sum Spend`; `Ticket/Deal Counts` to **`COUNT DISTINCT`**. | Stops Q from summing percentages/flags (which previously yielded nonsensical values like `"Win Rate = 315"` or `"Days to Close = 33,315"`). |
| **Named Filters** | Created **`Won Deals Only`** (`deal_stage = 'Won'`), **`Resolved Tickets Only`** (`ticket_resolved_date IS NOT NULL`), and **`At-Risk Accounts`** (`at_risk_account_flag = 1`). | Prevents `$0` Lost deals from dragging down average deal size (`$1,417` vs. `$2,245`) and avoids skew from `59` null open tickets. |
| **Excluded Fields** | Excluded `data_source`, `opportunity_id`, `lead_id`, `ticket_id` from narrative suggestions (kept available only for distinct counting). | Eliminates irrelevant ID columns from Q auto-generated charts and filters. |

---

## 2. Before vs. After Topic Comparison (3 Baseline Questions)

1. **Baseline Question 1:** *"What is our average deal value and win rate by sales region?"*
   - **Before Topic:** Averaged `$0` Lost deals (`$1,417.24` overall; Central `$1,331.48`, East `$1,442.76`, West `$1,504.50`) and returned raw `Won/Lost` string counts instead of a win rate percentage.
   - **After Topic:** Applied `Won Deals Only` + `Win Rate (%)` average -> Reported **`$2,245.08` Won avg** (West `$2,559.21`, East `$2,495.58`, Central `$1,904.76`) and exact win rates (**Central `69.90%`**, **West `58.79%`**, **East `57.81%`**; **`63.13%` overall**).

2. **Baseline Question 2:** *"Which marketing channel has the highest conversion rate and ROI?"*
   - **Before Topic:** Conflated lead `campaign_response` (`27.19%`) with conversion and averaged row-level ROI percentages instead of weighting by spend.
   - **After Topic:** Separated Response Rate (**Direct Mail `53.02%`**) from Closed-Won Conversion (**Direct Mail `48.99%`**, **Partner Referral `31.10%`**, **Paid Social `22.77%`**, **Email `2.78%`**, **Organic `0.89%`**) and returned exact aggregate ROI (**Direct Mail `-70.74%`** best vs. **Organic `-97.79%`** worst).

3. **Baseline Question 3:** *"Show me at-risk Enterprise accounts with high ticket volume, negative sentiment, and total revenue."*
   - **Before Topic:** Queried `novatech_unified` (`63,420` rows) using naive `SUM(deal_value)`, inflating `YieldMax Software` from `$40,722` to **`$13,601,148`** (`334 × 15` row multiplication!) and ignoring the `59` undocumented null sentiment tickets.
   - **After Topic:** Used `At-Risk Accounts` named filter + deduplicated CRM revenue -> Correctly ranked **YieldMax Software (`$40,722`, `334` tickets, `18.9%` neg)**, **TrueNorth Electronics (`$16,747`, `180` tickets, `25.6%` neg)**, and **LionGate Holdings (`$16,275`, `176` tickets, `21.6%` neg)** across `$145,735` total flagged revenue.
