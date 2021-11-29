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

    # データを保存
    all_features_data.to_csv('./data/features_data/all_features_data_spotify.csv', encoding='utf-8-sig', index=False)




if __name__ == '__main__':
    sys.exit(main())
