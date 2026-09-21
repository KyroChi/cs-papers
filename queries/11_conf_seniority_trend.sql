-- Q11. [needs data/conf] Who are the authors, by seniority, over time.
-- Share of author-instances by seniority tier, per venue per year. This is the
-- direct (self-reported) answer to "is it PhD students?" for top-ML venues.
SELECT
    venue, year,
    count(*) FILTER (WHERE seniority <> 'Unknown')  AS known_positions,
    round(100.0 * count(*) FILTER (WHERE seniority = 'PhD student')             / count(*) FILTER (WHERE seniority <> 'Unknown'), 1) AS pct_phd,
    round(100.0 * count(*) FILTER (WHERE seniority = 'Junior student (MS/UG)')  / count(*) FILTER (WHERE seniority <> 'Unknown'), 1) AS pct_junior,
    round(100.0 * count(*) FILTER (WHERE seniority = 'Postdoc')                 / count(*) FILTER (WHERE seniority <> 'Unknown'), 1) AS pct_postdoc,
    round(100.0 * count(*) FILTER (WHERE seniority = 'Faculty')                 / count(*) FILTER (WHERE seniority <> 'Unknown'), 1) AS pct_faculty,
    round(100.0 * count(*) FILTER (WHERE seniority IN ('Industry/research staff','Researcher (unspecified)')) / count(*) FILTER (WHERE seniority <> 'Unknown'), 1) AS pct_industry_research
FROM conf_authors
GROUP BY venue, year
ORDER BY venue, year;
