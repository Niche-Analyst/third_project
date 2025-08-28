WITH ranked AS (
    SELECT
        campaign_id,
        drama_name,
        brand_name,
        industry,
        roi_percent,
        PERCENT_RANK() OVER (PARTITION BY industry ORDER BY roi_percent DESC) AS roi_percentile
    FROM ppl_dummy_data
)
SELECT
    campaign_id,
    drama_name,
    brand_name,
    industry,
    roi_percent,
    CASE
        WHEN roi_percentile <= 0.10 THEN '상위 10% 이내'
        WHEN roi_percentile <= 0.50 THEN '상위 50% 이내'
        WHEN roi_percentile <= 0.80 THEN '상위 80% 이내'
        ELSE '하위 20%'
    END AS roi_group
FROM ranked
WHERE industry = 'F&B'   -- 프론트에서 선택한 industry 값
ORDER BY roi_percent DESC;