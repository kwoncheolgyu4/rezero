import pandas as pd

# CSV 파일 로드
input_file = "../daejeon_search/daejeon_data.csv"
output_file = "msr/cleaned_daejeon_data.csv"

# 데이터 읽기
df = pd.read_csv(input_file)

# LOTNO_ADDR에서 '산', '번지' 제거
df['LOTNO_ADDR'] = df['LOTNO_ADDR'].str.replace('산 ', '', regex=False)
df['LOTNO_ADDR'] = df['LOTNO_ADDR'].str.replace('번지', '', regex=False)
df['LOTNO_ADDR'] = df['LOTNO_ADDR'].str.strip()  # 불필요한 공백 제거

# 필요한 열만 선택
cleaned_data = df[['LOTNO_ADDR', 'STNDD_YR', 'USE_MM', 'ELRW_USQNT', 'CTY_GAS_USQNT']]

# 새로운 CSV로 저장
cleaned_data.to_csv(output_file, index=False)

print(f"정리된 데이터가 '{output_file}'로 저장되었습니다.")