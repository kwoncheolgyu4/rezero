import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('daejeon_data.csv')

# 삭제할 열 리스트
columns_to_drop = ['LOTNO_MNO', 'LOTNO_SNO', 'GPS_LOT', 'GPS_LAT', 'SUM_NRG_USQNT', 'ELRW_TOE_USQNT', 'CTY_GAS_TOE_USQNT', 'SUM_NRG_TOE_USQNT', 'SUM_GRGS_DSAMT']

# 열 삭제
df = df.drop(columns=columns_to_drop)

# 결과 확인
print(df.head())

# 필요하면 수정된 데이터를 새 CSV 파일로 저장
df.to_csv('daejeon_data_column_del.csv', index=False)