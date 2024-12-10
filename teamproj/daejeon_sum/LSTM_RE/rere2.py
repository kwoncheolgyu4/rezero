import os
import glob
import pandas as pd

# 작업할 폴더 경로
folder_path = "./data_second"

# 모든 CSV 파일 순회
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

for file_path in csv_files:
    # CSV 파일 읽기
    df = pd.read_csv(file_path, encoding='utf-8')

    # 공백 제거
    df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)

    # 빈 행 제거
    df = df.dropna(how='all')

    # 숫자에 포함된 ',' 제거
    df = df.applymap(
        lambda x: str(x).replace(",", "") if str(x).replace(",", "").isdigit() else x
    )

    # 결과 저장 (원본 파일 덮어쓰기)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')

    print(f"Processed file: {file_path}")