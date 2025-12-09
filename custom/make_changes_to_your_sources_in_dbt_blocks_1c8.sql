-- Make sure to verify that Mage Pro has updated mage_sources.yml
-- to include the latest upstream blocks and their corresponding source tables.
-- The file should contain entries like:
-- sources:
--   - name: mage_<pipeline_name>
--     tables:
--       - name: <block_name>_get_data
--         identifier: mage_<pipeline_name>_<block_uuid>

-- Reference the source in your dbt model using the source() macro:
-- {{ source('<pipeline_name>', '<block_name>_get_data') }}

-- Example usage:
SELECT
    *
FROM {{ source('mage_dbt_tutorial', 'dbt_tutorial_get_data') }}
