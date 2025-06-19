-- Docs: https://docs.mage.ai/guides/sql-blocks
MERGE sales_data AS target
USING new_sales AS source
ON target.customer_id = source.customer_id

-- UPDATE on data changes when timestamp is newer
WHEN MATCHED AND (
    source.last_updated > target.last_updated
    AND (
        source.total_sales != target.total_sales
        OR source.order_count != target.order_count
        OR source.status != target.status
    )
) THEN
    UPDATE SET
        total_sales = source.total_sales,
        order_count = source.order_count,
        status = source.status,
        last_updated = source.last_updated

-- ➕ INSERT: New customers
WHEN NOT MATCHED THEN
    INSERT (customer_id, total_sales, order_count, status, last_updated)
    VALUES (source.customer_id, source.total_sales, source.order_count, 
            source.status, source.last_updated);