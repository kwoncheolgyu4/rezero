import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

# 데이터 로드
data = pd.read_csv('daejeon_data_column_group.csv')

# 필요한 컬럼 선택
selected_columns = ['ADDR_CD', 'YEAR', 'MONTH', 'ELE', 'GAS']
data = data[selected_columns]

# 데이터 정렬
data = data.sort_values(by=['ADDR_CD', 'YEAR', 'MONTH'])

# 동별로 그룹화
grouped_data = data.groupby('ADDR_CD')

# 결과 저장용
all_results = []

# 동별로 예측
for addr_cd, group in grouped_data:
    print(f"Processing: {addr_cd}")

    # 학습 데이터(2020년까지)와 테스트 데이터(2021~2022년) 분리
    train_data = group[group['YEAR'] <= 2020]
    test_data = group[group['YEAR'] > 2020]

    # 피처 생성: 이전 12개월의 데이터로 다음 달 예측
    def create_features(df):
        df = df.copy()
        for lag in range(1, 13):  # 이전 12개월
            df[f'ELE_LAG_{lag}'] = df['ELE'].shift(lag)
            df[f'GAS_LAG_{lag}'] = df['GAS'].shift(lag)
        return df

    # 학습 및 테스트 데이터에 피처 생성
    train_data = create_features(train_data).dropna()  # 결측치 제거
    test_data = create_features(test_data).dropna()  # 결측치 제거

    # 입력(X)과 출력(y) 분리
    features = [col for col in train_data.columns if 'LAG' in col]
    X_train, y_train_ele = train_data[features], train_data['ELE']
    X_train, y_train_gas = train_data[features], train_data['GAS']
    X_test, y_test_ele = test_data[features], test_data['ELE']
    X_test, y_test_gas = test_data[features], test_data['GAS']

    # 모델 학습 (전기 사용량)
    model_ele = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model_ele.fit(X_train, y_train_ele)

    # 모델 학습 (가스 사용량)
    model_gas = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model_gas.fit(X_train, y_train_gas)

    # 예측
    y_pred_ele = model_ele.predict(X_test)
    y_pred_gas = model_gas.predict(X_test)

    # 결과 저장
    results = pd.DataFrame({
        'ADDR_CD': addr_cd,
        'YEAR': test_data['YEAR'],
        'MONTH': test_data['MONTH'],
        '실제 전기 사용량': y_test_ele,
        '예측 전기 사용량': y_pred_ele,
        '실제 가스 사용량': y_test_gas,
        '예측 가스 사용량': y_pred_gas
    })
    all_results.append(results)

# 모든 동의 결과 합치기
final_results = pd.concat(all_results)

# CSV로 저장
final_results.to_csv('xgboost_predicted_results_2021_2022_by_addr2.csv', index=False, encoding='utf-8-sig')
print("동별 예측 결과가 저장되었습니다: xgboost_predicted_results_2021_2022_by_addr.csv")

# 모델 평가
mse_ele = mean_squared_error(y_test_ele, y_pred_ele)
mae_ele = mean_absolute_error(y_test_ele, y_pred_ele)
print(f"전기 사용량 - MSE: {mse_ele:.2f}, MAE: {mae_ele:.2f}")

mse_gas = mean_squared_error(y_test_gas, y_pred_gas)
mae_gas = mean_absolute_error(y_test_gas, y_pred_gas)
print(f"가스 사용량 - MSE: {mse_gas:.2f}, MAE: {mae_gas:.2f}")