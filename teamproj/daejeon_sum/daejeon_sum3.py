import pandas as pd

# 원본 CSV 파일 경로
input_file = "msr/processed_approval_del.csv"

# 결과를 저장할 새로운 파일 경로
output_file = "msr/processed_approval_del2.csv"

# 데이터 읽기
df = pd.read_csv(input_file)

# 사용승인일자 컬럼 제거
df = df.drop(columns=['지붕구조'])

# 결과 저장
df.to_csv(output_file, index=False)

print(f"사용승인일자가 제거된 데이터가 '{output_file}'에 저장되었습니다.")