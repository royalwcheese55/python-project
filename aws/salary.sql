SELECT name, department, salary
FROM (
  SELECT
    name,
    department,
    salary,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk,
    MAX(DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC))
      OVER (PARTITION BY department) AS max_rnk
  FROM employees
) t
WHERE rnk = 2
   OR (max_rnk = 1 AND rnk = 1);