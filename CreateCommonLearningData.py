#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys
import pandas as pd


def main():
    # データ読み込み
    common_data = pd.read_csv('./data/common_data/common_data.csv')
    common_params = pd.read_csv('./data/common_data/common_params.csv')

    # 閾値以上なら1（快），未満なら0（不快）
    for index, row in common_data.iterrows():
        tmp = common_params[common_params['class'] == row['class']]
        if row['pleasure'] >= float(tmp['threshold']):
            common_data.at[index, 'pleasure'] = 1
        else:
            common_data.at[index, 'pleasure'] = 0
    print(common_data)


if __name__ == '__main__':
    sys.exit(main())
