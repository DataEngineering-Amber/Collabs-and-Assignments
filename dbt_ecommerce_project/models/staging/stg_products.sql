SELECT
  product_id,
  product_name,
  category,
  CAST(price AS DOUBLE) AS price
FROM {{ ref('raw_products') }}
