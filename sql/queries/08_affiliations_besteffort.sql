
SELECT
    count(*)                                          AS cs_papers,
    count(*) FILTER (WHERE authors LIKE '%(%')        AS with_paren_tag,
    round(100.0 * count(*) FILTER (WHERE authors LIKE '%(%') / count(*), 1) AS pct_covered
FROM papers WHERE primary_category LIKE 'cs.%';

WITH tags AS (
    SELECT trim(t) AS affiliation
    FROM papers,
         UNNEST(regexp_extract_all(authors, '\(([^)]*)\)', 1)) AS u(t)
    WHERE primary_category LIKE 'cs.%'
)
SELECT affiliation, count(*) AS mentions
FROM tags
WHERE affiliation <> '' AND length(affiliation) <= 40
GROUP BY affiliation
ORDER BY mentions DESC
LIMIT 25;
