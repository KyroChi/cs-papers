-- Q10. [needs data/conf] China vs US vs rest at NeurIPS/ICML/ICLR over time.
-- Share of author-instances (each authorship counted) by institution country,
-- per venue per year. Company domains = HQ country (see conf_setup caveats).
SELECT
    venue, year,
    count(*) FILTER (WHERE domain <> '')                    AS authorships,
    round(100.0 * count(*) FILTER (WHERE country = 'United States') / count(*) FILTER (WHERE domain <> ''), 1) AS pct_us,
    round(100.0 * count(*) FILTER (WHERE country = 'China')         / count(*) FILTER (WHERE domain <> ''), 1) AS pct_china,
    round(100.0 * count(*) FILTER (WHERE country NOT IN ('United States','China','Other/Unknown','Unknown') AND domain <> '') / count(*) FILTER (WHERE domain <> ''), 1) AS pct_other_named,
    round(100.0 * count(*) FILTER (WHERE country IN ('Other/Unknown')) / count(*) FILTER (WHERE domain <> ''), 1) AS pct_unclassified
FROM conf_authors
GROUP BY venue, year
ORDER BY venue, year;
