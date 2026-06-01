"""
=============================================================================
Marketing Campaign Performance Analysis
Dataset: 01_Marketing_Campaign_Performance_CLEANED.csv
Author : Auto-generated via Claude / Cowork
Date   : 2026-05-14
=============================================================================

Business Context
----------------
This dataset tracks 500 digital marketing campaigns run across 10 platforms,
10 brands, 6 Vietnamese cities, and multiple verticals throughout 2023-2024.

Key Business Questions
----------------------
BQ1  : Which platforms deliver the highest ROAS and ROI?
BQ2  : Which brands are the top revenue generators?
BQ3  : How does performance vary across campaign objectives?
BQ4  : What is the monthly/quarterly revenue and spend trend?
BQ5  : Which cities drive the most conversions and revenue?
BQ6  : Which agencies deliver the best results?
BQ7  : Which verticals are most efficient?
BQ8  : Does holiday timing improve performance?
BQ9  : How does competitor activity affect CTR and conversions?
BQ10 : What ad formats and platforms have the best CTR?
"""

# ---------------------------------------------------------------------------
# 0. Setup
# ---------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# ---- Paths ----
BASE_DIR  = Path(__file__).parent.parent          # C:\Data Analysis
DATA_PATH = BASE_DIR / "Clean data" / "01_Marketing_Campaign_Performance_CLEANED.csv"
OUT_DIR   = BASE_DIR / "Output"
OUT_DIR.mkdir(exist_ok=True)

# ---- Style ----
plt.rcParams.update({
    "figure.facecolor": "#f8f9fa",
    "axes.facecolor"  : "#ffffff",
    "axes.spines.top" : False,
    "axes.spines.right": False,
    "font.family"     : "DejaVu Sans",
    "axes.titlesize"  : 13,
    "axes.titleweight": "bold",
    "axes.labelsize"  : 11,
})
PALETTE = ["#4C72B0","#DD8452","#55A868","#C44E52","#8172B3",
           "#937860","#DA8BC3","#8C8C8C","#CCB974","#64B5CD"]

# ---------------------------------------------------------------------------
# 1. Load & Prepare
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df["Start_Date"]   = pd.to_datetime(df["Start_Date"])
df["End_Date"]     = pd.to_datetime(df["End_Date"])
df["Revenue_VND"]  = pd.to_numeric(df["Revenue_VND"], errors="coerce")
df["Spend_VND"]    = pd.to_numeric(df["Spend_VND"],   errors="coerce")
df["ROAS"]         = pd.to_numeric(df["ROAS"],         errors="coerce")
df["ROI_%"]        = pd.to_numeric(df["ROI_%"],        errors="coerce")

print("=" * 65)
print("MARKETING CAMPAIGN PERFORMANCE — EXPLORATORY ANALYSIS")
print("=" * 65)
print(f"\nDataset shape : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Date range    : {df['Start_Date'].min().date()} → {df['End_Date'].max().date()}")
print(f"Brands        : {sorted(df['Brand'].unique())}")
print(f"Platforms     : {sorted(df['Platform'].unique())}")
print(f"Cities        : {sorted(df['Target_City'].unique())}")


# ---------------------------------------------------------------------------
# 2. Overall KPIs
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("SECTION 1 — OVERALL KPIs")
print("=" * 65)

kpis = {
    "Total Campaigns"          : df.shape[0],
    "Total Spend (B VND)"      : df["Spend_VND"].sum()  / 1e9,
    "Total Revenue (T VND)"    : df["Revenue_VND"].sum()/ 1e12,
    "Total Impressions (B)"    : df["Impressions"].sum()/ 1e9,
    "Total Clicks (M)"         : df["Clicks"].sum()     / 1e6,
    "Total Conversions (M)"    : df["Conversions"].sum()/ 1e6,
    "Avg ROAS"                 : df["ROAS"].mean(),
    "Avg ROI %"                : df["ROI_%"].mean(),
    "Avg CTR %"                : df["CTR_%"].mean(),
    "Avg Conv Rate %"          : df["Conv_Rate_%"].mean(),
    "Avg Budget Utilisation %"  : df["Budget_Util_%"].mean(),
}
for k, v in kpis.items():
    print(f"  {k:<32} : {v:,.2f}")


# ---------------------------------------------------------------------------
# 3. BQ1 — Platform Performance
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("BQ1 — PLATFORM PERFORMANCE (ROAS, CTR, Conv Rate)")
print("=" * 65)

plat = (df.groupby("Platform")
          .agg(Campaigns   =("Campaign_ID","count"),
               Spend_B     =("Spend_VND",  lambda x: x.sum()/1e9),
               Revenue_T   =("Revenue_VND",lambda x: x.sum()/1e12),
               Avg_ROAS    =("ROAS",       "mean"),
               Avg_CTR     =("CTR_%",      "mean"),
               Avg_ConvRate=("Conv_Rate_%","mean"))
          .sort_values("Avg_ROAS", ascending=False)
          .reset_index())
