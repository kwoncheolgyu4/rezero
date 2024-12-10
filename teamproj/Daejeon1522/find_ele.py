import pandas as pd
import re
import os

# 폴더 내 CSV 파일 목록 가져오기
folder_path = './대덕구'  # 폴더 경로
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 구별 시군구 코드 매핑
district_codes = {
    '동구': '30110',
    '대덕구': '30230',
    '서구': '30170',
    '유성구': '30200',
    '중구': '30140'
}

# 컬럼명 매핑 (한글 -> 영어)
column_mapping = {
    '지번주소': 'LOTNO_ADDR',
    '도로명주소': 'ROAD_NM_ADDR',
    '시군구코드': 'SGNG_CD',
    '법정동코드': 'STDG_CD',
    '지번본번': 'LOTNO_MNO',
    '지번부번': 'LOTNO_SNO',
    'GPS경도': 'GPS_LOT',
    'GPS위도': 'GPS_LAT',
    '기준년도': 'STNDD_YR',
    '사용월': 'USE_MM',
    '전력사용량': 'ELRW_USQNT',
    '도시가스사용량': 'CTY_GAS_USQNT',
    '합계에너지사용량': 'SUM_NRG_USQNT',
    '전력TOE사용량': 'ELRW_TOE_USQNT',
    '도시가스TOE사용량': 'CTY_GAS_TOE_USQNT',
    '합계에너지TOE사용량': 'SUM_NRG_TOE_USQNT',
    '전력온실가스배출량': 'ELRW_GRGS_DSAMT',
    '도시가스온실가스배출량': 'CTY_GAS_GRGS_DSAMT',
    '합계온실가스배출량': 'SUM_GRGS_DSAMT'
}

# 법정동 코드 생성 함수
def create_legal_dong_code(row, district_code):
    stdg_cd = str(row['STDG_CD'])  # 법정동 코드
    legal_dong_code = district_code + stdg_cd  # 시군구코드 + 법정동코드
    return legal_dong_code

# CSV 파일을 처리하는 함수
def process_csv(file_path, district_name, save_path):
    # 시군구코드를 구별로 설정
    district_code = district_codes.get(district_name)

    if district_code is None:
        print(f"경고: '{district_name}'에 대한 시군구코드가 매핑되지 않았습니다.")
        return

    # CSV 파일 읽기
    data = pd.read_csv(file_path)

    # 법정동 코드 + 지번 주소 번지 + 도로명 주소 번지 + 산 여부 + 년월일 형식으로 locationId 생성
    def extract_location_id(row):
        # 1. 법정동 코드
        legal_dong_code = create_legal_dong_code(row, district_code)  # 법정동 코드 생성

        # 2. 지번 주소에서 모든 숫자 추출
        lotno_address = row['LOTNO_ADDR']  # 예시: '대전광역시 대덕구 갈전동 540번지'
        lotno_numbers = re.findall(r'\d+-?\d*', lotno_address)  # 숫자와 하이픈 포함
        lotno_number = ''.join(lotno_numbers) if lotno_numbers else '0'

        # 3. 도로명 주소에서 모든 숫자 추출
        road_address = row['ROAD_NM_ADDR']  # 예시: '대덕로 540번지', '대덕로 540-1번지'
        road_numbers = re.findall(r'\d+-?\d*', road_address)  # 숫자와 하이픈 포함
        road_number = ''.join(road_numbers) if road_numbers else '0'

        # 4. 산 여부 확인
        is_mountain = 'M' if '산' in lotno_address else ''

        # 5. 년월일
        year_month = str(row['STNDD_YR']) + str(row['USE_MM']).zfill(2)  # 예: 201501

        # 6. locationId 생성
        location_id = legal_dong_code + lotno_number + road_number + is_mountain + year_month
        return location_id

    # locationId 생성하여 새로운 컬럼에 추가
    data['locationId'] = data.apply(extract_location_id, axis=1)

    # STDG_CD를 시군구 코드 + 법정동 코드로 합치기
    data['STDG_CD'] = data.apply(lambda row: create_legal_dong_code(row, district_code), axis=1)

    # 중복된 locationId에 대해 번호를 1부터 시작하여 생성 (cumcount를 1부터 시작하게 함)
    data['location_id_count'] = data.groupby('locationId').cumcount() + 1  # _1부터 시작하도록 수정

    # locationId에 번호를 추가하여 고유한 location_id 생성
    data['location_id'] = data['locationId'] + "-" + data['location_id_count'].astype(str)

    # 필요한 컬럼만 추출 (DB에 맞는 형식으로 컬럼명 변경)
    result = data[['location_id', 'ELRW_USQNT', 'ELRW_TOE_USQNT', 'ELRW_GRGS_DSAMT']]

    # 슬라이스된 result에서 NaN을 0으로 설정할 때, .loc를 사용
    result.loc[:, 'ELRW_USQNT'] = result['ELRW_USQNT'].fillna(0)
    result.loc[:, 'ELRW_TOE_USQNT'] = result['ELRW_TOE_USQNT'].fillna(0)
    result.loc[:, 'ELRW_GRGS_DSAMT'] = result['ELRW_GRGS_DSAMT'].fillna(0)

    result.columns = ['location_id', 'elrw_usqnt', 'elrw_toe_usqnt', 'elrw_grgs_dsamt']

    # 결과를 새로운 CSV 파일로 저장 (저장 경로 포함)
    output_file = os.path.join(save_path, csv_file.split('.')[0] + '_ele.csv')
    result.to_csv(output_file, index=False)
    print(f'{output_file} 저장 완료')

# 저장 경로 지정
save_path = './대덕구/ele'

# 모든 CSV 파일에 대해 처리
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    district_name = csv_file.split('_')[1]  # 파일명에서 구 이름 추출
    process_csv(file_path, district_name, save_path)
