import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/olist_analytics")

rfm_query = """
WITH customer_rfm AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.price) AS monetary,
        MAX(o.order_purchase_timestamp) AS last_order_date
    FROM customers AS c
    INNER JOIN orders AS o
        ON c.customer_id = o.customer_id
    INNER JOIN order_items AS oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT
    customer_unique_id,
    frequency,
    monetary,
    last_order_date,
    (SELECT MAX(order_purchase_timestamp) FROM orders)::date - last_order_date::date AS recency_days
FROM customer_rfm;
"""

rfm_df = pd.read_sql(rfm_query, engine)

print(rfm_df.head())
print(rfm_df.shape)



# Select just the R, F, M columns for clustering
rfm_features = rfm_df[["recency_days", "frequency", "monetary"]]

# Scale them so no single column dominates due to bigger raw numbers
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_features)

# Run KMeans with 4 clusters (a reasonable starting point)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm_df["cluster"] = kmeans.fit_predict(rfm_scaled)

print(rfm_df.groupby("cluster")[["recency_days", "frequency", "monetary"]].mean())
print(rfm_df["cluster"].value_counts())

cluster_labels = {
    0: "High-Value One-Timers",
    1: "Lost/Dormant Customers",
    2: "Loyal/Repeat Customers",
    3: "Recent One-Time Customers"
}

rfm_df["segment"] = rfm_df["cluster"].map(cluster_labels)

print(rfm_df[["customer_unique_id", "recency_days", "frequency", "monetary", "segment"]].head(10))

cluster_labels = {
    0: "High-Value One-Timers",
    1: "Lost/Dormant Customers",
    2: "Loyal/Repeat Customers",
    3: "Recent One-Time Customers"
}

rfm_df["segment"] = rfm_df["cluster"].map(cluster_labels)

print(rfm_df[["customer_unique_id", "recency_days", "frequency", "monetary", "segment"]].head(10))


plt.figure(figsize=(10, 6))
for segment in rfm_df["segment"].unique():
    subset = rfm_df[rfm_df["segment"] == segment]
    plt.scatter(subset["recency_days"], subset["monetary"], label=segment, alpha=0.5, s=10)

plt.xlabel("Recency (days since last order)")
plt.ylabel("Monetary (total spend)")
plt.title("Customer Segments: Recency vs. Monetary Value")
plt.legend()
plt.savefig("customer_segments.png", dpi=150, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10, 6))
for segment in rfm_df["segment"].unique():
    subset = rfm_df[rfm_df["segment"] == segment]
    plt.scatter(subset["recency_days"], subset["frequency"], label=segment, alpha=0.5, s=10)

plt.xlabel("Recency (days since last order)")
plt.ylabel("Frequency (number of orders)")
plt.title("Customer Segments: Recency vs. Frequency")
plt.legend()
plt.savefig("customer_segments_frequency.png", dpi=150, bbox_inches="tight")
plt.show()