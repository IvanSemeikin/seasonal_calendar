import streamlit as st
import pandas as pd
import altair as alt

# Пример данных
data = {'День': [1, 2, 3, 4, 5],
        'Продажи': [10, 15, 8, 12, 20],
        'Выручка': [100, 150, 80, 120, 200],
        'Средний_чек': [10, 10, 10, 10, 10]}

df = pd.DataFrame(data)

# Строим график с тремя осями
chart = alt.Chart(df).mark_bar().encode(
    x='День',
    y='Продажи',
    color=alt.value('blue')
).properties(
    title='График продаж, выручки и среднего чека'
)

# Добавляем вспомогательные оси для выручки и среднего чека
revenue_axis = alt.Axis(title='Выручка', grid=False, position='right')
average_check_axis = alt.Axis(title='Средний чек', grid=False, position='right', offset=50)

chart = chart.encode(
    y='Выручка:Q',
    color=alt.value('orange')
).add_selection(
    alt.selection_single(bind='legend', fields=['axis'], init={'axis': 'left'})
).transform_fold(
    ['Продажи', 'Выручка', 'Средний_чек'],
    as_=['axis', 'value']
).transform_calculate(
    "axis", alt.expr.if_(alt.datum.axis == "Средний_чек", "right", "left")
).encode(
    y=alt.Y('value:Q', axis=alt.Axis(title='Продажи', grid=False)),
    color=alt.Color('axis:N', legend=None)
).properties(
    height=300
)

# Отображаем график в Streamlit
st.altair_chart(chart, use_container_width=True)
