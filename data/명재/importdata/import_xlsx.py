import mysql.connector
import pandas as pd
import sys
import os
import glob

DB_CONFIG = {
    "user": "lguplus6",
    "password": "lg6p@ssw0rd~!",
    "host": "localhost",
    "port": 3306,
    "database": "tv_data"
}

TABLE_NAME = 'ppl_dummy_data'
XLSX_FOLDER_PATH = r'C:\Users\Admin\Desktop\THIRD_PROJECT'  # 폴더 경로

def get_existing_columns(cursor, db_name, table_name):
    """
    해당 테이블의 실제 컬럼 목록을 가져옴
    """
    query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
    """
    cursor.execute(query, (db_name, table_name))
    return set(row[0] for row in cursor.fetchall())

def load_xlsx_to_mariadb(xlsx_file_path, db_config, table_name):
    conn = None
    cursor = None
    try:
        print(f"\n📁 파일 적재 시작: {xlsx_file_path}")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 현재 테이블의 실제 컬럼 목록 조회
        actual_columns = get_existing_columns(cursor, db_config["database"], table_name)

        # Excel 읽기
        df = pd.read_excel(xlsx_file_path)

        # 컬럼 필터링 (DB에 존재하는 컬럼만)
        valid_columns = [col for col in df.columns if col in actual_columns]
        invalid_columns = [col for col in df.columns if col not in actual_columns]

        if not valid_columns:
            print(f"❌ 파일 {xlsx_file_path}에 유효한 컬럼이 없습니다. 건너뜀.")
            return

        if invalid_columns:
            print(f"⚠️ 테이블에 존재하지 않는 컬럼 (무시됨): {invalid_columns}")

        df = df[valid_columns]  # DB 컬럼과 맞는 컬럼만 사용

        # NaN → None 변환
        df = df.where(pd.notnull(df), None)

        insert_sql = f"""
            INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in valid_columns])})
            VALUES ({', '.join(['%s'] * len(valid_columns))})
        """

        data_to_insert = [tuple(row) for row in df.to_numpy()]

        # executemany 사용
        cursor.executemany(insert_sql, data_to_insert)
        conn.commit()

        print(f"✅ {len(data_to_insert)}개 행 삽입 완료")

    except FileNotFoundError:
        print(f"❌ 파일 찾을 수 없음: {xlsx_file_path}")
    except mysql.connector.Error as err:
        print(f"❌ DB 오류: {err}")
    except Exception as e:
        print(f"❌ 기타 오류: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def load_all_xlsx_in_folder(folder_path, db_config, table_name):
    xlsx_files = glob.glob(os.path.join(folder_path, "*.xlsx"))
    print(f"총 {len(xlsx_files)}개 XLSX 파일 발견됨.")

    for file_path in xlsx_files:
        load_xlsx_to_mariadb(file_path, db_config, table_name)

# --- 메인 실행 ---
if __name__ == "__main__":
    print("--- 전체 XLSX 데이터 MariaDB 적재 시작 ---\n")
    load_all_xlsx_in_folder(XLSX_FOLDER_PATH, DB_CONFIG, TABLE_NAME)
    print("\n--- 모든 파일 처리 완료 ---")
