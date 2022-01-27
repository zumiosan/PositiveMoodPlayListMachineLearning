#!usr/bin/env python
# -*- cording: utf-8 -*-
import pprint
import sys

import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor

impressions = ['hh', 'mh', 'mm', 'lm', 'll']

pleasure_level = 0.8

impression_level = 0.8

class_name_to_num = {
    'hh': 1,
    'mh': 2,
    'mm': 3,
    'lm': 4,
    'll': 5,
}

class_num_to_name = {
    1: 'hh',
    2: 'mh',
    3: 'mm',
    4: 'lm',
    5: 'll',
}


def get_connection():
    return psycopg2.connect(
        dsn='postgres://postgres:pos.pos..pos@localhost:5432/positive_mood_playlist',
        cursor_factory=DictCursor
    )


def execute_query(query):
    """
    クエリの実行
    :return: 実行結果
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = []
            for row in cur:
                rows.append(dict(row))
    return rows


def get_impression_data(class_name, class_num, impression_username, pleasure_username):

    query = f"WITH table1 AS (SELECT * FROM impression_info WHERE username='{impression_username}')," \
            f"table2 AS (SELECT * FROM pleasure_info WHERE username='{pleasure_username}')," \
            f"table3 AS (SELECT * FROM table1 INNER JOIN table2 ON table1.mid = table2.mid) "\
            "SELECT count(*) FROM table3 " \
            f"WHERE class_num={class_num} AND {class_name} >= {impression_level}"
    data = execute_query(query)
    return data


def get_impression_pleasure_data(class_name, class_num, impression_username, pleasure_username):

    query = f"WITH table1 AS (SELECT * FROM impression_info WHERE username='{impression_username}')," \
            f"table2 AS (SELECT * FROM pleasure_info WHERE username='{pleasure_username}')," \
            f"table3 AS (SELECT * FROM table1 INNER JOIN table2 ON table1.mid = table2.mid) "\
            "SELECT count(*) FROM table3 " \
            f"WHERE class_num={class_num} AND {class_name} >= {impression_level} AND pleasure >= {pleasure_level} "
    data = execute_query(query)
    return data


def get_impression_data_no_class_num(class_name, impression_username, pleasure_username):
    query = f"WITH table1 AS (SELECT * FROM impression_info WHERE username='{impression_username}')," \
            f"table2 AS (SELECT * FROM pleasure_info WHERE username='{pleasure_username}')," \
            f"table3 AS (SELECT * FROM table1 INNER JOIN table2 ON table1.mid = table2.mid) " \
            "SELECT count(*) FROM table3 " \
            f"WHERE {class_name} >= {impression_level}"
    data = execute_query(query)
    return data


def main():
    impression_result_data = []
    common_pleasure_result_data = []
    personal_pleasure_result_data = []
    for i in range(1, 15):
        tmp_impression_result_data = [f'pmp_user{i}']
        tmp_common_pleasure_result_data = [f'pmp_user{i}']
        tmp_personal_pleasure_result_data = [f'pmp_user{i}']
        for class_name in impressions:
            # print(f'pmp_user{i}', class_name)
            data_impression = get_impression_data(class_name, class_name_to_num[class_name], f'pmp_user{i}', f'pmp_user{i}')
            data_common = get_impression_pleasure_data(class_name, class_name_to_num[class_name], f'pmp_user{i}', 'common')
            data_personal = get_impression_pleasure_data(class_name, class_name_to_num[class_name], f'pmp_user{i}', f'pmp_user{i}')
            # print(data_impression[0]['count'], data_personal[0]['count'], data_common[0]['count'])
            tmp_impression_result_data.append(data_impression[0]['count'])
            tmp_common_pleasure_result_data.append(data_common[0]['count'])
            tmp_personal_pleasure_result_data.append(data_personal[0]['count'])
        impression_result_data.append(tmp_impression_result_data)
        common_pleasure_result_data.append(tmp_common_pleasure_result_data)
        personal_pleasure_result_data.append(tmp_personal_pleasure_result_data)

    impression_columns = ['username'] + [f'{i}_{impression_level}' for i in impressions]
    pleasure_columns = ['username'] + [f'{i}_{pleasure_level}' for i in impressions]
    impression_result_data = pd.DataFrame(impression_result_data, columns=impression_columns)
    common_pleasure_result_data = pd.DataFrame(common_pleasure_result_data, columns=pleasure_columns)
    personal_pleasure_result_data = pd.DataFrame(personal_pleasure_result_data, columns=pleasure_columns)
    impression_result_data.to_csv(f'./data/db_analys/track_num_i_{impression_level}.csv', encoding='utf-8-sig', index=False)
    common_pleasure_result_data.to_csv(f'./data/db_analys/track_num_i_{impression_level}_cp_{pleasure_level}.csv', encoding='utf-8-sig', index=False)
    personal_pleasure_result_data.to_csv(f'./data/db_analys/track_num_i_{impression_level}_pp_{pleasure_level}.csv', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    sys.exit(main())
