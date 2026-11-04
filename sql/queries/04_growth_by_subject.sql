SELECT
    year,
    count(*) FILTER (WHERE subject_group = 'Computer Science')     AS cs,
    count(*) FILTER (WHERE subject_group = 'Physics')              AS physics,
    count(*) FILTER (WHERE subject_group = 'Mathematics')          AS math,
    count(*) FILTER (WHERE subject_group = 'Statistics')           AS stat,
    count(*) FILTER (WHERE subject_group = 'Elec Eng & Systems')   AS eess,
    count(*) FILTER (WHERE subject_group = 'Quantitative Biology') AS q_bio,
    count(*) FILTER (WHERE subject_group = 'Economics')            AS econ,
    count(*)                                                       AS total
FROM papers_enriched
WHERE year IS NOT NULL AND year <= year(current_date)
GROUP BY year
ORDER BY year;

WITH by_cat AS (
    SELECT primary_category,
           count(*) FILTER (WHERE year = year(current_date) - 1) AS recent,
           count(*) FILTER (WHERE year = year(current_date) - 11) AS decade_ago
    FROM papers_enriched
    WHERE year IS NOT NULL
    GROUP BY primary_category
)
SELECT primary_category, decade_ago, recent, (recent - decade_ago) AS added
FROM by_cat
ORDER BY added DESC
LIMIT 20;
