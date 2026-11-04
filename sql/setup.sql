
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
    length(list_filter(
        regexp_split_to_array(
            regexp_replace(regexp_replace(authors, '\s*\(\(.*$', ''), '\([^)]*\)', '', 'g'),
            ',|\s+and\s+'),
        x -> trim(x) <> '' AND NOT regexp_matches(lower(trim(x)), '^et\.? ?al\.?$')
    )) AS author_count,
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
