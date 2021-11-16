#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys

import pandas as pd
from packages.files import get_file_paths, get_directory_paths, save_csv


def main():
    # ディレクトリ名取得
    base_path = f".{os.sep}data{os.sep}questionnaire_personal_data/"
    directory_paths = get_directory_paths(base_path)

    # 個人データを作る
    personal_impression_data = pd.DataFrame()
    personal_pleasure_data = pd.DataFrame()
    personal_data = pd.DataFrame()







if __name__ == '__main__':
    sys.exit(main())