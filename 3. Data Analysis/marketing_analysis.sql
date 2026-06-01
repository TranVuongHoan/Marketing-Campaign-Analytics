-- =============================================================================
-- Marketing Campaign Performance — SQL Analysis
-- Dataset : marketing_campaigns (from 01_Marketing_Campaign_Performance_CLEANED.csv)
-- Dialect : Standard SQL (compatible with PostgreSQL / BigQuery / DuckDB)
-- Date    : 2026-05-14
-- =============================================================================
-- HOW TO USE (DuckDB / local):
--   INSTALL duckdb; then run:
--   duckdb -c "CREATE TABLE marketing_campaigns AS
--              SELECT * FROM read_csv_auto('Clean data/01_Marketing_Campaign_Performance_CLEANED.csv',
--                                          header=true, all_varchar=false);"
--   Then paste and run the queries below.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- 0. Schema Reference
-- ---------------------------------------------------------------------------
-- Campaign_ID, Campaign_Name, Brand, Vertical, Platform, Ad_Format,
-- Objective, Target_Audience, Target_City, Campaign_Manager, Agency,
-- Start_Date, End_Date, Duration_Days, Month, Quarter, Season,
-- Competitor_Activity, Is_Holiday_Campaign, Status,
-- Budget_VND, Spend_VND, Budget_Util_%, Impressions, Reach, Frequency,
-- Clicks, CTR_%, CPC_VND, Video_Views, View_Rate_%,
-- Leads, Lead_Rate_%, CPL_VND,
-- Conversions, Conv_Rate_%, CPA_VND,
-- Avg_Order_Value_VND, Revenue_VND, ROAS, ROI_%
-- ---------------------------------------------------------------------------


-- ===========================================================================
-- SECTION 1 — OVERALL KPIs
-- ===========================================================================

SELECT
    COUNT(*)                                     AS total_campaigns,
    ROUND(SUM(Budget_VND)  / 1e9, 2)            AS total_budget_B_VND,
    ROUND(SUM(Spend_VND)   / 1e9, 2)            AS total_spend_B_VND,
    ROUND(SUM(Revenue_VND) / 1e12, 2)           AS total_revenue_T_VND,
    ROUND(AVG("Budget_Util_%"), 2)              AS avg_budget_util_pct,
    ROUND(SUM(Impressions) / 1e9, 2)            AS total_impressions_B,
    ROUND(SUM(Clicks)      / 1e6, 2)            AS total_clicks_M,
    ROUND(SUM(Conversions) / 1e6, 2)            AS total_conversions_M,
    ROUND(AVG("CTR_%"),    2)                   AS avg_ctr_pct,
    ROUND(AVG("Conv_Rate_%"), 2)               AS avg_conv_rate_pct,
    ROUND(AVG(ROAS),       2)                   AS avg_roas,
    ROUND(AVG("ROI_%"),    2)                   AS avg_roi_pct
FROM marketing_campaigns;


-- ===========================================================================
-- BQ1 — PLATFORM PERFORMANCE (ranked by ROAS)
-- ===========================================================================

SELECT
    Platform,
    COUNT(*)                                    AS campaigns,
    ROUND(SUM(Spend_VND)   / 1e9,  2)          AS spend_B_VND,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct,
    ROUND(AVG("Conv_Rate_%"),      2)          AS avg_conv_rate_pct,
    ROUND(SUM(Impressions) / 1e6,  2)          AS impressions_M,
    ROUND(SUM(Clicks)      / 1e6,  2)          AS clicks_M,
    ROUND(SUM(Conversions) / 1e3,  2)          AS conversions_K
FROM marketing_campaigns
GROUP BY Platform
ORDER BY avg_roas DESC;


-- ===========================================================================
-- BQ1b — PLATFORM FUNNEL: Impression → Click → Conversion
-- ===========================================================================

SELECT
    Platform,
    ROUND(SUM(Impressions) / 1e6, 2)           AS impressions_M,
    ROUND(SUM(Clicks)      / 1e6, 2)           AS clicks_M,
    ROUND(SUM(Conversions) / 1e3, 2)           AS conversions_K,
    ROUND(100.0 * SUM(Clicks)      / NULLIF(SUM(Impressions), 0), 2) AS impression_to_click_pct,
    ROUND(100.0 * SUM(Conversions) / NULLIF(SUM(Clicks),      0), 2) AS click_to_conv_pct
FROM marketing_campaigns
GROUP BY Platform
ORDER BY impression_to_click_pct DESC;


-- ===========================================================================
-- BQ2 — BRAND PERFORMANCE
-- ===========================================================================

SELECT
    Brand,
    COUNT(*)                                    AS campaigns,
    ROUND(SUM(Spend_VND)   / 1e9,  2)          AS spend_B_VND,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(SUM(Revenue_VND) / NULLIF(SUM(Spend_VND), 0), 2) AS actual_roas,
    ROUND(AVG(ROAS),               2)          AS avg_campaign_roas,
    ROUND(AVG("ROI_%"),            2)          AS avg_roi_pct,
    ROUND(SUM(Conversions) / 1e3,  2)          AS conversions_K
