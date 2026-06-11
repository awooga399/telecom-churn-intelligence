SELECT
tenure,
clients_by_tenure,
ROUND((clients_by_tenure * 100.0)/clients, 2) AS pct_clients
FROM(
	SELECT
	tenure,
	SUM(COUNT(*)) OVER(ORDER BY tenure DESC) AS clients_by_tenure,
	SUM(COUNT(*)) OVER() AS clients
	FROM customers
	GROUP BY tenure
) AS t
ORDER BY tenure;