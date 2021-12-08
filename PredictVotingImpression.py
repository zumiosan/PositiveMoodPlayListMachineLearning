#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from packages.files import get_directory_paths
from DataProcessingImpression import DataProcessingImpression
import pickle
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


class_list = [['hh', 'mh'], ['hh', 'mm'], ['hh', 'ml'], ['hh', 'll'],
              ['mh', 'mm'], ['mh', 'ml'], ['mh', 'll'],
              ['mm', 'ml'], ['mm', 'll'],
              ['ml', 'll'], ]


class VotingClassifierImpression:
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

        # モデルの学習に使ったデータの列の順番
        self.columns_orders = get_columns_order(self.models)

        # 予測結果を格納したlist
        self.pred_results = []

        # 各クラスの確率の合計
        self.proba_hh = 0
        self.proba_mh = 0
        self.proba_mm = 0
        self.proba_ml = 0
        self.proba_ll = 0

        # プレイリスト作成用に全ての予測結果の確率を格納したlist
        self.all_proba_results = []

        # midと印象確率が格納されたデータ
        self.result_data = None

    def predict(self, x_test):
        """
        複数の分類機を使って予測する
        :param x_test: テストデータ
        """
        # 各クラスの確率の合計値の初期化
        self.proba_hh = 0
        self.proba_mh = 0
        self.proba_mm = 0
        self.proba_ml = 0
        self.proba_ll = 0

        # 確率の合計を求めていく
        for model, column_names in zip(self.models, self.columns_orders):
            classes = model.classes_
            x_test = x_test[column_names]
            pred_proba = model.predict_proba(x_test)
            self.sum_proba(classes, pred_proba[0])

        # 各確率の平均をとって一番大きかったものを予測結果とする
        self.__get_results()

        # print('_______')

    def sum_proba(self, classes, pred_proba):
        """
        確率の合計を求める.
        :param classes: クラスが格納されたlist
        :param pred_proba: 各クラスの確率が格納されたlist
        """
        # 各クラスの確率を足していく
        for class_, proba in zip(classes, pred_proba):
            # print(class_, proba)
            if class_ == 1:
                self.proba_hh += proba
            elif class_ == 2:
                self.proba_mh += proba
            elif class_ == 3:
                self.proba_mm += proba
            elif class_ == 4:
                self.proba_ml += proba
            elif class_ == 5:
                self.proba_ll += proba
            else:
                pass
        # print('~~~~~~~~~~')

    def __get_results(self):
        """
        確率の平均と結果を求める
        """

        # 各確率の平均をとる
        probabilities = [self.proba_hh, self.proba_mh, self.proba_mm, self.proba_ml, self.proba_ll]
        results = []
        for i, proba in enumerate(probabilities):
            try:
                ave = proba / 4
            except ZeroDivisionError:
                ave = 0.0

            results.append(ave)
        # self.proba_results.append(results)

        results = [round(i, 2) for i in results]
        # print(results)

        self.all_proba_results.append(results)

        # 確率の平均が一番大きかったものを予測結果とする
        result_class = results.index(max(results)) + 1
        self.pred_results.append(result_class)

    def create_proba_data(self, mid):
        """
        midと各印象の印象確率，主要な印象を結合したデータを作成して保存する
        :param mid:
        :return:
        """
        columns = ['mid', 'hh', 'mh', 'mm', 'lm', 'll', 'class']
        self.all_proba_results = pd.DataFrame(self.all_proba_results)
        self.pred_results = pd.DataFrame(self.pred_results)
        # print(self.proba_results)
        data = pd.concat([mid, self.all_proba_results, self.pred_results], axis=1)
        data.columns = columns
        self.result_data = data

        self.result_data.to_csv(f'{self.dir_path}all_proba_data_spotify.csv', encoding='utf-8', index=False)

    # def add_class_num(self):


def get_models(dir_path):
    """
    保存されているモデルを取得する
    :param dir_path: モデルが保存されているディレクトリのpath
    :return: 保存されているモデルが格納されたlist
    """
    # モデルを取得する
    models = []
    for class_name in class_list:
        class_name1, class_name2 = class_name[0], class_name[1]
        path = f'{dir_path}/models/voting_model_impression_{class_name1}_{class_name2}.pickle'
        with open(path, mode='rb') as fp:
            model = pickle.load(fp)
            models.append(model)

    return models


def get_columns_order(models):
    """
    モデルの学習の際に使用した列名を取得する．
    :param models:
    :return:
    """
    columns_orders = []
    for model in models:
        columns_order = model.feature_names_in_
        columns_orders.append(columns_order)
    return columns_orders


def predict_impression_class(all_data_path, dir_path):
    # テストデータの読み込み
    all_data = DataProcessingImpression(all_data_path)
    all_data.standardization()
    all_data.discretization(num=20)

    # インスタンス生成
    models = VotingClassifierImpression(dir_path)

    # 予測
    columns = all_data.x.columns
    # print(columns)
    for index, line in all_data.x.iterrows():
        print(index)
        array = line.to_numpy()
        # print(array.shape[0])
        array = array.reshape(1, array.shape[0])
        x_test = pd.DataFrame(array, columns=columns)
        models.predict(x_test)

    # 予測結果の確率とmidを結合
    models.create_proba_data(all_data.mid)


def main():

    # 全楽曲の特徴量データのパス
    all_data_path = './data/features_data/all_features_data_spotify.csv'

    # 共通印象の推定
    predict_impression_class(
        all_data_path=all_data_path,
        dir_path='./data/common_data/',
    )

    # 個人印象の推定
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)
    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        predict_impression_class(
            all_data_path=all_data_path,
            dir_path=directory_path,
        )


if __name__ == '__main__':
    sys.exit(main())
