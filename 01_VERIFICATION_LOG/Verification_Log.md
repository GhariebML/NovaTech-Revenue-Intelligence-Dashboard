# NovaTech Data Verification Log

**Student Name:** Mohamed Abd Elsalam Mohamed Gharieb  
**Course:** Future AWS Agentic AI Business Professional — Course 2 of 3 (Business Intelligence and Knowledge Management Foundations with Amazon Quick)  
**Date:** 25 November 2026

## Instructions

Query each pre-indexed knowledge base using Quick Chat (and cross-verify against the official starter CSVs and `Data_Dictionary.md`). Record the expected answer from the Data Dictionary, Q's observed/verified response, and a Pass/Fail assessment. Minimum 6 entries required; **10 structured entries** across all three data knowledge bases plus Reference Documents are documented below.

## Verification Log

| # | Knowledge Base | Question Asked | Expected Answer (Data Dictionary & Starter CSV) | Q's Actual Answer | Match? | Notes |
|---|---|---|---|---|---|---|
| **1** | **NovaTech CRM Deals** | How many total deal rows, unique accounts, and date range exist in NovaTech CRM Deals? | `499` rows, `20` columns, `85` unique accounts (`ACCT-001` to `ACCT-085`), created `2023-06-17` to `2025-01-25` (closed through `2025-01-31`). | `499` deals across `85` unique accounts (`ACCT-001`–`ACCT-085`), spanning creation `2023-06-17` to `2025-01-25` and close dates through `2025-01-31`. | **PASS** | Exact match across row counts, account keys, and date bounds. |
| **2** | **NovaTech CRM Deals** | What is the Won vs. Lost breakdown, total deal revenue, and null count for `loss_reason`? | `315` Won deals (`63.13%`), `184` Lost deals (`36.87%`), `315` nulls in `loss_reason` (blank on all Won deals). Total won revenue = `$707,201.00`. | `315` Won (`$707,201.00` total; `$2,245.08` mean won deal), `184` Lost (`$0.00` value), and `315` null values in `loss_reason`. | **PASS** | Confirmed that `$0` Lost deals pull overall all-deal average down to `$1,417.24`. |
| **3** | **NovaTech CRM Deals** | How many distinct sales reps, sales managers, regions, and product lines exist? | `30` unique reps, `6` sales managers, `3` regions (`Central`, `East`, `West`), `7` products across `2` categories (`NovaPulse`, `NovaEdge`). | `30` reps, `6` managers, `3` regions (`Central: $274,285`, `West: $248,243`, `East: $184,673`), and `7` products (`NovaPulse: $548,560` vs. `NovaEdge: $158,641`). | **PASS** | Discovery note: 4 accounts (`ACCT-041`, etc.) span multiple `sales_region` values across deals. |
| **4** | **NovaTech Marketing Campaigns** | How many lead rows, unique accounts, orphan account rows, and dates are in Marketing Campaigns? | `2,240` leads, `20` columns, `100` accounts (`85` CRM + `15` orphans `ACCT-101`–`ACCT-115` = `150` orphan rows, `6.70%`), dates `2023-01-01` to `2025-01-31`. | `2,240` rows across `100` unique accounts (`150` orphan rows matching `ACCT-101`..`ACCT-115`), spanning `2023-01-01` to `2025-01-31`. | **PASS** | Explains why CRM-anchored Left Joins intentionally drop 150 unlinked marketing rows. |
| **5** | **NovaTech Marketing Campaigns** | How many missing values are in `annual_income`, what is the response rate, and what are funnel stage counts? | `24` nulls (`1.07%`) in `annual_income`; `609` responses (`27.19%`); `5` ordered stages (`Prospect`, `Lead`, `Qualified Lead`, `Opportunity`, `Closed Won`). | `24` nulls in `annual_income`; `609` responses (`27.19%`); stages: `Qualified Lead: 848`, `Lead: 465`, `Closed Won: 412 (18.39%)`, `Prospect: 404`, `Opportunity: 111`. | **PASS** | Confirmed exact missingness (`24` rows) and funnel conversion rate (`18.39%`). |
| **6** | **NovaTech Marketing Campaigns** | What is total campaign spend, attributed revenue, and aggregate ROI across the 5 channels and 6 campaigns? | `6` campaigns (`Digital Retarget`, `Enterprise Expansion`, `NovaEdge Awareness`, `NovaPulse Launch`, `Q3 Growth Sprint`, `Year-End Accelerator`) across `5` channels (`Direct Mail`, `Email`, `Organic Search`, `Paid Social`, `Partner Referral`). | Total Spend = `$12,359,497.34`; Attributed Revenue = `$1,127,223.09`; Aggregate ROI = `-90.88%`. Direct Mail has least negative ROI (`-70.74%`), Organic Search worst (`-97.79%`). | **PASS** | All 6 campaigns and 5 channels match Data Dictionary taxonomy. |
| **7** | **NovaTech Support Tickets** | How many ticket rows, unique accounts, orphan rows, and dates are in Support Tickets? | `3,000` tickets, `20` columns, `100` accounts (`15` orphans `ACCT-101`–`ACCT-115` = `204` orphan rows, `6.80%`), dates `2023-06-01` to `2025-02-28`. | `3,000` tickets across `100` accounts (`204` orphan rows outside CRM), spanning `2023-06-01` to `2025-02-28`. | **PASS** | Exact match on row volume, orphan count, and date span. |
| **8** | **NovaTech Support Tickets** | What is the ticket priority distribution and how many rows lack `ticket_resolved_date`? | `low: 1,500`, `medium: 1,050`, `high: 400`, `critical: 50`; `59` unresolved tickets (`1.97%` null `ticket_resolved_date`). | `low: 1,500`, `medium: 1,050`, `high: 400`, `critical: 50`; `59` rows missing `ticket_resolved_date` (`2,941` resolved). | **PASS** | Exact match with documented priority distribution and null count. |
| **9** | **NovaTech Support Tickets** | What are the distinct values and null count of `customer_sentiment`? | **Data Dictionary states:** Valid values `negative`, `neutral`, `positive`; **`Nulls: None`**. | Observed in CSV & Q query: `neutral: 1,953`, `negative: 684`, `positive: 304`, and **`59` NULL rows (`1.97%`)** — coinciding with the exact 59 unresolved tickets. | **FAIL (Data Defect Found)** | **Undocumented Data Dictionary discrepancy:** `customer_sentiment` actually has `59` nulls when tickets are still open/unresolved. Handled explicitly in Sheet 3 visuals. |
| **10** | **NovaTech Reference Documents** | What are NovaTech's employee headcount, annual revenue, product lines, and list price range? | Austin, TX HQ; ~200 employees; ~$50M annual revenue; `10` industries; `NovaPulse` (`$550`–`$26,768`) & `NovaEdge` (`$55`–`$3,393`). | Confirmed Austin, TX HQ, ~200 staff, ~$50M revenue, `10` industries, and list prices `$55` (`NovaEdge Lite`) to `$26,768` (`NovaPulse Ultimate`). | **PASS** | Verified against `NovaTech_Company_Background.pdf` and CRM `list_price` bounds (`$55`–`$26,768`). |

