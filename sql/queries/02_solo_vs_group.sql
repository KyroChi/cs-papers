SELECT
    year,
    count(*) AS papers,
    round(100.0 * count(*) FILTER (WHERE author_count = 1)      / count(*), 1) AS pct_solo,
    round(100.0 * count(*) FILTER (WHERE author_count BETWEEN 2 AND 3)  / count(*), 1) AS pct_2_3,
    round(100.0 * count(*) FILTER (WHERE author_count BETWEEN 4 AND 6)  / count(*), 1) AS pct_4_6,
    round(100.0 * count(*) FILTER (WHERE author_count BETWEEN 7 AND 10) / count(*), 1) AS pct_7_10,
    round(100.0 * count(*) FILTER (WHERE author_count > 10)     / count(*), 1) AS pct_11plus
FROM papers_enriched
WHERE year IS NOT NULL AND year <= year(current_date) AND author_count > 0
GROUP BY year
ORDER BY year;
