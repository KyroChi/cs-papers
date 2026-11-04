
SELECT
    year,
    count(*) FILTER (WHERE majority_region <> 'Unknown')                         AS papers,
    round(100.0 * count(*) FILTER (WHERE majority_region='China') / count(*) FILTER (WHERE majority_region<>'Unknown'), 1) AS pct_china,
    round(100.0 * count(*) FILTER (WHERE majority_region='US')    / count(*) FILTER (WHERE majority_region<>'Unknown'), 1) AS pct_us,
    round(100.0 * count(*) FILTER (WHERE majority_region='Other') / count(*) FILTER (WHERE majority_region<>'Unknown'), 1) AS pct_other,
    count(*) FILTER (WHERE majority_region='Unknown')                            AS unattributed
FROM conf_paper_region
WHERE year >= 2021
GROUP BY year ORDER BY year;

SELECT
    venue, year,
    count(*) FILTER (WHERE majority_region='China') AS china,
    count(*) FILTER (WHERE majority_region='US')    AS us,
    count(*) FILTER (WHERE majority_region='Other') AS other,
    round(100.0 * count(*) FILTER (WHERE majority_region='China') / count(*) FILTER (WHERE majority_region<>'Unknown'), 1) AS pct_china,
    round(100.0 * count(*) FILTER (WHERE majority_region='US')    / count(*) FILTER (WHERE majority_region<>'Unknown'), 1) AS pct_us
FROM conf_paper_region
WHERE year >= 2021
GROUP BY venue, year ORDER BY venue, year;

SELECT
    year,
    count(*) FILTER (WHERE n_known > 0)                          AS papers,
    round(100.0 * count(*) FILTER (WHERE any_china) / count(*) FILTER (WHERE n_known>0), 1) AS pct_any_china,
    round(100.0 * count(*) FILTER (WHERE any_us)    / count(*) FILTER (WHERE n_known>0), 1) AS pct_any_us,
    round(100.0 * count(*) FILTER (WHERE any_china AND any_us) / count(*) FILTER (WHERE n_known>0), 1) AS pct_us_china_joint
FROM conf_paper_region
WHERE year >= 2021
GROUP BY year ORDER BY year;
