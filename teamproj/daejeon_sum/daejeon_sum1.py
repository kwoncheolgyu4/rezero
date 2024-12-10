import pandas as pd
import os

# 데이터가 있는 폴더 경로
folder_path = "ECO310101"

# 대전광역시 데이터를 저장할 리스트
dataframes = []

# 폴더 내 파일 처리
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):  # CSV 파일만 처리
        filepath = os.path.join(folder_path, filename)

        # 파일 읽기
        df = pd.read_csv(filepath)

        # 대전광역시 데이터 필터링
        daejeon_data = df[df['LOTNO_ADDR'].str.contains("대전광역시", na=False)]

        # 리스트에 추가
        dataframes.append(daejeon_data)

# 모든 대전광역시 데이터를 하나로 병합
merged_data = pd.concat(dataframes, ignore_index=True)

# 결과를 새로운 CSV 파일로 저장
output_file = "../daejeon_search/daejeon_data.csv"
merged_data.to_csv(output_file, index=False)

print(f"대전광역시 데이터가 '{output_file}'로 저장되었습니다.")