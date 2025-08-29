import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import mysql.connector
import pandas as pd

# -------------------------------
# Matplotlib 한글 폰트 설정
# -------------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False 

# -------------------------------
# DB 연결 설정
# -------------------------------
DB_CONFIG = {
    "user": "admin1",
    "password": "yosep1234",
    "host": "ppl-databse.c3mgm880ipe5.ap-northeast-2.rds.amazonaws.com",
    "port": 3306,
    "database": "PPL_Service"
}

# -------------------------------
# SQL 실행 함수
# -------------------------------
def get_ROI_group(industry):
    query = """
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
        roi_group,
        AVG(roi_percent) AS avg_roi,
        COUNT(*) AS campaign_count
    FROM (
        SELECT *,
            CASE
                WHEN roi_percentile <= 0.10 THEN '상위 10% 이내'
                WHEN roi_percentile <= 0.50 THEN '상위 50% 이내'
                WHEN roi_percentile <= 0.80 THEN '상위 80% 이내'
            END AS roi_group
        FROM ranked
        WHERE industry = %s
    ) t
    WHERE roi_group IS NOT NULL  -- 하위 20% 제외
    GROUP BY roi_group
    ORDER BY FIELD(roi_group,'상위 10% 이내','상위 50% 이내','상위 80% 이내');
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn, params=(industry,))
    conn.close()
    return df

# -------------------------------
# DB에서 ROI 데이터 가져오기
# -------------------------------
industry = "F&B"  # 예시, 프론트에서 선택
df_roi = get_ROI_group(industry)

# ROI 값과 라벨, 색상
roi_labels = df_roi['roi_group'].tolist()
roi_values = df_roi['avg_roi'].tolist()
colors = ["#93c5fd", "#86efac", "#fcd34d"]

# -------------------------------
# Pyramid 시각화
# -------------------------------
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# 전체 삼각형
top = (5, 9)
left = (1, 1)
right = (9, 1)
pyramid = Polygon([left, right, top], closed=True, edgecolor='black', facecolor='white', lw=2)
ax.add_patch(pyramid)

# 층별 좌표 계산
layer_heights = [0.2, 0.3, 0.5]  # 전체 높이를 비율로 나누기
y_bottom = 1
for i, (label, value, color) in enumerate(zip(roi_labels[::-1], roi_values[::-1], colors[::-1])):
    h = layer_heights[i]*8
    x1 = 5 - 4*(1 - (y_bottom-1)/8)
    x2 = 5 + 4*(1 - (y_bottom-1)/8)
    x3 = 5 + 4*(1 - (y_bottom+h-1)/8)
    x4 = 5 - 4*(1 - (y_bottom+h-1)/8)
    layer = Polygon([(x1,y_bottom),(x2,y_bottom),(x3,y_bottom+h),(x4,y_bottom+h)],
                    closed=True, facecolor=color, edgecolor='black')
    ax.add_patch(layer)
    ax.text(5, y_bottom+h/2, f"{label}\n{value:.1f}×", ha='center', va='center', fontsize=12, weight='bold')
    y_bottom += h

# 설명
plt.text(5, 0.5, "상위 10%: 고효율 고점\n50%: 안정 구간\n80%: 보편 성과", ha='center', va='top', fontsize=10, color='gray')

plt.show()