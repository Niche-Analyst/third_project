WITH ranked AS (
    SELECT
        industry,
        campaign_id,
        brand_name,
        drama_genre,
        drama_name,
        ppl_type,
        roi_percent,
        RANK() OVER (PARTITION BY industry ORDER BY roi_percent DESC) AS roi_rank
    FROM ppl_dummy_data
),
industry_avg AS (
    SELECT
        industry,
        AVG(roi_percent) AS avg_roi,
        MAX(roi_percent) AS max_roi,
        MIN(roi_percent) AS min_roi
    FROM ppl_dummy_data
    GROUP BY industry
)
SELECT
    r.industry,
    r.campaign_id,
    r.brand_name,
    r.drama_genre,
    r.drama_name,
    r.ppl_type,
    r.roi_percent,
    r.roi_rank,
    ia.avg_roi,
    ia.max_roi,
    ia.min_roi
FROM ranked r
JOIN industry_avg ia ON r.industry = ia.industry
WHERE r.roi_rank <= 3   -- 상위 N개 (여기서는 3개)
-- AND r.industry = "부동산" 선택한 industry 값
ORDER BY r.industry, r.roi_rank;