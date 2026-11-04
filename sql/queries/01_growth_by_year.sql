SELECT
    year,
    count(*)                                            AS papers,
    round(100.0 * (count(*) - lag(count(*)) OVER (ORDER BY year))
          / lag(count(*)) OVER (ORDER BY year), 1)      AS yoy_pct
FROM papers_enriched
WHERE year IS NOT NULL AND year <= year(current_date)
GROUP BY year
ORDER BY year;
