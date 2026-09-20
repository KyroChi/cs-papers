-- Q5. The "PhD students?" proxy. Metadata has no seniority field, so we
-- approximate early-career researchers by FIRST APPEARANCE of an author name.
--
-- Method: explode each paper into (author, year), find each author's first
-- year on arXiv, then count how many authors debut each year and how many
-- papers are written entirely by first-year authors.
--
-- BIG CAVEAT: name collisions. "Y. Wang" is thousands of people; initials
-- merge distinct authors. Treat these numbers as directional, not exact.
WITH exploded AS (
    SELECT
        trim(a) AS author,
        year
    FROM papers_enriched,
         UNNEST(regexp_split_to_array(authors, ',|\s+and\s+')) AS t(a)
    WHERE year IS NOT NULL AND year <= year(current_date) AND trim(a) <> ''
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
