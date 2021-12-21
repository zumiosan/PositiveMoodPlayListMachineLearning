#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random

import pandas as pd


def main():
    result_df = pd.DataFrame()
    for i in range(1, 15):
        username = f'pmp_user{i}'
        playlist_type_list = []
        for j in range(5):
            tmp_list = [j for j in range(0, 6)]
            random.shuffle(tmp_list)
            playlist_type_list = playlist_type_list + tmp_list
        df = pd.DataFrame(playlist_type_list, columns=['playlist_type'])
        df['username'] = username
        df['ex_id'] = range(1, len(df) + 1)
        # print(df)
        result_df = pd.concat([result_df, df])
    result_df.to_csv('./data/db_data/experiment_info.csv', encoding='utf-8-sig', index=False)
    # print(result_df)


if __name__ == '__main__':
    sys.exit(main())
