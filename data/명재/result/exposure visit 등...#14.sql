WITH ranked AS (
    SELECT
        campaign_id,
        industry,
        roi_percent,
        actual_reach,
        online_search_increase_percent,
        website_traffic_increase_percent,
        sales_increase_won,
        PERCENT_RANK() OVER (PARTITION BY industry ORDER BY roi_percent DESC) AS roi_percentile
    FROM ppl_dummy_data
    WHERE 
        industry = 'F&B'  -- 선택한 industry 값
        AND roi_percent IS NOT NULL
)
SELECT
    CASE
        WHEN roi_percentile <= 0.10 THEN 'Top10'
        WHEN roi_percentile <= 0.50 THEN 'Top50'
        WHEN roi_percentile <= 0.80 THEN 'Top80'
    END AS roi_group,
    AVG(actual_reach) AS avg_exposure,
    AVG(online_search_increase_percent) AS avg_interest,
    AVG(website_traffic_increase_percent) AS avg_visit,
    AVG(sales_increase_won) AS avg_purchase
FROM ranked
WHERE 
    roi_percentile <= 0.80
GROUP BY roi_group
ORDER BY FIELD(roi_group,'Top10','Top50','Top80');