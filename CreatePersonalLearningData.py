#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
import pandas as pd
from packages.files import save_csv, get_directory_paths, get_file_paths
from packages.CalcPleasureClass import calc_pleasure_class


def main():
    # ディレクトリ名取得
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)

    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        personal_data = pd.read_csv(directory_path + 'personal_all.csv')
        personal_params = pd.read_csv(directory_path + 'personal_params.csv')
        features_data = pd.read_csv('./data/features_data/questionnaire_features_data.csv')
        learning_data_common = pd.read_csv('./data/common_data/learning_data_common.csv')
        del personal_data['sid']

        # 閾値以上か未満かでクラス分け
        personal_data = calc_pleasure_class(personal_data, personal_params)
        # print(personal_data)

        # 特徴量データと結合させる
        learning_data = pd.merge(personal_data, features_data, on='mid')

        # csvを保存
        save_csv(directory_path + 'learning_data_personal.csv', learning_data)


if __name__ == '__main__':
    sys.exit(main())
