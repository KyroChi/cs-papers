-- Q6. Decompose the surge. Between a baseline year and a recent year, how
-- much of the TOTAL added volume came from each subject group, and from each
-- author-count bucket? This directly answers "who/what is responsible."
--
-- Edit :baseline / :recent below (defaults: 10 years apart).
WITH bounds AS (
    SELECT year(current_date) - 11 AS baseline, year(current_date) - 1 AS recent
),
tagged AS (
    SELECT
        subject_group,
        CASE
            WHEN author_count = 1            THEN '1 (solo)'
            WHEN author_count BETWEEN 2 AND 3 THEN '2-3'
            WHEN author_count BETWEEN 4 AND 6 THEN '4-6'
            WHEN author_count BETWEEN 7 AND 10 THEN '7-10'
            ELSE '11+'
        END AS team_bucket,
        year
    FROM papers_enriched, bounds
    WHERE year IN (bounds.baseline, bounds.recent) AND author_count > 0
)
-- contribution to growth by subject group
SELECT
    'subject_group' AS dimension, subject_group AS value,
    count(*) FILTER (WHERE year = (SELECT baseline FROM bounds)) AS baseline_papers,
    count(*) FILTER (WHERE year = (SELECT recent   FROM bounds)) AS recent_papers,
    count(*) FILTER (WHERE year = (SELECT recent FROM bounds))
      - count(*) FILTER (WHERE year = (SELECT baseline FROM bounds)) AS added
FROM tagged GROUP BY subject_group
UNION ALL
SELECT
    'team_bucket', team_bucket,
    count(*) FILTER (WHERE year = (SELECT baseline FROM bounds)),
    count(*) FILTER (WHERE year = (SELECT recent   FROM bounds)),
    count(*) FILTER (WHERE year = (SELECT recent FROM bounds))
      - count(*) FILTER (WHERE year = (SELECT baseline FROM bounds))
FROM tagged GROUP BY team_bucket
ORDER BY dimension, added DESC;
