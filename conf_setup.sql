-- conf_setup.sql — views over the Paper Copilot author files (NeurIPS/ICML/ICLR).
-- Loaded automatically by run.py when data/conf/ is present. Builds:
--   conf_papers  : one row per paper (venue, year, id, raw author/aff strings)
--   conf_authors : one row per (paper, author) with primary domain, country,
--                  sector (academia/industry), and seniority tier.
--
-- CAVEATS: (1) company domains map to HQ country, NOT office location — a
-- Google-Beijing author counts as US here; academic domains (.edu, .edu.cn,
-- .ac.*) are unambiguous, so an academia-only cut is the cleanest China/US
-- signal. (2) Affiliation coverage varies by venue-year. (3) Within one author,
-- multiple concurrent affiliations are '+'-joined; we keep the FIRST (primary).

CREATE OR REPLACE VIEW conf_papers AS
SELECT
    regexp_extract(filename, 'conf/([a-z]+)_', 1)              AS venue,
    CAST(regexp_extract(filename, '(\d{4})\.jsonl', 1) AS INT) AS year,
    id, author, aff, aff_domain, position
FROM read_json_auto('data/conf/*.jsonl', union_by_name := true, filename := true);

CREATE OR REPLACE VIEW conf_authors AS
WITH split AS (
    SELECT venue, year, id,
        string_split(coalesce(author, ''), ';')     AS a,
        string_split(coalesce(aff, ''), ';')         AS af,
        string_split(coalesce(aff_domain, ''), ';')  AS ad,
        string_split(coalesce(position, ''), ';')    AS po
    FROM conf_papers
),
exploded AS (
    SELECT venue, year, id,
        i                                                   AS author_no,
        trim(a[i])                                          AS author,
        trim(af[i])                                         AS aff,
        lower(trim(split_part(ad[i], '+', 1)))              AS domain,
        lower(trim(split_part(po[i], '+', 1)))              AS position
    FROM split, unnest(range(1, length(ad) + 1)) AS g(i)
),
tagged AS (
    SELECT *,
        lower(split_part(domain, '.', -1)) AS tld
    FROM exploded
)
SELECT
    venue, year, id, author_no, author, aff, domain, position,
    -- sector: academia vs industry vs other
    CASE
        WHEN domain LIKE '%.edu' OR domain LIKE '%.edu.%' OR domain LIKE '%.ac.%'
             OR domain LIKE '%.edu.cn' OR domain LIKE 'uni%' OR aff ILIKE '%universit%'
             OR aff ILIKE '%institute of technology%' OR aff ILIKE '%college%' THEN 'Academia'
        WHEN domain IN ('google.com','microsoft.com','meta.com','fb.com','amazon.com',
             'ibm.com','nvidia.com','apple.com','openai.com','adobe.com','deepmind.com',
             'anthropic.com','alibaba-inc.com','huawei.com','tencent.com','bytedance.com',
             'baidu.com','sensetime.com','megvii.com','samsung.com','naver.com','qualcomm.com',
             'intel.com','salesforce.com','bosch.com','sony.com','jd.com','kuaishou.com')
             OR domain LIKE '%research.%' THEN 'Industry'
        WHEN domain = '' THEN 'Unknown'
        ELSE 'Other'
    END AS sector,
    -- country from domain (company => HQ; academic ccTLD => unambiguous)
    CASE
        WHEN domain = '' THEN 'Unknown'
        WHEN domain LIKE '%.cn' THEN 'China'
        WHEN domain IN ('alibaba-inc.com','huawei.com','tencent.com','bytedance.com',
             'baidu.com','sensetime.com','megvii.com','kuaishou.com','jd.com','xiaomi.com',
             'netease.com','antgroup.com','deepseek.com','iflytek.com','meituan.com',
             'sensetime.com','mail.ustc.edu.cn') THEN 'China'
        WHEN domain IN ('google.com','microsoft.com','meta.com','fb.com','amazon.com',
             'ibm.com','nvidia.com','apple.com','openai.com','adobe.com','anthropic.com',
             'salesforce.com','qualcomm.com','intel.com','netflix.com','tesla.com') THEN 'United States'
        WHEN domain LIKE '%.edu' OR domain LIKE '%.gov' OR domain LIKE '%.mil' THEN 'United States'
        WHEN tld = 'uk' THEN 'United Kingdom'
        WHEN domain = 'deepmind.com' THEN 'United Kingdom'
        WHEN tld = 'de' THEN 'Germany'      WHEN tld = 'fr' THEN 'France'
        WHEN tld = 'jp' THEN 'Japan'        WHEN tld = 'kr' THEN 'South Korea'
        WHEN domain IN ('samsung.com','naver.com','kakaocorp.com') THEN 'South Korea'
        WHEN tld = 'ca' THEN 'Canada'       WHEN tld = 'ch' THEN 'Switzerland'
        WHEN tld = 'in' THEN 'India'        WHEN tld = 'sg' THEN 'Singapore'
        WHEN tld = 'il' THEN 'Israel'       WHEN tld = 'au' THEN 'Australia'
        WHEN tld = 'hk' THEN 'Hong Kong'    WHEN tld = 'tw' THEN 'Taiwan'
        WHEN tld = 'nl' THEN 'Netherlands'  WHEN tld = 'it' THEN 'Italy'
        WHEN tld = 'es' THEN 'Spain'        WHEN tld = 'se' THEN 'Sweden'
        WHEN tld = 'at' THEN 'Austria'      WHEN tld = 'be' THEN 'Belgium'
        WHEN tld = 'dk' THEN 'Denmark'      WHEN tld = 'fi' THEN 'Finland'
        WHEN tld = 'no' THEN 'Norway'       WHEN tld = 'ru' THEN 'Russia'
        WHEN tld = 'pl' THEN 'Poland'       WHEN tld = 'br' THEN 'Brazil'
        WHEN tld = 'ie' THEN 'Ireland'      WHEN tld = 'nz' THEN 'New Zealand'
        ELSE 'Other/Unknown'
    END AS country,
    -- region: the three buckets we track (Unknown = no domain given)
    CASE
        WHEN domain = '' THEN 'Unknown'
        WHEN country = 'China' THEN 'China'
        WHEN country = 'United States' THEN 'US'
        ELSE 'Other'
    END AS region,
    -- seniority tier from position text
    CASE
        WHEN position LIKE '%phd%' OR position LIKE '%ph.d%' OR position LIKE '%doctoral%'
             OR position LIKE '%dphil%' THEN 'PhD student'
        WHEN position LIKE '%postdoc%' OR position LIKE '%post-doc%' THEN 'Postdoc'
        WHEN position LIKE '%professor%' OR position LIKE '%lecturer%' OR position LIKE '%faculty%'
             OR position LIKE '%principal investigator%' OR position LIKE '%reader%' THEN 'Faculty'
        WHEN position LIKE '%ms student%' OR position LIKE '%msc%' OR position LIKE '%master%'
             OR position LIKE '%undergrad%' OR position LIKE '%bachelor%'
             OR position LIKE '%m.s%' THEN 'Junior student (MS/UG)'
        WHEN position LIKE '%research scientist%' OR position LIKE '%engineer%'
             OR position LIKE '%principal researcher%' OR position LIKE '%intern%'
             OR position LIKE '%research fellow%' OR position LIKE '%scientist%'
             OR position LIKE '%director%' OR position LIKE '%staff%' THEN 'Industry/research staff'
        WHEN position LIKE '%researcher%' THEN 'Researcher (unspecified)'
        WHEN position = '' THEN 'Unknown'
        ELSE 'Other'
    END AS seniority
