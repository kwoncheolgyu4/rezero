import pandas as pd

# CSV 파일 불러오기
file_path = 'daejeon_data_column_del.csv'
df = pd.read_csv(file_path)

# SGNG_CD와 STDG_CD를 합쳐 새로운 열 생성 (예: 'COMBINED_CD')
df['COMBINED_CD'] = df['SGNG_CD'].astype(str) + df['STDG_CD'].astype(str)

# 기존 열 삭제
df = df.drop(columns=['SGNG_CD', 'STDG_CD'])

# 결과를 다시 저장
output_file = 'daejeon_data_coulumn_sum.csv'
df.to_csv(output_file, index=False)

print(f"새로운 파일이 저장되었습니다: {output_file}")