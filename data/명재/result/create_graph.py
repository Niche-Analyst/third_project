# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor

# # -------------------------------
# # 1. 데이터 불러오기
# # -------------------------------
# # 파일 경로가 사용자의 환경에 맞게 설정되어야 합니다.
# file_path = "PPL_Marketing_ROI_Analysis_English.xlsx"
# df = pd.read_excel(file_path)

# # -------------------------------
# # 1. Feature / Target Setting
# # -------------------------------
# features = [
#     "num_ppl_scenes",
#     "total_exposure_seconds",
#     "avg_viewer_rating_percent",
#     "brand_awareness_pre_percent",
#     "purchase_intent_pre_percent",
#     "production_cost_won",
#     "media_cost_won"
# ]
# target_roi = "roi_percent"
# target_sales = "sales_increase_won"

# # Fill missing values with 0.
# X = df[features].fillna(0)
# y_roi = df[target_roi].fillna(0)
# y_sales = df[target_sales].fillna(0)

# # Train/Test split
# X_train, X_test, y_roi_train, y_roi_test, y_sales_train, y_sales_test = train_test_split(
#     X, y_roi, y_sales, test_size=0.2, random_state=42
# )

# # -------------------------------
# # 2. Train RandomForest Models
# # -------------------------------
# model_roi = RandomForestRegressor(n_estimators=200, random_state=42)
# model_sales = RandomForestRegressor(n_estimators=200, random_state=42)
# model_roi.fit(X_train, y_roi_train)
# model_sales.fit(X_train, y_sales_train)

# # -------------------------------
# # 3. Graph 1: Relationship between Total Exposure Seconds and ROI
# # -------------------------------
# plt.figure(figsize=(10, 6))
# plt.scatter(df['total_exposure_seconds'], df['roi_percent'], alpha=0.6, s=50, c='b')
# plt.title('총 노출 시간(초) 대 ROI(%) 관계', fontsize=15)
# plt.xlabel('총 노출 시간 (초)', fontsize=12)
# plt.ylabel('ROI (%)', fontsize=12)
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.savefig('total_exposure_vs_roi_scatter.png')

# # -------------------------------
# # 4. Graph 2: What-if Simulation for Sales Increase
# # -------------------------------
# # Create a range for the "total_exposure_seconds" feature.
# exposure_range = np.linspace(df['total_exposure_seconds'].min(), df['total_exposure_seconds'].max(), 100)

# # Create a base DataFrame for prediction by taking the average of all other features.
# what_if_df = pd.DataFrame({
#     'num_ppl_scenes': [df['num_ppl_scenes'].mean()] * 100,
#     'total_exposure_seconds': exposure_range,
#     'avg_viewer_rating_percent': [df['avg_viewer_rating_percent'].mean()] * 100,
#     'brand_awareness_pre_percent': [df['brand_awareness_pre_percent'].mean()] * 100,
#     'purchase_intent_pre_percent': [df['purchase_intent_pre_percent'].mean()] * 100,
#     'production_cost_won': [df['production_cost_won'].mean()] * 100,
#     'media_cost_won': [df['media_cost_won'].mean()] * 100
# })

# # Use the trained model to predict sales increase for the what-if scenarios.
# predicted_sales = model_sales.predict(what_if_df)

# # Plot the what-if simulation results.
# plt.figure(figsize=(10, 6))
# plt.plot(exposure_range, predicted_sales, color='g', linewidth=3, label='예측 매출 증가')
# plt.title('총 노출 시간에 따른 매출 증가 예측 시뮬레이션', fontsize=15)
# plt.xlabel('총 노출 시간 (초)', fontsize=12)
# plt.ylabel('예측 매출 증가 (₩)', fontsize=12)
# plt.legend()
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.savefig('sales_increase_what_if.png')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import os

# -------------------------------
# 1. 프론트엔드에서 선택된 산업 정보 받기
# -------------------------------
# 이 부분을 프론트엔드에서 받은 값으로 대체하세요.
selected_industry = "자동차" 

# -------------------------------
# 2. 데이터 불러오기 및 필터링
# -------------------------------
file_path = "PPL_Marketing_ROI_Analysis_English.xlsx"
df = pd.read_excel(file_path)

# 선택된 산업에 해당하는 데이터만 필터링
df_selected_industry = df[df['industry'] == selected_industry].copy()

# 데이터가 충분한지 확인
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

    model_roi = RandomForestRegressor(n_estimators=200, random_state=42)
    model_sales = RandomForestRegressor(n_estimators=200, random_state=42)
    model_roi.fit(X_train, y_roi_train)
    model_sales.fit(X_train, y_sales_train)

    # -------------------------------
    # 4. 그래프 1: 노출 시간 대 ROI 관계 시각화
    # -------------------------------
    plt.figure(figsize=(10, 6))
    plt.scatter(df_selected_industry['total_exposure_seconds'], df_selected_industry['roi_percent'], alpha=0.6, s=50, c='b')
    plt.title(f'[{selected_industry}] 총 노출 시간(초) 대 ROI(%) 관계', fontsize=15)
    plt.xlabel('총 노출 시간 (초)', fontsize=12)
    plt.ylabel('ROI (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'{selected_industry}_roi_scatter.png')
    plt.close()

    # -------------------------------
    # 5. 그래프 2: 노출 시간에 따른 매출 증가 예측 시뮬레이션
    # -------------------------------
    exposure_range = np.linspace(df_selected_industry['total_exposure_seconds'].min(), df_selected_industry['total_exposure_seconds'].max(), 100)
    
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
    plt.show()
    plt.savefig(f'{selected_industry}_sales_what_if.png')
    plt.close()

    print(f"'{selected_industry}' 산업에 대한 두 그래프가 성공적으로 생성되었습니다.")