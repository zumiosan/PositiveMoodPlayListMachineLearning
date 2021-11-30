#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
import pandas as pd
import numpy as np
from scipy import stats
from packages.files import save_csv, get_directory_paths


def percent_point(mu, sigma, nu, percent=0.20):
    # 確率密度関数を生成
    return round(stats.t.ppf(q=percent, df=nu, loc=mu, scale=sigma), 2)


def calc_percent_point(df, percent=0.20):

    percent_points = []
    for index, row in df.iterrows():
        point = percent_point(mu=row['mu'], sigma=row['sigma'], nu=row['nu'], percent=percent)
        percent_points.append(point)
    df['20_percent_point'] = percent_points

    return df


def main():
    # 共通快不快度の分布のパラメータの読み込み
    params_common = pd.read_csv('./data/common_data/common_params.csv')

    # 左側20％点を算出する
    df = calc_percent_point(params_common, 0.20)
    save_csv('./data/common_data/common_params_percent.csv', df)

    # 個人快不快度
    # ディレクトリ名取得
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)

    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        params_personal = pd.read_csv(directory_path + 'personal_params.csv', encoding='utf-8-sig')

        # 左側20％を算出
        df = calc_percent_point(params_personal, 0.20)
        save_csv(directory_path + 'personal_params_percent.csv', df)


if __name__ == '__main__':
    sys.exit(main())
