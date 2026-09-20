-- Q8. Institutions — BEST EFFORT ONLY. This metadata has NO email/affiliation
-- field (only ~71 of 3.1M author strings contain an '@'). The single signal is
-- parenthetical lab tags some authors add, e.g. "Jane Doe (MIT)".
--
-- HEAVY CAVEATS:
--   * Coverage is only ~6% of papers, and skews to certain communities/eras.
--   * Tags are lab acronyms, not normalized institutions ("LAAS", "INRIA Rennes").
--   * NOT a representative sample. Do not draw population conclusions from this.
-- For real institution analysis, enrich via OpenAlex / Semantic Scholar by
-- arXiv ID (they carry affiliations) — no PDFs required.

-- coverage check for CS
SELECT
    count(*)                                          AS cs_papers,
    count(*) FILTER (WHERE authors LIKE '%(%')        AS with_paren_tag,
    round(100.0 * count(*) FILTER (WHERE authors LIKE '%(%') / count(*), 1) AS pct_covered
FROM papers WHERE primary_category LIKE 'cs.%';

-- top parenthetical affiliation tags among CS papers (of the ~6% that have them)
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
