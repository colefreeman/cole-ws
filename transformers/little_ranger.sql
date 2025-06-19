SELECT 
  SHA256(CONCAT(
    COALESCE(player_name, 'NULL_PLAYER'),
    COALESCE(event_name, 'NULL_EVENT'),
    COALESCE(CAST(round_number AS STRING), 'NULL_ROUND'),
    COALESCE(CAST(thru AS STRING), 'NULL_THRU')
  )) as hash_key
  , player_name
  , tournament_date
  , course_name
  , round_number
  , thru
  , strokes_gained_total
  , CASE 
      WHEN player_name IS NULL 
        OR event_name IS NULL 
        OR round_number IS NULL 
        OR thru IS NULL
      THEN 'INCOMPLETE' 
      ELSE 'VALID' 
    END as data_quality_flag
FROM golf_stats;