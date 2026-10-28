# Enrich my account list with account attributes, demographics, and ZIP population stats.
# Note: pct_homeowners is stored as a fraction (0-1), so the 50% threshold is 0.5
spark.sql(f"""
  CREATE TABLE IF NOT EXISTS {mine('account_portfolio_insights')}
  COMMENT 'Your accounts classified by type and operating company, with demographics compared to their ZIP population' AS
  WITH base AS (
    SELECT a.account_id, a.account_type, a.operating_company, a.opco_name, a.status, a.zip_code, a.city, a.state,
           d.age_of_primary, d.household_size, d.own_rent, d.income_bracket, d.credit_score_range, d.usage_tier,
           d.avg_monthly_usage_kwh, d.years_as_customer,
           p.median_household_income AS zip_median_household_income,
           p.pct_homeowners          AS zip_pct_homeowners,
           p.median_age              AS zip_median_age,
           p.poverty_rate            AS zip_poverty_rate,
           CASE d.income_bracket
             WHEN 'Under $25K'  THEN 20000
             WHEN '$25K-$50K'   THEN 37500
             WHEN '$50K-$75K'   THEN 62500
             WHEN '$75K-$100K'  THEN 87500
             WHEN '$100K-$150K' THEN 125000
             WHEN '$150K-$250K' THEN 200000
             WHEN 'Over $250K'  THEN 300000
           END AS est_income
    FROM {mine('my_account_list')} l
    JOIN {accounts} a USING (account_id)
    LEFT JOIN {account_demographics} d USING (account_id)
    LEFT JOIN {population_stats} p ON p.zip_code = a.zip_code
  )
  SELECT account_id, account_type, operating_company, opco_name, status, zip_code, city, state,
         age_of_primary, household_size, own_rent, income_bracket, credit_score_range, usage_tier,
         avg_monthly_usage_kwh, years_as_customer,
         zip_median_household_income, zip_pct_homeowners, zip_median_age, zip_poverty_rate,
         CASE WHEN est_income > zip_median_household_income * 1.2 THEN 'above'
              WHEN est_income < zip_median_household_income * 0.8 THEN 'below'
              ELSE 'near' END AS income_vs_zip,
         CASE WHEN own_rent = 'Own'  AND zip_pct_homeowners <  0.5 THEN 'owner in a renter-majority ZIP'
              WHEN own_rent = 'Rent' AND zip_pct_homeowners >= 0.5 THEN 'renter in an owner-majority ZIP'
              ELSE 'typical for ZIP' END AS owner_vs_zip
  FROM base
""")

df = spark.table(mine('account_portfolio_insights'))
print(f"✓ {mine('account_portfolio_insights')}: {df.count()} rows, {len(df.columns)} columns")
display(df)