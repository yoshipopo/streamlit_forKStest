#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 17:51:47 2022

@author: harukiyoshida
"""

import streamlit as st
import sys
#import pandas_datareader.data as web
import pandas as pd
import numpy as np

def main():
  st.title('モンテカルロシミュレーション')
  st.caption(sys.version)
  path = 'data_j.xls'
  df_all_company_list = path_to_df_all_company_list(path)
  st.write('全銘柄')
  st.dataframe(df_all_company_list)

 
def path_to_df_all_company_list(path):
    df_all_company_list = pd.read_excel(path)
    df_all_company_list = df_all_company_list.replace('-', np.nan)
    df_all_company_list['コード&銘柄名'] = df_all_company_list['コード'].astype(str)+df_all_company_list['銘柄名']
    return df_all_company_list
  
if __name__ == "__main__":
    main()
