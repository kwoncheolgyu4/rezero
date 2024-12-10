import pandas as pd

# CSV 파일 읽기
file_path = "xgboost_predicted_results_2023_recursive_by_addr.csv"
df = pd.read_csv(file_path)

# 컬럼명 변경
df.rename(columns={
    '예측 전기 사용량': 'pre_ele_usa',
    '예측 가스 사용량': 'pre_gas_usa'
}, inplace=True)

# 온실가스 배출량 계산
electricity_emission_factor = 0.415  # 전기 배출계수 (kg CO₂e/kWh)
gas_emission_factor = 0.202         # 가스 배출계수 (kg CO₂e/kWh)

# 온실가스 배출량 계산 후 톤으로 변환 및 소수점 첫 번째 자리 반올림
df['pre_ele_emi'] = ((df['pre_ele_usa'] * electricity_emission_factor) / 1000).round(1)
df['pre_gas_emi'] = ((df['pre_gas_usa'] * gas_emission_factor) / 1000).round(1)

# 컬럼 데이터 타입 확인
print("Column Data Types:")
print(df.dtypes)

# 결과 저장
output_file_path = "updated_xgboost_predicted_results_2023_recursive_by_addr.csv"
df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"Updated file saved as {output_file_path}")