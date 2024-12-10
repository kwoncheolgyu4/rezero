import pandas as pd
import numpy as np
from xgboost import XGBRegressor

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

    # 학습 데이터(2021~2022)
    train_data = group[group['YEAR'] <= 2022]

    # 피처 생성: 이전 12개월 데이터를 활용
    def create_features(df):
        df = df.copy()
        for lag in range(1, 13):  # 이전 12개월
            df[f'ELE_LAG_{lag}'] = df['ELE'].shift(lag)
            df[f'GAS_LAG_{lag}'] = df['GAS'].shift(lag)
        return df

    # 학습 데이터에 피처 생성
    train_data = create_features(train_data).dropna()

    # 입력(X)과 출력(y) 분리
    features = [col for col in train_data.columns if 'LAG' in col]
    X_train, y_train_ele = train_data[features], train_data['ELE']
    X_train, y_train_gas = train_data[features], train_data['GAS']

    # 모델 학습 (전기 사용량)
    model_ele = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model_ele.fit(X_train, y_train_ele)

    # 모델 학습 (가스 사용량)
    model_gas = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model_gas.fit(X_train, y_train_gas)

    # 2022년 마지막 데이터를 기반으로 2023년 예측
    last_data = train_data.iloc[-1][features].values.reshape(1, -1)

    # 2023년 데이터 예측
    predictions = []
    for month in range(1, 13):  # 2023년 1월 ~ 12월
        # 전기 및 가스 사용량 예측
        pred_ele = model_ele.predict(last_data)[0]
        pred_gas = model_gas.predict(last_data)[0]

        # 예측 결과 저장
        predictions.append({'ADDR_CD': addr_cd, 'YEAR': 2023, 'MONTH': month,
                            '예측 전기 사용량': pred_ele, '예측 가스 사용량': pred_gas})

        # 다음 달 입력 데이터 업데이트
        next_row = last_data.flatten().tolist()  # 현재 입력 데이터
        next_row = next_row[2:]  # 가장 오래된 lag 데이터 제거
        next_row.extend([pred_ele, pred_gas])  # 새로운 예측값 추가
        last_data = np.array(next_row).reshape(1, -1)

    # 결과 저장
    results = pd.DataFrame(predictions)
    all_results.append(results)

# 모든 동의 결과 합치기
final_results = pd.concat(all_results)

# CSV로 저장
final_results.to_csv('xgboost_predicted_results_2023_recursive_by_addr.csv', index=False, encoding='utf-8-sig')
print("동별 예측 결과가 저장되었습니다: xgboost_predicted_results_2023_recursive_by_addr.csv")