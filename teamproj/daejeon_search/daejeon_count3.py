# import pandas as pd
#
# # CSV 파일 불러오기
# df = pd.read_csv('daejeon_data_coulumn_sum.csv')  # 'your_file.csv'는 파일 이름
#
# # LOTNO_ADDR 열에서 "청주"가 포함된 행 찾기
# cheongju_data = df[df['CTY_GAS_USQNT'].str.contains('0.0', na=False)]
#
# # 결과 확인
# print(cheongju_data)

import pandas as pd
#
# # CSV 파일 불러오기
# df = pd.read_csv('daejeon_data_coulumn_sum.csv')
#
# # CTY_GAS_USQNT 열에서 값이 0.0인 행 찾기
# cheongju_data = df[df['ELRW_USQNT'] == 0.0]
#
# # 결과 확인
# print(cheongju_data)
#
# import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('daejeon_data_coulumn_sum.csv')

# 두 열이 모두 0.0인 행 필터링
filtered_data = df[(df['COMBINED_CD'] == 3023012600)]

# LOTNO_ADDR 열에서 "석봉동"이 포함된 행 찾기

cheongju_data = filtered_data[filtered_data['LOTNO_ADDR'].str.contains('석봉동', na=False)]

# # COMBINED_CD 코드로 다시 검색
# specific_combined_cd = '3023012600'  # 검색할 COMBINED_CD 값
# filtered_data = df[df['COMBINED_CD'].str.contains('3023012600', na=False)]



# 결과 확인
print(cheongju_data)


