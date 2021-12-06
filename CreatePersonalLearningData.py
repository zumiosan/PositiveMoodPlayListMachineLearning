#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
import pandas as pd
from packages.files import save_csv, get_directory_paths
from packages.CalcPleasureClass import calc_pleasure_class


def calc_diff_mu(personal_params, common_params):
    """
    共通快不快度と個人快不快度のμの値の差を算出する
    :param personal_params:
    :param common_params:
    :return: 共通快不快度と個人快不快度の各印象クラスごとのμの値の差
    """
    diff_mu = {}
    for index, row in personal_params.iterrows():
        personal_mu = row['mu']
        common_mu = common_params.at[index, 'mu']
        diff = round(personal_mu - common_mu, 2)
        diff_mu[row['class']] = diff
    return diff_mu


def shift_common_pleasure(diff_mu, common_data, personal_data):
    """
    共通快不快度を個人快不快度のμとの差分だけ横に移動させて，個人データに結合させる．
    :param diff_mu: 共通快不快度と個人快不快度の各印象クラスごとのμの値の差
    :param common_data:
    :param personal_data:
    :return: 共通データを結合した個人データ
    """
    for index, row in common_data.iterrows():
        common_data.at[index, 'pleasure'] = row['pleasure'] + diff_mu[row['class']]
    personal_data = pd.concat([personal_data, common_data])
    personal_data.reset_index(inplace=True, drop=True)
    personal_data.sort_values('mid', inplace=True)

    return personal_data


def get_common_data_not_exist_personal(personal, common):
    """
    共通データから個人データにないものを取り出す
    :param personal:
    :param common:
    :return:　共通データから個人データにないものを抽出したもの
    """

    # 個人快不快度データに共通快不快度データを結合する．
    # 個人快不快度データになくて，共通快不快度データにあるものだけを取り出す．
    is_not_exist_mid = []
    for index, row in common.iterrows():
        if not int(row['mid']) in personal['mid'].values:
            is_not_exist_mid.append(int(row['mid']))
    common = common[common['mid'].isin(is_not_exist_mid)]

    return common

# def get_add_common_data(y_personal, y_common):
#     """
#     個人快不快度データと共通快不快度データを合わせたものを返す
#     :param y_personal:
#     :param y_common:
#     :return: 共通快不快度データを結合したデータ
#     """
#     # 平均値の差を求める．
#     # diff_median = round(y_personal['pleasure'].median() - y_common['pleasure'].median(), 2)
#     diff_mean = round(y_personal['pleasure'].mean() - y_common['pleasure'].mean(), 2)
#
#     # 共通快不快度データを平均値の差分だけ動かす
#     # y_common['pleasure'] = y_common['pleasure'] + diff_median
#     y_common['pleasure'] = y_common['pleasure'] + diff_mean
#
#     # 個人快不快度データに共通快不快度データを結合する．
#     # 個人快不快度データになくて，共通快不快度データにあるものだけを足す．
#     is_not_exist_mid = []
#     for index, row in y_common.iterrows():
#         if not row['mid'] in y_personal['mid']:
#             is_not_exist_mid.append(row['mid'])
#     y_personal = pd.concat([y_personal, y_common[y_common['mid'].isin(is_not_exist_mid)]])
#
#     return y_personal


def main():
    # ディレクトリ名取得
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)

    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        personal_data = pd.read_csv(directory_path + 'personal_all.csv')
        # print(personal_data)
        personal_params = pd.read_csv(directory_path + 'personal_params.csv')
        del personal_data['sid']

        # 共通データを読み込み
        common_data = pd.read_csv('./data/common_data/common_data.csv')
        common_params = pd.read_csv('./data/common_data/common_params.csv')

        # 特徴量データ読み込み
        features_data = pd.read_csv('./data/features_data/questionnaire_features_data.csv')

        # 個人データに個人の回答が得られていない楽曲に対する印象と快不快度を共通データから取得する
        common_data = get_common_data_not_exist_personal(personal_data, common_data)
        # print(common_data)

        # 個人快不快度の分布の平均値に合わせて共通快不快度データを移動させて結合する
        diff_mu = calc_diff_mu(personal_params, common_params)
        # print(diff_mu)
        personal_data = shift_common_pleasure(diff_mu, common_data, personal_data)

        # 閾値以上か未満かでクラス分け
        personal_data = calc_pleasure_class(personal_data, personal_params)
        # print(personal_data)

        # 特徴量データと結合させる
        learning_data = pd.merge(personal_data, features_data, on='mid')

        # csvを保存
        save_csv(directory_path + 'learning_data_personal.csv', learning_data)


if __name__ == '__main__':
    sys.exit(main())
