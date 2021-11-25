#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys

import numpy as np
import pandas as pd
from packages.files import get_file_paths, get_directory_paths, save_csv


def main():
    # ディレクトリ名取得
    base_path = './data/personal_data/'
    directory = get_directory_paths(base_path)

if __name__ == '__main__':
    sys.exit(main())
