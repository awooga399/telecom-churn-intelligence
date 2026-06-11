SELECT
CASE churn
	WHEN 1 THEN 'Churned' ELSE 'Retained' END AS segment,
COUNT(*) AS clients,
ROUND(SUM(monthlycharges), 2) AS nrr,
ROUND(AVG(monthlycharges), 2) AS average_mrr
FROM customers
GROUP BY churn;