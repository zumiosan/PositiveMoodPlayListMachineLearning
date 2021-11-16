#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys

import pandas as pd
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from packages.files import get_file_paths, get_directory_paths, save_csv


def concat_questionnaire_data(file_paths):
    """
    同じ種類のアンケートデータを複数受け取って結合したものを返す
    :param file_paths:
    :return: 楽曲番号と印象を結合したもの，楽曲番号と快不快度を結合したもの
    """

    data_class = None
    data_pleasure = None
    for index, file_path in enumerate(file_paths):
        if index == 0:
            data = pd.read_csv(file_path, encoding="utf-8-sig")
            data_class = data[['mid', 'class']]
            data_pleasure = data[['mid', 'pleasure']]
        else:
            tmp = pd.read_csv(file_path, encoding="utf-8-sig")
            data_class = data_class.join(tmp[['class']], rsuffix=f'_{index + 1}')
            data_pleasure = data_pleasure.join(tmp[['pleasure']], rsuffix=f'_{index + 1}')

    return data_class, data_pleasure


def get_mode(data_list):
    """
    リスト内の最頻値を求める
    :param data_list:　データの入ったリスト
    :return: 最頻値のリスト
    """

    # 最頻値とその数を求める．
    counter = Counter(data_list)
    frequency_data = counter.most_common()
    max_frequency = frequency_data[0][1]

    # 最頻値が複数ないか調べる
    modes = []
    for data in frequency_data:
        if data[1] == max_frequency:
            modes.append(data[0])
    return modes


def calc_common_impression(data_class):
    """
    共通印象を求める．基本は多数決，無理なら平均値とって四捨五入
    :param data_class: 印象に関するアンケート結果
    :return: 共通印象データ
    """

    common_data = data_class[['mid']]
    tmp_class = data_class.loc[:, "class":]
    common_class = []
    for index, row in tmp_class.iterrows():
        modes = get_mode(row)
        if len(modes) > 1:
            mean = sum(modes) / len(modes)
            common_class.append(float(Decimal(str(mean)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)))
        else:
            common_class.append(modes[0])

    common_data = common_data.copy()
    common_data['class'] = common_class

    return common_data


def calc_common_pleasure(data_pleasure):
    """
    共通快不快度を求める．得られたデータの平均をとる．
    :param data_pleasure: 快不快度に関するアンケート結果
    :return: 共通快不快度データ
    """

    common_data = data_pleasure[['mid']]
    tmp_pleasure = data_pleasure.loc[:, 'pleasure':].mean(axis=1)
    tmp_pleasure = tmp_pleasure.map(
        lambda x: float(Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)))

    common_data = common_data.copy()
    common_data['pleasure'] = tmp_pleasure

    return common_data


def main():
    # ディレクトリ名取得
    base_path = f".{os.sep}data{os.sep}questionnaire_data/"
    directory_paths = get_directory_paths(base_path)
    # print(directory_paths)

    # 共通データを作る
    common_impression_data = pd.DataFrame()
    common_pleasure_data = pd.DataFrame()
    common_data = pd.DataFrame()
    for directory_path in directory_paths:
        file_paths = get_file_paths(directory_path)
        # print(file_names)

        # ファイルを読み込んで結合する
        data_class, data_pleasure = concat_questionnaire_data(file_paths)
        # print(data_class, data_pleasure)

        # 共通印象と快不快度を求める
        data_common_class = calc_common_impression(data_class)
        data_common_pleasure = calc_common_pleasure(data_pleasure)
        # print(data_common_class)
        # print(data_common_pleasure)

        # 共通印象と共通快不快度を結合して共通データに結合する
        df_common = pd.merge(data_common_pleasure, data_common_class, on='mid')
        # print(df_common)
        common_data = pd.concat([common_data, df_common], axis=0)

        # 共通印象データと共通快不快度データに結合する
        common_impression_data = pd.concat([common_impression_data, data_common_class], axis=0)
        common_pleasure_data = pd.concat([common_pleasure_data, data_common_pleasure], axis=0)
        # print(common_impression_data, common_pleasure_data)

    # 作成したデータの保存
    save_path = f".{os.sep}data{os.sep}common_data"
    common_impression_data.sort_values('mid', inplace=True)
    save_csv(os.path.join(save_path, 'common_impression_data.csv'), common_impression_data)

    common_pleasure_data.sort_values('mid', inplace=True)
    save_csv(os.path.join(save_path, 'common_pleasure_data.csv'), common_pleasure_data)

    common_data.sort_values('mid', inplace=True)
    save_csv(os.path.join(save_path, 'common_data.csv'), common_data)


if __name__ == '__main__':
    sys.exit(main())
