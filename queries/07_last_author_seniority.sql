-- Q7. Last-author seniority in CS. In CS the last author is conventionally the
-- senior/PI. We measure the last author's:
--   * career age = paper year - the year that name first appeared on arXiv
--   * career output = total arXiv papers that name is on (any position)
-- and track it over time and against team size.
--
-- CAVEATS: (1) name collisions inflate output and understate career age for
-- common names ("Y. Wang"); (2) last-author-as-senior is a CS convention, not
-- a rule (many subfields use alphabetical or contribution order). Directional.
--
-- Author string is cleaned of parenthetical affiliations, e.g. "Smith (MIT)".

CREATE OR REPLACE TEMP MACRO author_list(s) AS
    list_filter(
        regexp_split_to_array(regexp_replace(s, '\([^)]*\)', '', 'g'), ',|\s+and\s+'),
        x -> trim(x) <> ''
    );

-- one row per (author, paper-year) across ALL of arXiv, for debut + output
CREATE OR REPLACE TEMP TABLE author_stats AS
WITH exploded AS (
    SELECT trim(a) AS author, CAST(year(first_version_date) AS INTEGER) AS year
    FROM papers, UNNEST(author_list(authors)) AS t(a)
    WHERE first_version_date IS NOT NULL
)
SELECT author, min(year) AS debut_year, count(*) AS career_papers
FROM exploded GROUP BY author;

-- CS papers with their last author resolved
CREATE OR REPLACE TEMP TABLE cs_last AS
SELECT
    p.paper_id,
    CAST(year(p.first_version_date) AS INTEGER) AS year,
    length(author_list(p.authors))              AS author_count,
    trim(author_list(p.authors)[length(author_list(p.authors))]) AS last_author
FROM papers p
WHERE p.primary_category LIKE 'cs.%' AND p.first_version_date IS NOT NULL;

-- A) by year: is the typical CS senior author getting older / more prolific?
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

-- B) recent CS (2020+): does a bigger team come with a more senior last author?
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

