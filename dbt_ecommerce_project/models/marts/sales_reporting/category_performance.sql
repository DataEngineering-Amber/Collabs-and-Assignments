SELECT
  p.category,
  COUNT(s.order_id)  AS total_sales,
  SUM(s.total_price) AS total_revenue,
  AVG(p.price)       AS avg_price
FROM {{ ref('stg_sales') }} s
JOIN {{ ref('stg_products') }} p USING (product_id)
GROUP BY p.category
ORDER BY total_revenue DESC
