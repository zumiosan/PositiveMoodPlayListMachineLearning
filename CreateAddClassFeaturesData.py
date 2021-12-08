#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
from packages.files import get_directory_paths
import pandas as pd


def create_add_class_data(all_data_impression_path, all_features_data_path, dir_path):
    """
    特徴量データに推定した楽曲の印象情報を付与する
    :param all_data_impression_path:
    :param all_features_data_path:
    :param dir_path:
    :return:
    """
    # データの読み込み
    all_features_data = pd.read_csv(all_features_data_path)
    all_data_impression = pd.read_csv(all_data_impression_path)

    # midと推定した印象だけ取得
    all_data_impression = all_data_impression.loc[:, ['mid', 'class']]

    # 結合する
    result_data = pd.merge(all_features_data, all_data_impression, on='mid')
    # print(result_data)
    result_data.to_csv(f'{dir_path}all_data_spotify_add_classes.csv', encoding='utf-8', index=False)


def main():

    all_features_data_path = './data/features_data/all_features_data_spotify.csv'

    # 共通印象の推定
    create_add_class_data(
        all_data_impression_path='./data/common_data/all_proba_data_spotify.csv',
        all_features_data_path=all_features_data_path,
        dir_path='./data/common_data/',
    )

    # 個人印象の推定
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)
    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        create_add_class_data(
            all_data_impression_path=f'{directory_path}all_proba_data_spotify.csv',
            all_features_data_path= all_features_data_path,
            dir_path=directory_path,
        )


if __name__ == '__main__':
    sys.exit(main())
