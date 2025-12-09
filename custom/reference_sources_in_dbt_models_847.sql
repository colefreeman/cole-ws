WITH events_clean AS (
    SELECT
        user_id
        , CAST(event_timestamp AS DATE) AS activity_date
    FROM {{ source('mage_dbt_tutorial', 'dbt_tutorial_get_data') }}
    WHERE user_id IS NOT NULL
)
SELECT
    activity_date
    , COUNT(DISTINCT user_id) AS active_users
FROM events_clean
GROUP BY activity_date
ORDER BY activity_date DESC
LIMIT 30;
