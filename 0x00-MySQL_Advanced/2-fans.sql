-- a SQL script that ranks country origins of bands, ordered by the number of fans
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands GROUP BY 1 ORDER BY 2 DESC;
