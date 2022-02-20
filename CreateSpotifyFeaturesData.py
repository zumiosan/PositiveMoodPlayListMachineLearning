#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
import pandas as pd


def main():
    # データ読み込み
    all_features_data = pd.read_csv('./data/features_data/all_features_data.csv')
    spotify_features_data = pd.read_csv('./data/features_data/spotify_features_data.csv')
    spotify_features_data = pd.merge(spotify_features_data.loc[:, "mid"], spotify_features_data.loc[:, "acousticness":"valence"], left_index=True, right_index=True)
    # print(spotify_features_data)

    # spotifyの特徴量があるものだけ取り出す．
    spotify_mid = spotify_features_data['mid'].values
    all_features_data = all_features_data[all_features_data['mid'].isin(spotify_mid)]
    # print(all_features_data)

    # spotifyの特徴量を結合
    all_features_data = pd.merge(all_features_data, spotify_features_data, on='mid')
    # print(all_features_data)

    # 前のデータにはあるのに今回のにはないものを引っ張ってくる．
    all_features_data_spotify_pre = pd.read_csv('./data/features_data/all_features_data_spotify_pre.csv')
    del all_features_data_spotify_pre['class']
    indexs = all_features_data['mid'].values
    is_not_exist_mid = []
    for i in all_features_data_spotify_pre['mid'].values:
        if i not in indexs:
            print(i)
            is_not_exist_mid.append(i)
    all_features_data_spotify_pre = all_features_data_spotify_pre[all_features_data_spotify_pre['mid'].isin(is_not_exist_mid)]
    all_features_data = pd.concat([all_features_data, all_features_data_spotify_pre]).sort_values(
        by='mid')

    # データを保存
    all_features_data.to_csv('./data/features_data/all_features_data_spotify.csv', encoding='utf-8-sig', index=False)




if __name__ == '__main__':
    sys.exit(main())
