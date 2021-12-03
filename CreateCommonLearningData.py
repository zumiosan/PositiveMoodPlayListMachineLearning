#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
import pandas as pd
from packages.files import save_csv
from packages.CalcPleasureClass import calc_pleasure_class


def main():
    # データ読み込み
    common_data = pd.read_csv('./data/common_data/common_data.csv')
    common_params = pd.read_csv('./data/common_data/common_params.csv')
    features_data = pd.read_csv('./data/features_data/questionnaire_features_data.csv')

    # 閾値以上か未満かでクラス分け
    common_data = calc_pleasure_class(common_data, common_params)
    # print(common_data)

    # 特徴量データと結合させる
    learning_data = pd.merge(common_data, features_data, on='mid')

    # csvを保存
    save_csv('./data/common_data/learning_data_common.csv', learning_data)


if __name__ == '__main__':
    sys.exit(main())
