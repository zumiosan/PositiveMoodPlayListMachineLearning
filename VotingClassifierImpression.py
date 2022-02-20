#!usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import sys

import pickle
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from packages.files import get_directory_paths
from DataProcessingImpression import DataProcessingImpression
import pandas as pd


def create_voting_classifier(file_path, dir_path):
    """
    2クラスで印象分類を行うVotingClassifierを10種類生成する
    """
    class_list = [['hh', 'mh'], ['hh', 'mm'], ['hh', 'lm'], ['hh', 'll'],
                  ['mh', 'mm'], ['mh', 'lm'], ['mh', 'll'],
                  ['mm', 'lm'], ['mm', 'll'],
                  ['lm', 'll'], ]

    for class_name in class_list:
        # class_name = ['hh', 'mm']
        # 学習データ読み込み
        data = DataProcessingImpression(file_path)
        # print(len(data.df.columns))
        class_name1, class_name2 = class_name[0], class_name[1]
        # データを指定したクラスのデータにする
        data.get_target_impression_class(class_name1, class_name2)

        # print(data.x_selected, data.y_selected)

        # モデルを生成
        model1 = GaussianNB()
        model2 = KNeighborsClassifier()
        model3 = RandomForestClassifier()
        models = [('gnb', model1), ('knc', model2), ('rfc', model3)]
        vote = VotingClassifier(estimators=models, voting='soft')

        # 学習
        vote.fit(data.x_selected, data.y_selected)

        # モデルの保存
        model_dir_path = f'{dir_path}/models'
        if not os.path.isdir(model_dir_path):
            os.makedirs(model_dir_path)
        with open(f'{model_dir_path}/voting_model_impression_{class_name1}_{class_name2}.pickle', mode='wb') as fp:
            pickle.dump(vote, fp)


def main():
    # 共通印象分類器の作成
    create_voting_classifier(
        file_path='./data/common_data/learning_data_common_impression.csv',
        dir_path='./data/common_data/',
    )

    # 個人印象分類器の作成
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)
    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        create_voting_classifier(
            file_path=directory_path + 'learning_data_personal_impression.csv',
            dir_path=directory_path,
        )


if __name__ == '__main__':
    sys.exit(main())
