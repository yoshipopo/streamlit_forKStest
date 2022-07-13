#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 17:51:47 2022

@author: harukiyoshida
"""

import streamlit as st
import sys
#import pandas_datareader.data as web
import pandas
import numpy

st.title('モンテカルロシミュレーション')
st.caption(sys.version)
path = 'data_j.xls'
df_all_company_list = path_to_df_all_company_list(path)
st.write('全銘柄')
st.dataframe(df_all_company_list)
