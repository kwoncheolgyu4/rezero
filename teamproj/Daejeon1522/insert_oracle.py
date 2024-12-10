import cx_Oracle
import pandas as pd
import os
import psycopg2

# Oracle 데이터베이스 연결 정보 설정
dsn_tns = cx_Oracle.makedsn('192.168.0.86', '1521', service_name='xe')  # 예: 'localhost', '1521', 'xe'
connection = cx_Oracle.connect(user='proj', password='proj', dsn=dsn_tns)

# CSV 파일이 들어있는 폴더 경로
folder_path = './대덕구/total'  # 예: './csv_files'

# 폴더 내 모든 CSV 파일 리스트 가져오기
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Oracle 테이블에 데이터 삽입 함수
def import_csv_to_oracle(csv_file):
    # CSV 파일 경로
    csv_path = os.path.join(folder_path, csv_file)
    print(csv_path)
    # CSV 파일 읽기 (pandas 사용)
    df = pd.read_csv(csv_path)

    # 테이블 이름과 컬럼에 맞게 아래 쿼리 작성

    # elrw_usage
    # cty_gas_usage
    # total_usage

    table_name = 'total_usage'  # Oracle 테이블 이름
    columns = ', '.join(df.columns)  # DataFrame 컬럼 이름
    placeholders = ', '.join([':{}'.format(i) for i in df.columns])  # Placeholder
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    cursor = connection.cursor()
    for row in df.itertuples(index=False, name=None):
        try:
            cursor.execute(insert_query, row)
        except psycopg2.IntegrityError as e:  # 중복된 ID가 원인일 경우
            print(f"중복된 ID: {row.ID}에서 오류 발생: {str(e)}")  # row.ID를 적절한 컬럼명으로 변경
        except Exception as e:
            print(f"오류 발생: {str(e)}, {insert_query} {row}")

    # 커밋하여 변경사항 저장
    connection.commit()
    cursor.close()
    print(f"{csv_file} 파일이 성공적으로 임포트되었습니다.")

# 모든 CSV 파일에 대해 데이터 삽입 수행
for csv_file in csv_files:
    import_csv_to_oracle(csv_file)

# 연결 종료
connection.close()

print("모든 CSV 파일이 성공적으로 Oracle 데이터베이스에 임포트되었습니다.")
