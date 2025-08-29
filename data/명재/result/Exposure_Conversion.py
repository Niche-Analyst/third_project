import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Matplotlib 한글 폰트 설정
# -------------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False 

# -------------------------------
# 1. DB 연결 설정
# -------------------------------
DB_CONFIG = {
    "user": "lguplus6",
    "password": "lg6p@ssw0rd~!",
    "host": "localhost",
    "port": 3306,
    "database": "tv_data"
}

# -------------------------------
# 2. 실행할 SQL 쿼리
# -------------------------------
query = """
WITH ranked AS (
    SELECT
        campaign_id,
        industry,
        roi_percent,
        actual_reach,
        -- 방문자 수 = 실제 도달 인원 * 웹사이트 트래픽 증가율(%)
        ROUND(actual_reach * website_traffic_increase_percent / 100.0) AS visit_count,
        -- 구매자 수 = 실제 도달 인원 * 구매 의도(%) 
        ROUND(actual_reach * purchase_intent_post_percent / 100.0) AS purchase_count,
        PERCENT_RANK() OVER (PARTITION BY industry ORDER BY roi_percent DESC) AS roi_percentile
    FROM ppl_dummy_data
    WHERE 
        industry = 'F&B'
        AND roi_percent IS NOT NULL
)
SELECT
    CASE
        WHEN roi_percentile <= 0.10 THEN 'Top10'
        WHEN roi_percentile <= 0.50 THEN 'Top50'
        WHEN roi_percentile <= 0.80 THEN 'Top80'
    END AS roi_group,
    AVG(actual_reach) AS avg_exposure,       -- 노출 (사람 수)
    AVG(actual_reach) AS avg_interest,       -- 관심 (실제 도달 인원)
    AVG(visit_count) AS avg_visit,           -- 방문 (사람 수 변환)
    AVG(purchase_count) AS avg_purchase      -- 구매 (사람 수 변환)
FROM ranked
WHERE 
    roi_percentile <= 0.80
GROUP BY roi_group
ORDER BY FIELD(roi_group,'Top10','Top50','Top80');
"""

# -------------------------------
# 3. DB에서 데이터 가져오기
# -------------------------------
conn = mysql.connector.connect(**DB_CONFIG)
df = pd.read_sql(query, conn)
conn.close()

print("쿼리 결과:")
print(df)

# -------------------------------
# 4. ROI 그룹별 개별 차트
# -------------------------------
for idx, row in df.iterrows():
    roi_group = row["roi_group"]

    # 원하는 순서대로 리스트 정의
    metric_order = [
        ("평균 노출(Exposure)", row["avg_exposure"]),
        ("평균 관심도(Interest)", row["avg_interest"]),
        ("평균 방문(Visit)", row["avg_visit"]),
        ("평균 구매(Purchase)", row["avg_purchase"]),
    ]

    labels, values = zip(*metric_order)

    plt.figure(figsize=(8, 5))
    plt.barh(labels, values, color="skyblue")
    plt.title(f"{roi_group} 성과 지표", fontsize=14)
    plt.xlabel("평균 값", fontsize=12)
    plt.ylabel("성과 지표", fontsize=12)
    plt.gca().invert_yaxis()   # 🔥 y축 뒤집기
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()