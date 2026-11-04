SELECT
    year,
    count(*)                             AS papers,
    round(avg(author_count), 2)          AS mean_authors,
    median(author_count)                 AS median_authors,
    max(author_count)                    AS max_authors
FROM papers_enriched
WHERE year IS NOT NULL AND year <= year(current_date) AND author_count > 0
GROUP BY year
ORDER BY year;
