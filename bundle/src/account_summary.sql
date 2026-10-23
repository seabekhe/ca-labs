-- Accounts by type, operating company, and status. The table name carries your suffix (pipeline configuration).
CREATE OR REFRESH MATERIALIZED VIEW account_summary_${suffix}
COMMENT 'Accounts by type, operating company, and status (deployed from a bundle)'
AS SELECT account_type, operating_company, status, count(*) AS accounts
FROM accounts
GROUP BY account_type, operating_company, status;
