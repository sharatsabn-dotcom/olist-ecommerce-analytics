-- RFM base query: Recency (days since last order), Frequency (order count),
-- and Monetary (total spend) per customer. Feeds into Python KMeans clustering.
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