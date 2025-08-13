SELECT
  order_id,
  customer_id,
  product_id,
  CAST(order_date AS DATE) AS order_date,
  CAST(total_price AS DOUBLE) AS total_price
FROM {{ ref('raw_sales') }}
