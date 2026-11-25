# Data Transformation & No-Code ETL Architecture Guide

**Project:** Revenue Intelligence Dashboard for NovaTech Solutions  
**Tooling:** Amazon Quick Data Preparation & SPICE (10 GB In-Memory Engine)  
**Author:** Mohamed Abd Elsalam Mohamed Gharieb | **Date:** 25 November 2026

---

## 1. SPICE Ingestion Inventory (4 Datasets Saved)

| SPICE Dataset Name | Role | Row Count | Column Count | Key Data Quality Notes |
|---|---|---:|---:|---|
| `novatech_crm_deals` | Source + Anchor Table | `499` | `20` base + `2` calc (`22`) | `85` unique accounts (`ACCT-001`..`ACCT-085`); `315` null `loss_reason` (expected for Won deals); 4 accounts span >1 `sales_region` |
| `novatech_marketing_campaigns` | Source Table | `2,240` | `20` base + `2` calc (`22`) | `100` unique accounts (`150` orphan rows `ACCT-101`..`ACCT-115`); `24` nulls in `annual_income` (`1.07%`) |
| `novatech_support_tickets` | Source Table | `3,000` | `20` base + `2` calc (`22`) | `100` unique accounts (`204` orphan rows `ACCT-101`..`ACCT-115`); `59` null `ticket_resolved_date` + `59` undocumented null `customer_sentiment` |
| `novatech_unified` | Joined Cross-Domain Table | `63,420` | `58` base + calc (`62+`) | Left Join anchored on `novatech_crm_deals` via `account_id`; excludes `354` orphan leads/tickets (`ACCT-101`..`ACCT-115`) |

---

## 2. Data Type & Schema Corrections Applied

1. **Date & DateTime Parsing:**
   - `deal_created_date`, `deal_closed_date` (`CRM`), `campaign_date` (`Marketing`), and `ticket_created_date` (`Support`) converted from raw `String` to `Date (YYYY-MM-DD)`.
   - `ticket_resolved_date` (`Support`) converted to `DateTime (YYYY-MM-DD HH:MM:SS)` to preserve sub-day SLA hour accuracy (`58.71` mean hours).
2. **Geographic Hierarchies:**
   - `headquarters` (`CRM`, 15 countries) and `Mkt_Src_Cd` (`Marketing`, 8 ISO alpha-2 codes) mapped to `Country` geographic data type.
3. **Currency & Quantitative Indicators:**
   - `deal_value`, `list_price`, `annual_revenue_usd`, `campaign_spend`, `revenue_attributed`, and `annual_income` typed as `Currency (USD)` / `Decimal`.
   - `campaign_response`, `complaint_flag`, `payment_impact`, `security_incident`, and `data_loss` confirmed as binary `Integer (0/1)` flags for direct rate aggregation.

---

## 3. Calculated Fields (Business Logic)

1. **`days_to_close`** (`CRM`): `dateDiff(deal_created_date, deal_closed_date, 'DD')` -> Overall mean `66.76` days (`71.92` Won vs. `57.93` Lost).
2. **`win_rate_flag`** (`CRM`): `ifelse(deal_stage = 'Won', 1, 0)` -> Powers `avg(win_rate_flag) = 63.13%` across regions, managers, and products.
3. **`campaign_roi_pct`** (`Marketing`): `((revenue_attributed - campaign_spend) / campaign_spend) * 100` -> Flags aggregate `-90.88%` ROI and channel efficiency gaps (`-70.74%` Direct Mail vs. `-97.79%` Organic Search).
4. **`resolution_time_days` / `_hours`** (`Support`): `dateDiff(ticket_created_date, ticket_resolved_date, 'DD')` -> Exposes flat SLA (`1.79d` critical vs. `1.97d` low) across `2,941` resolved tickets.
5. **`at_risk_account_flag`** (`Unified / Account 360`): Flags accounts with `>= 80` tickets, `>= 18%` negative sentiment, and `>= $6,000` won CRM revenue (`9` Enterprise accounts representing `$145,735` or `20.61%` of total revenue).

---

## 4. Join Strategy, Anchor Table & Many-to-Many Fan-Out Mitigation

- **Anchor Table:** `novatech_crm_deals` (`499` deals across all `85` revenue-generating/pipeline accounts).
- **Join Configuration:** Two **Left Joins** on `account_id`:
  - `novatech_crm_deals` LEFT JOIN `novatech_marketing_campaigns` ON `account_id`
  - `novatech_crm_deals` LEFT JOIN `novatech_support_tickets` ON `account_id`
- **Why CRM Anchor + Left Join?** Preserves 100% of sales accounts (`ACCT-001` to `ACCT-085`) even if a deal lacks marketing or support history, while excluding `15` unlinked orphan accounts (`ACCT-101`..`ACCT-115`: `150` marketing rows + `204` support rows) that do not correspond to CRM accounts. (Those orphan rows remain fully visible in source datasets on Sheets 1 and 3.)
- **Fan-Out Control:** Because an account like `ACCT-041` (`YieldMax Software`) has `15` CRM deals, `1` marketing lead, and `334` support tickets, the unified join creates `15 × 1 × 334 = 5,010` rows for that single account (`63,420` rows total). Summing `deal_value` directly over `novatech_unified` inflates NovaTech revenue from `$707,201` to `$100,900,682` (`142.68x`). Therefore:
  - **Sheet 1 (Marketing Funnel)** queries `novatech_marketing_campaigns` directly.
  - **Sheet 2 (Sales Pipeline)** queries `novatech_crm_deals` directly.
  - **Sheet 3 (Customer Health)** uses `novatech_unified` with **distinct counts** (`distinct_count(ticket_id)`, `distinct_count(opportunity_id)`) and **account-deduplicated aggregation** (verified against `novatech_account_360_summary.csv`).
