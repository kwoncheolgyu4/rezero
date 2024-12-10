import pandas as pd

# CSV 파일 불러오기
file_path = 'daejeon_data_coulumn_sum8.csv'
df = pd.read_csv(file_path)

# 조건에 맞는 데이터를 필터링하여 COMBINED_CD 값을 변경
condition = (df['LOTNO_ADDR'].str.contains('대전광역시 중구 문창동', na=False)) & (df['COMBINED_CD'] == 3014011100)
df.loc[condition, 'COMBINED_CD'] = 3014010500

# 변경된 데이터 확인
print(df[condition])

# 변경된 데이터를 새로운 CSV 파일로 저장
output_file = 'daejeon_data_coulumn_sum8.csv'
df.to_csv(output_file, index=False)
print(f"데이터가 성공적으로 변경되고 저장되었습니다: {output_file}")