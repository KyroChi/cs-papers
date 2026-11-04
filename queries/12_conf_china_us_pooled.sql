SELECT
    year,
    count(*) FILTER (WHERE domain <> '')                                        AS authorships_all,
    round(100.0 * count(*) FILTER (WHERE country='United States') / count(*) FILTER (WHERE domain<>''), 1) AS us_all,
    round(100.0 * count(*) FILTER (WHERE country='China')         / count(*) FILTER (WHERE domain<>''), 1) AS cn_all,
    round(100.0 * count(*) FILTER (WHERE country='United States' AND sector='Academia')
                / nullif(count(*) FILTER (WHERE sector='Academia' AND domain<>''),0), 1) AS us_academia,
    round(100.0 * count(*) FILTER (WHERE country='China' AND sector='Academia')
                / nullif(count(*) FILTER (WHERE sector='Academia' AND domain<>''),0), 1) AS cn_academia
FROM conf_authors
GROUP BY year
ORDER BY year;
