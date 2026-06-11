WITH tenure_segments AS (
	SELECT
	churn,
	tenure,
	CASE
		WHEN tenure <= 12 THEN '0-12'
	    WHEN tenure <= 24 THEN '13-24'
	    WHEN tenure <= 48 THEN '25-48'
	    ELSE '49+'
	END AS tenure_bucket
	FROM customers
)


SELECT
tenure_bucket,
COUNT(*)                    AS total_clients,
SUM(churn)                  AS churned,
ROUND(AVG(churn) * 100, 2)  AS churn_rate
FROM tenure_segments
GROUP BY tenure_bucket
ORDER BY MIN(tenure);