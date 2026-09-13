-- Total revenue from all delivered orders
SELECT
	SUM(oi.price) AS total_revenue
FROM orders AS o
INNER JOIN order_items AS oi
	ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';
