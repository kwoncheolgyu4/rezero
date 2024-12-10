import pandas as pd

# 파일 경로
file_path = "./data_second/동구_인구_2021_ref.csv"

# CSV 파일 읽기
df = pd.read_csv(file_path, encoding='utf-8')

# 조건에 따라 값 변경
df.loc[(df['addr'] == "용계동") & (df['total'] == "-"), 'total'] = 0
df.loc[(df['addr'] == "용계동") & (df['households'] == "-"), 'households'] = 0

# 저장
df.to_csv(file_path, index=False, encoding='utf-8-sig')

print("Updated total and households values for addr='용계동' with '-' to 0.")