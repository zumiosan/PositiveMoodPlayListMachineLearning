#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys

import numpy as np
import pandas as pd
import pymc3 as pm
from packages.files import get_directory_paths, save_csv


def bayesian_inference(y):
    """
    pymc3でベイズ推定を行う
    :param y: 快不快度データ
    :return:
    """
    params = {}
    y = y['pleasure'].values
    with pm.Model() as threshold:
        mu = pm.Normal('mu', mu=0, sd=10)
        sigma = pm.HalfNormal('sigma', sd=10)
        nu = pm.DiscreteUniform('nu', lower=1, upper=10)
        t = pm.StudentT('t', nu=nu, mu=mu, sigma=sigma, observed=y)
        trace = pm.sample(3000, tune=1000, random_seed=123, chains=4, cores=4)
        params['mu'] = round(trace['mu'].mean(), 2)
        params['sigma'] = round(trace['sigma'].mean(), 2)
        params['nu'] = round(trace['nu'].mean(), 2)
    # params = {'mu': 0.56, 'sigma': 0.1, 'nu': 6.88}
    return params


def get_add_common_data(y_personal, y_common):
    """
    個人快不快度データと共通快不快度データを合わせたものを返す
    :param y_personal:
    :param y_common:
    :return: 共通快不快度データを結合したデータ
    """
    # 平均値の差を求める．
    # diff_median = round(y_personal['pleasure'].median() - y_common['pleasure'].median(), 2)
    diff_mean = round(y_personal['pleasure'].mean() - y_common['pleasure'].mean(), 2)

    # 共通快不快度データを平均値の差分だけ動かす
    # y_common['pleasure'] = y_common['pleasure'] + diff_median
    y_common['pleasure'] = y_common['pleasure'] + diff_mean

    # 個人快不快度データに共通快不快度データを結合する．
    # 個人快不快度データになくて，共通快不快度データにあるものだけを足す．
    is_not_exist_mid = []
    for index, row in y_common.iterrows():
        if not row['mid'] in y_personal['mid']:
            is_not_exist_mid.append(row['mid'])
    y_personal = pd.concat([y_personal, y_common[y_common['mid'].isin(is_not_exist_mid)]])

    return y_personal


def get_params_personal(y_personal, y_common):
    """
    ベイズ推定を行い，個人快不快度の分布のパラメータを推定する．
    :param y_personal: 個人快不快度データ
    :param y_common: 共通快不快度データ
    :return: パラメータ
    """
    # ベイズ推定ができなかった場合は共通快不快度データを足し合わせて再度行う．
    # try:
    #     params = bayesian_inference(y_personal)
    # except (RuntimeError, ValueError):
    #     params = bayesian_inference(get_add_common_data(y_personal, y_common))

    params = bayesian_inference(get_add_common_data(y_personal, y_common))

    params = pd.DataFrame([params])

    return params


def get_params_common(y_common):
    """
    ベイズ推定を行い，共通快不快度の分布のパラメータを推定する．
    :param y_common: 共通快不快度データ
    :return: パラメータ
    """
    params = bayesian_inference(y_common)
    params = pd.DataFrame([params])

    return params


def calc_threshold(params):
    """
    快不快度の閾値を算出する．
    :param params: 分布のパラメータ
    :return:　算出結果
    """
    mu_sum_sigma_list = []
    mu_sub_sigma_list = []
    threshold_list = []
    for index, row in params.iterrows():
        # mu-sigmaを求める
        mu_sub_sigma = round(row['mu'] - row['sigma'], 2)
        mu_sub_sigma_list.append(mu_sub_sigma)
        # mu+sigmaを求める
        mu_sum_sigma = round(row['mu'] - row['sigma'], 2)
        mu_sum_sigma_list.append(mu_sum_sigma)
        # muが0.5以上ならmu-sigmaを閾値，mu+sigmaを閾値にする
        if row['mu'] >= 0.5:
            threshold_list.append(mu_sub_sigma)
        else:
            threshold_list.append(mu_sum_sigma)
    params['mu-sigma'] = mu_sub_sigma_list
    params['mu+sigma'] = mu_sum_sigma_list
    params['threshold'] = threshold_list
    return params