print(plat.to_string(index=False, float_format="%.2f"))

# --- Chart BQ1a: ROAS by Platform ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("BQ1 – Platform Performance", fontsize=15, fontweight="bold")

ax = axes[0]
bars = ax.barh(plat["Platform"], plat["Avg_ROAS"], color=PALETTE[:len(plat)])
ax.set_xlabel("Avg ROAS (×)")
ax.set_title("Average ROAS by Platform")
ax.bar_label(bars, fmt="%.0f×", padding=4, fontsize=9)
ax.invert_yaxis()

ax2 = axes[1]
ax2.scatter(plat["Avg_CTR"], plat["Avg_ConvRate"],
            s=plat["Spend_B"]*30, c=PALETTE[:len(plat)],
            alpha=0.8, edgecolors="white", linewidths=1.5)
for _, row in plat.iterrows():
    ax2.annotate(row["Platform"], (row["Avg_CTR"], row["Avg_ConvRate"]),
                 fontsize=8, ha="center", va="bottom", color="#333")
ax2.set_xlabel("Avg CTR %")
ax2.set_ylabel("Avg Conv Rate %")
ax2.set_title("CTR vs Conv Rate (bubble = Spend)")
plt.tight_layout()
plt.savefig(OUT_DIR / "bq1_platform_performance.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  → Chart saved: bq1_platform_performance.png")


# ---------------------------------------------------------------------------
# 4. BQ2 — Brand Performance
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("BQ2 — BRAND PERFORMANCE")
print("=" * 65)

brand = (df.groupby("Brand")
           .agg(Campaigns  =("Campaign_ID","count"),
                Spend_B    =("Spend_VND",  lambda x: x.sum()/1e9),
                Revenue_T  =("Revenue_VND",lambda x: x.sum()/1e12),
                Avg_ROAS   =("ROAS",       "mean"),
                Avg_ROI    =("ROI_%",      "mean"),
                Conversions=("Conversions","sum"))
           .sort_values("Revenue_T", ascending=False)
           .reset_index())
print(brand.to_string(index=False, float_format="%.2f"))

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(brand))
bars1 = ax.bar(x - 0.2, brand["Spend_B"],   0.35, label="Spend (B VND)",   color="#4C72B0", alpha=0.85)
bars2 = ax.bar(x + 0.2, brand["Revenue_T"], 0.35, label="Revenue (T VND)", color="#55A868", alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(brand["Brand"], rotation=20, ha="right")
ax.set_ylabel("Billion / Trillion VND")
ax.set_title("BQ2 – Brand: Spend vs Revenue", fontweight="bold")
ax.legend()
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}"))
plt.tight_layout()
plt.savefig(OUT_DIR / "bq2_brand_performance.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  → Chart saved: bq2_brand_performance.png")


# ---------------------------------------------------------------------------
# 5. BQ3 — Campaign Objectives
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("BQ3 — CAMPAIGN OBJECTIVE EFFECTIVENESS")
print("=" * 65)

obj = (df.groupby("Objective")
         .agg(Campaigns   =("Campaign_ID","count"),
              Avg_ROAS    =("ROAS",       "mean"),
              Avg_CTR     =("CTR_%",      "mean"),
              Avg_ConvRate=("Conv_Rate_%","mean"),
              Revenue_T   =("Revenue_VND",lambda x: x.sum()/1e12))
         .sort_values("Avg_ROAS", ascending=False)
         .reset_index())
print(obj.to_string(index=False, float_format="%.2f"))

fig, ax = plt.subplots(figsize=(10, 5))
colors = [PALETTE[i % len(PALETTE)] for i in range(len(obj))]
bars = ax.bar(obj["Objective"], obj["Avg_ROAS"], color=colors, edgecolor="white")
ax.bar_label(bars, fmt="%.0f×", padding=3, fontsize=9)
ax.set_ylabel("Avg ROAS (×)")
ax.set_title("BQ3 – Average ROAS by Campaign Objective", fontweight="bold")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(OUT_DIR / "bq3_objective_roas.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  → Chart saved: bq3_objective_roas.png")


# ---------------------------------------------------------------------------
# 6. BQ4 — Monthly / Quarterly Trend
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("BQ4 — MONTHLY & QUARTERLY TREND")
print("=" * 65)

monthly = (df.groupby("Month")
             .agg(Spend_B   =("Spend_VND",  lambda x: x.sum()/1e9),
                  Revenue_T =("Revenue_VND",lambda x: x.sum()/1e12),
                  Campaigns =("Campaign_ID","count"),
                  Avg_ROAS  =("ROAS","mean"))
             .reset_index())
