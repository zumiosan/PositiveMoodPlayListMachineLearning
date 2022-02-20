#!usr/bin/env python
# -*- cording: utf-8 -*-


import os
import sys

from DataProcessingPleasure import DataProcessingPleasure
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
from packages.files import get_directory_paths
import numpy as np
import pandas as pd

class_list = ['hh', 'mh', 'mm', 'lm', 'll']


def tow_class_cross_validation(file_path, class_name, cv):

    # データ読み込み
    data = DataProcessingPleasure(file_path)

    # モデルを生成
    model1 = GaussianNB()
    model4 = KNeighborsClassifier()
    model5 = RandomForestClassifier(random_state=None)
    models = [('gnb', model1), ('knc', model4), ('rfc', model5)]
    vote = VotingClassifier(estimators=models, voting='soft')
    # 交差検証
    scores = cross_val_score(vote, data.x, data.y_pleasure, cv=cv)
    # 分類機の名前
    print(f'voting_classifier_{class_name}')
    # 各分割におけるスコア
    print('Cross-Validation scores: {}'.format(scores))
    # スコアの平均値
    print('Average score: {}'.format(np.mean(scores)))

    # csv変換用データに入れる
    # print(type(scores.tolist()[0]))
    scores = scores.tolist()
    scores.append(np.mean(scores))
    scores = [round(i, 2) for i in scores]
    scores.insert(0, f'{class_name}')
    return scores
    data_list.append(scores)


def save_csv(dir_path, data_list, cv):
    # csv用のデータ
    columns = list(range(1, cv + 1))
    columns.insert(0, "分類器")
    columns.append('平均')
    data_list = pd.DataFrame(data_list, columns=columns)
    data_list.to_csv(f'{dir_path}cross_validation_result_pleasure.csv', index=False, encoding='utf-8')


def main():

    cv = 4

    # 共通印象の推定
    data_list = []
    dir_path = './data/common_data/'
    for class_name in class_list:
        scores = tow_class_cross_validation(
            file_path=f'./data/common_data/learning_data_common_pleasure_{class_name}.csv',
            cv=cv,
            class_name=class_name
        )
        data_list.append(scores)

    save_csv(
        data_list=data_list,
        cv=cv,
        dir_path=dir_path
    )

    # 個人印象の推定
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)
    for directory_path in directory_paths:
        data_list = []
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        for class_name in class_list:
            scores = tow_class_cross_validation(
                file_path=f'{directory_path}learning_data_personal_pleasure_{class_name}.csv',
                cv=cv,
                class_name=class_name
            )
            data_list.append(scores)

        save_csv(
            data_list=data_list,
            cv=cv,
            dir_path=directory_path
        )


if __name__ == '__main__':
    sys.exit(main())