# def calc_threshold_common(params):
#     """
#     共通快不快度の閾値を算出する．
#     :param params: 分布のパラメータ
#     :return:　算出結果
#     """
#     mu_sum_sigma_list = []
#     mu_sub_sigma_list = []
#     threshold_list = []
#     for index, row in params.iterrows():
#         # mu-sigmaを求める
#         mu_sub_sigma = round(row['mu'] - row['sigma'], 2)
#         mu_sub_sigma_list.append(mu_sub_sigma)
#         # mu+sigmaを求める
#         mu_sum_sigma = round(row['mu'] - row['sigma'], 2)
#         mu_sum_sigma_list.append(mu_sum_sigma)
#         # muが0.5以上ならmu-sigmaを閾値，mu+sigmaを閾値にする
#         if row['mu'] >= 0.5:
#             threshold_list.append(mu_sub_sigma)
#         else:
#             threshold_list.append(mu_sum_sigma)
#     params['mu-sigma'] = mu_sub_sigma_list
#     params['mu+sigma'] = mu_sum_sigma_list
#     params['threshold'] = threshold_list
#     return params
#
#
# def calc_threshold_personal(params_personal, params_common):
#     """
#     個人快不快度の閾値を算出する．
#     :param params_personal: 個人快不快度の分布のパラメータ
#     :param params_common: 共通快不快度の分布のパラメータ
#     :return: 算出結果
#     """
#     mu_sigma_list = []
#     threshold_list = []
#     for index, row in params_personal.iterrows():
#         # mu-1sigmaを求める
#         mu_sigma = round(row['mu'] - row['sigma'], 2)
#         mu_sigma_list.append(mu_sigma)
#         # muが共通快不快度のmu-sigmaより小さければ0を閾値，muが0.5以上ならmu-sigmaを閾値，それ以外はmuを閾値にする
#         tmp = params_common[params_common['class'] == row['class']]
#         if row['mu'] < float(tmp['mu-sigma']):
#             threshold_list.append(0)
#         elif row['mu'] >= 0.5:
#             threshold_list.append(mu_sigma)
#         else:
#             threshold_list.append(row['mu'])
#     params_personal['mu-sigma'] = mu_sigma_list
#     params_personal['threshold'] = threshold_list
#     return params_personal


def get_class_data(data):
    """
    各クラスごとにデータを分割したリストを返します．
    :param data: 個人，共通データ
    :return　class_data:　各クラスごとのデータが格納されたリスト
    """
    class_data = []
    for i in range(1, 6):
        class_data.append(data[data["class"] == i].reset_index(drop=True))

    return class_data


def main():
    # 共通データの読み込み
    common_data = pd.read_csv('./data/common_data/common_data.csv', encoding='utf-8-sig')
    class_data_common = get_class_data(common_data)

    # 共通快不快度の分布のパラメータを求める．
    params_common = pd.DataFrame()
    for index, y_common in enumerate(class_data_common):
        params = get_params_common(y_common)
        params['class'] = index + 1
        params_common = pd.concat([params_common, params])
    # 閾値を算出する
    params_common = calc_threshold(params_common)
    # csvに保存
    save_csv('./data/common_data/common_params.csv', params_common)

    # 個人快不快度の閾値を求める
    # ディレクトリ名取得
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)

    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        data = pd.read_csv(directory_path + 'personal_all.csv', encoding='utf-8-sig')
        del data['sid']
        # print(data)

        # 各クラスごとにデータを分割
        class_data_personal = get_class_data(data)

        # 各クラスのデータの分布のパラメータを求める
        params_personal = pd.DataFrame()
        for index, (y_personal, y_common) in enumerate(zip(class_data_personal, class_data_common)):
            params = get_params_personal(y_personal, y_common)
            params['class'] = index + 1
            params_personal = pd.concat([params_personal, params])

        # 閾値を算出する
        params_personal = calc_threshold(params_personal)
        save_csv(directory_path + 'personal_params.csv', params_personal)


if __name__ == '__main__':
    sys.exit(main())
