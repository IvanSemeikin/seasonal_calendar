import streamlit as st
import pandas as pd
import plotly.express as px

# Пример данных
data = {'День': [1, 2, 3, 4, 5],
        'Продажи': [10, 15, 8, 12, 20],
        'Выручка': [100, 150, 80, 120, 200],
        'Средний_чек': [10, 10, 10, 10, 10]}

df = pd.DataFrame(data)

# Строим график с тремя осями
fig = px.bar(df, x='День', y='Продажи', color='Продажи', title='График продаж')

fig.update_layout(
    yaxis=dict(title='Продажи', side='left', showgrid=False),
    yaxis2=dict(title='Выручка', side='right', overlaying='y', showgrid=False),
    yaxis3=dict(title='Средний чек', side='right', overlaying='y', showgrid=False, anchor='free', position=0.9),
)

fig.show()

# Отображаем график в Streamlit
st.plotly_chart(fig, use_container_width=True)
