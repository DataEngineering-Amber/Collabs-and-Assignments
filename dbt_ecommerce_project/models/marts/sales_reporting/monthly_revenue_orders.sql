SELECT
  strftime(order_date, '%Y-%m') AS month,
  COUNT(order_id)               AS total_orders,
  SUM(total_price)              AS total_revenue
FROM {{ ref('stg_sales') }}
GROUP BY month
ORDER BY month
