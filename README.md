# Olist E-Commerce Analytics: Customer Retention & Segmentation

Analyzing 100K+ orders across 7 relational tables from a Brazilian e-commerce marketplace to uncover revenue trends, customer retention patterns, and behavioral segments using PostgreSQL and Python.

## Problem Statement

Understanding whether customers return for repeat purchases is critical for any e-commerce business — a one-time customer base signals a growth strategy that constantly needs to refill the top of the funnel, while strong repeat purchasing suggests a more sustainable, profitable customer base. This project analyzes order, customer, and payment data from Olist, a Brazilian e-commerce marketplace, to answer three questions: How often do customers return to make a second purchase? Which customers are most valuable, and what distinguishes them? And where should the business focus its retention efforts to improve long-term revenue?

## Tech Stack

- **PostgreSQL** — relational database
- **pgAdmin** — database management/query tool
- **Python** — data loading and analysis
- **pandas** — data manipulation
- **SQLAlchemy** — Python-to-PostgreSQL connection
- **psycopg2** — PostgreSQL database adapter
- **python-dotenv** — secure credential management
- **scikit-learn** — KMeans clustering for customer segmentation
- **matplotlib** — data visualization

## Approach

- **Data source**: Started with 9 raw CSV files from the Olist Brazilian E-Commerce public dataset, covering customers, orders, products, sellers, payments, and reviews.

- **Schema design**: Designed a normalized relational schema in PostgreSQL with 7 tables, using primary and foreign keys to properly connect customers, orders, order items, products, sellers, payments, and reviews.

- **Data pipeline (ETL)**: Built a Python pipeline using pandas and SQLAlchemy to clean and load ~550,000 rows into PostgreSQL. This included handling a real data quality issue — 814 duplicate `review_id` values in the raw reviews data — by removing duplicates before loading.

- **SQL analysis**: Wrote a series of SQL queries in PostgreSQL covering revenue trends, month-over-month growth (window functions), top product rankings, cohort retention analysis, customer lifetime value, and RFM (Recency, Frequency, Monetary) metrics.

- **Customer segmentation**: Used the RFM data to perform K-Means clustering in Python (scikit-learn), grouping customers into 4 behavioral segments. Visualized the segments with matplotlib across two dimensions — recency vs. monetary value, and recency vs. purchase frequency — to understand what actually distinguishes each group.

## Key Findings

- **Very low repeat purchase rate**: Only ~3% of customers (2,774 of 93,358) made multiple purchases, while 97% were one-time customers.

- **Recency drives segmentation more than spending**: Customer segments were primarily differentiated by *when* a customer last purchased, rather than *how much* they spent. High-Value One-Time Customers averaged $1,142 per order but still did not return — high spend didn't predict repeat behavior.

- **Cohort retention confirms the pattern**: Cohort analysis showed a sharp drop in active customers after the first month across all cohorts, reinforcing the RFM findings and indicating that customer retention is a major challenge.

- **Strong revenue growth with a seasonal spike**: Monthly revenue grew from near-zero in late 2016 to a steady ~$650K/month by late 2017, before a sharp spike in November 2017 (~$1M), consistent with the Black Friday/holiday shopping season. Growth plateaued around $850K-950K/month through mid-2018.

**Overall Insight**: The analysis suggests that the primary business opportunity is improving customer retention and converting high-value one-time buyers into repeat customers, rather than simply increasing spend from existing purchases.

## Visualizations

- `revenue_trend.png` — Monthly revenue from Sept 2016 to Aug 2018, showing overall growth and a seasonal spike
- `customer_segments.png` — Customer segments by recency vs. monetary value
- `customer_segments_frequency.png` — Customer segments by recency vs. purchase frequency

## Business Recommendations

- **Launch a loyalty/membership program.** Since 97% of customers never return, a rewards program offering discounts or perks on future purchases could incentivize one-time buyers to come back, directly targeting the low repeat-purchase rate identified in this analysis.

- **Create a targeted offer for high-value one-time buyers.** Since the "High-Value One-Timers" segment already spends significantly more per order ($1,142 avg) but shows no repeat behavior, a tiered incentive (e.g., "spend over $X, get Y% off your next order") could specifically convert this segment into repeat customers — likely a higher-ROI target than broad, untargeted campaigns.

- **Time retention outreach immediately after the first purchase.** Cohort analysis showed retention drops sharply after month 0, meaning the highest-risk window for losing a customer is right after their first order. A post-purchase membership invite or follow-up offer sent shortly after checkout — rather than weeks or months later — would target the exact moment customers are most likely to churn.

## How to Run This

1. Clone this repository
2. Download the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle and place the CSVs in a `data/` folder in the project root
3. Create a PostgreSQL database named `olist_analytics`
4. Run the schema creation SQL (`schema.sql`) in pgAdmin's Query Tool to create the tables
5. Create a `.env` file in the project root with your database password:
DB_PASSWORD=your_password_here
6. Install dependencies:
pip install pandas sqlalchemy psycopg2-binary python-dotenv scikit-learn matplotlib
7. Run `main.py` to load the data into PostgreSQL
8. Run `rfm_analysis.py` to generate the RFM segmentation and charts
9. Explore the analysis queries in the `sql/` folder using pgAdmin's Query Tool

## Repo Structure

```
olist-ecommerce-analytics/
├── main.py                          # ETL pipeline: loads all 7 CSVs into PostgreSQL
├── rfm_analysis.py                  # Pulls RFM data, runs KMeans clustering, generates charts
├── revenue_trend.py                 # Pulls monthly revenue data and generates trend chart
├── schema.sql                       # Database schema (CREATE TABLE statements for all 7 tables)
├── sql/
│   ├── 01_total_revenue.sql
│   ├── 02_monthly_revenue.sql
│   ├── 03_month-over-month_growth_rate.sql
│   ├── 04_top_products.sql
│   ├── 05_cohort_retention.sql
│   ├── 06_customer_lifetime_value.sql
│   └── 07_rfm_analysis.sql
├── revenue_trend.png                # Chart: Monthly revenue trend
├── customer_segments.png            # Chart: Recency vs. Monetary segments
├── customer_segments_frequency.png  # Chart: Recency vs. Frequency segments
├── .gitignore
└── README.md
```
```