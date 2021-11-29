#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys

import pandas as pd
from packages.files import get_file_paths, get_directory_paths, save_csv


def concat_questionnaire_personal_data(file_paths):
    """
    個人のアンケートファイルを複数受け取って結合する．
    :param file_paths:
    :return: 楽曲番号と印象を結合したもの，楽曲番号と快不快度を結合したもの，楽曲番号と印象，快不快度を結合したもの
    """

    # 読み込みと連結
    personal_impression = pd.DataFrame()
    personal_pleasure = pd.DataFrame()
    personal_all = pd.DataFrame()
    for file_path in file_paths:
        data = pd.read_csv(file_path, encoding='utf-8-sig')
        personal_all = pd.concat([personal_all, data])
        personal_impression = pd.concat([personal_impression, data[['mid', 'class']]])
        personal_pleasure = pd.concat([personal_pleasure, data[['mid', 'pleasure']]])

    # mid順にソート
    personal_all.sort_values('mid', inplace=True)
    personal_impression.sort_values('mid', inplace=True)
    personal_pleasure.sort_values('mid', inplace=True)

    return personal_impression, personal_pleasure, personal_all


def main():
    # ディレクトリ名取得
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)

    # 個人データを作る
    for directory_path in directory_paths:
        file_paths = get_file_paths(directory_path)
        # print(file_paths)

        # ファイルを読み込んで結合する
        personal_impression, personal_pleasure, personal_all = concat_questionnaire_personal_data(file_paths)

        dir_path = f'{directory_path}/personal_data'
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        # csvに保存
        save_csv(f'{directory_path}/personal_data/personal_all.csv', personal_all)
        save_csv(f'{directory_path}/personal_data/personal_impression.csv', personal_impression)
        save_csv(f'{directory_path}/personal_data/personal_pleasure.csv', personal_pleasure)


if __name__ == '__main__':
    sys.exit(main())