import os
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# 현재 실행 파일의 경로를 기준으로 데이터 폴더 설정
base_folder = os.getcwd()  # 현재 실행 중인 폴더
output_folder = os.path.join(base_folder, "predicted_results")
os.makedirs(output_folder, exist_ok=True)

# 구별 데이터 처리
districts = ['서구', '중구', '동구', '유성구', '대덕구']

for district in districts:
    district_path = os.path.join(base_folder, district)  # 각 구의 폴더
    if not os.path.exists(district_path):
        print(f"{district_path} 경로가 없습니다. 건너뜁니다.")
        continue

    # 구별 결과 저장 폴더 생성
    district_output_folder = os.path.join(output_folder, district)
    os.makedirs(district_output_folder, exist_ok=True)

    for file in os.listdir(district_path):
        if file.endswith(".csv"):
            file_path = os.path.join(district_path, file)

            # 데이터 로드
            df = pd.read_csv(file_path)

            # 필요한 컬럼 확인
            required_columns = {'STNDD_YR', 'USE_MM', 'ELRW_USQNT', 'CTY_GAS_USQNT'}
            if not required_columns.issubset(df.columns):
                print(f"{file_path}에 필요한 컬럼이 없습니다. 건너뜁니다.")
                continue

            # 'YYYY-MM' 컬럼 생성 (USE_MM이 숫자일 경우 변환)
            df['YYYY-MM'] = df['STNDD_YR'].astype(str) + '-' + df['USE_MM'].astype(str).str.zfill(2)

            # 2021년까지 데이터 필터링
            df = df[df['STNDD_YR'] <= 2021]

            # 전력 사용량 데이터
            df_elrw = df.rename(columns={"YYYY-MM": "ds", "ELRW_USQNT": "y"})[['ds', 'y']]
            df_elrw['ds'] = pd.to_datetime(df_elrw['ds'])

            # Prophet 학습
            model_elrw = Prophet()
            model_elrw.fit(df_elrw)

            # 2022년과 2023년 예측
            future_elrw = model_elrw.make_future_dataframe(periods=24, freq='MS')  # 24개월 예측
            forecast_elrw = model_elrw.predict(future_elrw)

            # 2022년부터 2023년까지 데이터 필터링
            forecast_elrw_filtered = forecast_elrw[(forecast_elrw['ds'] >= '2022-01-01') & (forecast_elrw['ds'] <= '2023-12-31')]

            # 결과 저장
            elrw_output_file = f"{district_output_folder}/{file.replace('.csv', '_elrw_forecast_2022_2023.csv')}"
            forecast_elrw_filtered[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(elrw_output_file, index=False, encoding='utf-8-sig')

            print(f"{file} 전력 사용량 예측 완료 (2022-2023): {elrw_output_file}")