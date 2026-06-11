SELECT
contract,
COUNT(*) AS total_clients,
SUM(churn) AS churned,
ROUND(AVG(churn) * 100, 2) AS churn_rate
FROM customers
GROUP BY contract
ORDER BY churn_rate DESC;