
CREATE OR REPLACE TEMP MACRO author_list(s) AS
    list_filter(
        regexp_split_to_array(
            regexp_replace(regexp_replace(s, '\s*\(\(.*$', ''), '\([^)]*\)', '', 'g'),
            ',|\s+and\s+'),
        x -> trim(x) <> '' AND NOT regexp_matches(lower(trim(x)), '^et\.? ?al\.?$')
    );

CREATE OR REPLACE TEMP TABLE author_stats AS
WITH exploded AS (
    SELECT trim(a) AS author, CAST(year(first_version_date) AS INTEGER) AS year
    FROM papers, UNNEST(author_list(authors)) AS t(a)
    WHERE first_version_date IS NOT NULL
)
SELECT author, min(year) AS debut_year, count(*) AS career_papers
FROM exploded GROUP BY author;

CREATE OR REPLACE TEMP TABLE cs_last AS
SELECT
    p.paper_id,
    CAST(year(p.first_version_date) AS INTEGER) AS year,
    length(author_list(p.authors))              AS author_count,
    trim(author_list(p.authors)[length(author_list(p.authors))]) AS last_author
FROM papers p
WHERE p.primary_category LIKE 'cs.%' AND p.first_version_date IS NOT NULL;

SELECT
    c.year,
    count(*)                                         AS cs_papers,
    median(c.year - s.debut_year)                    AS median_last_author_career_age,
    median(s.career_papers)                          AS median_last_author_total_papers,
    round(100.0 * count(*) FILTER (WHERE c.year = s.debut_year) / count(*), 1)
                                                     AS pct_last_author_is_newcomer
FROM cs_last c JOIN author_stats s ON c.last_author = s.author
WHERE c.year BETWEEN 2000 AND year(current_date)
GROUP BY c.year ORDER BY c.year;

SELECT
    CASE
        WHEN c.author_count = 1            THEN '1 (solo)'
        WHEN c.author_count BETWEEN 2 AND 3 THEN '2-3'
        WHEN c.author_count BETWEEN 4 AND 6 THEN '4-6'
        WHEN c.author_count BETWEEN 7 AND 10 THEN '7-10'
        ELSE '11+'
    END AS team_bucket,
    count(*)                          AS cs_papers,
    median(c.year - s.debut_year)     AS median_last_author_career_age,
    median(s.career_papers)           AS median_last_author_total_papers
FROM cs_last c JOIN author_stats s ON c.last_author = s.author
WHERE c.year >= 2020
GROUP BY team_bucket
ORDER BY min(c.author_count);

