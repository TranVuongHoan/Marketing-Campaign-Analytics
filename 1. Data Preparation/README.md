# 1. Data Preparation

## Dataset Overview

The dataset `06_Marketing_Digital_Campaign.xlsx` contains **500 campaign records** across **10 advertising platforms**, **10 brands**, **8 campaign objectives**, and **6 target cities** in Vietnam.

## Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `Campaign_ID` | String | Unique campaign identifier (e.g., MKT-00001) |
| `Campaign_Name` | String | Descriptive campaign name |
| `Brand` | String | Brand running the campaign (10 brands) |
| `Platform` | String | Advertising platform (Email, SMS, Google, Facebook, etc.) |
| `Objective` | String | Campaign goal (Brand Awareness, Conversions, Traffic, etc.) |
| `Target_City` | String | Geographic target (Hanoi, HCMC, Da Nang, Hai Phong, Can Tho, Nationwide) |
| `Industry_Vertical` | String | Business vertical (Electronics, Fashion, Health, etc.) |
| `Agency` | String | Managing agency (Publicis, Ogilvy, In-house, etc.) |
| `Start_Date` | Date | Campaign start date |
| `End_Date` | Date | Campaign end date |
| `Budget_VND` | Float | Allocated budget in VND |
| `Actual_Spend_VND` | Float | Actual amount spent |
| `Impressions` | Integer | Total ad impressions served |
| `Clicks` | Integer | Total clicks received |
| `Conversions` | Integer | Total conversions achieved |
| `Revenue_VND` | Float | Revenue attributed to campaign |
| `ROAS` | Float | Return on Ad Spend (Revenue / Spend) |
| `CTR` | Float | Click-Through Rate (%) |
| `Conv_Rate` | Float | Conversion Rate (%) |
| `Competitor_Activity` | String | Competitor pressure level (Low, Medium, High) |
| `Status` | String | Campaign status (Completed, Running, Paused, etc.) |

## Dataset Size

- **Rows:** 500 campaigns
- **Total Spend:** 100.0 Billion VND
- **Total Revenue:** 56.74 Trillion VND
- **Period:** Full year (Q1–Q4)
