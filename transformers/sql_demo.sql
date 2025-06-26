-- Docs: https://docs.mage.ai/guides/sql-blocks
-- Strategic backfill: Fix data quality issues incrementally
WITH affected_partitions AS (
    -- Step 1: Investigate scope of data quality issues
    SELECT 
        DATE(created_at) as partition_date,
        COUNT(*) as total_records,
        COUNT(CASE WHEN player_name IS NULL THEN 1 END) as null_names,
        ROUND(COUNT(CASE WHEN player_name IS NULL THEN 1 END) * 100.0 / COUNT(*), 2) as null_percentage
    FROM raw_golf_scores 
    WHERE created_at >= '2024-01-01'
    GROUP BY DATE(created_at)
    HAVING null_percentage > 5  -- Flag problematic partitions
),
clean_backfill_data AS (
    -- Step 2: Apply fixed logic with proper validation
    SELECT 
        player_id, 
        player_name, 
        score, 
        created_at,
        'BACKFILLED' as data_quality_flag
    FROM raw_golf_scores r
    INNER JOIN affected_partitions ap 
        ON DATE(r.created_at) = ap.partition_date
    WHERE r.player_name IS NOT NULL 
      AND r.score BETWEEN 50 AND 150  -- Business rule validation
      AND DATE(r.created_at) = '2024-01-15'  -- Test single partition first
)
-- Step 3: Insert clean data incrementally
INSERT INTO clean_golf_scores 
SELECT player_id, player_name, score, created_at
FROM clean_backfill_data;

-- Validate results
SELECT 
    COUNT(*) as backfilled_records,
    COUNT(CASE WHEN player_name IS NULL THEN 1 END) as remaining_nulls
FROM clean_golf_scores 
WHERE DATE(created_at) = '2024-01-15';