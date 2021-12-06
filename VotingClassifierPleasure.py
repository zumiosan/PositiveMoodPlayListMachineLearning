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
from DataProcessingPleasure import DataProcessingPleasure
import pandas as pd


def create_voting_classifier(file_path, dir_path, class_name):
    """
    2クラスで快不快分類を行うVotingClassifierを10種類生成する
    """

    # 学習データ読み込み
    data = DataProcessingPleasure(file_path)
    # print(data.x, data.y_pleasure)

    # モデルを生成
    model1 = GaussianNB()
    model2 = KNeighborsClassifier()
    model3 = RandomForestClassifier()
    models = [('gnb', model1), ('knc', model2), ('rfc', model3)]
    vote = VotingClassifier(estimators=models, voting='soft')

    # 学習
    vote.fit(data.x, data.y_pleasure)

    # モデルの保存
    model_dir_path = f'{dir_path}/models'
    if not os.path.isdir(model_dir_path):
        os.makedirs(model_dir_path)
    with open(f'{model_dir_path}/voring_model_pleasure_{class_name}.pickle', mode='wb') as fp:
        pickle.dump(vote, fp)


def main():
    class_list = ['hh', 'mh', 'mm', 'lm', 'll']
    for class_name in class_list:
        # 共通印象データに対する前処理
        create_voting_classifier(
            file_path=f'./data/common_data/learning_data_common_pleasure_{class_name}.csv',
            dir_path='./data/common_data/',
            class_name=class_name
        )

    # 個人印象データに対する前処理
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)
    for directory_path in directory_paths:
        directory_path = f'{directory_path}/personal_data/'
        for class_name in class_list:
            # 個人データ読み込み
            create_voting_classifier(
                file_path=directory_path + f'learning_data_personal_pleasure_{class_name}.csv',
                dir_path=directory_path,
                class_name=class_name
            )


if __name__ == '__main__':
    sys.exit(main())
