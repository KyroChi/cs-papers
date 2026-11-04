WITH exploded AS (
    SELECT
        trim(a) AS author,
        year
    FROM papers_enriched,
         UNNEST(regexp_split_to_array(
             regexp_replace(regexp_replace(authors, '\s*\(\(.*$', ''), '\([^)]*\)', '', 'g'),
             ',|\s+and\s+')) AS t(a)
    WHERE year IS NOT NULL AND year <= year(current_date) AND trim(a) <> ''
      AND NOT regexp_matches(lower(trim(a)), '^et\.? ?al\.?$')
),
first_seen AS (
    SELECT author, min(year) AS debut_year
    FROM exploded
    GROUP BY author
)
SELECT
    debut_year AS year,
    count(*)   AS new_authors_debuting
FROM first_seen
GROUP BY debut_year
ORDER BY debut_year;
