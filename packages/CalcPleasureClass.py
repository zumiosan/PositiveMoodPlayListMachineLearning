#!usr/bin/env python
# -*- cording: utf-8 -*-

import os
import sys


def calc_pleasure_class(df_data, df_params):
    # 閾値以上なら1（快），未満なら0（不快）
    for index, row in df_data.iterrows():
        tmp = df_params[df_params['class'] == row['class']]
        if row['pleasure'] >= float(tmp['threshold']):
            df_data.at[index, 'pleasure'] = 1
        else:
            df_data.at[index, 'pleasure'] = 0

    return df_data
