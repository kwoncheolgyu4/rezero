import os
import glob
import pandas as pd

# 작업할 폴더 경로
folder_path = "data_second"

# 모든 CSV 파일 순회
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

for file_path in csv_files:
    # CSV 파일 읽기
    df = pd.read_csv(file_path, encoding='utf-8')

    # addr 컬럼 값의 공백 제거
    if 'addr' in df.columns:
        df['addr'] = df['addr'].str.replace(" ", "", regex=False)

    # 결과 저장 (원본 파일 덮어쓰기)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')

    print(f"Processed file: {file_path}")