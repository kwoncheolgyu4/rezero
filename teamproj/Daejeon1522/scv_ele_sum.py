import os
import pandas as pd

# 폴더 경로 설정
districts = ['서구', '동구', '중구', '대덕구', '유성구']

# 출력 폴더 설정
output_folder = "processed_data"
os.makedirs(output_folder, exist_ok=True)

# 데이터 처리
for district in districts:
    district_path = os.path.join(district)  # 각 구의 폴더
    if not os.path.exists(district_path):
        print(f"{district_path} 경로가 없습니다. 건너뜁니다.")
        continue

    # 폴더 내의 모든 CSV 파일 처리
    for file in os.listdir(district_path):
        if file.endswith(".csv"):
            file_path = os.path.join(district_path, file)

            # 데이터 읽기
            df = pd.read_csv(file_path)

            # 필요한 컬럼 확인
            required_columns = {'STNDD_YR', 'USE_MM', 'ELRW_USQNT', 'CTY_GAS_USQNT'}
            if not required_columns.issubset(df.columns):
                print(f"{file_path}에 필요한 컬럼이 없습니다. 건너뜁니다.")
                continue

            # 'YYYY-MM' 컬럼 생성
            df['YYYY-MM'] = df['STNDD_YR'].astype(str) + '-' + df['USE_MM'].astype(str).str.zfill(2)

            # 전력 사용량 데이터 처리
            elrw_df = df.groupby('YYYY-MM')['ELRW_USQNT'].sum().reset_index()
            elrw_output_file = f"{district}_{file.replace('.csv', '_elrw_processed.csv')}"
            elrw_output_path = os.path.join(output_folder, elrw_output_file)
            elrw_df.to_csv(elrw_output_path, index=False, encoding='utf-8-sig')
            print(f"{elrw_output_path} 저장 완료.")

            # 도시가스 사용량 데이터 처리
            cty_gas_df = df.groupby('YYYY-MM')['CTY_GAS_USQNT'].sum().reset_index()
            cty_gas_output_file = f"{district}_{file.replace('.csv', '_cty_gas_processed.csv')}"
            cty_gas_output_path = os.path.join(output_folder, cty_gas_output_file)
            cty_gas_df.to_csv(cty_gas_output_path, index=False, encoding='utf-8-sig')
            print(f"{cty_gas_output_path} 저장 완료.")