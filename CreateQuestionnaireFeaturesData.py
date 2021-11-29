#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
import pandas as pd


def main():
    # データ読み込み
    questionnaire_data = pd.read_csv('./data/common_data/common_data.csv')
    all_features_data_spotify = pd.read_csv('./data/features_data/all_features_data_spotify.csv')

    # アンケートに使用した楽曲の特徴量を取り出す．
    questionnaire_mid = questionnaire_data['mid'].values
    all_features_data_spotify = all_features_data_spotify[all_features_data_spotify['mid'].isin(questionnaire_mid)]
    # print(all_features_data_spotify)

    indexs = all_features_data_spotify['mid'].values

    for i in questionnaire_mid:
        if i not in indexs:
            print(i)


if __name__ == '__main__':
    sys.exit(main())
