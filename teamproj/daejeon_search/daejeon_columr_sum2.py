import pandas as pd

# CSV 파일 불러오기
file_path = 'daejeon_data_coulumn_sum8.csv'
df = pd.read_csv(file_path)

# 주소에서 "대전광역시 xx구 xx동" 추출
df['주소'] = df['LOTNO_ADDR'].str.extract(r'(대전광역시 \w+구 \w+동)')

# 기존 열 삭제
df = df.drop(columns='LOTNO_ADDR')

# 그룹화: 주소, COMBINED_CD, 기준년도, 사용월별 합계
aggregated_data = df.groupby(['주소', 'COMBINED_CD', 'STNDD_YR', 'USE_MM'], as_index=False).agg({
    'ELRW_USQNT': 'sum',        # 전력사용량 합계
    'CTY_GAS_USQNT': 'sum',     # 가스사용량 합계
    'ELRW_GRGS_DSAMT': 'sum',   # 전력 온실가스 배출량 합계
    'CTY_GAS_GRGS_DSAMT': 'sum' # 도시가스 온실가스 배출량 합계
})

# 열 이름 변경
aggregated_data.rename(columns={
    '주소': 'ADDR',
    'COMBINED_CD': 'ADDR_CD',
    'STNDD_YR': 'YEAR',
    'USE_MM': 'MONTH',
    'ELRW_USQNT': 'ELE',
    'CTY_GAS_USQNT': 'GAS',
    'ELRW_GRGS_DSAMT': 'ELE_DSA',
    'CTY_GAS_GRGS_DSAMT': 'GAS_DSA'
}, inplace=True)

# 결과 확인
print(aggregated_data)

# 결과를 CSV 파일로 저장
output_file = 'daejeon_data_column_group.csv'
aggregated_data.to_csv(output_file, index=False)
print(f"그룹화된 데이터가 저장되었습니다: {output_file}")