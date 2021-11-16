#!usr/bin/env python
#-*- cording: utf-8 -*-

import os
import sys

import pandas as pd


def get_file_paths(path):
    """
    指定したpath内にあるファイルのpathを取得します．
    :param path: パス
    :return: ファイル名のリスト
    """

    files = os.listdir(path)
    return [os.path.join(path, f) for f in files if not f.startswith('.') and os.path.isfile(os.path.join(path, f))]


def get_directory_paths(path):
    """
    指定したpath内にあるディレクトリのpathを取得します．
    :param path: パス
    :return: ディレクトリ名のリスト
    """

    directories = os.listdir(path)
    return [os.path.join(path, d) for d in directories if not os.path.isfile(os.path.join(path, d))]


def save_csv(path, df):
    """
    作成したデータフレームをcsv形式で保存します．
    :param path: 保存先
    :param df: データフレーム
    """

    df.to_csv(path, encoding='utf-8', index=False)

