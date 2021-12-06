#!usr/bin/python env
# -*- cording: utf-8 -*-

import os
import sys

import numpy as np
import pandas as pd
import sklearn.preprocessing as pre
from sklearn.feature_selection import SelectPercentile
from packages.files import get_directory_paths


def get_class_number(class_name):
    """
    クラス番号を返す
    :param class_name: クラスの名前
    :return: クラス番号
    """
    # クラス番号の取得
    if class_name == 'hh':
        class_num = 1
    elif class_name == 'mh':
        class_num = 2
    elif class_name == 'mm':
        class_num = 3
    elif class_name == 'ml':
        class_num = 4
    elif class_name == 'll':
        class_num = 5
    else:
        class_num = None

    return class_num


class DataProcessingImpression:
    """
    データの前処理を行うクラス
    """

    def __init__(self, file_name):
        """
        データ周りを扱うクラスのインスタンス生成
        """
        # 読み込んだデータ
        self.df = pd.read_csv(file_name)

        # midの保存
        self.mid = None
        try:
            self.mid = self.df['mid']
        except KeyError:
            pass

        # midとsidの削除
        try:
            del self.df['mid']
            del self.df['pleasure']
            del self.df['sid']
        except KeyError:
            pass

        # データのカラム
        self.columns = self.df.columns

        # 欠損値処理
        self.df.fillna(value=self.df.mean(), inplace=True)
        self.df.columns = self.columns

        # 説明変数と目的変数
        self.x = self.df.loc[:, list(set(self.columns) - {'class'})]
        self.x_columns = self.x.columns
        self.y_impression = None
        try:
            self.y_impression = self.df.loc[:, 'class']
        except KeyError:
            pass

        # 特徴選択後の説明へんす
        self.x_selected = None
        self.y_selected = None

        # 前処理のスケーラー
        self.scaler = None

    def get_target_impression_class(self, *args):
        """
        選択したクラスのデータだけ取り出す
        :param args: クラス名
        """
        # 引数を格納
        class_names = [i for i in args]
        print(class_names)

        # クラス番号取得
        for i, name in enumerate(class_names):
            class_names[i] = get_class_number(name)

        # 選択した印象のデータだけ取り出す
        self.x_selected = pd.DataFrame([self.x.loc[index, :] for index, class_num in enumerate(self.y_impression) if int(class_num) in class_names])
        self.y_selected = pd.Series([self.y_impression[index] for index, class_num in enumerate(self.y_impression) if int(class_num) in class_names], name='impression')

    def standardization(self):
        """
        データを標準化する
        :return:
        """
        self.scaler = pre.StandardScaler()
        self.scaler.fit(self.x)
        data_stand_x = self.scaler.transform(self.x)
        data_stand_x = pd.DataFrame(data_stand_x)
        self.x = data_stand_x
        self.x.columns = self.x_columns

    def discretization(self, num):
        """
        データを離散化する
        :param num: binの数
        """
        for name in self.x:
            self.x[name] = pd.cut(self.x[name], num, labels=False)

    def features_select(self):
        """
        特徴量選択を行う
        """
        selector = SelectPercentile(percentile=40)
        selector.fit(self.x, self.y_impression)
        mask = selector.get_support()
        # print(data.columns)
        # print(mask)

        # 特徴選択後のコラム
        columns = []
        for i, tf in enumerate(mask):
            if tf:
                columns.append(self.x_columns[i])

        # 特徴選択後のデータ
        self.x = pd.DataFrame(selector.transform(self.x), columns=columns)


def preprocessing_impression_data(file_path, dir_path, file_name):
    data = DataProcessingImpression(file_path)
    # print(data.df)
    # print(data.x_columns)

    # 標準化
    data.standardization()
    # print(data.x)

    # 離散化
    data.discretization(num=20)
    # print(data.x)

    # 特徴選択
    data.features_select()

    # データを保存
    df = pd.concat([data.x, data.y_impression], axis=1)
    df.to_csv(f'{dir_path + file_name}.csv', index=False, encoding='utf-8-sig')


def main():
    # 共通印象データに対する前処理
    preprocessing_impression_data(
        file_path='./data/common_data/learning_data_common.csv',
        dir_path='./data/common_data/',
        file_name='learning_data_common_impression',
    )

    # 個人印象データに対する前処理
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)
    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        preprocessing_impression_data(
            file_path=directory_path + 'learning_data_personal.csv',
            dir_path=directory_path,
            file_name='learning_data_personal_impression',
        )


if __name__ == '__main__':
    sys.exit(main())
