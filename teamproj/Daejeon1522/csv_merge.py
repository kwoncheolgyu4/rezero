from pathlib import Path
import pandas as pd
import os
import re


def merge_files_by_dong(base_dir1, base_dir2, output_dir):
    # 첫 번째 폴더에서 파일 이름 추출
    files1 = os.listdir(base_dir1)
    files2 = os.listdir(base_dir2)

    print(files1)
    print(files2)


    # 동 이름 추출
    dong_names = set(
        [re.search(r"대전광역시 중구 (\S+)_data", f).group(1) for f in files1 if re.search(r"대전광역시 중구 (\S+)_data", f)])

    print(dong_names)

    for dong in dong_names:
        # 각 동 이름으로 파일 경로 생성
        file1 = f"대전광역시 중구 {dong}_data(15-18).csv"
        file2 = f"대전광역시 중구 {dong}_data_(19-22).csv"


        # 두 폴더에서 해당 파일 찾기
        path1 = Path(base_dir1) / file1
        path2 = Path(base_dir2) / file2

        # 경로를 항상 POSIX 스타일로 강제 적용
        path1 = path1.as_posix()
        path2 = path2.as_posix()

        # 두 파일이 존재하는지 확인
        if os.path.exists(path1) and os.path.exists(path2):
            # 파일 병합
            df1 = pd.read_csv(path1)
            df2 = pd.read_csv(path2)
            merged_df = pd.concat([df1, df2], ignore_index=True)

            # 병합 결과 저장
            output_file = os.path.join(output_dir, f"대전광역시_중구_{dong}_data(15-22).csv")
            merged_df.to_csv(output_file, index=False, encoding='utf-8')
            print(f"{dong} 병합 완료: {output_file}")
        else:
            print(f"{dong}에 대한 파일이 두 폴더 모두에 존재하지 않습니다.")


# 경로 설정
base_dir1 = "../Daejeon1518/중구"
base_dir2 = "../Daejeon1922/중구"
output_dir = "./중구"
# 결과 저장 경로가 없다면 생성
os.makedirs(output_dir, exist_ok=True)

# 병합 실행
merge_files_by_dong(base_dir1, base_dir2, output_dir)

