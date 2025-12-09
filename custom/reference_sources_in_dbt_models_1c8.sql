-- Reference the upstream Mage block as a source table in dbt
SELECT
    *
FROM {{ source('mage_dbt_tutorial', 'dbt_tutorial_get_data') }}
