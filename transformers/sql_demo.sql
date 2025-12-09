WITH source_with_hash AS (
  SELECT *,
    SHA256(CONCAT(
      COALESCE(player_name, 'NULL'),
      COALESCE(CAST(score AS STRING), 'NULL'),
      COALESCE(event_date, 'NULL')
    )) as row_hash
  FROM golf_api_raw 
  WHERE event_date BETWEEN '2024-06-01' AND '2024-06-07'
)

MERGE golf_clean_fact t
USING source_with_hash s
ON t.player_name = s.player_name 
   AND t.event_date = s.event_date
WHEN MATCHED AND t.row_hash != s.row_hash THEN
  UPDATE SET score = s.score, updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
  INSERT (player_name, score, event_date, row_hash)
  VALUES (s.player_name, s.score, s.event_date, s.row_hash)