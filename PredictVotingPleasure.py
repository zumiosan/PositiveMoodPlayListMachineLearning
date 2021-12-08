#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from packages.files import get_directory_paths
from DataProcessingPleasure import DataProcessingPleasure
import pickle
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


class_list = ['hh', 'mh', 'mm', 'lm', 'll']


class VotingClassifierPleasure:
    """
    投票形式でクラスを予測するクラスです．
    """
    def __init__(self, dir_path):
        """
        インスタンスを生成する
        :param : dir_path: モデルやデータが保存されているディレクトリのパス
        """
        # ディレクトリのパス
        self.dir_path = dir_path

        # モデルを格納
        self.models = get_models(self.dir_path)

        # 予測結果を格納したlist
        self.pred_results = []

        # プレイリスト作成用に全ての予測結果の確率を格納したlist
        self.all_proba_results = []

        # midと快確率が格納されたデータ
        self.result_data = None

    def predict(self, x_test, class_num):
        """
        快不快度分類機を使って予測する
        :param class_num:
        :param x_test: テストデータ
        """

        #  快確率を求めていく
        model = self.models[int(class_num)]
        column_names = model.feature_names_in_
        x_test = x_test[column_names]
        pred_proba = model.predict_proba(x_test)
        pleasure = round(pred_proba[0][1], 2)
        self.pred_results.append(pleasure)
        # classes = model.classes_
        # print(classes)

    def create_proba_data(self, mid):
        columns = ['mid', 'pleasure']
        self.pred_results = pd.DataFrame(self.pred_results)
        # print(self.proba_results)
        data = pd.concat([mid, self.pred_results], axis=1)
        data.columns = columns
        self.result_data = data

        self.result_data.to_csv(f'{self.dir_path}all_pleasure_data_spotify.csv', encoding='utf-8', index=False)


def get_models(dir_path):
    """
    保存されているモデルを取得する
    :param dir_path: モデルが保存されているディレクトリのpath
    :return: 保存されているモデルが格納されたdict
    """
    # モデルを取得する
    models = {}
    for class_name in class_list:
        path = f'{dir_path}/models/voting_model_pleasure_{class_name}.pickle'
        with open(path, mode='rb') as fp:
            model = pickle.load(fp)
            models[get_class_num(class_name)] = model

    return models


def get_class_num(class_name):
    if class_name == 'hh':
        return 1
    elif class_name == 'mh':
        return 2
    elif class_name == 'mm':
        return 3
    elif class_name == 'lm':
        return 4
    elif class_name == 'll':
        return 5


def predict_pleasure(all_data_impression_path, dir_path):
    # テストデータの読み込み
    all_data = DataProcessingPleasure(all_data_impression_path)
    all_data.standardization()
    all_data.discretization(num=20)

    # インスタンス生成
    models = VotingClassifierPleasure(dir_path)

    # 予測
    columns = all_data.x.columns
    # print(columns)
    for index, line in all_data.x.iterrows():
        print(index)
        array = line.to_numpy()
        # print(array.shape[0])
        array = array.reshape(1, array.shape[0])
        x_test = pd.DataFrame(array, columns=columns)
        models.predict(x_test, all_data.y_impression[index])

    # 予測結果の快確率とmidを結合
    models.create_proba_data(all_data.mid)


def main():

    # 共通印象の推定
    # predict_pleasure(
    #     all_data_impression_path='./data/common_data/all_data_spotify_add_classes.csv',
    #     dir_path='./data/common_data/',
    # )

    # 個人印象の推定
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)
    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        predict_pleasure(
            all_data_impression_path=f'{directory_path}all_data_spotify_add_classes.csv',
            dir_path=directory_path,
        )


if __name__ == '__main__':
    sys.exit(main())
