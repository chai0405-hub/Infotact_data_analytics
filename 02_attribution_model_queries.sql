-- 02_attribution_model_queries.sql
-- Project: Multi-Touch Marketing Attribution and ROI Dashboard
-- Author: Chaitanya Pawar
-- Purpose: SQL logic for customer journey ranking, attribution modeling, and KPI calculation.

-- NOTE:
-- This SQL is written in a standard style and can be adapted for PostgreSQL, MySQL 8+, SQLite, BigQuery, or Snowflake.
-- Assumed main table name: fact_touchpoints
-- If your table has another name, replace fact_touchpoints with that table name.

-----------------------------------------------------------------------
-- 1. View all touchpoints with journey ranking
-----------------------------------------------------------------------

SELECT
    event_id,
    user_id,
    journey_id,
    session_id,
    event_timestamp_utc,
    event_date,
    channel,
    channel_group,
    campaign,
    funnel_stage,
    event_type,
    ad_spend,
    is_conversion,
    conversion_value,

    ROW_NUMBER() OVER (
        PARTITION BY journey_id
        ORDER BY event_timestamp_utc
    ) AS first_touch_rank,

    ROW_NUMBER() OVER (
        PARTITION BY journey_id
        ORDER BY event_timestamp_utc DESC
    ) AS last_touch_rank,

    COUNT(*) OVER (
        PARTITION BY journey_id
    ) AS total_touchpoints

FROM fact_touchpoints;


-----------------------------------------------------------------------
-- 2. Identify converted journeys
-----------------------------------------------------------------------

SELECT DISTINCT
    journey_id
FROM fact_touchpoints
WHERE is_conversion = 1;


-----------------------------------------------------------------------
-- 3. First-Touch Attribution
-- The first channel in the converted journey gets full conversion credit.
-----------------------------------------------------------------------

WITH ranked_touchpoints AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY journey_id
            ORDER BY event_timestamp_utc
        ) AS first_touch_rank
    FROM fact_touchpoints
    WHERE journey_id IN (
        SELECT DISTINCT journey_id
        FROM fact_touchpoints
        WHERE is_conversion = 1
    )
),
journey_revenue AS (
    SELECT
        journey_id,
        MAX(conversion_value) AS journey_revenue
    FROM fact_touchpoints
    GROUP BY journey_id
)

SELECT
    'First-Touch' AS attribution_model,
    r.journey_id,
    r.channel,
    r.campaign,
    1 AS attributed_conversions,
    j.journey_revenue AS attributed_revenue
FROM ranked_touchpoints r
JOIN journey_revenue j
    ON r.journey_id = j.journey_id
WHERE r.first_touch_rank = 1;


-----------------------------------------------------------------------
-- 4. Last-Touch Attribution
-- The last channel in the converted journey gets full conversion credit.
-----------------------------------------------------------------------

WITH ranked_touchpoints AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY journey_id
            ORDER BY event_timestamp_utc DESC
        ) AS last_touch_rank
    FROM fact_touchpoints
    WHERE journey_id IN (
        SELECT DISTINCT journey_id
        FROM fact_touchpoints
        WHERE is_conversion = 1
    )
),
journey_revenue AS (
    SELECT
        journey_id,
        MAX(conversion_value) AS journey_revenue
    FROM fact_touchpoints
    GROUP BY journey_id
)

SELECT
    'Last-Touch' AS attribution_model,
    r.journey_id,
    r.channel,
    r.campaign,
    1 AS attributed_conversions,
    j.journey_revenue AS attributed_revenue
FROM ranked_touchpoints r
JOIN journey_revenue j
    ON r.journey_id = j.journey_id
WHERE r.last_touch_rank = 1;


-----------------------------------------------------------------------
-- 5. Linear Attribution
-- All touchpoints in a converted journey share conversion and revenue equally.
-----------------------------------------------------------------------

WITH converted_touchpoints AS (
    SELECT
        *
    FROM fact_touchpoints
    WHERE journey_id IN (
        SELECT DISTINCT journey_id
        FROM fact_touchpoints
        WHERE is_conversion = 1
    )
),
touchpoint_counts AS (
    SELECT
        journey_id,
        COUNT(*) AS total_touchpoints
    FROM converted_touchpoints
    GROUP BY journey_id
),
journey_revenue AS (
    SELECT
        journey_id,
        MAX(conversion_value) AS journey_revenue
    FROM fact_touchpoints
    GROUP BY journey_id
)

SELECT
    'Linear' AS attribution_model,
    c.journey_id,
    c.channel,
    c.campaign,
    1.0 / t.total_touchpoints AS attributed_conversions,
    j.journey_revenue / t.total_touchpoints AS attributed_revenue
FROM converted_touchpoints c
JOIN touchpoint_counts t
    ON c.journey_id = t.journey_id
JOIN journey_revenue j
    ON c.journey_id = j.journey_id;


-----------------------------------------------------------------------
-- 6. Channel-level spend summary
-----------------------------------------------------------------------

SELECT
    channel,
    SUM(ad_spend) AS total_spend
FROM fact_touchpoints
GROUP BY channel;


-----------------------------------------------------------------------
-- 7. Final KPI summary by attribution model and channel
-- This query assumes attribution_output table/view is already created
-- from First-Touch, Last-Touch, and Linear attribution results.
-----------------------------------------------------------------------

SELECT
    a.attribution_model,
    a.channel,
    SUM(a.attributed_conversions) AS attributed_conversions,
    SUM(a.attributed_revenue) AS attributed_revenue,
    s.total_spend,

    CASE
        WHEN s.total_spend = 0 THEN 0
        ELSE SUM(a.attributed_revenue) / s.total_spend
    END AS roas,

    CASE
        WHEN SUM(a.attributed_conversions) = 0 THEN 0
        ELSE s.total_spend / SUM(a.attributed_conversions)
    END AS cac

FROM attribution_output a
JOIN (
    SELECT
        channel,
        SUM(ad_spend) AS total_spend
    FROM fact_touchpoints
    GROUP BY channel
) s
    ON a.channel = s.channel

GROUP BY
    a.attribution_model,
    a.channel,
    s.total_spend

ORDER BY
    a.attribution_model,
    roas DESC;
