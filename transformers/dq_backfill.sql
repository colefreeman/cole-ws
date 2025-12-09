SELECT 
  sales_rep
  , region
  , month_name
  , monthly_sales
  
  -- creates cumulative sales by month
  SUM(monthly_sales) OVER (PARTITION BY sales_rep ORDER BY month_number) AS quarterly_running_total,
  
  -- creates monthly rank by region
  RANK() OVER (PARTITION BY region, month_name ORDER BY monthly_sales DESC) AS monthly_region_rank

FROM quarterly_sales_summary
ORDER BY region, sales_rep, month_number;