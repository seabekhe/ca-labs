-- Hurricane Impact Analysis
-- Identify customers in impact zones and their communication preferences

SELECT
  a.account_id,
  a.account_name,
  a.city,
  a.zip_code,
  z.impact_severity,
  z.estimated_outage_hours,
  c.email,
  c.sms_opt_in,
  c.language_preference
FROM {catalog}.{schema}.accounts a
JOIN {catalog}.{schema}.storm_impact_zones z 
  ON a.zip_code = z.zip_code
JOIN {catalog}.{schema}.customer_contacts c 
  ON a.account_id = c.account_id
WHERE z.storm_id = 'STM-2026-0013'  -- Hurricane Epsilon
  AND (c.email_opt_in OR c.sms_opt_in)
ORDER BY z.estimated_outage_hours DESC
LIMIT 100;
