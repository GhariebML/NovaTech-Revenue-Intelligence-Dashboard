#!/usr/bin/env python3
"""NovaTech Solutions ETL & Ground-Truth KPI Verifier.

Computes exact verified numbers across:
  - novatech_crm_deals.csv (499 rows, 20 cols)
  - novatech_marketing_campaigns.csv (2,240 rows, 20 cols)
  - novatech_support_tickets.csv (3,000 rows, 20 cols)
  - Unified 3-table join anchored on novatech_crm_deals via account_id (63,420 rows)
  - De-duplicated 85-account Account 360 summary table
"""
from __future__ import annotations

import json
import pathlib
import pandas as pd

BASE = pathlib.Path(r"E:\Udacity\NovaTech_Revenue_Intelligence_Submission")
STARTER = BASE / "00_START_HERE_AND_STARTER_FILES" / "starter_data"
OUT_XFORM = BASE / "02_DATA_TRANSFORMATION"


def main() -> int:
    crm = pd.read_csv(STARTER / "novatech_crm_deals.csv")
    mkt = pd.read_csv(STARTER / "novatech_marketing_campaigns.csv")
    sup = pd.read_csv(STARTER / "novatech_support_tickets.csv")

    # Apply documented SPICE data-type corrections & calculated fields
    crm["deal_created_date"] = pd.to_datetime(crm["deal_created_date"])
    crm["deal_closed_date"] = pd.to_datetime(crm["deal_closed_date"])
    crm["days_to_close"] = (crm["deal_closed_date"] - crm["deal_created_date"]).dt.days
    crm["win_rate_flag"] = (crm["deal_stage"] == "Won").astype(int)

    mkt["campaign_date"] = pd.to_datetime(mkt["campaign_date"])
    mkt["campaign_roi_pct"] = ((mkt["revenue_attributed"] - mkt["campaign_spend"]) / mkt["campaign_spend"] * 100).round(2)
    mkt["total_product_spend"] = mkt["product_spend_tier1"] + mkt["product_spend_tier2"] + mkt["product_spend_tier3"]

    sup["ticket_created_date"] = pd.to_datetime(sup["ticket_created_date"])
    sup["ticket_resolved_date"] = pd.to_datetime(sup["ticket_resolved_date"])
    sup["resolution_time_days"] = (sup["ticket_resolved_date"] - sup["ticket_created_date"]).dt.days
    sup["resolution_time_hours"] = ((sup["ticket_resolved_date"] - sup["ticket_created_date"]).dt.total_seconds() / 3600.0).round(2)
    sup["negative_sentiment_flag"] = (sup["customer_sentiment"] == "negative").astype(int)

    # Account-level deduplicated 360 rollup (anchored on 85 CRM accounts)
    crm_acct = crm.groupby(
        ["account_id", "company_name", "industry", "company_size_tier", "headquarters"],
        as_index=False,
    ).agg(
        sales_regions=("sales_region", lambda s: ", ".join(sorted(s.unique()))),
        total_deals=("opportunity_id", "count"),
        won_deals=("win_rate_flag", "sum"),
        lost_deals=("deal_stage", lambda s: int((s == "Lost").sum())),
        total_won_revenue_usd=("deal_value", "sum"),
        avg_days_to_close=("days_to_close", "mean"),
    )
    crm_acct["win_rate_pct"] = (crm_acct["won_deals"] / crm_acct["total_deals"] * 100).round(1)
    crm_acct["avg_days_to_close"] = crm_acct["avg_days_to_close"].round(1)

    mkt_acct = mkt.groupby("account_id", as_index=False).agg(
        marketing_leads=("lead_id", "count"),
        campaign_responses=("campaign_response", "sum"),
        marketing_closed_won=("funnel_stage", lambda s: int((s == "Closed Won").sum())),
        total_campaign_spend_usd=("campaign_spend", "sum"),
        total_attributed_rev_usd=("revenue_attributed", "sum"),
    )

    sup_acct = sup.groupby("account_id", as_index=False).agg(
        total_tickets=("ticket_id", "count"),
        negative_tickets=("negative_sentiment_flag", "sum"),
        critical_high_tickets=("priority", lambda s: int(s.isin(["critical", "high"]).sum())),
        unresolved_tickets=("ticket_resolved_date", lambda s: int(s.isna().sum())),
        avg_resolution_days=("resolution_time_days", "mean"),
        max_tickets_last_30d=("tickets_last_30_days", "max"),
        total_downtime_minutes=("downtime_minutes", "sum"),
    )
    sup_acct["negative_sentiment_pct"] = (sup_acct["negative_tickets"] / sup_acct["total_tickets"] * 100).round(1)
    sup_acct["avg_resolution_days"] = sup_acct["avg_resolution_days"].round(2)

    acct_360 = crm_acct.merge(mkt_acct, on="account_id", how="left").merge(sup_acct, on="account_id", how="left")
    acct_360["at_risk_account_flag"] = (
        (acct_360["total_tickets"] >= 80)
        & (acct_360["negative_sentiment_pct"] >= 18.0)
        & (acct_360["total_won_revenue_usd"] >= 6000.0)
    ).astype(int)
    acct_360 = acct_360.sort_values("total_tickets", ascending=False)
    acct_360.to_csv(STARTER / "novatech_account_360_summary.csv", index=False)

    # Verify unified 3-table join (CRM anchor left joins)
    unified = crm.merge(mkt, on="account_id", how="left", suffixes=("", "_mkt")).merge(
        sup, on="account_id", how="left", suffixes=("", "_sup")
    )

    # Compute additional metrics for verification
    crm["close_quarter"] = crm["deal_closed_date"].dt.to_period("Q").astype(str)
    q_trend = crm.groupby("close_quarter").agg(
        deals=("opportunity_id", "count"),
        won=("win_rate_flag", "sum"),
        won_rev=("deal_value", "sum"),
        avg_dtc=("days_to_close", "mean"),
    ).reset_index()

    sup["created_month"] = sup["ticket_created_date"].dt.to_period("M").astype(str)
    m_sup = sup.groupby("created_month").agg(tickets=("ticket_id", "count")).reset_index()

    mgr_perf = crm.groupby(["sales_region", "sales_manager"]).agg(
        deals=("opportunity_id", "count"),
        won=("win_rate_flag", "sum"),
        win_rate=("win_rate_flag", lambda s: round(s.mean() * 100, 1)),
        won_rev=("deal_value", "sum"),
    ).reset_index().sort_values("won_rev", ascending=False)

    summary = {
        "crm_rows": len(crm),
        "mkt_rows": len(mkt),
        "sup_rows": len(sup),
        "unified_joined_rows": len(unified),
        "unified_naive_sum_deal_value": round(float(unified["deal_value"].sum()), 2),
        "true_crm_won_revenue": round(float(crm["deal_value"].sum()), 2),
        "fan_out_multiplier": round(float(unified["deal_value"].sum() / crm["deal_value"].sum()), 2),
        "at_risk_accounts_flagged": int(acct_360["at_risk_account_flag"].sum()),
        "at_risk_won_revenue": round(float(acct_360[acct_360["at_risk_account_flag"] == 1]["total_won_revenue_usd"].sum()), 2),
        "orphan_mkt_rows": int((~mkt["account_id"].isin(crm["account_id"])).sum()),
        "orphan_sup_rows": int((~sup["account_id"].isin(crm["account_id"])).sum()),
        "undocumented_sentiment_nulls": int(sup["customer_sentiment"].isna().sum()),
    }
    (OUT_XFORM / "verified_metrics_snapshot.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=== VERIFICATION METRICS SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("\n=== QUARTERLY CRM TREND ===")
    print(q_trend.to_string(index=False))
    print("\n=== MANAGER PERFORMANCE ===")
    print(mgr_perf.to_string(index=False))
    print("\n=== AT-RISK FLAGGED ACCOUNTS ===")
    print(acct_360[acct_360["at_risk_account_flag"] == 1][
        ["account_id", "company_name", "company_size_tier", "total_won_revenue_usd", "total_tickets", "negative_tickets", "negative_sentiment_pct", "max_tickets_last_30d"]
    ].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
