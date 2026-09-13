-- Month-over-month revenue growth rate using LAG() window function
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month,
        SUM(oi.price) AS total_revenue,
		LAG(SUM(oi.price)) OVER (
			ORDER BY DATE_TRUNC('month', o.order_purchase_timestamp)
		) AS previous_month_revenue
    FROM orders AS o
    INNER JOIN order_items AS oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY order_month
)
SELECT
    order_month,
    total_revenue,
    previous_month_revenue,
	ROUND((total_revenue - previous_month_revenue) / previous_month_revenue * 100, 2) AS percentage_growth
FROM monthly_revenue
ORDER BY order_month;