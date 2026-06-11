SELECT
customerid,
contract,
monthlycharges,
churn,
ranked
FROM(
SELECT *,
ROW_NUMBER() OVER(PARTITION BY contract ORDER BY monthlycharges DESC, customerid) AS ranked
FROM customers
) AS ranked_customers
WHERE ranked <=5;