import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('daejeon_data_coulumn_sum8.csv')

# LOTNO_ADDR 열에서 "석봉동"이 포함된 행 찾기
cheongju_data = df[df['ROAD_NM_ADDR'].str.contains('대전광역시 서구 도솔로305번길 2', na=False)]

# # COMBINED_CD 코드로 다시 검색
# specific_combined_cd = '3023012600'  # 검색할 COMBINED_CD 값
# filtered_data = cheongju_data[cheongju_data['LOTNO_ADDR'] == specific_combined_cd]

# 결과 확인
print(cheongju_data)
