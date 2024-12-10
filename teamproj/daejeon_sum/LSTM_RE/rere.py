import pandas as pd

# 데이터 로드
file_path = 'daejeon_data_column_group_2022.csv'
data = pd.read_csv(file_path)

# YEAR 열의 2019년 이전 데이터 삭제
filtered_data = data[data['YEAR'] >= 2020]

# 새로운 파일로 저장
output_file = 'daejeon_data_column_group_2022.csv'
filtered_data.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Filtered data saved to: {output_file}")