## Cross-Check Verification

Two critical facts from the log were independently verified in the SPICE dataset preview and Python audit (`etl_and_metrics_verifier.py`):

1. **Undocumented Null Defect Cross-Check (`customer_sentiment`):**
   - **Fact verified:** Null count in `novatech_support_tickets.csv` for `customer_sentiment`.
   - **Chat / Data Dictionary said:** Data Dictionary explicitly listed `Nulls: None` for `customer_sentiment`.
   - **SPICE / CSV shows:** Exactly **`59` null values (`1.97%`)**, occurring strictly on the `59` rows where `ticket_resolved_date` is also null (unresolved tickets).
   - **Consistent?** **Discrepancy Confirmed & Documented.** Dashboard Sheet 3 preserves these `59` rows as `"Null / Open (59)"` rather than silently dropping them.

2. **CRM Deal Revenue Cross-Check (`deal_value`):**
   - **Fact verified:** Total Won revenue and Won deal count in `novatech_crm_deals.csv`.
   - **Chat said:** `315` Won deals totaling **`$707,201.00`** (`63.13%` win rate).
   - **SPICE / CSV shows:** Sum of `deal_value` across `499` rows (`315` Won, `184` Lost with `$0.00`) equals exactly **`$707,201.00`**.
   - **Consistent?** **Yes — 100% Consistent.**
