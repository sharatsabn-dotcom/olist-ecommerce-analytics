-- Revenue broken down by calendar month, to track growth over time
SELECT
	DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month,
	SUM(oi.price) AS total_revenue
FROM orders AS o
INNER JOIN order_items AS oi
	ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY order_month
ORDER BY order_month;
