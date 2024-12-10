import pandas as pd
import os

# 구별 시군구 코드 매핑
district_codes = {
    '동구': '30110',
    '대덕구': '30230',
    '서구': '30170',
    '유성구': '30200',
    '중구': '30140'
}

def extract_dong_and_stdg_cd(csv_dir, output_file, district_name):
    # CSV 파일 읽기
    files = os.listdir(csv_dir)
    data = []  # 데이터를 담을 리스트

    # 시군구코드를 구별로 설정
    district_code = district_codes.get(district_name)

    for file in files:
        file_path = os.path.join(csv_dir, file)

        # CSV 파일을 pandas DataFrame으로 읽기
        df = pd.read_csv(file_path, encoding='utf-8')

        # '대전광역시 ' 또는 다른 구 이름이 포함된 부분을 자동으로 찾아 제거
        df['DONG_NAME'] = df['DONG_NAME'].str.replace(r'^.*?시\s*', '', regex=True)

        # 필요한 열 추출: DONG_NAME과 STDG_CD
        df_filtered = df[['DONG_NAME', 'STDG_CD']]

        # 중복 제거: 동일한 동 이름에 대해 첫 번째 등장한 STDG_CD만 남김
        df_unique = df_filtered.drop_duplicates(subset=['DONG_NAME'])

        # 동별로 STDG_CD와 시군구코드 값을 저장
        for dong, stdg_cd in zip(df_unique['DONG_NAME'], df_unique['STDG_CD']):
            # 새로운 법정동 코드 생성: 시군구 코드 + 법정동 코드
            new_legal_dong_code = district_code + stdg_cd
            data.append([dong, new_legal_dong_code, district_code])

    # 리스트를 DataFrame으로 변환
    df_result = pd.DataFrame(data, columns=['동 이름', '법정동 코드', '시군구 코드'])

    # DataFrame을 CSV 파일로 저장
    df_result.to_csv(output_file, index=False, encoding='utf-8')
    print(f"{output_file}에 동 이름, 법정동 코드, 시군구 코드가 저장되었습니다.")

def combine_csv_from_multiple_folders(folder_paths, output_file):
    all_data = []

    # 여러 폴더의 데이터 추출
    for folder, district_name in folder_paths:
        files = os.listdir(folder)
        for file in files:
            file_path = os.path.join(folder, file)
            df = pd.read_csv(file_path, encoding='utf-8')

            # '대전광역시 ' 또는 다른 구 이름이 포함된 부분을 자동으로 찾아 제거
            df['DONG_NAME'] = df['DONG_NAME'].str.replace(r'^.*?시\s.*?\s', '', regex=True)

            # 필요한 열 추출: DONG_NAME과 STDG_CD
            df_filtered = df[['DONG_NAME', 'STDG_CD']]
            df_unique = df_filtered.drop_duplicates(subset=['DONG_NAME'])

            # 시군구코드를 구별로 설정
            district_code = district_codes.get(district_name)

            if district_code is None:
                print(f"경고: '{district_name}'에 대한 시군구코드가 매핑되지 않았습니다.")
                continue  # 해당 구는 건너뛰고 계속 처리

            # 새로운 법정동 코드 생성: 시군구 코드 + 법정동 코드
            for dong, stdg_cd in zip(df_unique['DONG_NAME'], df_unique['STDG_CD']):
                new_legal_dong_code = district_code + str(stdg_cd)  # stdg_cd를 str로 변환
                all_data.append([dong, new_legal_dong_code, district_code])

    # 전체 데이터를 하나의 DataFrame으로 변환
    df_combined = pd.DataFrame(all_data, columns=['동 이름', '법정동 코드', '시군구 코드'])

    # DataFrame을 CSV로 저장
    df_combined.to_csv(output_file, index=False, encoding='utf-8')
    print(f"모든 폴더의 데이터를 합친 {output_file}이 저장되었습니다.")


# 예시 폴더 경로와 구 이름
csv_dir_1 = [
    ("./대덕구", "대덕구"),
    ("./동구", "동구"),
    ("./서구", "서구"),
    ("./유성구", "유성구"),
    ("./중구", "중구")
]  # 여러 개의 폴더 경로와 구 이름 리스트

# 첫 번째 폴더와 두 번째 폴더들 포함하여 모든 데이터를 합쳐서 저장
combine_csv_from_multiple_folders(csv_dir_1, "./동_코드/dong.csv")
