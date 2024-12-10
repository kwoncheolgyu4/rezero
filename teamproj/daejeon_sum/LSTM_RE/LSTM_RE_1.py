import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# 데이터 로드
data = pd.read_csv('daejeon_data_column_group.csv')

# 데이터 확인
print(data.head())

# 필요한 컬럼 선택
selected_columns = ['ADDR_CD', 'YEAR', 'MONTH', 'ELE', 'GAS']
data = data[selected_columns]

# 데이터 정렬
data = data.sort_values(by=['ADDR_CD', 'YEAR', 'MONTH'])

# 2021년까지의 데이터로 학습용 데이터 추출
train_data = data[data['YEAR'] <= 2021]

# 2022년 데이터를 테스트용 데이터로 분리
test_data = data[data['YEAR'] == 2022]

# 월별 데이터만 남기기
train_values = train_data[['ELE', 'GAS']].values
test_values = test_data[['ELE', 'GAS']].values

# 정규화 (MinMaxScaler 사용)
scaler = MinMaxScaler()
train_scaled = scaler.fit_transform(train_values)
test_scaled = scaler.transform(test_values)

# 시계열 데이터 생성 함수
def create_sequences(data, sequence_length):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i + sequence_length])
        y.append(data[i + sequence_length])
    return np.array(X), np.array(y)

# 시계열 길이 (입력으로 사용할 이전 월의 개수)
sequence_length = 12  # 12개월 (1년) 사용

# 학습 데이터 시계열 생성
X_train, y_train = create_sequences(train_scaled, sequence_length)

# 테스트 데이터 시계열 생성
X_test, y_test = create_sequences(test_scaled, sequence_length)

# LSTM 모델 설계
model = Sequential([
    LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True),
    Dropout(0.2),
    LSTM(32, return_sequences=False),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(2)  # 전기(ELE), 가스(GAS) 두 가지 예측
])

# 모델 컴파일
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 모델 요약 출력
model.summary()

# 모델 학습
history = model.fit(
    X_train, y_train,
    epochs=20,  # 반복 학습 횟수
    batch_size=32,
    validation_split=0.2,  # 학습 데이터의 20%를 검증에 사용
    verbose=1
)

# 2022년 데이터 예측
y_pred = model.predict(X_test)

# 정규화된 데이터를 원래 값으로 복원
y_test_rescaled = scaler.inverse_transform(y_test)
y_pred_rescaled = scaler.inverse_transform(y_pred)

# 결과 비교
import pandas as pd
results = pd.DataFrame({
    "실제 전기 사용량": y_test_rescaled[:, 0],
    "예측 전기 사용량": y_pred_rescaled[:, 0],
    "실제 가스 사용량": y_test_rescaled[:, 1],
    "예측 가스 사용량": y_pred_rescaled[:, 1]
})

# 결과 출력
print(results.head())

# 예측 결과를 CSV 파일로 저장
output_file = "predicted_results_2022.csv"
results.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"예측 결과가 CSV 파일로 저장되었습니다: {output_file}")

import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

# MSE와 MAE 계산
mse_ele = mean_squared_error(y_test_rescaled[:, 0], y_pred_rescaled[:, 0])
mae_ele = mean_absolute_error(y_test_rescaled[:, 0], y_pred_rescaled[:, 0])

mse_gas = mean_squared_error(y_test_rescaled[:, 1], y_pred_rescaled[:, 1])
mae_gas = mean_absolute_error(y_test_rescaled[:, 1], y_pred_rescaled[:, 1])

print(f"전기 사용량 - MSE: {mse_ele}, MAE: {mae_ele}")
print(f"가스 사용량 - MSE: {mse_gas}, MAE: {mae_gas}")

# 학습 과정 시각화
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()