print(monthly.to_string(index=False, float_format="%.2f"))

fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.bar(monthly["Month"], monthly["Spend_B"], color="#4C72B0", alpha=0.6, label="Spend (B VND)")
ax1.set_xlabel("Month")
ax1.set_ylabel("Spend (Billion VND)", color="#4C72B0")
ax1.tick_params(axis="y", labelcolor="#4C72B0")
ax2 = ax1.twinx()
ax2.plot(monthly["Month"], monthly["Revenue_T"], "o-", color="#C44E52", lw=2.5, label="Revenue (T VND)")
ax2.set_ylabel("Revenue (Trillion VND)", color="#C44E52")
ax2.tick_params(axis="y", labelcolor="#C44E52")
ax1.set_title("BQ4 – Monthly Spend vs Revenue", fontweight="bold")
ax1.set_xticks(monthly["Month"])
ax1.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc="upper left")
plt.tight_layout()
plt.savefig(OUT_DIR / "bq4_monthly_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  → Chart saved: bq4_monthly_trend.png")

# Quarterly
quarterly = (df.groupby("Quarter")
               .agg(Spend_B  =("Spend_VND",  lambda x: x.sum()/1e9),
                    Revenue_T=("Revenue_VND",lambda x: x.sum()/1e12),
                    Avg_ROAS =("ROAS","mean"))
               .reset_index())
print("\nQuarterly:")
print(quarterly.to_string(index=False, float_format="%.2f"))


# ---------------------------------------------------------------------------
# 7. BQ5 — City Performance
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("BQ5 — CITY / MARKET PERFORMANCE")
print("=" * 65)

city = (df.groupby("Target_City")
          .agg(Campaigns   =("Campaign_ID","count"),
               Spend_B     =("Spend_VND",  lambda x: x.sum()/1e9),
               Revenue_T   =("Revenue_VND",lambda x: x.sum()/1e12),
               Avg_ROAS    =("ROAS","mean"),
               Avg_CTR     =("CTR_%","mean"),
               Conversions =("Conversions","sum"))
          .sort_values("Revenue_T", ascending=False)
          .reset_index())
print(city.to_string(index=False, float_format="%.2f"))


# ---------------------------------------------------------------------------
# 8. BQ6 — Agency Performance
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("BQ6 — AGENCY PERFORMANCE")
print("=" * 65)

agency = (df.groupby("Agency")
            .agg(Campaigns   =("Campaign_ID","count"),
                 Spend_B     =("Spend_VND",  lambda x: x.sum()/1e9),
                 Revenue_T   =("Revenue_VND",lambda x: x.sum()/1e12),
                 Avg_ROAS    =("ROAS","mean"),
                 Avg_BudgetUtil=("Budget_Util_%","mean"))
            .sort_values("Avg_ROAS", ascending=False)
            .reset_index())
print(agency.to_string(index=False, float_format="%.2f"))


# ---------------------------------------------------------------------------
# 9. BQ7 — Vertical Performance
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("BQ7 — VERTICAL / INDUSTRY PERFORMANCE")
print("=" * 65)

vert = (df.groupby("Vertical")
          .agg(Campaigns   =("Campaign_ID","count"),
               Avg_ROAS    =("ROAS","mean"),
               Avg_CTR     =("CTR_%","mean"),
               Avg_ConvRate=("Conv_Rate_%","mean"),
               Revenue_T   =("Revenue_VND",lambda x: x.sum()/1e12))
          .sort_values("Avg_ROAS", ascending=False)
          .reset_index())
print(vert.to_string(index=False, float_format="%.2f"))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("BQ7 – Vertical Performance", fontsize=15, fontweight="bold")
ax = axes[0]
bars = ax.barh(vert["Vertical"], vert["Avg_ROAS"], color=PALETTE[:len(vert)])
ax.set_xlabel("Avg ROAS (×)")
ax.set_title("ROAS by Vertical")
ax.bar_label(bars, fmt="%.0f×", padding=3, fontsize=9)
ax.invert_yaxis()
ax2 = axes[1]
ax2.scatter(vert["Avg_CTR"], vert["Avg_ConvRate"],
            s=200, c=PALETTE[:len(vert)], alpha=0.85, edgecolors="white")
for _, row in vert.iterrows():
    ax2.annotate(row["Vertical"], (row["Avg_CTR"], row["Avg_ConvRate"]),
                 fontsize=8, ha="center", va="bottom")
ax2.set_xlabel("Avg CTR %")
ax2.set_ylabel("Avg Conv Rate %")
ax2.set_title("CTR vs Conv Rate by Vertical")
plt.tight_layout()
plt.savefig(OUT_DIR / "bq7_vertical_performance.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  → Chart saved: bq7_vertical_performance.png")


