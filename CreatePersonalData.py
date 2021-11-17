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

    data_impression = pd.DataFrame()
    data_pleasure = pd.DataFrame()
    data_all = pd.DataFrame()
    for file_path in file_paths:
        data =


def main():
    # ディレクトリ名取得
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)

    # 個人データを作る
    personal_impression_data = pd.DataFrame()
    personal_pleasure_data = pd.DataFrame()
    personal_data = pd.DataFrame()
    for directory_path in directory_paths:
        file_paths = get_file_paths(directory_path)
        # print(file_paths)

        # ファイルを読み込んで結合する
        data_class, data_pleasure = concat_questionnaire_personal_data(file_paths)




if __name__ == '__main__':
    sys.exit(main())