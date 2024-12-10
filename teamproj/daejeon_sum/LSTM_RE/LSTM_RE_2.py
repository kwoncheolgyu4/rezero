import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

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
    train_data = group[group['YEAR'] <= 2020][['ELE', 'GAS']].values
    test_data = group[group['YEAR'] >= 2021][['ELE', 'GAS']].values

    # 데이터 비어 있는 경우 처리
    if train_data.shape[0] == 0:
        print(f"No training data for {addr_cd}. Skipping this group.")
        continue
    if test_data.shape[0] == 0:
        print(f"No test data for {addr_cd}. Skipping this group.")
        continue

    # 정규화
    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(train_data)
    test_scaled = scaler.transform(test_data)

    # 시계열 데이터 생성 함수
    def create_sequences(data, sequence_length):
        X, y = [], []
        for i in range(len(data) - sequence_length):
            X.append(data[i:i + sequence_length])
            y.append(data[i + sequence_length])
        print(f"Generated {len(X)} sequences from data of length {len(data)} with sequence_length {sequence_length}.")
        return np.array(X), np.array(y)

    sequence_length = 12  # 12개월

    # 학습 데이터 시계열 생성
    if len(train_scaled) >= sequence_length:
        X_train, y_train = create_sequences(train_scaled, sequence_length)
    else:
        print("Insufficient training data for sequence generation. Skipping this group.")
        continue

    # 테스트 데이터 시계열 생성
    if len(test_scaled) >= sequence_length:
        X_test, y_test = create_sequences(test_scaled, sequence_length)
    else:
        print("Insufficient test data for sequence generation. Skipping this group.")
        continue

    # LSTM 모델 생성 및 학습
    model = Sequential([
        LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(2)  # 전기와 가스
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # 모델 학습
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

    # 예측
    y_pred = model.predict(X_test)

    # 결과 복원
    y_test_rescaled = scaler.inverse_transform(y_test)
    y_pred_rescaled = scaler.inverse_transform(y_pred)

    # 결과 저장
    results = pd.DataFrame({
        'ADDR_CD': addr_cd,
        '실제 전기 사용량': y_test_rescaled[:, 0],
        '예측 전기 사용량': y_pred_rescaled[:, 0],
        '실제 가스 사용량': y_test_rescaled[:, 1],
        '예측 가스 사용량': y_pred_rescaled[:, 1]
    })
    all_results.append(results)

# 모든 동의 결과 합치기
final_results = pd.concat(all_results)

# CSV로 저장
final_results.to_csv('predicted_results_2021_2022_by_addr.csv', index=False, encoding='utf-8-sig')
print("동별 예측 결과가 저장되었습니다: predicted_results_2021_2022_by_addr.csv")