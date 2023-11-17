import streamlit as st
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objs as go

# Пример данных
data = {'День': [1, 2, 3, 4, 5],
        'Продажи': [10, 15, 8, 12, 20],
        'Выручка': [100, 150, 80, 120, 200],
        'Средний_чек': [10, 10, 10, 10, 10]}

df = pd.DataFrame(data)

# Создаем график с тремя осями
fig = sp.make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=df['День'], y=df['Продажи'], name='Продажи'), secondary_y=False)
fig.add_trace(go.Scatter(x=df['День'], y=df['Выручка'], mode='lines', name='Выручка'), secondary_y=True)
fig.add_trace(go.Scatter(x=df['День'], y=df['Средний_чек'], mode='lines', name='Средний чек'), secondary_y=True)

# Настройка макета
fig.update_layout(title='График продаж, выручки и среднего чека')

# Отображаем график в Streamlit
st.plotly_chart(fig, use_container_width=True)
