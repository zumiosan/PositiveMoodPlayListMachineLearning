#!usr/bin/env python
# -*- cording: utf-8 -*-


import os
import sys

from DataProcessingImpression import DataProcessingImpression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
from packages.files import get_directory_paths
import numpy as np
import pandas as pd

class_list = [['hh', 'mh'], ['hh', 'mm'], ['hh', 'lm'], ['hh', 'll'],
              ['mh', 'mm'], ['mh', 'lm'], ['mh', 'll'],
              ['mm', 'lm'], ['mm', 'll'],
              ['lm', 'll'], ]


def tow_class_average_cross_validation(file_name, cv=4):
    # データの読み込み
    data = DataProcessingImpression(file_name)
    # クラスごとに分ける
    class_data_set = []
    for i in range(5):
        class_data = [line for index, line in data.df.iterrows() if line['class'] == i + 1]
        class_data = pd.DataFrame(class_data)
        class_data.columns = data.columns
        class_data.reset_index(inplace=True, drop=True)
        # 分割する
        dfs = np.array_split(class_data, cv)
        # print(dfs)
        # print(class_data)
        class_data_set.append(dfs)
    # print(class_data_set)

    # データセットを分割の数分作る
    data_sets = []
    for i in range(cv):
        for index, class_data in enumerate(class_data_set):
            # print(class_data)
            if index == 0:
                data_set = class_data[i]
            else:
                data_set = pd.concat([data_set, class_data[i]])
        data_set.reset_index(inplace=True, drop=True)
        data_sets.append(data_set)
        # print(data_set)

    # 学習データとテストデータを作る
    for i in range(cv):
        test_data = data_sets[i]
        train_data_sets = [data_set for index, data_set in enumerate(data_sets) if not i == index]
        for index, data_set in enumerate(train_data_sets):
            if index == 0:
                train_data = data_set
            else:
                train_data = pd.concat([train_data, data_set])
        test_data.to_csv('./data/cross_validate_test_data' + str(i) + '.csv', index=False)
        train_data.to_csv('./data/cross_validate_train_data' + str(i) + '.csv', index=False)


def tow_class_cross_validation(file_path, dir_path, cv):
    # csv用のデータ
    columns = list(range(1, cv+1))
    columns.insert(0, "分類器")
    columns.append('平均')
    data_list = []
    for class_name in class_list:
        # データ読み込み
        class_name1, class_name2 = class_name[0], class_name[1]
        data = DataProcessingImpression(file_path)
        data.get_target_impression_class(class_name1, class_name2)

        # モデルを生成
        model1 = GaussianNB()
        model4 = KNeighborsClassifier()
        model5 = RandomForestClassifier(random_state=None)
        models = [('gnb', model1), ('knc', model4), ('rfc', model5)]
        vote = VotingClassifier(estimators=models, voting='soft')
        # 交差検証
        scores = cross_val_score(vote, data.x_selected, data.y_selected, cv=cv)
        # 分類機の名前
        print(f'voting_classifier_{class_name1}_{class_name2}')
        # 各分割におけるスコア
        print('Cross-Validation scores: {}'.format(scores))
        # スコアの平均値
        print('Average score: {}'.format(np.mean(scores)))

        # csv変換用データに入れる
        # print(type(scores.tolist()[0]))
        scores = scores.tolist()
        scores.append(np.mean(scores))
        scores = [round(i, 2) for i in scores]
        scores.insert(0, f'{class_name1}_{class_name2}')
        data_list.append(scores)

    data_list = pd.DataFrame(data_list, columns=columns)
    data_list.to_csv(f'{dir_path}cross_validation_result_impression.csv', index=False, encoding='utf-8')


def main():
    # 共通印象の推定
    tow_class_cross_validation(
        file_path='./data/common_data/learning_data_common_impression.csv',
        dir_path='./data/common_data/',
        cv=4,
    )

    # 個人印象の推定
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)
    for directory_path in directory_paths:
        # 個人データ読み込み
        directory_path = f'{directory_path}/personal_data/'
        tow_class_cross_validation(
            file_path=f'{directory_path}learning_data_personal_impression.csv',
            dir_path=directory_path,
            cv=4,
        )


if __name__ == '__main__':
    sys.exit(main())