FROM tagged;

-- Paper-level region attribution. For each submission we count authors by
-- region (among those with a known domain) and assign a dominant region by
-- plurality (ties: China, then US, then Other). Also exposes first-author
-- region and any-author flags for collaboration views.
CREATE OR REPLACE VIEW conf_paper_region AS
WITH pa AS (
    SELECT venue, year, id,
        count(*) FILTER (WHERE region = 'China') AS n_cn,
        count(*) FILTER (WHERE region = 'US')    AS n_us,
        count(*) FILTER (WHERE region = 'Other') AS n_other,
        count(*) FILTER (WHERE region <> 'Unknown') AS n_known,
        count(*) AS n_authors,
        min_by(region, author_no) FILTER (WHERE region <> 'Unknown') AS first_region
    FROM conf_authors
    GROUP BY venue, year, id
)
SELECT *,
    (n_cn > 0)  AS any_china,
    (n_us > 0)  AS any_us,
    -- Attribute the paper to the region with the MOST authors. On a tie for
    -- the top count, pick fairly among the tied regions — a "coin flip" made
    -- deterministic by hashing the paper id, so it's uniform in aggregate but
    -- reproducible across runs. Handles 2- and 3-way ties.
    CASE WHEN n_known = 0 THEN 'Unknown' ELSE
        list_transform(
            list_filter(
                [{'r':'China','n':n_cn}, {'r':'US','n':n_us}, {'r':'Other','n':n_other}],
                x -> x.n = greatest(n_cn, n_us, n_other) AND x.n > 0),
            x -> x.r
        )[ CAST(hash(id) % len(list_filter(
                [{'r':'China','n':n_cn}, {'r':'US','n':n_us}, {'r':'Other','n':n_other}],
                x -> x.n = greatest(n_cn, n_us, n_other) AND x.n > 0)) AS BIGINT) + 1 ]
    END AS majority_region
FROM pa;
