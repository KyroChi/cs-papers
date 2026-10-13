-- setup.sql — builds the base views over the downloaded parquet.
-- Run once (run.py does this automatically). Creates:
--   papers          : raw rows, 1:1 with the parquet
--   papers_enriched : adds year, author_count, coarse subject group
--
-- Author counting is a PROXY. arXiv's `authors` field is a raw display
-- string ("A. Smith, B. Jones and C. Lee"). We split on commas and the
-- word "and". This is the standard approach, with two known caveats:
--   * A collaboration ("ATLAS Collaboration") counts as 1 author.
--   * A handful of malformed lists mis-split.
-- Good enough for trends; not for exact per-paper author counts.

CREATE OR REPLACE VIEW papers AS
SELECT * FROM read_parquet('data/arxiv_metadata.parquet');

CREATE OR REPLACE VIEW papers_enriched AS
SELECT
    paper_id,
    title,
    authors,
    categories,
    primary_category,
    first_version_date,
    latest_version_date,
    n_versions,
    comments,
    CAST(year(first_version_date) AS INTEGER) AS year,
    -- author count proxy: drop the trailing "((1) affil ...)" block, strip inline
    -- "(affiliation)" parens, split on commas / the word "and", drop "et al".
    length(list_filter(
        regexp_split_to_array(
            regexp_replace(regexp_replace(authors, '\s*\(\(.*$', ''), '\([^)]*\)', '', 'g'),
            ',|\s+and\s+'),
        x -> trim(x) <> '' AND NOT regexp_matches(lower(trim(x)), '^et\.? ?al\.?$')
    )) AS author_count,
    -- coarse arXiv "group" from the primary category
    CASE
        WHEN primary_category LIKE 'cs.%'                        THEN 'Computer Science'
        WHEN primary_category LIKE 'math.%'                      THEN 'Mathematics'
        WHEN primary_category LIKE 'stat.%'                      THEN 'Statistics'
        WHEN primary_category LIKE 'eess.%'                      THEN 'Elec Eng & Systems'
        WHEN primary_category LIKE 'econ.%'                      THEN 'Economics'
        WHEN primary_category LIKE 'q-bio%'                      THEN 'Quantitative Biology'
        WHEN primary_category LIKE 'q-fin%'                      THEN 'Quantitative Finance'
        WHEN primary_category LIKE 'astro-ph%'                   THEN 'Physics'
        WHEN primary_category LIKE 'cond-mat%'                   THEN 'Physics'
        WHEN primary_category LIKE 'hep-%'                       THEN 'Physics'
        WHEN primary_category LIKE 'gr-qc'                       THEN 'Physics'
        WHEN primary_category LIKE 'nucl-%'                      THEN 'Physics'
        WHEN primary_category LIKE 'quant-ph'                    THEN 'Physics'
        WHEN primary_category LIKE 'physics.%'                   THEN 'Physics'
        WHEN primary_category LIKE 'nlin.%'                      THEN 'Physics'
        WHEN primary_category LIKE 'math-ph'                     THEN 'Physics'
        ELSE 'Other/Physics-misc'
    END AS subject_group
FROM papers;
