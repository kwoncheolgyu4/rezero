import pandas as pd

# 파일 경로
daejeon_file = 'daejeon_data_column_group_2022.csv'
asos_file = './data/OBS_ASOS_MNH_20241127194747.csv'

# 데이터 로드
daejeon_data = pd.read_csv(daejeon_file)
asos_data = pd.read_csv(asos_file, encoding='cp949')  # 인코딩 문제 해결

# 1. 열 이름 변경 (기존 평균 데이터 사용)
asos_data = asos_data.rename(columns={
    '평균기온(°C)': 'AVG_TEMPERATURE',
    '월합강수량(00~24h만)(mm)': 'TOTAL_RAINFALL',
    '평균상대습도(%)': 'AVG_HUMIDITY'
})

# 2. '일시'를 YEAR와 MONTH로 분리
asos_data['일시'] = pd.to_datetime(asos_data['일시'])  # 일시를 datetime 형식으로 변환
asos_data['YEAR'] = asos_data['일시'].dt.year  # 연도 추출
asos_data['MONTH'] = asos_data['일시'].dt.month  # 월 추출

# 3. 필요없는 열 제거 (필요한 열만 남기기)
asos_data = asos_data[['YEAR', 'MONTH', 'AVG_TEMPERATURE', 'TOTAL_RAINFALL', 'AVG_HUMIDITY']]

# 4. daejeon_data_column_group_2022.csv와 병합
merged_data = pd.merge(
    daejeon_data,
    asos_data,
    how='left',  # 연도와 월 기준으로 병합
    on=['YEAR', 'MONTH']
)

# 5. 결과 저장
output_file = 'daejeon_data_column_group_with_weather.csv'
merged_data.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"병합된 데이터가 저장되었습니다: {output_file}")