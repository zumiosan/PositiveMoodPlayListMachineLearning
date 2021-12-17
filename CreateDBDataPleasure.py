#!usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import sys

from packages.files import get_directory_paths
import pandas as pd


def main():

    result_data = pd.DataFrame()

    # DBに入れる共通印象データを作成
    common_pleasure_data = pd.read_csv('./data/common_data/all_pleasure_data_spotify.csv')
    common_pleasure_data['username'] = 'common'
    result_data = pd.concat([result_data, common_pleasure_data])
    # print(result_data)
    # print(common_pleasure_data)

    # DBに入れる個人印象データを作成
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)
    directory_names = [i.split('/')[-1] for i in directory_paths]
    user_info = pd.read_csv('./data/db_data/user_info.csv')
    for directory_path, directory_name in zip(directory_paths, directory_names):
        # print(directory_path, directory_name)
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        personal_pleasure_data = pd.read_csv(f'{directory_path}all_pleasure_data_spotify.csv')
        username = user_info[user_info['name'] == directory_name]['username'].values
        personal_pleasure_data['username'] = username[0]
        result_data = pd.concat([result_data, personal_pleasure_data])
        # print(personal_pleasure_data)
    # print(result_data)
    result_data['mid'] = result_data['mid'].astype('int')
    result_data.to_csv('./data/db_data/pleasure_info.csv', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    sys.exit(main())
