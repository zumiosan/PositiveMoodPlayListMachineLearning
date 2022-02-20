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
    # # print(all_features_data_spotify)

    # 前のデータにはあるのに今回のにはないものを引っ張ってくる．
    all_features_data_spotify_pre = pd.read_csv('./data/features_data/all_features_data_spotify_pre.csv')
    del all_features_data_spotify_pre['class']
    indexs = all_features_data_spotify['mid'].values
    is_not_exist_mid = []
    for i in questionnaire_mid:
        if i not in indexs:
            print(i)
            is_not_exist_mid.append(i)
    all_features_data_spotify_pre = all_features_data_spotify_pre[all_features_data_spotify_pre['mid'].isin(is_not_exist_mid)]
    all_features_data_spotify = pd.concat([all_features_data_spotify, all_features_data_spotify_pre]).sort_values(by='mid')
    print(all_features_data_spotify)
    all_features_data_spotify.to_csv('./data/features_data/questionnaire_features_data.csv', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    sys.exit(main())
