import streamlit as st
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objs as go

# Пример данных
data = {'День': [1, 2, 3, 4, 5],
        'Продажи': [10, 25, 15, 12, 23],
        'Выручка': [100, 150, 80, 120, 250],
        'Средний_чек': [10, 6, 7, 12, 10]}

df = pd.DataFrame(data)

# Создаем график с тремя осями
fig = go.Figure()

# Добавляем столбцы для Продаж
fig.add_trace(go.Bar(x=df['День'], y=df['Продажи'], name='Продажи', marker_color='blue', width=0.4))

# Создаем вторую ось для Выручки
fig.add_trace(go.Bar(x=df['День'], y=df['Выручка'], name='Выручка', yaxis='y2', marker_color='orange', width=0.4))

# Создаем третью ось для Среднего чека
fig.add_trace(go.Scatter(x=df['День'], y=df['Средний_чек'], mode='lines', name='Средний чек', yaxis='y3', marker_color='green'))

# Настройка макета
fig.update_layout(title='График продаж, выручки и среднего чека',
                  yaxis=dict(title='Продажи', showgrid=False),
                  yaxis2=dict(title='Выручка', showgrid=False, overlaying='y', side='right'),
                  yaxis3=dict(title='Средний чек', showgrid=False, overlaying='y', side='right'))

# Отображаем график в Streamlit
st.plotly_chart(fig, use_container_width=True)
