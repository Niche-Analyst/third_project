import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Matplotlib 한글 폰트 설정
# -------------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False 

# # -------------------------------
# # 1. DB 연결 설정
# # -------------------------------
# DB_CONFIG = {
#     "user": "lguplus6",
#     "password": "lg6p@ssw0rd~!",
#     "host": "localhost",
#     "port": 3306,
#     "database": "tv_data"
# }

# # -------------------------------
# # 2. 실행할 SQL 쿼리
# # -------------------------------
# query = """
# WITH ranked AS (
#     SELECT
#         campaign_id,
#         industry,
#         roi_percent,
#         actual_reach,
#         online_search_increase_percent,
#         website_traffic_increase_percent,
#         sales_increase_won,
#         PERCENT_RANK() OVER (PARTITION BY industry ORDER BY roi_percent DESC) AS roi_percentile
#     FROM ppl_dummy_data
#     WHERE 
#         industry = 'F&B'
#         AND roi_percent IS NOT NULL
# )
# SELECT
#     CASE
#         WHEN roi_percentile <= 0.10 THEN 'Top10'
#         WHEN roi_percentile <= 0.50 THEN 'Top50'
#         WHEN roi_percentile <= 0.80 THEN 'Top80'
#     END AS roi_group,
#     AVG(actual_reach) AS avg_exposure,
#     AVG(online_search_increase_percent) AS avg_interest,
#     AVG(website_traffic_increase_percent) AS avg_visit,
#     AVG(sales_increase_won) AS avg_purchase
# FROM ranked
# WHERE 
#     roi_percentile <= 0.80
# GROUP BY roi_group
# ORDER BY FIELD(roi_group,'Top10','Top50','Top80');
# """

# # -------------------------------
# # 3. DB에서 데이터 가져오기
# # -------------------------------
# conn = mysql.connector.connect(**DB_CONFIG)
# df = pd.read_sql(query, conn)
# conn.close()

# print("쿼리 결과:")
# print(df)

# # -------------------------------
# # 4. 가로형 bar 차트 그리기
# # -------------------------------
# # index: roi_group, values: 평균 지표들
# df.set_index("roi_group", inplace=True)

# ax = df.plot(kind="barh", figsize=(10, 6))

# plt.title("F&B 산업군 ROI 그룹별 성과 지표", fontsize=14)
# plt.xlabel("평균 값", fontsize=12)
# plt.ylabel("ROI 그룹", fontsize=12)
# plt.legend(
#     title="성과 지표",
#     loc="best"
# )
# plt.grid(axis="x", linestyle="--", alpha=0.7)

# plt.tight_layout()
# plt.show()


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
    metrics = {
        "평균 노출(Exposure)": row["avg_exposure"],
        "평균 관심도(Interest)": row["avg_interest"],
        "평균 방문(Visit)": row["avg_visit"],
        "평균 구매(Purchase)": row["avg_purchase"],
    }

    plt.figure(figsize=(8, 5))
    plt.barh(list(metrics.keys()), list(metrics.values()), color="skyblue")
    plt.title(f"{roi_group} 성과 지표", fontsize=14)
    plt.xlabel("평균 값", fontsize=12)
    plt.ylabel("성과 지표", fontsize=12)
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    # 차트 표시
    plt.tight_layout()
    plt.show()