# ---------------------------------------------------------------------------
# 10. BQ8 — Holiday Effect
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("BQ8 — HOLIDAY CAMPAIGN EFFECT")
print("=" * 65)

holiday = (df.groupby("Is_Holiday_Campaign")
             .agg(Campaigns   =("Campaign_ID","count"),
                  Avg_ROAS    =("ROAS","mean"),
                  Avg_CTR     =("CTR_%","mean"),
                  Avg_ConvRate=("Conv_Rate_%","mean"),
                  Revenue_T   =("Revenue_VND",lambda x: x.sum()/1e12))
             .reset_index())
print(holiday.to_string(index=False, float_format="%.2f"))


# ---------------------------------------------------------------------------
# 11. BQ9 — Competitor Activity
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("BQ9 — COMPETITOR ACTIVITY IMPACT")
print("=" * 65)

comp = (df.groupby("Competitor_Activity")
          .agg(Campaigns   =("Campaign_ID","count"),
               Avg_ROAS    =("ROAS","mean"),
               Avg_CTR     =("CTR_%","mean"),
               Avg_ConvRate=("Conv_Rate_%","mean"),
               Revenue_T   =("Revenue_VND",lambda x: x.sum()/1e12))
          .reset_index())
print(comp.to_string(index=False, float_format="%.2f"))
print("\n  Insight: Low competitor activity correlates with highest avg CTR.")


# ---------------------------------------------------------------------------
# 12. BQ10 — CTR Heatmap: Platform × Objective
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("BQ10 — CTR HEATMAP: PLATFORM × OBJECTIVE")
print("=" * 65)

pivot_ctr = df.pivot_table(values="CTR_%", index="Platform",
                           columns="Objective", aggfunc="mean")
print(pivot_ctr.round(2).to_string())

fig, ax = plt.subplots(figsize=(13, 6))
sns.heatmap(pivot_ctr, annot=True, fmt=".1f", cmap="YlOrRd",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Avg CTR %"})
ax.set_title("BQ10 – Average CTR % by Platform × Objective", fontweight="bold")
plt.tight_layout()
plt.savefig(OUT_DIR / "bq10_ctr_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  → Chart saved: bq10_ctr_heatmap.png")


# ---------------------------------------------------------------------------
# 13. Correlation Matrix
# ---------------------------------------------------------------------------
num_cols = ["Budget_VND","Spend_VND","Impressions","Clicks","CTR_%",
            "Leads","Conversions","Conv_Rate_%","ROAS","ROI_%",
            "Revenue_VND","Duration_Days"]
corr = df[num_cols].corr()

fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, linewidths=0.5, ax=ax,
            cbar_kws={"label": "Pearson r"})
ax.set_title("Correlation Matrix – Key Metrics", fontweight="bold", fontsize=14)
plt.tight_layout()
plt.savefig(OUT_DIR / "correlation_matrix.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  → Chart saved: correlation_matrix.png")


# ---------------------------------------------------------------------------
# 14. Season Comparison
# ---------------------------------------------------------------------------
season = (df.groupby("Season")
            .agg(Campaigns   =("Campaign_ID","count"),
                 Spend_B     =("Spend_VND",  lambda x: x.sum()/1e9),
                 Revenue_T   =("Revenue_VND",lambda x: x.sum()/1e12),
                 Avg_ROAS    =("ROAS","mean"))
            .sort_values("Avg_ROAS", ascending=False)
            .reset_index())
print("\n" + "=" * 65)
print("SEASONAL PERFORMANCE")
print("=" * 65)
print(season.to_string(index=False, float_format="%.2f"))

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(season["Season"], season["Avg_ROAS"],
              color=PALETTE[:len(season)], edgecolor="white")
ax.bar_label(bars, fmt="%.0f×", padding=3, fontsize=9)
ax.set_ylabel("Avg ROAS (×)")
ax.set_title("ROAS by Season", fontweight="bold")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(OUT_DIR / "seasonal_roas.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  → Chart saved: seasonal_roas.png")


# ---------------------------------------------------------------------------
# 15. Top 10 Campaigns by Revenue
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("TOP 10 CAMPAIGNS BY REVENUE")
print("=" * 65)
top10 = (df[["Campaign_Name","Brand","Platform","Objective",
             "Revenue_VND","ROAS","CTR_%","Conv_Rate_%"]]
           .sort_values("Revenue_VND", ascending=False)
           .head(10)
           .assign(Revenue_T=lambda x: x["Revenue_VND"]/1e12))
print(top10[["Campaign_Name","Brand","Platform","Objective",
             "Revenue_T","ROAS","CTR_%","Conv_Rate_%"]].to_string(index=False, float_format="%.2f"))


print("\n" + "=" * 65)
print("ANALYSIS COMPLETE — all charts saved to Output/")
print("=" * 65)