FROM marketing_campaigns
GROUP BY Brand
ORDER BY revenue_T_VND DESC;


-- ===========================================================================
-- BQ3 — CAMPAIGN OBJECTIVE EFFECTIVENESS
-- ===========================================================================

SELECT
    Objective,
    COUNT(*)                                    AS campaigns,
    ROUND(SUM(Spend_VND)   / 1e9,  2)          AS spend_B_VND,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct,
    ROUND(AVG("Conv_Rate_%"),      2)          AS avg_conv_rate_pct,
    ROUND(SUM(Conversions) / 1e3,  2)          AS conversions_K
FROM marketing_campaigns
GROUP BY Objective
ORDER BY avg_roas DESC;


-- ===========================================================================
-- BQ4a — MONTHLY TREND
-- ===========================================================================

SELECT
    Month,
    COUNT(*)                                    AS campaigns,
    ROUND(SUM(Spend_VND)   / 1e9,  2)          AS spend_B_VND,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct,
    ROUND(SUM(Conversions) / 1e3,  2)          AS conversions_K
FROM marketing_campaigns
GROUP BY Month
ORDER BY Month;


-- ===========================================================================
-- BQ4b — QUARTERLY TREND
-- ===========================================================================

SELECT
    Quarter,
    COUNT(*)                                    AS campaigns,
    ROUND(SUM(Spend_VND)   / 1e9,  2)          AS spend_B_VND,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct
FROM marketing_campaigns
GROUP BY Quarter
ORDER BY Quarter;


-- ===========================================================================
-- BQ5 — CITY / MARKET PERFORMANCE
-- ===========================================================================

SELECT
    Target_City,
    COUNT(*)                                    AS campaigns,
    ROUND(SUM(Spend_VND)   / 1e9,  2)          AS spend_B_VND,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct,
    ROUND(SUM(Conversions) / 1e3,  2)          AS conversions_K,
    ROUND(SUM(Leads)       / 1e3,  2)          AS leads_K
FROM marketing_campaigns
GROUP BY Target_City
ORDER BY revenue_T_VND DESC;


-- ===========================================================================
-- BQ6 — AGENCY PERFORMANCE
-- ===========================================================================

SELECT
    Agency,
    COUNT(*)                                    AS campaigns,
    ROUND(SUM(Spend_VND)   / 1e9,  2)          AS spend_B_VND,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("Budget_Util_%"),    2)          AS avg_budget_util_pct,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct
FROM marketing_campaigns
GROUP BY Agency
ORDER BY avg_roas DESC;


-- ===========================================================================
-- BQ7 — VERTICAL / INDUSTRY PERFORMANCE
-- ===========================================================================

SELECT
    Vertical,
    COUNT(*)                                    AS campaigns,
    ROUND(SUM(Spend_VND)   / 1e9,  2)          AS spend_B_VND,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct,
    ROUND(AVG("Conv_Rate_%"),      2)          AS avg_conv_rate_pct
FROM marketing_campaigns
GROUP BY Vertical
ORDER BY avg_roas DESC;


-- ===========================================================================
-- BQ8 — HOLIDAY CAMPAIGN EFFECT
-- ===========================================================================

SELECT
    Is_Holiday_Campaign,
    COUNT(*)                                    AS campaigns,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct,
    ROUND(AVG("Conv_Rate_%"),      2)          AS avg_conv_rate_pct,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(AVG("Budget_Util_%"),    2)          AS avg_budget_util_pct
FROM marketing_campaigns
GROUP BY Is_Holiday_Campaign;


-- ===========================================================================
-- BQ9 — COMPETITOR ACTIVITY IMPACT
-- ===========================================================================

SELECT
    Competitor_Activity,
    COUNT(*)                                    AS campaigns,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct,
    ROUND(AVG("Conv_Rate_%"),      2)          AS avg_conv_rate_pct,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(SUM(Spend_VND)   / 1e9,  2)          AS spend_B_VND
FROM marketing_campaigns
GROUP BY Competitor_Activity
ORDER BY avg_ctr_pct DESC;


-- ===========================================================================
-- BQ10 — CTR by Platform × Objective (pivot-style with conditional aggregation)
-- ===========================================================================

SELECT
    Platform,
    ROUND(AVG(CASE WHEN Objective = 'Brand Awareness' THEN "CTR_%" END), 2) AS "Brand Awareness CTR",
    ROUND(AVG(CASE WHEN Objective = 'Video Views'     THEN "CTR_%" END), 2) AS "Video Views CTR",
    ROUND(AVG(CASE WHEN Objective = 'Reach'           THEN "CTR_%" END), 2) AS "Reach CTR",
    ROUND(AVG(CASE WHEN Objective = 'App Install'     THEN "CTR_%" END), 2) AS "App Install CTR",
    ROUND(AVG(CASE WHEN Objective = 'Conversions'     THEN "CTR_%" END), 2) AS "Conversions CTR",
    ROUND(AVG(CASE WHEN Objective = 'Lead Generation' THEN "CTR_%" END), 2) AS "Lead Gen CTR",
    ROUND(AVG(CASE WHEN Objective = 'Traffic'         THEN "CTR_%" END), 2) AS "Traffic CTR",
    ROUND(AVG(CASE WHEN Objective = 'Retargeting'     THEN "CTR_%" END), 2) AS "Retargeting CTR",
    ROUND(AVG("CTR_%"), 2)                                                   AS overall_avg_ctr
