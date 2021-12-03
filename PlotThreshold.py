#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
import pandas as pd
import numpy as np
from scipy import stats
from packages.files import save_csv, get_directory_paths
from ClassDict import class_dict
import matplotlib.pyplot as plt
import math


def calc_threshold(mu, sigma, nu):
    # 閾値を計算
    if mu < 0.5:
        value = mu + sigma
    elif mu >= 0.5:
        value = mu - sigma
    return value


def plot_threshold(df_params, df_pleasure, path):
    # 各クラスごとに分割
    class_data = []
    for i in range(1, 6):
        class_data.append(df_pleasure[df_pleasure["class"] == i].reset_index())

    if not os.path.exists(f'{path}/figure'):
        os.mkdir(f'{path}/figure')

    # データをプロット
    for index, row in df_params.iterrows():

        # 分布の作成
        x = np.linspace(0, 1, 100)
        t_prior = stats.t(df=row['nu'], loc=row['mu'], scale=row['sigma'])
        y = t_prior.pdf(x)
        plot = class_data[int(row['class'] - 1)]['pleasure'].plot.hist(density=True)
        plot.plot(x, y, label=f"mu:{row['mu']}, sigma:{row['sigma']}, nu:{row['nu']}")
        try:
            y_index = math.floor(row['Threshold'] * 100) - 1
            plot.vlines(row['Threshold'], ymax=10, ymin=0, colors='red',
                        label=f"mu-sigma:{row['Threshold']}")
        except IndexError:
            pass
        plot.legend(loc='best')
        plot.set_xlabel('Pleasure')
        plot.set_title(f"{class_dict[int(row['class'])]}")
        plot.set_xlim([0, 1])
        plot.set_ylim([0, 8])
        plot.set_xticks(np.arange(0, 1, 0.1))
        plot.grid()
        plt.savefig(f"{path + os.sep + 'figure' + os.sep + class_dict[int(row['class'])]}_prior.png", dpi=300)
        plt.clf()


def get_threshold(df):

    thresholds = []
    for index, row in df.iterrows():
        point = calc_threshold(mu=row['mu'], sigma=row['sigma'], nu=row['nu'])
        thresholds.append(point)
    df['Threshold'] = thresholds

    return df


def main():
    # 個人快不快度
    # ディレクトリ名取得
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)

    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        params_personal = pd.read_csv(directory_path + 'personal_params.csv', encoding='utf-8-sig')
        pleasure_personal = pd.read_csv(directory_path + 'personal_all.csv', encoding='utf-8-sig')

        # 閾値算出
        df = get_threshold(params_personal)
        save_csv(directory_path + 'personal_params_percent.csv', df)

        # 閾値プロット
        plot_threshold(df, pleasure_personal, directory_path)


if __name__ == '__main__':
    sys.exit(main())
