import os
import pandas as pd
import warnings

# 경고 숨기기
warnings.simplefilter("ignore", UserWarning)

# bil_data 폴더 설정
base_folder = "대전_건축이력"
output_folder = os.path.join(base_folder, "combined_outputs")
os.makedirs(output_folder, exist_ok=True)  # 결과 저장 폴더 생성

# 대상 열
target_columns = ["대지위치", "건축면적(㎡)", "주구조", "용도", "지붕구조", "사용승인일자"]

# 폴더 탐색
for folder in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder)
    if os.path.isdir(folder_path):  # 폴더인지 확인
        district_output_folder = os.path.join(output_folder, folder)  # 구별 폴더 생성
        os.makedirs(district_output_folder, exist_ok=True)

        combined_data = []  # 구별 데이터를 저장할 리스트

        for file in os.listdir(folder_path):
            if file.endswith(".xlsx"):  # .xlsx 파일만 처리
                file_path = os.path.join(folder_path, file)
                print(f"처리 중: {file_path}")

                try:
                    # Excel 파일 읽기
                    df = pd.read_excel(file_path, sheet_name="상세현황", usecols=target_columns)

                    # 열 이름 변경
                    df.rename(columns={"건축면적(㎡)": "건축면적"}, inplace=True)

                    # '건축면적'이 숫자로 처리될 수 있도록 변환
                    df["건축면적"] = pd.to_numeric(df["건축면적"], errors="coerce")
                    combined_data.append(df)
                except Exception as e:
                    print(f"에러 발생: {file_path} - {e}")

        # 구별 데이터프레임 합치기
        if combined_data:
            combined_df = pd.concat(combined_data, ignore_index=True)

            # '대지위치' 기준으로 그룹화 및 합산
            grouped_df = (
                combined_df.groupby("대지위치", as_index=False)
                .agg({
                    "건축면적": "sum",  # 건축면적 합산
                    "주구조": "first",  # 나머지 컬럼은 첫 번째 값 사용
                    "용도": "first",
                    "지붕구조": "first",
                    "사용승인일자": "first",
                })
            )

            # 결과를 구별 폴더에 CSV로 저장
            output_file = os.path.join(district_output_folder, f"{folder}_combined.csv")
            grouped_df.to_csv(output_file, index=False, encoding="utf-8-sig")
            print(f"결과 저장 완료: {output_file}")