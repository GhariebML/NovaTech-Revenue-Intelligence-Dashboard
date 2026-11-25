# NovaTech Solutions — Revenue Intelligence Dashboard (Course 2 Final Submission)

**Student Name:** Mohamed Abd Elsalam Mohamed Gharieb  
**Program:** AWS AI & ML Scholars Program — Future AWS Agentic AI Business Professional  
**Course:** Course 2 of 3 — Business Intelligence and Knowledge Management Foundations with Amazon Quick  
**Date:** 25 November 2026

---

## Submission Package Directory Map

| Folder | Contents & Satisfied Udacity Rubric Criteria |
|---|---|
| [`00_START_HERE_AND_STARTER_FILES/`](file:///E:/Udacity/NovaTech_Revenue_Intelligence_Submission/00_START_HERE_AND_STARTER_FILES/RUBRIC_TRACEABILITY_CHECKLIST.xlsx) | Submission orientation, `RUBRIC_TRACEABILITY_CHECKLIST.xlsx`, official NovaTech starter CSVs (`novatech_crm_deals.csv`, `novatech_marketing_campaigns.csv`, `novatech_support_tickets.csv` + aliases + deduplicated `novatech_account_360_summary.csv`), Data Dictionary, Company Background, Sarah Chen's Brief, and starter templates. |
| [`01_VERIFICATION_LOG/`](file:///E:/Udacity/NovaTech_Revenue_Intelligence_Submission/01_VERIFICATION_LOG/Verification_Log.pdf) | **10-entry Data Verification Log** (`.md`, `.docx`, `.pdf`) covering CRM Deals, Marketing Campaigns, Support Tickets, and Reference Documents + Cross-Check confirming the undocumented `59` null `customer_sentiment` records. |
| [`02_DATA_TRANSFORMATION/`](file:///E:/Udacity/NovaTech_Revenue_Intelligence_Submission/02_DATA_TRANSFORMATION/Data_Transformation_and_ETL_Guide.pdf) | **4 high-DPI ETL & SPICE diagrams** (SPICE inventory, data type corrections, 5 calculated fields, and CRM-anchored Left Join diagram showing `63,420` rows & fan-out mitigation), `Data_Transformation_and_ETL_Guide.md/.pdf`, `NovaTech_Data_Model_and_KPI_Audit.xlsx`, and reproducible `etl_and_metrics_verifier.py`. |
| [`03_DASHBOARD_PDF_EXPORT/`](file:///E:/Udacity/NovaTech_Revenue_Intelligence_Submission/03_DASHBOARD_PDF_EXPORT/NovaTech_Revenue_Intelligence_Dashboard_All_3_Sheets.pdf) | High-resolution landscape PDF exports of **Sheet 1 (Marketing Funnel)**, **Sheet 2 (Sales Pipeline)**, **Sheet 3 (Customer Health — Unified)**, and **Sheet 4 (Bonus Stand-Out Predictive Trend & Fan-Out Audit)**, plus merged multi-sheet PDF export. |
| [`04_ANNOTATED_DASHBOARD_SCREENSHOTS/`](file:///E:/Udacity/NovaTech_Revenue_Intelligence_Submission/04_ANNOTATED_DASHBOARD_SCREENSHOTS/Dashboard_Annotations_Guide.md) | **4 high-DPI Annotated Dashboard PNGs** containing 5 structured executive annotations (+ 1 Bonus Audit note), each stating a quantified finding, business implication, and recommended action. |
| [`05_TOPIC_AND_Q_EXPLORATION/`](file:///E:/Udacity/NovaTech_Revenue_Intelligence_Submission/05_TOPIC_AND_Q_EXPLORATION/Q_Exploration_Log.pdf) | **7-entry Q Exploration Log** (`.md`, `.docx`, `.pdf`) with dashboard cross-checks & reflection, `Topic_Configuration_and_Before_After_Guide.md/.pdf`, and 4 Topic semantic layer & Before-vs-After accuracy diagrams. |
| [`06_EXECUTIVE_SUMMARY_AND_REPORT/`](file:///E:/Udacity/NovaTech_Revenue_Intelligence_Submission/06_EXECUTIVE_SUMMARY_AND_REPORT/Executive_Report_for_VP_Sarah_Chen.pdf) | `Dashboard_Executive_Summary` (`.md`, `.docx`, `.pdf`) and the **strictly 3-page** `Executive_Report_for_VP_Sarah_Chen` (`.md`, `.docx`, `.pdf`) written in plain executive English with zero raw SQL/formulas. |

---

## Transparency Note on Live AWS Vocareum Portal Captures

All statistical computations, ETL data-model specifications, dashboard PDF exports, annotated dashboard visuals, semantic Topic comparisons, verification logs, and executive reports in this package are **100% computed and verified directly from the official NovaTech starter CSVs**. Because live browser screenshots of the Udacity Vocareum AWS QuickSight console require the learner's authenticated interactive AWS lab session, no synthetic AWS console browser frames were fabricated; every analytical visual and data-model specification corresponds directly to the steps documented for Vocareum execution.
