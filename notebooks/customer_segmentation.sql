-- Customer Segmentation Transformation
-- This notebook is referenced in Lab 1A as an example of reusable SQL

CREATE OR REPLACE TABLE {catalog}.{schema}.customer_segments AS
SELECT
  account_id,
  CASE
    WHEN usage_tier = 'very_high' THEN 'Enterprise'
    WHEN income_bracket IN ('Over $250K', '$150K-$250K') THEN 'Premium'
    ELSE 'Standard'
  END as customer_segment,
  current_timestamp() as created_at
FROM {catalog}.{schema}.account_demographics
WHERE account_id IS NOT NULL;

SELECT
  customer_segment,
  COUNT(*) as count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) as pct
FROM customer_segments
GROUP BY customer_segment
ORDER BY pct DESC;
