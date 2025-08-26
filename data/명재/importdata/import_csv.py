import mysql.connector
import csv
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

TABLE_NAME = 'ad_effect_analysis'
CSV_FOLDER_PATH = r'C:\Users\Admin\Desktop\THIRD_PROJECT'  # 폴더 경로

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

def load_csv_to_mariadb(csv_file_path, db_config, table_name):
    conn = None
    cursor = None
    try:
        print(f"\n📁 파일 적재 시작: {csv_file_path}")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 현재 테이블의 실제 컬럼 목록 조회
        actual_columns = get_existing_columns(cursor, db_config["database"], table_name)

        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)

            # CSV 헤더 중 테이블에 존재하는 컬럼만 선택
            valid_columns = [col.strip() for col in header if col.strip() in actual_columns]
            invalid_columns = [col.strip() for col in header if col.strip() not in actual_columns]

            if not valid_columns:
                print(f"❌ 파일 {csv_file_path}에 유효한 컬럼이 없습니다. 건너뜀.")
                return

            if invalid_columns:
                print(f"⚠️ 테이블에 존재하지 않는 컬럼 (무시됨): {invalid_columns}")

            insert_sql = f"""
                INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in valid_columns])})
                VALUES ({', '.join(['%s'] * len(valid_columns))})
            """

            data_to_insert = []
            batch_size = 1000

            for row_num, row in enumerate(csv_reader):
                if len(row) != len(header):
                    print(f"⚠️  {row_num + 1}번째 행의 컬럼 수 불일치. 건너뜀.")
                    continue

                row_dict = dict(zip(header, row))
                processed_row = []

                for col in valid_columns:
                    val = row_dict.get(col, '').strip()
                    if col.endswith('_WTCHNG_RT'):
                        try:
                            processed_row.append(float(val) if val != '' else 0.0)
                        except ValueError:
                            print(f"⚠️  숫자 변환 실패 → 0.0 처리: {val}")
                            processed_row.append(0.0)
                    elif val == '':
                        processed_row.append(None)
                    else:
                        processed_row.append(val)

                data_to_insert.append(tuple(processed_row))

                if (row_num + 1) % batch_size == 0:
                    try:
                        cursor.executemany(insert_sql, data_to_insert)
                        conn.commit()
                        print(f"✅ {row_num + 1}개 행 커밋 완료")
                        data_to_insert = []
                    except mysql.connector.Error as err:
                        print(f"❌ 배치 삽입 오류 발생: {err}")
                        conn.rollback()
                        data_to_insert = []

            if data_to_insert:
                try:
                    cursor.executemany(insert_sql, data_to_insert)
                    conn.commit()
                    print(f"✅ 최종 {len(data_to_insert)}개 행 커밋 완료")
                except mysql.connector.Error as err:
                    print(f"❌ 최종 배치 삽입 오류 발생: {err}")
                    conn.rollback()

        print(f"🎉 파일 '{csv_file_path}' 적재 완료.")

    except FileNotFoundError:
        print(f"❌ 파일 찾을 수 없음: {csv_file_path}")
    except mysql.connector.Error as err:
        print(f"❌ DB 오류: {err}")
    except Exception as e:
        print(f"❌ 기타 오류: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def load_all_csvs_in_folder(folder_path, db_config, table_name):
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    print(f"총 {len(csv_files)}개 CSV 파일 발견됨.")

    for file_path in csv_files:
        load_csv_to_mariadb(file_path, db_config, table_name)

# --- 메인 실행 ---
if __name__ == "__main__":
    print("--- 전체 CSV 데이터 MariaDB 적재 시작 ---\n")
    load_all_csvs_in_folder(CSV_FOLDER_PATH, DB_CONFIG, TABLE_NAME)
    print("\n--- 모든 파일 처리 완료 ---")