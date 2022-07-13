#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 17:51:47 2022

@author: harukiyoshida
"""

import streamlit as st
import sys
from pandas_datareader.stooq import StooqDailyReader
import pandas as pd
import numpy as np
from collections import deque
import datetime as dt
import plotly.graph_objects as go

st.set_page_config(layout="wide")

def main():
  st.title('モンテカルロシミュレーション')
  st.write(sys.version)
  
  #st.snow()
  
  path = 'data_j.xls'
  df_all_company_list = path_to_df_all_company_list(path)
  st.write('全銘柄')
  st.dataframe(df_all_company_list)
  
  selections = st.multiselect('銘柄を複数選択してください',df_all_company_list['コード&銘柄名'],)
                              #['8306三菱ＵＦＪフィナンシャル・グループ','8591オリックス','9020東日本旅客鉄道','9101日本郵船'])
  st.write('選択した銘柄')
  
  
  st.dataframe(selections_to_selected_company_list_and_selected_company_list_hyouji(df_all_company_list,selections)[0])
  selected_company_list = selections_to_selected_company_list_and_selected_company_list_hyouji(df_all_company_list,selections)[1]
  selected_company_list_hyouji = selections_to_selected_company_list_and_selected_company_list_hyouji(df_all_company_list,selections)[2]
  selected_company_list_hyouji_datenashi = selections
  
  
  duration = st.slider('株価取得期間は？(年)',1,10,2,)
  N = st.slider('モンテカルロ法回数は？',100,100000,10000,)
  
  #press_button = st.button("submit,csv取得")
  #st.session_state["is_pressed"] = button_states()
  if st.button("submit,csv取得"):
    
    df_price_merged = selected_company_list_to_get_df(selected_company_list,selected_company_list_hyouji,duration)[0]
    df_tourakuritu_merged = selected_company_list_to_get_df(selected_company_list,selected_company_list_hyouji,duration)[1]

    st.dataframe(df_price_merged)
    
    a=df_price_merged
    fig = go.Figure()
    for i in range(len(selected_company_list_hyouji_datenashi)):
      fig.add_trace(go.Scatter(x=a['Date'],
                          y=a.iloc[:,i+1],
                          name=selected_company_list_hyouji_datenashi[i])
                    )
    fig.update_traces(hovertemplate='%{y}')
    fig.update_layout(hovermode='x')
    fig.update_layout(height=500,width=1500,
                      title='株価推移',
                      xaxis={'title': 'Date'},
                      yaxis={'title': 'price/円'})                  
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig)
    
  
"""
def session_change():
    if "is_pressed" in st.session_state:
        st.session_state["is_pressed"].update({"pressed": None})
        """
        
def path_to_df_all_company_list(path):
    df_all_company_list = pd.read_excel(path)
    df_all_company_list = df_all_company_list.replace('-', np.nan)
    df_all_company_list['コード&銘柄名'] = df_all_company_list['コード'].astype(str)+df_all_company_list['銘柄名']
    return df_all_company_list
  
def selections_to_selected_company_list_and_selected_company_list_hyouji(df_all_company_list,selections):
    df_meigarasenntaku_temp = df_all_company_list[df_all_company_list['コード&銘柄名'].isin(selections)]
    selected_company_list = [str(i)+'.JP' for i in df_meigarasenntaku_temp['コード']]
    d = deque(selections)
    d.appendleft('Date')
    selected_company_list_hyouji = list(d)
    return df_meigarasenntaku_temp, selected_company_list, selected_company_list_hyouji

def selected_company_list_to_get_df(selected_company_list,selected_company_list_hyouji,duration):
    end = dt.datetime.now()
    start = end-dt.timedelta(days=duration*365)
    for i in range(len(selected_company_list)):
        code = selected_company_list[i]

        stooq = StooqDailyReader(code, start=start, end=end)
        df = stooq.read()  # pandas.core.frame.DataFrame

        df_price = df['Close']
        df_price = df_price.reset_index()

        df_tourakuritu = df['Close']
        df_tourakuritu = df_tourakuritu.pct_change(-1)
        df_tourakuritu = df_tourakuritu.reset_index()
        df_tourakuritu = df_tourakuritu.dropna()
        df_tourakuritu = df_tourakuritu.reset_index(drop=True)

        if i ==0:
          df_price_merged = df_price
          df_tourakuritu_merged = df_tourakuritu
        else:
          df_price_merged=pd.merge(df_price_merged, df_price, on='Date')
          df_tourakuritu_merged=pd.merge(df_tourakuritu_merged, df_tourakuritu, on='Date')
          
    df_price_merged = df_price_merged.set_axis(selected_company_list_hyouji, axis='columns')
    df_tourakuritu_merged = df_tourakuritu_merged.set_axis(selected_company_list_hyouji, axis='columns')
    df_price_merged['Date'] = df_price_merged['Date'].dt.round("D")
    df_tourakuritu_merged['Date'] = df_tourakuritu_merged['Date'].dt.round("D")
    return df_price_merged, df_tourakuritu_merged
  
  
if __name__ == "__main__":
    main()
