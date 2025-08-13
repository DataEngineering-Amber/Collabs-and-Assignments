WITH customer_revenue AS (
  SELECT
    customer_id,
    COUNT(order_id)  AS total_orders,
    SUM(total_price) AS total_revenue,
    AVG(total_price) AS avg_order_value
  FROM {{ ref('stg_sales') }}
  GROUP BY customer_id
)
SELECT * FROM customer_revenue
ORDER BY total_revenue DESC
