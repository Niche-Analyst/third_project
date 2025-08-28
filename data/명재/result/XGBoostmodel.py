import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor  # ✅ XGBoost 추가
import os

# -------------------------------
# Matplotlib 한글 폰트 설정
# -------------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False 

# -------------------------------
# 1. 프론트엔드에서 선택된 산업 정보 받기
# -------------------------------
selected_industry = "여행/레저" 
clean_industry_name = selected_industry.replace('/', '_').replace(' ', '_')

# -------------------------------
# 2. 데이터 불러오기 및 필터링
# -------------------------------
file_path = "PPL_Marketing_ROI_Analysis_English.xlsx"
df = pd.read_excel(file_path)

df_selected_industry = df[df['industry'] == selected_industry].copy()

if len(df_selected_industry) < 20:
    print(f"오류: '{selected_industry}' 산업에 대한 데이터가 부족하여 분석을 진행할 수 없습니다.")
else:
    # -------------------------------
    # 3. 피처 / 타깃 설정 및 모델 학습
    # -------------------------------
    features = [
        "num_ppl_scenes", "total_exposure_seconds", "avg_viewer_rating_percent",
        "brand_awareness_pre_percent", "purchase_intent_pre_percent",
        "production_cost_won", "media_cost_won"
    ]
    target_roi = "roi_percent"
    target_sales = "sales_increase_won"

    X = df_selected_industry[features].fillna(0)
    y_roi = df_selected_industry[target_roi].fillna(0)
    y_sales = df_selected_industry[target_sales].fillna(0)

    X_train, X_test, y_roi_train, y_roi_test, y_sales_train, y_sales_test = train_test_split(
        X, y_roi, y_sales, test_size=0.2, random_state=42
    )

    # ✅ RandomForest → XGBoost 교체
    model_roi = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )
    model_sales = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )

    model_roi.fit(X_train, y_roi_train)
    model_sales.fit(X_train, y_sales_train)

    # -------------------------------
    # 5. 그래프 2: 노출 시간에 따른 매출 증가 예측 시뮬레이션
    # -------------------------------
    exposure_range = np.linspace(
        df_selected_industry['total_exposure_seconds'].min(),
        df_selected_industry['total_exposure_seconds'].max(),
        100
    )
    
    what_if_df = pd.DataFrame({
        'num_ppl_scenes': [df_selected_industry['num_ppl_scenes'].mean()] * 100,
        'total_exposure_seconds': exposure_range,
        'avg_viewer_rating_percent': [df_selected_industry['avg_viewer_rating_percent'].mean()] * 100,
        'brand_awareness_pre_percent': [df_selected_industry['brand_awareness_pre_percent'].mean()] * 100,
        'purchase_intent_pre_percent': [df_selected_industry['purchase_intent_pre_percent'].mean()] * 100,
        'production_cost_won': [df_selected_industry['production_cost_won'].mean()] * 100,
        'media_cost_won': [df_selected_industry['media_cost_won'].mean()] * 100
    })

    predicted_sales = model_sales.predict(what_if_df)

    plt.figure(figsize=(10, 6))
    plt.plot(exposure_range, predicted_sales, color='g', linewidth=3, label='예측 매출 증가')
    plt.title(f'[{selected_industry}] 총 노출 시간에 따른 매출 증가 예측', fontsize=15)
    plt.xlabel('총 노출 시간 (초)', fontsize=12)
    plt.ylabel('예측 매출 증가 (₩)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    # ✅ 그래프를 PNG 파일로 저장
    output_dir = "graphs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{clean_industry_name}_sales_prediction.png")
    plt.savefig(output_path, dpi=300)  # 고해상도 저장
    print(f"그래프가 저장되었습니다 → {output_path}")

    plt.show()
    plt.close()