FROM marketing_campaigns
GROUP BY Platform
ORDER BY overall_avg_ctr DESC;


-- ===========================================================================
-- EXTRA — TOP 20 CAMPAIGNS BY REVENUE
-- ===========================================================================

SELECT
    Campaign_ID,
    Campaign_Name,
    Brand,
    Platform,
    Objective,
    Target_City,
    ROUND(Revenue_VND / 1e12, 3)               AS revenue_T_VND,
    ROUND(ROAS,                2)              AS roas,
    ROUND("CTR_%",             2)             AS ctr_pct,
    ROUND("Conv_Rate_%",       2)            AS conv_rate_pct,
    Status
FROM marketing_campaigns
ORDER BY Revenue_VND DESC
LIMIT 20;


-- ===========================================================================
-- EXTRA — BUDGET EFFICIENCY: OVER-BUDGET AND UNDER-PERFORMING CAMPAIGNS
-- ===========================================================================

SELECT
    Campaign_ID,
    Campaign_Name,
    Brand,
    Platform,
    ROUND("Budget_Util_%",  1)                 AS budget_util_pct,
    ROUND(ROAS,             2)                 AS roas,
    ROUND("ROI_%",          2)                 AS roi_pct,
    Status
FROM marketing_campaigns
WHERE "Budget_Util_%" > 95          -- high spend
  AND ROAS < 10                     -- but low return
ORDER BY roi_pct ASC
LIMIT 15;


-- ===========================================================================
-- EXTRA — SEASONAL PERFORMANCE
-- ===========================================================================

SELECT
    Season,
    COUNT(*)                                    AS campaigns,
    ROUND(SUM(Spend_VND)   / 1e9,  2)          AS spend_B_VND,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct
FROM marketing_campaigns
GROUP BY Season
ORDER BY avg_roas DESC;


-- ===========================================================================
-- EXTRA — CAMPAIGN MANAGER LEADERBOARD (min 5 campaigns)
-- ===========================================================================

SELECT
    Campaign_Manager,
    COUNT(*)                                    AS campaigns,
    ROUND(AVG(ROAS),               2)          AS avg_roas,
    ROUND(AVG("CTR_%"),            2)          AS avg_ctr_pct,
    ROUND(SUM(Revenue_VND) / 1e12, 2)          AS revenue_T_VND
FROM marketing_campaigns
GROUP BY Campaign_Manager
HAVING COUNT(*) >= 5
ORDER BY avg_roas DESC
LIMIT 15;


-- ===========================================================================
-- EXTRA — ROAS DISTRIBUTION BUCKETS
-- ===========================================================================

SELECT
    CASE
        WHEN ROAS < 1    THEN '< 1× (Loss)'
        WHEN ROAS < 10   THEN '1–10× (Low)'
        WHEN ROAS < 50   THEN '10–50× (Medium)'
        WHEN ROAS < 200  THEN '50–200× (High)'
        WHEN ROAS < 1000 THEN '200–1000× (Very High)'
        ELSE             '> 1000× (Exceptional)'
    END                                         AS roas_bucket,
    COUNT(*)                                    AS campaigns,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pct_of_total,
    ROUND(AVG(ROAS),   2)                       AS avg_roas_in_bucket,
    ROUND(AVG("CTR_%"), 2)                     AS avg_ctr_pct
FROM marketing_campaigns
GROUP BY roas_bucket
ORDER BY AVG(ROAS);


-- ===========================================================================
-- EXTRA — PLATFORM × CITY REVENUE MATRIX
-- ===========================================================================

SELECT
    Platform,
    ROUND(SUM(CASE WHEN Target_City = 'Hà Nội'    THEN Revenue_VND END) / 1e12, 2) AS "Hanoi (T VND)",
    ROUND(SUM(CASE WHEN Target_City = 'TP. HCM'   THEN Revenue_VND END) / 1e12, 2) AS "TP. HCM (T VND)",
    ROUND(SUM(CASE WHEN Target_City = 'Hải Phòng' THEN Revenue_VND END) / 1e12, 2) AS "Hai Phong (T VND)",
    ROUND(SUM(CASE WHEN Target_City = 'Đà Nẵng'   THEN Revenue_VND END) / 1e12, 2) AS "Da Nang (T VND)",
    ROUND(SUM(CASE WHEN Target_City = 'Cần Thơ'   THEN Revenue_VND END) / 1e12, 2) AS "Can Tho (T VND)",
    ROUND(SUM(CASE WHEN Target_City = 'Toàn quốc' THEN Revenue_VND END) / 1e12, 2) AS "Nationwide (T VND)",
    ROUND(SUM(Revenue_VND) / 1e12, 2)           AS total_revenue_T_VND
FROM marketing_campaigns
GROUP BY Platform
ORDER BY total_revenue_T_VND DESC;
