WITH ordered AS (
  SELECT
    customer_id, order_id, order_date,
    LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_date
  FROM {{ ref('stg_sales') }}
),
diffs AS (
  SELECT
    customer_id, order_date,
    CASE WHEN prev_order_date IS NULL THEN NULL
         ELSE date_diff('day', prev_order_date, order_date)
    END AS days_between
  FROM ordered
)
SELECT
  customer_id,
  COUNT(*)          AS total_orders,
  MIN(order_date)   AS first_order,
  MAX(order_date)   AS last_order,
  AVG(days_between) AS avg_days_between_orders
FROM diffs
GROUP BY customer_id
ORDER BY avg_days_between_orders NULLS LAST
