-- Top 5 individual products by total revenue, using RANK() window function
WITH product_rankings AS (
	SELECT
		p.product_id,
		p.product_category_name,
		SUM(oi.price) AS total_revenue,
		RANK() OVER(
			ORDER BY SUM(oi.price) DESC
		) AS product_rank
	FROM order_items AS oi
	INNER JOIN products AS p
		ON oi.product_id = p.product_id
	GROUP BY
		p.product_id,
		p.product_category_name
)
SELECT
	product_id,
	product_category_name,
	total_revenue,
	product_rank
FROM product_rankings
WHERE product_rank <= 5;