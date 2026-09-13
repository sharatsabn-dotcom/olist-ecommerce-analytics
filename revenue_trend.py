import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/olist_analytics")

revenue_query = """
SELECT 
	DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month,
	SUM(oi.price) AS total_revenue
FROM orders AS o
INNER JOIN order_items AS oi
	ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY order_month
ORDER BY order_month;
"""

revenue_df = pd.read_sql(revenue_query, engine)

plt.figure(figsize=(12, 6))
plt.plot(revenue_df["order_month"], revenue_df["total_revenue"], marker="o")
plt.xlabel("Month")
plt.ylabel("Total Revenue ($)")
plt.title("Monthly Revenue Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("revenue_trend.png", dpi=150, bbox_inches="tight")
plt.show()