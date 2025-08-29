import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import textwrap

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
def get_top3_by_industry(industry):
    query = """
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
    WHERE r.roi_rank <= 3
      AND r.industry = %s
    ORDER BY r.roi_rank;
    """

    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn, params=(industry,))
    conn.close()
    return df

# -------------------------------
# 카드형 이미지 그리기
# -------------------------------
def plot_cards(df, industry):
    fig, axes = plt.subplots(1, len(df), figsize=(15, 5))
    if len(df) == 1:
        axes = [axes]  # ensure iterable

    for ax, (_, row) in zip(axes, df.iterrows()):
        ax.axis("off")

        # 카드에 넣을 데이터 (라벨-값 쌍)
        table_data = [
            ["드라마명", row["drama_name"]],
            ["브랜드", row["brand_name"]],
            ["PPL 타입", row["ppl_type"]],
            ["ROI", f"{row['roi_percent']}%"],
            ["산업군 평균 ROI", f"{round(row['avg_roi'],2)}%"],
        ]

        # 테이블 생성
        table = ax.table(
            cellText=table_data,
            colLabels=None,   # 라벨은 좌측에 이미 있음
            cellLoc="left",   # 셀 안 텍스트 정렬
            loc="center"
        )

        # 스타일 조정
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 1.5)  # 세로 간격 늘리기

        # 테두리/배경 색상 커스터마이즈
        for key, cell in table.get_celld().items():
            cell.set_edgecolor("black")
            cell.set_linewidth(0.5)
            if key[0] % 2 == 0:  # 짝수행 배경색
                cell.set_facecolor("#f1f8ff")
            else:
                cell.set_facecolor("#ffffff")

    plt.suptitle(f"산업군: {industry} - TOP3 PPL 캠페인", fontsize=16)
    plt.tight_layout()
    plt.show()

# -------------------------------
# 실행
# -------------------------------
industry = "F&B"  # 직접 입력 가능
df = get_top3_by_industry(industry)

if df.empty:
    print(f"'{industry}' 산업군 데이터 없음")
else:
    plot_cards(df, industry)

