SELECT
internetservice,
COUNT(*)  AS clients,
ROUND(AVG(churn) * 100, 2) AS churn_rate,
ROUND(AVG(monthlycharges), 2) AS average_mrr
FROM customers
GROUP BY internetservice
ORDER BY churn_rate DESC;