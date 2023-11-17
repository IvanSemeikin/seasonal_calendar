import requests
import json
import csv
import pandas as pd
import numpy as np
import streamlit as st
import os
from datetime import datetime, timedelta, date
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import openpyxl
import io
from io import BytesIO
from PIL import Image
from openpyxl.drawing.image import Image as OpenpyxlImage
# import matplotlib.pyplot as plt


# ________________________________________________________ чтение файлов с гитхаба
 
folder_path = 'wb_data_for_seasonal_calendar/'
wildberries = {}
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_excel(file_path)
        # Замена нижнего подчеркивания на слэш и удаление расширения .xlsx
        key = file_name.replace('_', '/').replace('.xlsx', '')
        wildberries[key] = df

folder_path_ozon = 'ozon_data_for_seasonal_calendar/'
ozon = {}
for file_name in os.listdir(folder_path_ozon):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path_ozon, file_name)
        df_ozon = pd.read_excel(file_path)
        # Замена нижнего подчеркивания на слэш и удаление расширения .xlsx
        key = file_name.replace('_', '/').replace('.xlsx', '')
        ozon[key] = df_ozon

# ________________________________________________________ загрузка и обработка данных для топ категорий от Вани
@st.cache_data()
def merge_excel_files_sales(folder_path):
    # Создаем пустой датафрейм
    merged_df = pd.DataFrame()

    # Проходим по всем файлам excel в папке
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)

            # Загружаем данные из файла
            df = pd.read_excel(file_path)

            # Переименовываем столбцы в соответствии с условиями
            if 'period' in df.columns:
                df = df.rename(columns={'period': f'period_{os.path.splitext(filename)[0]}'})
                df[f'period_{os.path.splitext(filename)[0]}'] = pd.to_datetime(
                    df[f'period_{os.path.splitext(filename)[0]}'])
            if 'sales' in df.columns:
                df = df.rename(columns={'sales': os.path.splitext(filename)[0]})
            if 'revenue' in df.columns:
                df = df.rename(columns={'revenue': f'revenue_{os.path.splitext(filename)[0]}'})

            # Добавляем таблицу в новый датафрейм
            merged_df = pd.concat([merged_df, df], axis=1)

    merged_df = merged_df.rename(columns={merged_df.columns[0]: 'Дата'})
    merged_df = merged_df.drop(columns=merged_df.filter(like='revenue_').columns)
    merged_df = merged_df.drop(columns=merged_df.filter(like='period').columns)
    merged_df = merged_df.set_index('Дата')
    merged_df = merged_df.iloc[:-2]

    return merged_df
 
@st.cache_data()
def merge_excel_files_revenue(folder_path):
    # Создаем пустой датафрейм
    merged_df = pd.DataFrame()

    # Проходим по всем файлам excel в папке
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)

            # Загружаем данные из файла
            df = pd.read_excel(file_path)

            # Переименовываем столбцы в соответствии с условиями
            if 'period' in df.columns:
                df = df.rename(columns={'period': f'period_{os.path.splitext(filename)[0]}'})
                df[f'period_{os.path.splitext(filename)[0]}'] = pd.to_datetime(
                    df[f'period_{os.path.splitext(filename)[0]}'])
            if 'revenue' in df.columns:
                df = df.rename(columns={'revenue': os.path.splitext(filename)[0]})
            if 'sales' in df.columns:
                df = df.rename(columns={'sales': f'sales_{os.path.splitext(filename)[0]}'})

            # Добавляем таблицу в новый датафрейм
            merged_df = pd.concat([merged_df, df], axis=1)

    merged_df = merged_df.rename(columns={merged_df.columns[0]: 'Дата'})
    merged_df = merged_df.drop(columns=merged_df.filter(like='sales_').columns)
    merged_df = merged_df.drop(columns=merged_df.filter(like='period').columns)
    merged_df = merged_df.set_index('Дата')
    merged_df = merged_df.iloc[:-2]

    return merged_df


def final_obrabotka(dataset_3):
    # Применяем resample для суммирования по месяцам
    monthly_sum_df = dataset_3.resample('M').sum()
    monthly_sum_df_t = monthly_sum_df.T

    # Получаем новые имена для столбцов, начиная с 1
    new_columns_names = {old_col: i + 1 for i, old_col in enumerate(monthly_sum_df_t.columns)}

    # Переименовываем столбцы
    monthly_sum_df_t.rename(columns=new_columns_names, inplace=True)

    monthly_sum_df_t['Январь_абс'] = monthly_sum_df_t[1] + monthly_sum_df_t[13] + monthly_sum_df_t[25]   # + monthly_sum_df_t[37]
    monthly_sum_df_t['Февраль_абс'] = monthly_sum_df_t[2] + monthly_sum_df_t[14] + monthly_sum_df_t[26]   # + monthly_sum_df_t[38]
    monthly_sum_df_t['Март_абс'] = monthly_sum_df_t[3] + monthly_sum_df_t[15] + monthly_sum_df_t[27]   # + monthly_sum_df_t[39]
    monthly_sum_df_t['Апрель_абс'] = monthly_sum_df_t[4] + monthly_sum_df_t[16] + monthly_sum_df_t[28]   # + monthly_sum_df_t[40]
    monthly_sum_df_t['Май_абс'] = monthly_sum_df_t[5] + monthly_sum_df_t[17] + monthly_sum_df_t[29]   # + monthly_sum_df_t[41]
    monthly_sum_df_t['Июнь_абс'] = monthly_sum_df_t[6] + monthly_sum_df_t[18] + monthly_sum_df_t[30]   # + monthly_sum_df_t[42]
    monthly_sum_df_t['Июль_абс'] = monthly_sum_df_t[7] + monthly_sum_df_t[19] + monthly_sum_df_t[31]   # + monthly_sum_df_t[43]
    monthly_sum_df_t['Август_абс'] = monthly_sum_df_t[8] + monthly_sum_df_t[20] + monthly_sum_df_t[32]   # + monthly_sum_df_t[44]
    monthly_sum_df_t['Сентябрь_абс'] = monthly_sum_df_t[9] + monthly_sum_df_t[21] + monthly_sum_df_t[33]   # + monthly_sum_df_t[45]
    monthly_sum_df_t['Октябрь_абс'] = monthly_sum_df_t[10] + monthly_sum_df_t[22] + monthly_sum_df_t[34]   # + monthly_sum_df_t[46]
    monthly_sum_df_t['Ноябрь_абс'] = monthly_sum_df_t[11] + monthly_sum_df_t[23] + monthly_sum_df_t[35]
    monthly_sum_df_t['Декабрь_абс'] = monthly_sum_df_t[12] + monthly_sum_df_t[24] + monthly_sum_df_t[36]

    new_monthly_sum_df_t = monthly_sum_df_t.iloc[:, -12:]

    new_monthly_sum_df_t['Сумма'] = new_monthly_sum_df_t.sum(axis=1)

    new_monthly_sum_df_t['Январь'] = new_monthly_sum_df_t['Январь_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Февраль'] = new_monthly_sum_df_t['Февраль_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Март'] = new_monthly_sum_df_t['Март_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Апрель'] = new_monthly_sum_df_t['Апрель_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Май'] = new_monthly_sum_df_t['Май_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Июнь'] = new_monthly_sum_df_t['Июнь_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Июль'] = new_monthly_sum_df_t['Июль_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Август'] = new_monthly_sum_df_t['Август_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Сентябрь'] = new_monthly_sum_df_t['Сентябрь_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Октябрь'] = new_monthly_sum_df_t['Октябрь_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Ноябрь'] = new_monthly_sum_df_t['Ноябрь_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_monthly_sum_df_t['Декабрь'] = new_monthly_sum_df_t['Декабрь_абс'] / new_monthly_sum_df_t['Сумма'] * 100
    new_new_monthly_sum_df_t = new_monthly_sum_df_t.iloc[:, -12:]

    return new_new_monthly_sum_df_t





# _______________________________________ функция календаря сезонности

@st.cache_data()

def seasonal_calendar(df):

    df['period'] = pd.to_datetime(df['period'])
    
    # Инициализация словарей для продаж и выручки по месяцам для каждого года
    monthly_sales_2020 = {month: [0] for month in range(1, 13)}
    monthly_sales_2021 = {month: [0] for month in range(1, 13)}
    monthly_sales_2022 = {month: [0] for month in range(1, 13)}
    monthly_sales_2023 = {month: [0] for month in range(1, 13)}

    monthly_revenue_2020 = {month: [0] for month in range(1, 13)}
    monthly_revenue_2021 = {month: [0] for month in range(1, 13)}
    monthly_revenue_2022 = {month: [0] for month in range(1, 13)}
    monthly_revenue_2023 = {month: [0] for month in range(1, 13)}

    
    for index, row in df.iterrows():
        year = row['period'].year 
        month = row['period'].month
        sales = row['sales']
        revenue = row['revenue']
        
        if year == 2020:
            monthly_sales_2020[month][0] += sales
            monthly_revenue_2020[month][0] += revenue
        elif year == 2021:
            monthly_sales_2021[month][0] += sales
            monthly_revenue_2021[month][0] += revenue
        elif year == 2022:
            monthly_sales_2022[month][0] += sales
            monthly_revenue_2022[month][0] += revenue
        elif year == 2023:
            monthly_sales_2023[month][0] += sales
            monthly_revenue_2023[month][0] += revenue

    # Подсчет и вывод сумм и средних значений для каждого года
    # Продажи
    monthly_sales_totals_2020 = [round(monthly_sales_2020[month][0], 1) for month in range(1, 13)]
    monthly_sales_totals_2021 = [round(monthly_sales_2021[month][0], 1) for month in range(1, 13)]
    monthly_sales_totals_2022 = [round(monthly_sales_2022[month][0], 1) for month in range(1, 13)]
    monthly_sales_totals_2023 = [round(monthly_sales_2023[month][0], 1) for month in range(1, 13)]

    total_sales_2020 = sum(monthly_sales_totals_2020)
    total_sales_2021 = sum(monthly_sales_totals_2021)
    total_sales_2022 = sum(monthly_sales_totals_2022)
    total_sales_2023 = sum(monthly_sales_totals_2023)

    avg_monthly_sales = [round((monthly_sales_2020[month][0] + monthly_sales_2021[month][0] + monthly_sales_2022[month][0] + monthly_sales_2023[month][0]) / 4, 1) for month in range(1, 13)]

    # Выручка
    monthly_revenue_totals_2020 = [round(monthly_revenue_2020[month][0], 1) for month in range(1, 13)]
    monthly_revenue_totals_2021 = [round(monthly_revenue_2021[month][0], 1) for month in range(1, 13)]
    monthly_revenue_totals_2022 = [round(monthly_revenue_2022[month][0], 1) for month in range(1, 13)]
    monthly_revenue_totals_2023 = [round(monthly_revenue_2023[month][0], 1) for month in range(1, 13)]

    total_revenue_2020 = sum(monthly_revenue_totals_2020)
    total_revenue_2021 = sum(monthly_revenue_totals_2021)
    total_revenue_2022 = sum(monthly_revenue_totals_2022)
    total_revenue_2023 = sum(monthly_revenue_totals_2023)

    avg_monthly_revenue = [round((monthly_revenue_2020[month][0] + monthly_revenue_2021[month][0] + monthly_revenue_2022[month][0] + monthly_revenue_2023[month][0]) / 4, 1) for month in range(1, 13)]


    # Расчет долей продаж и выручки по месяцам для каждого года
     # Продажи по долям
    share_of_sales_2020 = [round(x / total_sales_2020 * 100, 1) if total_sales_2020 else 0 for x in monthly_sales_totals_2020]
    share_of_sales_2021 = [round(x / total_sales_2021 * 100, 1) if total_sales_2021 else 0 for x in monthly_sales_totals_2021]
    share_of_sales_2022 = [round(x / total_sales_2022 * 100, 1) if total_sales_2022 else 0 for x in monthly_sales_totals_2022]
    share_of_sales_2023 = [round(x / total_sales_2023 * 100, 1) if total_sales_2023 else 0 for x in monthly_sales_totals_2023]
    
    # Выручка по долям
    share_of_revenue_2020 = [round(x / total_revenue_2020 * 100, 1) if total_revenue_2020 else 0 for x in monthly_revenue_totals_2020]
    share_of_revenue_2021 = [round(x / total_revenue_2021 * 100, 1) if total_revenue_2021 else 0 for x in monthly_revenue_totals_2021]
    share_of_revenue_2022 = [round(x / total_revenue_2022 * 100, 1) if total_revenue_2022 else 0 for x in monthly_revenue_totals_2022]
    share_of_revenue_2023 = [round(x / total_revenue_2023 * 100, 1) if total_revenue_2023 else 0 for x in monthly_revenue_totals_2023]


    
    # Расчет средних долей продаж и выручки по месяцам за все годы
    avg_monthly_sales_share = [round(sum(shares) / 4, 1) for shares in zip(share_of_sales_2020, share_of_sales_2021, share_of_sales_2022, share_of_sales_2023)]
    avg_monthly_revenue_share = [round(sum(shares) / 4, 1) for shares in zip(share_of_revenue_2020, share_of_revenue_2021, share_of_revenue_2022, share_of_revenue_2023)]



    # Получаем средние чеки для каждого месяца каждого года
    monthly_bills_totals_2020 = [round(revenue_m / sales_m, 1) if sales_m != 0 else 0 for revenue_m, sales_m in zip(monthly_revenue_totals_2020, monthly_sales_totals_2020)]
    monthly_bills_totals_2021 = [round(revenue_m / sales_m, 1) if sales_m != 0 else 0 for revenue_m, sales_m in zip(monthly_revenue_totals_2021, monthly_sales_totals_2021)]
    monthly_bills_totals_2022 = [round(revenue_m / sales_m, 1) if sales_m != 0 else 0 for revenue_m, sales_m in zip(monthly_revenue_totals_2022, monthly_sales_totals_2022)]
    monthly_bills_totals_2023 = [round(revenue_m / sales_m, 1) if sales_m != 0 else 0 for revenue_m, sales_m in zip(monthly_revenue_totals_2023, monthly_sales_totals_2023)]

    # Получаем значения средних чеков для каждого года
    avg_bills_2020 = total_revenue_2020 / total_sales_2020 if total_sales_2020 != 0 else 0
    avg_bills_2021 = total_revenue_2021 / total_sales_2021 if total_sales_2021 != 0 else 0
    avg_bills_2022 = total_revenue_2022 / total_sales_2022 if total_sales_2022 != 0 else 0
    avg_bills_2023 = total_revenue_2023 / total_sales_2023 if total_sales_2023 != 0 else 0

    # Получаем абсолютные отклонения для каждого месяца от величины среднего чека за год
    deviation_monthly_bills_2020 = [m_bills - avg_bills_2020 for m_bills in monthly_bills_totals_2020]
    deviation_monthly_bills_2021 = [m_bills - avg_bills_2021 for m_bills in monthly_bills_totals_2021]
    deviation_monthly_bills_2022 = [m_bills - avg_bills_2022 for m_bills in monthly_bills_totals_2022]
    deviation_monthly_bills_2023 = [m_bills - avg_bills_2023 for m_bills in monthly_bills_totals_2023]

    # Получаем относительные отклонения для каждого месяца от величины среднего чека за год
    deviation_percent_monthly_bills_2020 = [deviation_m_bill / avg_bills_2020 * 100 if avg_bills_2020 != 0 else 0
                                            for deviation_m_bill in deviation_monthly_bills_2020]
    deviation_percent_monthly_bills_2021 = [deviation_m_bill / avg_bills_2021 * 100 if avg_bills_2021 != 0 else 0
                                            for deviation_m_bill in deviation_monthly_bills_2021]
    deviation_percent_monthly_bills_2022 = [deviation_m_bill / avg_bills_2022 * 100 if avg_bills_2022 != 0 else 0
                                            for deviation_m_bill in deviation_monthly_bills_2022]
    deviation_percent_monthly_bills_2023 = [deviation_m_bill / avg_bills_2023 * 100 if avg_bills_2023 != 0 else 0
                                            for deviation_m_bill in deviation_monthly_bills_2023]
    # Дополнительные расчеты и выводы могут быть добавлены аналогично

    # Возвращение всех собранных данных
    return (
        monthly_sales_totals_2020, monthly_sales_totals_2021, monthly_sales_totals_2022, monthly_sales_totals_2023,
        total_sales_2020, total_sales_2021, total_sales_2022, total_sales_2023,
        avg_monthly_sales,
        monthly_revenue_totals_2020, monthly_revenue_totals_2021, monthly_revenue_totals_2022, monthly_revenue_totals_2023,
        total_revenue_2020, total_revenue_2021, total_revenue_2022, total_revenue_2023,
        avg_monthly_revenue,
        share_of_sales_2020, share_of_sales_2021, share_of_sales_2022, share_of_sales_2023,
        share_of_revenue_2020, share_of_revenue_2021, share_of_revenue_2022, share_of_revenue_2023,
        avg_monthly_sales_share, avg_monthly_revenue_share, monthly_bills_totals_2020, monthly_bills_totals_2021, monthly_bills_totals_2022, monthly_bills_totals_2023,
        avg_bills_2020, avg_bills_2021, avg_bills_2022, avg_bills_2023,
        deviation_monthly_bills_2020, deviation_monthly_bills_2021, deviation_monthly_bills_2022, deviation_monthly_bills_2023,
        deviation_percent_monthly_bills_2020, deviation_percent_monthly_bills_2021, deviation_percent_monthly_bills_2022, deviation_percent_monthly_bills_2023
    )

# _______________________________________________ получение категорий вб для выпадающего списка
#@st.cache_data()
#def get_wb_categories():
#    url = 'http://mpstats.io/api/wb/get/categories'
#    headers = {
#        'X-Mpstats-TOKEN': '64ee0e4f67a005.746995831774b14d378d3e3022e4e2f8a3698042',
#        'Content-Type': 'application/json'
#    }
#    response = requests.get(url, headers=headers)
#    if response.status_code == 200:
#        data = response.json()
#        formatted_data = [
#            {
#                "url": category.get("url"),
#                "name": category.get("name"),
#                "path": category.get("path")
#            }
#            for category in data
#        ]
        # Исключаем категории, которые начинаются с 'Акции'
#        filtered_data = [item for item in formatted_data if not item['path'].startswith('Акции')]
#        return filtered_data
#    else:
#       print(f"Запрос не отработан: {response.status_code}")
#        return []

# _______________________________________________получение категорий Озон для выпадающего списка (апи)

#@st.cache_data()
#def get_ozon_categories():
#    url = 'http://mpstats.io/api/oz/get/categories'
#    headers = {
#        'X-Mpstats-TOKEN': '64ee0e4f67a005.746995831774b14d378d3e3022e4e2f8a3698042',
#        'Content-Type': 'application/json'
#    }
#    response = requests.get(url, headers=headers)
#    if response.status_code == 200:
#        data = response.json()
#        formatted_data = [
#            {
#                "url": category.get("url"),
#                "name": category.get("name"),
#                "path": category.get("path")
#            }
#            for category in data
#        ]
#        # Исключаем категории, которые начинаются с 'Акции'
#        filtered_data = [item for item in formatted_data if not item['path'].startswith('Акции')]
#        return filtered_data
#    else:
#        print(f"Запрос не отработан: {response.status_code}")
#        return []

# ____________________________________________________ Функция для получения дат по месяцам за несколько лет
def get_dates_for_months(months, start_year, end_year):
    dates = []
    for year in range(start_year, end_year + 1):
        for month in months:
            month_start_date = date(year, month, 1)
            next_month = month + 1 if month != 12 else 1
            next_year = year if month != 12 else year + 1
            month_end_date = date(next_year, next_month, 1) - timedelta(days=1)
            dates.append((month_start_date, month_end_date))
    return dates



def get_top_products_for_selected_months(data, top_n):
    top_sales = []
    top_revenue = []

    # Сбор данных по продажам и выручке
    for category_path, results in data.items():
        # Получение данных из словаря
        total_sales = results['sales']
        total_revenue = results['revenue']

        # Добавление данных в списки
        top_sales.append((category_path, total_sales))
        top_revenue.append((category_path, total_revenue))

    # Сортировка и выбор топ категорий
    top_sales.sort(key=lambda x: x[1], reverse=True)
    top_revenue.sort(key=lambda x: x[1], reverse=True)

    # Ограничение результатов до указанного количества топ-элементов
    return {
        'top_by_sales': top_sales[:top_n],
        'top_by_revenue': top_revenue[:top_n]
    }



# ________________________________________________________ визуализации продаж и выручки в категориях (вариант без подписей)
#def plot_data(df, title):
#    fig = make_subplots(rows=1, cols=len(df.columns) + 1, subplot_titles=df.columns.to_list() + ['Сводный'])
#
#    for i, col in enumerate(df.columns, start=1):
#        fig.add_trace(
#            go.Bar(y=df.index, x=df[col], name=col, orientation='h'),
#            row=1, col=i
#        )

    # сводный график
#    for col in df.columns:
#        if col not in ['AVG']:  # Исключаем 'AVG'
#            fig.add_trace(
#                go.Bar(y=df.index, x=df[col], name=col, showlegend=False, orientation='h'),
#                row=1, col=len(df.columns) + 1
#            )

#    fig.update_layout(title_text=title, height=600, width=1200)
#    return fig

# ________________________________________________________ визуализации продаж и выручки в категориях (вариант с подписями) + сводная таблица
def plot_data(df, title):
    fig = make_subplots(rows=1, cols=len(df.columns) + 1, subplot_titles=df.columns.to_list() + ['Сводный'])

    for i, col in enumerate(df.columns, start=1):
        trace = go.Bar(y=df.index, x=df[col], name=col, orientation='h')
        fig.add_trace(trace, row=1, col=i)

        # Добавление аннотаций для каждого столбца
        for j, value in enumerate(df[col]):
            fig.add_annotation(
                x=value, y=df.index[j],
                text=str(value),
                showarrow=False,
                xanchor='left',
                row=1, col=i
            )

    # сводный график
    for col in df.columns:
        if col not in ['AVG']:  # Исключаем 'AVG'
            fig.add_trace(
                go.Bar(y=df.index, x=df[col], name=col, showlegend=False, orientation='h'),
                row=1, col=len(df.columns) + 1
            )

    fig.update_layout(title_text=title, height=600, width=1200)
    return fig
    

def plot_total_data(df):
    # # График для общих продаж
    # fig_total_sales = go.Figure()
    # fig_total_sales.add_trace(go.Scatter(x=df.index, y=df['Total Sales'], mode='lines+markers', name='Total Sales'))
    # fig_total_sales.update_layout(title='Общие продажи по годам', xaxis_title='Год', yaxis_title='Общие продажи')

    # # График для общей выручки
    # fig_total_revenue = go.Figure()
    # fig_total_revenue.add_trace(go.Scatter(x=df.index, y=df['Total Revenue'], mode='lines+markers', name='Total Revenue'))
    # fig_total_revenue.update_layout(title='Общая выручка по годам', xaxis_title='Год', yaxis_title='Общая выручка')



    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    x_labels = [f'{month} {year}' for year in sales_data.columns for month in months]

    # Преобразование DataFrame в одномерный массив для графика
    sales_values = sales_data.values.flatten()
    revenue_values = revenue_data.values.flatten()

    # График для общих продаж
    fig_total_sales = go.Figure()
    fig_total_sales.add_trace(go.Scatter(x=x_labels, y=sales_values, mode='lines+markers', name='Total Sales'))
    fig_total_sales.update_layout(title='Общие продажи по месяцам', xaxis_title='Месяц и год', yaxis_title='Общие продажи')

    # График для общей выручки
    fig_total_revenue = go.Figure()
    fig_total_revenue.add_trace(go.Scatter(x=x_labels, y=revenue_values, mode='lines+markers', name='Total Revenue'))
    fig_total_revenue.update_layout(title='Общая выручка по месяцам', xaxis_title='Месяц и год', yaxis_title='Общая выручка')

    # Комбинированный столбчатый график
    fig_combined = go.Figure()
    bar_width = 0.4
    fig_combined.add_trace(go.Bar(
        x=df.index - bar_width/2,  # Сдвиг влево на половину ширины столбца
        y=df['Total Sales'],
        name='Total Sales',
        marker_color='blue',
        width=bar_width
    ))
    fig_combined.add_trace(go.Bar(
        x=df.index + bar_width/2,  # Сдвиг вправо на половину ширины столбца
        y=df['Total Revenue'],
        name='Total Revenue',
        marker_color='green',
        yaxis='y2',
        width=bar_width
    ))

    fig_combined.update_layout(
        title='Общие продажи и выручка по годам',
        xaxis=dict(title='Год', tickmode='array', tickvals=df.index),
        yaxis=dict(title='Общие продажи', side='left'),
        yaxis2=dict(title='Общая выручка', side='right', overlaying='y', showgrid=False),
        barmode='group'
    )

    return fig_total_sales, fig_total_revenue, fig_combined


# ____________________________________________________________________________ подготовка данных к сохранению в эксель

def prepare_data_for_excel(platform, report_type):
    if platform in ['Wildberries', 'Ozon'] and report_type == 'Данные по категории':
        data_frames = {'Sales': sales_data, 'Sales, %' : sales_share_data, 'Revenue': revenue_data, 'Revenue, %' : revenue_share_data, 'AVG Bill': bills_data, 'Total Data': total_data}

        # figures = [fig_sales, fig_revenue, fig_total_sales, fig_total_revenue, fig_combined]
        # images = [convert_fig_to_image(fig) for fig in figures]

        return data_frames #, images

    elif platform in ['Wildberries', 'Ozon'] and report_type == 'Топовые категории':
     data_frames =  {'Top Products by sales': top_sales_values, 'Top Products by revenue': top_revenue_values,'Sales': sales_data, 'Sales, %' : sales_share_data, 'Revenue': revenue_data, 'Revenue, %' : revenue_share_data, 'AVG Bill': bills_data, 'Total Data': total_data}
     return data_frames
        # return {'Top Products': top_sales_values, top_revenue_values}, None

def convert_fig_to_image(fig):
    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    return buf

# ================================================= Начало работы кода

# примененеие seasonal_calendar() к словарю wb

seasonal_results_wb = {}

# Применение функции seasonal_calendar к каждому DataFrame в wildberries
for key, df in wildberries.items():
    seasonal_results_wb[key] = seasonal_calendar(df)

# Отображение всех результатов в Streamlit (или другие действия с результатами)
for key, results in seasonal_results_wb.items():
     (monthly_sales_totals_2020, monthly_sales_totals_2021, monthly_sales_totals_2022, monthly_sales_totals_2023,
     total_sales_2020, total_sales_2021, total_sales_2022, total_sales_2023,
     avg_monthly_sales,
     monthly_revenue_totals_2020, monthly_revenue_totals_2021, monthly_revenue_totals_2022, monthly_revenue_totals_2023,
     total_revenue_2020, total_revenue_2021, total_revenue_2022, total_revenue_2023,
     avg_monthly_revenue,share_of_sales_2020, share_of_sales_2021, 
     share_of_sales_2022, share_of_sales_2023,share_of_revenue_2020, share_of_revenue_2021, share_of_revenue_2022, share_of_revenue_2023, avg_monthly_sales_share, avg_monthly_revenue_share,
     monthly_bills_totals_2020, monthly_bills_totals_2021, monthly_bills_totals_2022, monthly_bills_totals_2023,
     avg_bills_2020, avg_bills_2021, avg_bills_2022, avg_bills_2023,
     deviation_monthly_bills_2020, deviation_monthly_bills_2021, deviation_monthly_bills_2022, deviation_monthly_bills_2023,
     deviation_percent_monthly_bills_2020, deviation_percent_monthly_bills_2021, deviation_percent_monthly_bills_2022, deviation_percent_monthly_bills_2023) = results


#____________________________ примененеие seasonal_calendar() к словарю ozon

seasonal_results_ozon = {}

# Применение функции seasonal_calendar к каждому DataFrame в wildberries
for key, df_ozon in ozon.items():
    seasonal_results_ozon[key] = seasonal_calendar(df_ozon)

# Отображение всех результатов в Streamlit (или другие действия с результатами)
for key, results_ozon in seasonal_results_ozon.items():
    # st.write(f"Результаты для {key}:")
    (monthly_sales_totals_2020_ozon, monthly_sales_totals_2021_ozon, monthly_sales_totals_2022_ozon, monthly_sales_totals_2023_ozon,
     total_sales_2020_ozon, total_sales_2021_ozon, total_sales_2022_ozon, total_sales_2023_ozon,
     avg_monthly_sales_ozon,
     monthly_revenue_totals_2020_ozon, monthly_revenue_totals_2021_ozon, monthly_revenue_totals_2022_ozon, monthly_revenue_totals_2023_ozon,
     total_revenue_2020_ozon, total_revenue_2021_ozon, total_revenue_2022_ozon, total_revenue_2023_ozon,
     avg_monthly_revenue_ozon, share_of_sales_2020_ozon, share_of_sales_2021_ozon, 
     share_of_sales_2022_ozon, share_of_sales_2023_ozon,share_of_revenue_2020_ozon, share_of_revenue_2021_ozon, share_of_revenue_2022_ozon, share_of_revenue_2023_ozon, avg_monthly_sales_share_ozon, avg_monthly_revenue_share_ozon,
     monthly_bills_totals_2020_ozon, monthly_bills_totals_2021_ozon, monthly_bills_totals_2022_ozon, monthly_bills_totals_2023_ozon,
     avg_bills_2020_ozon, avg_bills_2021_ozon, avg_bills_2022_ozon, avg_bills_2023_ozon,
     deviation_monthly_bills_2020_ozon, deviation_monthly_bills_2021_ozon, deviation_monthly_bills_2022_ozon, deviation_monthly_bills_2023_ozon,
     deviation_percent_monthly_bills_2020_ozon, deviation_percent_monthly_bills_2021_ozon, deviation_percent_monthly_bills_2022_ozon, deviation_percent_monthly_bills_2023_ozon) = results_ozon


# ____________________________ Обработка данных для топа категорий от Вани
# озон
sales_ozon_top = merge_excel_files_sales('ozon_data_for_seasonal_calendar/')
revenue_ozon_top = merge_excel_files_revenue('ozon_data_for_seasonal_calendar/')

# wb
sales_wb_top = merge_excel_files_sales('wb_data_for_seasonal_calendar/')
revenue_wb_top = merge_excel_files_revenue('wb_data_for_seasonal_calendar/')



# ____________________________ список категорий для автономного подключения 

categories_wb = [
    'Автотовары/OFFroad', 'Автотовары/Автокосметика и автохимия','Автотовары/Автоэлектроника и навигация','Автотовары/Аксессуары в салон и багажник','Автотовары/Внешний тюнинг','Автотовары/Другие аксессуары и доп. оборудование', 'Автотовары/Запчасти для лодок и катеров',
    'Автотовары/Запчасти на легковые автомобили', 'Автотовары/Запчасти на силовую технику','Автотовары/Инструменты','Автотовары/Коврики','Автотовары/Краски и грунтовки',
    'Автотовары/Масла и жидкости','Автотовары/Мототовары', 'Автотовары/Шины и диски колесные','Аксессуары/Аксессуары для волос', 'Аксессуары/Аксессуары для одежды',
    'Аксессуары/Бижутерия','Аксессуары/Веера','Аксессуары/Галстуки и бабочки','Аксессуары/Головные уборы','Аксессуары/Зеркальца', 'Аксессуары/Зонты','Аксессуары/Кошельки и кредитницы', 'Аксессуары/Маски для сна', 'Аксессуары/Носовые платки','Аксессуары/Очки и футляры','Аксессуары/Перчатки и варежки', 'Аксессуары/Платки и шарфы',
    'Аксессуары/Религиозные','Аксессуары/Ремни и пояса','Аксессуары/Сумки и рюкзаки','Аксессуары/Часы и ремешки','Аксессуары/Чемоданы и защита багажа','Бытовая техника/Климатическая техника','Бытовая техника/Красота и здоровье',
    'Бытовая техника/Крупная бытовая техника','Бытовая техника/Садовая техника','Бытовая техника/Техника для дома','Бытовая техника/Техника для кухни','Детям/Детское питание','Детям/Для девочек','Детям/Для мальчиков','Детям/Для новорожденных','Детям/Конструкторы','Детям/Подарки детям','Детям/Подгузники','Детям/Религиозная одежда','Детям/Товары для малыша',
    'Для ремонта/Вентиляция','Для ремонта/Двери, окна и фурнитура','Для ремонта/Инструменты и оснастка','Для ремонта/Крепеж',
    'Для ремонта/Лакокрасочные материалы', 'Для ремонта/Отделочные материалы','Для ремонта/Сантехника, отопление и газоснабжение','Для ремонта/Стройматериалы','Для ремонта/Электрика','Дом/Ванная',
    'Дом/Все для праздника','Дом/Гостиная','Дом/Детская','Дом/Для курения','Дом/Досуг и творчество','Дом/Зеркала','Дом/Коврики','Дом/Кронштейны','Дом/Кухня',
    'Дом/Освещение','Дом/Отдых на природе','Дом/Парфюмерия для дома','Дом/Предметы интерьера','Дом/Прихожая','Дом/Религия, эзотерика','Дом/Спальня','Дом/Сувенирная продукция','Дом/Хозяйственные товары','Дом/Хранение вещей','Дом/Цветы, вазы и кашпо','Дом/Шторы','Женщинам/Белье',
    'Женщинам/Блузки и рубашки','Женщинам/Большие размеры','Женщинам/Брюки','Женщинам/Будущие мамы','Женщинам/Верхняя одежда',
    'Женщинам/Джемперы, водолазки и кардиганы','Женщинам/Джинсы','Женщинам/Для высоких','Женщинам/Для невысоких','Женщинам/Комбинезоны','Женщинам/Костюмы','Женщинам/Лонгсливы',
    'Женщинам/Одежда для дома','Женщинам/Офис','Женщинам/Пиджаки, жилеты и жакеты','Женщинам/Платья и сарафаны','Женщинам/Пляжная мода','Женщинам/Подарки женщинам','Женщинам/Религиозная','Женщинам/Свадьба',
    'Женщинам/Спецодежда и СИЗы','Женщинам/Толстовки, свитшоты и худи','Женщинам/Туники','Женщинам/Футболки и топы','Женщинам/Халаты','Женщинам/Шорты','Женщинам/Юбки',
    'Здоровье/БАДы','Здоровье/Грибы сушеные и капсулированные','Здоровье/Дезинфекция, стерилизация и утилизация','Здоровье/Контрацептивы и лубриканты','Здоровье/Лечебное питание','Здоровье/Маски защитные',
    'Здоровье/Медицинские изделия', 'Здоровье/Медицинские приборы', 'Здоровье/Оздоровление', 'Здоровье/Оптика', 'Здоровье/Ортопедия',
    'Здоровье/Реабилитация', 'Здоровье/Сиропы и бальзамы', 'Здоровье/Ухо, горло, нос', 'Здоровье/Уход за полостью рта', 'Зоотовары/Аквариумистика',
    'Зоотовары/Аксессуары для кормления', 'Зоотовары/Амуниция и дрессировка', 'Зоотовары/Ветаптека', 'Зоотовары/Груминг и уход', 'Зоотовары/Для грызунов и хорьков',
    'Зоотовары/Для кошек', 'Зоотовары/Для лошадей', 'Зоотовары/Для птиц', 'Зоотовары/Для собак', 'Зоотовары/Игрушки',
    'Зоотовары/Когтеточки и домики', 'Зоотовары/Корм и лакомства', 'Зоотовары/Лотки и наполнители', 'Зоотовары/Одежда', 'Зоотовары/Террариумистика',
    'Зоотовары/Транспортировка', 'Зоотовары/Фермерство', 'Игрушки/Антистресс', 'Игрушки/Для малышей', 'Игруushки/Для песочницы',
    'Игрушки/Игровые комплексы', 'Игрушки/Игровые наборы', 'Игрушки/Игрушечное оружие и аксессуары', 'Игрушки/Игрушечный транспорт', 'Игрушки/Игрушки для ванной',
    'Игрушки/Интерактивные', 'Игрушки/Кинетический песок', 'Игрушки/Конструкторы', 'Игрушки/Конструкторы LEGO', 'Игрушки/Куклы и аксессуары',
    'Игрушки/Музыкальные', 'Игрушки/Мыльные пузыри', 'Игрушки/Мягкие игрушки', 'Игрушки/Наборы для опытов', 'Игрушки/Настольные игры',
    'Игрушки/Радиоуправляемые', 'Игрушки/Развивающие игрушки', 'Игрушки/Сборные модели', 'Игрушки/Спортивные игры', 'Игрушки/Сюжетно-ролевые игры',
    'Игрушки/Творчество и рукоделие', 'Игрушки/Фигурки и роботы', 'Канцтовары/Бумажная продукция', 'Канцтовары/Карты и глобусы', 'Канцтовары/Офисные принадлежности',
    'Канцтовары/Письменные принадлежности', 'Канцтовары/Рисование и лепка', 'Канцтовары/Счетный материал', 'Канцтовары/Торговые принадлежности', 'Канцтовары/Чертежные принадлежности',
    'Книги/Астрология и эзотерика', 'Книги/Аудиокниги', 'Книги/Бизнес и менеджмент', 'Книги/Букинистика', 'Книги/Воспитание и развитие ребенка',
    'Книги/Дом, сад и огород', 'Книги/Интернет и технологии', 'Книги/Историческая и военная литература', 'Книги/Календари', 'Книги/Книги для детей',
    'Книги/Книги на иностранных языках', 'Книги/Коллекционные издания', 'Книги/Комиксы и манга', 'Книги/Красота, здоровье и спорт', 'Книги/Литературоведение и публицистика',
    'Книги/Мультимедиа', 'Книги/Научно-популярная литература', 'Книги/Образование', 'Книги/Плакаты', 'Книги/Политика и право',
    'Книги/Религия', 'Книги/Репринтные издания', 'Книги/Самообразование и развитие', 'Книги/Философия', 'Книги/Хобби и досуг',
    'Книги/Художественная литература', 'Красота/Аксессуары', 'Красота/Аптечная косметика', 'Красота/Волосы', 'Красота/Гигиена полости рта',
    'Красота/Детская декоративная косметика', 'Красота/Для загара', 'Красота/Для мам и малышей', 'Красота/Израильская косметика', 'Красота/Инструменты для парикмахеров',
    'Красота/Корейские бренды', 'Красота/Крымская косметика', 'Красота/Макияж', 'Красота/Мужская линия', 'Красота/Наборы для ухода',
    'Красота/Ногти', 'Красота/Органическая косметика', 'Красота/Парфюмерия', 'Красота/Подарочные наборы', 'Красота/Профессиональная косметика',
    'Красота/Средства личной гигиены', 'Красота/Уход за кожей', 'Мебель/Бескаркасная мебель', 'Мебель/Гардеробная мебель', 'Мебель/Детская мебель',
    'Мебель/Диваны и кресла', 'Мебель/Зеркала', 'Мебель/Компьютерная и геймерская мебель', 'Мебель/Мебель для гостиной', 'Мебель/Мебель для кухни',
    'Мебель/Мебель для прихожей', 'Мебель/Мебель для спальни', 'Мебель/Мебельная фурнитура', 'Мебель/Офисная мебель', 'Мебель/Столы и стулья',
    'Мебель/Торговая мебель', 'Мужчинам/Белье', 'Мужчинам/Большие размеры', 'Мужчинам/Брюки', 'Мужчинам/Верхняя одежда', 'Мужчинам/Джемперы, водолазки и кардиганы', 'Мужчинам/Джинсы',
    'Мужчинам/Для высоких', 'Мужчинам/Для невысоких', 'Мужчинам/Комбинезоны и полукомбинезоны', 'Мужчинам/Костюмы', 'Мужчинам/Лонгсливы',
    'Мужчинам/Майки', 'Мужчинам/Одежда для дома', 'Мужчинам/Офис', 'Мужчинам/Пиджаки, жилеты и жакеты', 'Мужчинам/Пижамы',
    'Мужчинам/Пляжная одежда', 'Мужчинам/Подарки мужчинам', 'Мужчинам/Религиозная', 'Мужчинам/Рубашки', 'Мужчинам/Свадьба',
    'Мужчинам/Спецодежда и СИЗы', 'Мужчинам/Толстовки, свитшоты и худи', 'Мужчинам/Футболки', 'Мужчинам/Футболки-поло', 'Мужчинам/Халаты',
    'Мужчинам/Шорты', 'Обувь/Аксессуары для обуви', 'Обувь/Детская', 'Обувь/Для новорожденных', 'Обувь/Женская',
    'Обувь/Мужская', 'Обувь/Ортопедическая обувь', 'Продукты/Бакалея', 'Продукты/Вкусные подарки', 'Продукты/Детское питание',
    'Продукты/Добавки пищевые', 'Продукты/Замороженная продукция', 'Продукты/Здоровое питание', 'Продукты/Молочные продукты и яйца', 'Продукты/Мясная продукция',
    'Продукты/Напитки', 'Продукты/Овощи', 'Продукты/Сладости и хлебобулочные изделия', 'Продукты/Снеки', 'Продукты/Фрукты и ягоды',
    'Продукты/Чай и кофе', 'Сад и дача/Бассейны', 'Сад и дача/Горшки, опоры и все для рассады', 'Сад и дача/Грили, мангалы и барбекю', 'Сад и дача/Дачные умывальники, души и туалеты',
    'Сад и дача/Полив и водоснабжение', 'Сад и дача/Растения, семена и грунты', 'Сад и дача/Садовая мебель', 'Сад и дача/Садовая техника', 'Сад и дача/Садовый декор',
    'Сад и дача/Садовый инструмент', 'Сад и дача/Теплицы, парники, укрывной материал', 'Сад и дача/Товары для бани и сауны', 'Сад и дача/Товары для кемпинга, пикника и отдыха', 'Сад и дача/Удобрения, химикаты и средства защиты',
    'Спорт/Велоспорт', 'Спорт/Водные виды спорта', 'Спорт/Для детей', 'Спорт/Для женщин', 'Спорт/Для мужчин',
    'Спорт/Единоборства', 'Спорт/Зимние виды спорта', 'Спорт/Командные виды спорта', 'Спорт/Конный спорт', 'Спорт/Оборудование для сдачи нормативов',
    'Спорт/Охота и рыбалка', 'Спорт/Парусный спорт', 'Спорт/Поддержка и восстановление', 'Спорт/Спортивная обувь', 'Спорт/Спортивное питание и косметика',
    'Спорт/Страйкбол и пейнтбол', 'Спорт/Товары для самообороны', 'Спорт/Фитнес и тренажеры', 'Спорт/Электроника', 'Товары для взрослых/Белье и аксессуары',
    'Товары для взрослых/Игры и сувениры', 'Товары для взрослых/Интимная косметика', 'Товары для взрослых/Интимная съедобная косметика', 'Товары для взрослых/Презервативы и лубриканты', 'Товары для взрослых/Секс игрушки',
    'Товары для взрослых/Фетиш и БДСМ', 'Электроника/Детская электроника', 'Электроника/Игровые консоли и игры', 'Электроника/Кабели и зарядные устройства', 'Электроника/Музыка и видео',
    'Электроника/Ноутбуки и компьютеры', 'Электроника/Офисная техника', 'Электроника/Развлечения и гаджеты', 'Электроника/Сетевое оборудование', 'Электроника/Системы безопасности',
    'Электроника/Смарт-часы и браслеты', 'Электроника/Смартфоны и телефоны', 'Электроника/Солнечные электростанции и комплектующие', 'Электроника/ТВ, Аудио, Фото, Видео техника', 'Электроника/Торговое оборудование',
    'Электроника/Умный дом', 'Электроника/Электротранспорт и аксессуары', 'Ювелирные изделия/Аксессуары для украшений', 'Ювелирные изделия/Браслеты', 'Ювелирные изделия/Броши',
    'Ювелирные изделия/Зажимы, запонки, ремни', 'Ювелирные изделия/Колье, цепи, шнурки', 'Ювелирные изделия/Кольца', 'Ювелирные изделия/Комплекты', 'Ювелирные изделия/Пирсинг',
    'Ювелирные изделия/Подвески и шармы', 'Ювелирные изделия/Серьги', 'Ювелирные изделия/Сувениры и столовое серебро','Ювелирные изделия/Украшения из золота','Ювелирные изделия/Украшения из керамики','Ювелирные изделия/Украшения из серебра','Ювелирные изделия/Часы','Ювелирные изделия/Четки']



categories_ozon = ['Автотовары/Автоаксессуары и принадлежности', 'Автотовары/Автозапчасти', 'Автотовары/Автозвук', 'Автотовары/Аккумуляторы и аксессуары',
                   'Автотовары/Инструменты и оборудование', 'Автотовары/Каталог ТО', 'Автотовары/Масла и автохимия',
                   'Автотовары/Товары для мототехники,  мотоэкипировка', 'Автотовары/Уход за автомобилем', 'Автотовары/Шины и диски',
                   'Автотовары/Электроника для авто', 'Антиквариат и коллекционирование/Антикварная мебель', 'Антиквариат и коллекционирование/Антикварная посуда',
                   'Антиквариат и коллекционирование/Винтажная галантерея', 'Антиквариат и коллекционирование/Винтажные предметы интерьера',
                   'Антиквариат и коллекционирование/Винтажные украшения', 'Антиквариат и коллекционирование/Коллекционирование',
                   'Антиквариат и коллекционирование/Старинные гравюры, карты, открытки', 'Антиквариат и коллекционирование/Сумки и часы',
                   'Аптека/Витамины, БАДы и пищевые добавки', 'Аптека/Гигиена полости рта', 'Аптека/Лекарственные средства', 'Аптека/Линзы, очки, аксессуары',
                   'Аптека/Личная гигиена', 'Аптека/Медицинская мебель', 'Аптека/Медицинская одежда', 'Аптека/Медицинские изделия', 'Аптека/Медицинские приборы',
                   'Аптека/Ортопедия', 'Аптека/Ручные массажеры и иппликаторы', 'Бытовая техника/Климатическая техника', 'Бытовая техника/Крупная бытовая техника',
                   'Бытовая техника/Техника для дома', 'Бытовая техника/Техника для красоты и здоровья', 'Бытовая техника/Техника для кухни',
                   'Бытовая химия/Карандаши для чистки утюгов', 'Бытовая химия/Освежители и ароматизаторы', 'Бытовая химия/Средства для мытья посуды',
                   'Бытовая химия/Средства для посудомоечных машин', 'Бытовая химия/Средства для смягчения воды', 'Бытовая химия/Средства для стирки',
                   'Бытовая химия/Средства для ухода за бытовой техникой', 'Бытовая химия/Средства для чистки кофемашины',
                   'Бытовая химия/Средства от насекомых и грызунов', 'Бытовая химия/Чистящие средства', 'Всё для игр/Mobile gaming',
                   'Всё для игр/Nintendo Switch', 'Всё для игр/PC', 'Всё для игр/PlayStation', 'Всё для игр/Xbox', 'Всё для игр/Геймпады',
                   'Всё для игр/Игровая атрибутика', 'Всё для игр/Игровые жанры', 'Всё для игр/Игровые приставки', 'Всё для игр/Игры для приставок',
                   'Всё для игр/Очки виртуальной реальности', 'Всё для игр/Ретро консоли', 'Детские товары/Детская комната',
                   'Детские товары/Детское питание', 'Детские товары/Игрушки и игры', 'Детские товары/Коляски и автокресла',
                   'Детские товары/Подгузники и гигиена', 'Детские товары/Спорт и игры на улице', 'Детские товары/Товары для кормления',
                   'Детские товары/Товары для мам', 'Детские товары/Товары для школы и обучения', 'Дом и сад/Дача и сад',
                   'Дом и сад/Декор и интерьер', 'Дом и сад/Освещение', 'Дом и сад/Посуда', 'Дом и сад/Текстиль', 'Дом и сад/Товары для бани и сауны',
                   'Дом и сад/Товары для курения', 'Дом и сад/Товары для праздников', 'Дом и сад/Хозяйственные товары', 'Дом и сад/Хранение вещей',
                   'Дом и сад/Цветы и растения', 'Канцелярские товары/Бумага', 'Канцелярские товары/Бумажная продукция',
                   'Канцелярские товары/Демонстрационные доски', 'Канцелярские товары/Калькуляторы', 'Канцелярские товары/Картриджи для лазерных принтеров',
                   'Канцелярские товары/Картриджи для струйных принтеров', 'Канцелярские товары/Настольные подставки и визитницы',
                   'Канцелярские товары/Оборудование для торговли', 'Канцелярские товары/Офисные принадлежности', 'Канцелярские товары/Папки и файлы',
                   'Канцелярские товары/Печати и штампы', 'Канцелярские товары/Письменные принадлежности', 'Канцелярские товары/Чертежные принадлежности',
                   'Красота и здоровье/Аппаратная косметология', 'Красота и здоровье/Ароматерапия', 'Красота и здоровье/Гигиена полости рта',
                   'Красота и здоровье/Макияж', 'Красота и здоровье/Маникюр и педикюр', 'Красота и здоровье/Оборудование и материалы для тату-салона',
                   'Красота и здоровье/Парфюмерия', 'Красота и здоровье/Уход за волосами', 'Красота и здоровье/Уход за лицом',
                   'Красота и здоровье/Уход за телом', 'Мебель/Детская мебель', 'Мебель/Мебель для ванной', 'Мебель/Мебельные гарнитуры и комплекты',
                   'Мебель/Мебельные модули', 'Мебель/Мягкая мебель', 'Мебель/Полки и стеллажи', 'Мебель/Садовая мебель', 'Мебель/Сейфы',
                   'Мебель/Столы и стулья', 'Мебель/Шкафы, тумбы и комоды', 'Музыка и видео/Виниловые пластинки', 'Одежда, обувь и аксессуары/Аксессуары',
                   'Одежда, обувь и аксессуары/Детям', 'Одежда, обувь и аксессуары/Женщинам', 'Одежда, обувь и аксессуары/Мужчинам',
                   'Одежда, обувь и аксессуары/Путешествия', 'Одежда, обувь и аксессуары/Средства для ухода за обувью',
                   'Одежда, обувь и аксессуары/Средства для ухода за одеждой', 'Продукты питания/Замороженные продукты',
                   'Продукты питания/Колбасы, сосиски, деликатесы', 'Продукты питания/Консервация', 'Продукты питания/Макароны, крупы, мука',
                   'Продукты питания/Масла, соусы, специи', 'Продукты питания/Молочные продукты и яйца', 'Продукты питания/Мясо и птица',
                   'Продукты питания/Овощи, фрукты, зелень', 'Продукты питания/Орехи, снэки', 'Продукты питания/Рыба, морепродукты',
                   'Продукты питания/Соки, воды, напитки', 'Продукты питания/Хлеб, выпечка, сладости', 'Продукты питания/Чай, кофе, какао',
                   'Спортивные товары/Активные виды отдыха', 'Спортивные товары/Виды спорта', 'Спортивные товары/Зимний спорт',
                   'Спортивные товары/Командные виды спорта', 'Спортивные товары/Одежда и обувь для спорта', 'Спортивные товары/Рыбалка и охота',
                   'Спортивные товары/Спортивная защита и экипировка', 'Спортивные товары/Спортивное питание', 'Спортивные товары/Тренажеры и фитнес',
                   'Спортивные товары/Туризм и отдых на природе', 'Строительство и ремонт/Вентиляция', 'Строительство и ремонт/Водоснабжение',
                   'Строительство и ремонт/Двери, окна, элементы домов', 'Строительство и ремонт/Инструменты', 'Строительство и ремонт/Краски, лаки и растворители',
                   'Строительство и ремонт/Крепеж и фурнитура', 'Строительство и ремонт/Отопление', 'Строительство и ремонт/Сантехника',
                   'Строительство и ремонт/Сауны и бани', 'Строительство и ремонт/Спецодежда и средства индивидуальной защиты',
                   'Строительство и ремонт/Строительные и отделочные материалы', 'Строительство и ремонт/Электрика', 'Супермаркет Экспресс/Бытовая химия',
                   'Супермаркет Экспресс/Детские товары', 'Супермаркет Экспресс/Дом и сад', 'Супермаркет Экспресс/Канцелярские товары',
                   'Супермаркет Экспресс/Красота и здоровье', 'Супермаркет Экспресс/Одежда, обувь и аксессуары', 'Супермаркет Экспресс/Продукты питания',
                   'Супермаркет Экспресс/Товары для животных', 'Супермаркет Экспресс/Хобби и творчество', 'Товары для взрослых/Аксессуары для взрослых',
                   'Товары для взрослых/Интимная косметика', 'Товары для взрослых/Секс игрушки', 'Товары для взрослых/Товары для БДСМ',
                   'Товары для взрослых/Эротические игры', 'Товары для взрослых/Эротические сувениры', 'Товары для взрослых/Эротическое белье и костюмы',
                   'Товары для животных/Ветаптека', 'Товары для животных/Гигиена', 'Товары для животных/Для грызунов', 'Товары для животных/Для кошек',
                   'Товары для животных/Для лошадей', 'Товары для животных/Для птиц', 'Товары для животных/Для рыб и рептилий', 'Товары для животных/Для собак',
                   'Товары для животных/Инкубаторы для яиц', 'Хобби и творчество/Аппликации', 'Хобби и творчество/Барельефы и витражи',
                   'Хобби и творчество/Выжигание, поделки из дерева', 'Хобби и творчество/Гадания и эзотерика', 'Хобби и творчество/Гравюры',
                   'Хобби и творчество/Изготовление игрушек', 'Хобби и творчество/Изготовление косметики и духов', 'Хобби и творчество/Изготовление свечей',
                   'Хобби и творчество/Лепка', 'Хобби и творчество/Моделирование', 'Хобби и творчество/Мозаика и фреска', 'Хобби и творчество/Музыкальные инструменты',
                   'Хобби и творчество/Мыловарение', 'Хобби и творчество/Наклейки', 'Хобби и творчество/Настольные и карточные игры', 'Хобби и творчество/Оригами',
                   'Хобби и творчество/Пазлы и головоломки', 'Хобби и творчество/Раскрашивание и роспись', 'Хобби и творчество/Рисование', 'Хобби и творчество/Рукоделие',
                   'Хобби и творчество/Создание картин, фоторамок, открыток', 'Хобби и творчество/Фокусы', 'Цифровые товары/Игры, развлечения',
                   'Цифровые товары/Программное обеспечение', 'Цифровые товары/Электронные подарочные сертификаты', 'Электроника/Аксессуары для электроники',
                   'Электроника/Игровые приставки и компьютеры', 'Электроника/Квадрокоптеры и аксессуары', 'Электроника/Компьютеры и комплектующие',
                   'Электроника/Моноблоки и системные блоки', 'Электроника/Навигаторы', 'Электроника/Наушники и аудиотехника',
                   'Электроника/Ноутбуки, планшеты и электронные книги', 'Электроника/Оптические приборы', 'Электроника/Офисная техника',
                   'Электроника/Телевизоры и видеотехника', 'Электроника/Телефоны и смарт-часы', 'Электроника/Умный дом и безопасность',
                   'Электроника/Фото- и видеокамеры', 'Электроника/Часы и электронные будильники', 'Электроника/Электронные сигареты и системы нагревания',
                   'Ювелирные украшения/Браслеты', 'Ювелирные украшения/Броши', 'Ювелирные украшения/Детские ювелирные изделия', 'Ювелирные украшения/Зажимы',
                   'Ювелирные украшения/Запонки', 'Ювелирные украшения/Кольца', 'Ювелирные украшения/Комплекты украшений', 'Ювелирные украшения/Пирсинг',
                   'Ювелирные украшения/Религиозные ювелирные изделия', 'Ювелирные украшения/Серьги', 'Ювелирные украшения/Средства для ухода',
                   'Ювелирные украшения/Сувениры', 'Ювелирные украшения/Украшения на шею', 'Ювелирные украшения/Часы', 'Ювелирные украшения/Шармы']


month_names = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
    5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
    9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", 
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

# __________________ Выбор режима работы с загрузкой данных с вб (выполняется через API, но зато можно посмотреть, каких данных нет и сообщить нам об ошибке
# platform = st.sidebar.selectbox("Выберите платформу", ['Wildberries', 'Ozon'])
# if platform == 'Wildberries':
#     report_type = st.sidebar.radio("Выберите тип отчета", ['Данные по категориям', 'Топ продуктов'])
#     if report_type == 'Данные по категориям':
        # categories = get_wb_categories()

# __________________ Выбор режима работы (обработка из списка)

platform = st.sidebar.selectbox("Выберите платформу", ['Wildberries', 'Ozon'])
if platform == 'Wildberries':
 report_type = st.sidebar.selectbox("Выберите тип отчета", ['Данные по категории', 'Топовые категории'])
 if report_type == 'Данные по категории':
  if categories_wb:
     selected_path = st.selectbox('Выберите категорию Wildberries:', categories_wb)

  if selected_path: # in seasonal_results_wb:
      st.write('Данные для выбранной категории:')
      results = seasonal_results_wb[selected_path]
  
      # Разбивка результатов на отдельные части
      (monthly_sales_totals_2020, monthly_sales_totals_2021, monthly_sales_totals_2022, monthly_sales_totals_2023,
       total_sales_2020, total_sales_2021, total_sales_2022, total_sales_2023,
       avg_monthly_sales,
       monthly_revenue_totals_2020, monthly_revenue_totals_2021, monthly_revenue_totals_2022, monthly_revenue_totals_2023,
       total_revenue_2020, total_revenue_2021, total_revenue_2022, total_revenue_2023,
       avg_monthly_revenue, share_of_sales_2020, share_of_sales_2021, share_of_sales_2022, share_of_sales_2023,share_of_revenue_2020, share_of_revenue_2021, 
       share_of_revenue_2022, share_of_revenue_2023, avg_monthly_sales_share, avg_monthly_revenue_share, monthly_bills_totals_2020, monthly_bills_totals_2021, monthly_bills_totals_2022, monthly_bills_totals_2023,
       avg_bills_2020, avg_bills_2021, avg_bills_2022, avg_bills_2023,
       deviation_monthly_bills_2020, deviation_monthly_bills_2021, deviation_monthly_bills_2022, deviation_monthly_bills_2023,
       deviation_percent_monthly_bills_2020, deviation_percent_monthly_bills_2021, deviation_percent_monthly_bills_2022, deviation_percent_monthly_bills_2023) = results
  
      # Создание DataFrame для продаж
      sales_data = pd.DataFrame({
          '2020': monthly_sales_totals_2020,
          '2021': monthly_sales_totals_2021,
          '2022': monthly_sales_totals_2022,
          '2023': monthly_sales_totals_2023,
          'AVG': avg_monthly_sales
      }, index= months)

      # Создание df для доли продаж
      sales_share_data = pd.DataFrame({
          '2020, %': share_of_sales_2020,
          '2021, %': share_of_sales_2021,
          '2022, %': share_of_sales_2022,
          '2023, %': share_of_sales_2023,
          'AVG, %': avg_monthly_sales_share
      }, index = months)


      # Создание DataFrame для всего
      total_data = pd.DataFrame({
          'Total Sales': [total_sales_2020, total_sales_2021, total_sales_2022, total_sales_2023],
          'Total Revenue': [total_revenue_2020, total_revenue_2021, total_revenue_2022, total_revenue_2023],
          'Avg Bill': [avg_bills_2020, avg_bills_2021, avg_bills_2022, avg_bills_2023]
      }, index=[2020, 2021, 2022, 2023])


     # Создание DataFrame для средних чеков
      bills_data = pd.DataFrame({
          '2020': monthly_bills_totals_2020 , #deviation_monthly_bills_2020, deviation_percent_monthly_bills_2020,
          '2021': monthly_bills_totals_2021 , #deviation_monthly_bills_2021, deviation_percent_monthly_bills_2021,
          '2022': monthly_bills_totals_2022 , #deviation_monthly_bills_2022, deviation_percent_monthly_bills_2022,
          '2023': monthly_bills_totals_2023  #deviation_monthly_bills_2023, deviation_percent_monthly_bills_2023
      }, index=months)


      # bills_data = pd.DataFrame({
      #  '2020': monthly_bills_totals_2020 + deviation_monthly_bills_2020 + deviation_percent_monthly_bills_2020,
      #  '2021': monthly_bills_totals_2021 + deviation_monthly_bills_2021 + deviation_percent_monthly_bills_2021,
      #  '2022': monthly_bills_totals_2022 + deviation_monthly_bills_2022 + deviation_percent_monthly_bills_2022,
      #  '2023': monthly_bills_totals_2023 + deviation_monthly_bills_2023 + deviation_percent_monthly_bills_2023
      # }, index=months)
  
      # Создание DataFrame для выручки
      revenue_data = pd.DataFrame({
          '2020': monthly_revenue_totals_2020,
          '2021': monthly_revenue_totals_2021,
          '2022': monthly_revenue_totals_2022,
          '2023': monthly_revenue_totals_2023,
          'AVG': avg_monthly_revenue
      }, index= months)

      # Создание df для доли выручки
      revenue_share_data = pd.DataFrame({
          '2020, %': share_of_revenue_2020,
          '2021, %': share_of_revenue_2021,
          '2022, %': share_of_revenue_2022,
          '2023, %': share_of_revenue_2023,
          'AVG, %': avg_monthly_revenue_share
      }, index = months)

   

        # Графики
      fig_sales = plot_data(sales_data, 'Распределение продаж по месяцам')
      fig_revenue = plot_data(revenue_data, 'Распределение выручки по месяцам')
      fig_sales_share = plot_data(sales_share_data, 'Распределение продаж по месяцам по долям')
      fig_revenue_share = plot_data(revenue_share_data, 'Распределение выручки по месяцам по долям')
      fig_bills = plot_data(bills_data, 'Значения среднего чека по месяцам')
      fig_total_sales, fig_total_revenue, fig_combined = plot_total_data(total_data)

  
      # Вывод DataFrame в Streamlit
      st.write("Продажи:")
      st.dataframe(sales_data)
      st.plotly_chart(fig_sales)

      st.write("Продажи по долям:")
      st.dataframe(sales_share_data)
      st.plotly_chart(fig_sales_share)
      
      
      st.write("Выручка:")
      st.dataframe(revenue_data)
      st.plotly_chart(fig_revenue)

      st.write("Выручка по долям:")
      st.dataframe(revenue_share_data)
      st.plotly_chart(fig_revenue_share)
      
      st.write("Средний чек:")
      st.dataframe(bills_data)
      st.plotly_chart(fig_bills)

      st.write("Общая сумма продаж и выручки по годам:")
      st.dataframe(total_data)
      st.plotly_chart(fig_total_sales)
      st.plotly_chart(fig_total_revenue)
      st.plotly_chart(fig_combined)           
 
 
 elif report_type == 'Топовые категории':
    top_n = st.sidebar.selectbox("Выберите количество подкатегорий", [10, 20, 50, 100])
    start_month_name = st.sidebar.selectbox("Выберите начальный месяц", list(month_names.values()))
    end_month_name = st.sidebar.selectbox("Выберите конечный месяц", list(month_names.values()))
 
    start_month = next(key for key, value in month_names.items() if value == start_month_name)
    end_month = next(key for key, value in month_names.items() if value == end_month_name)
 
    # Формируем список месяцев для анализа
    period_range = list(range(start_month, end_month + 1))
    # Обработка данных для продаж
    sales_wb_top_months = final_obrabotka(sales_wb_top)
    selected_columns_sales = sales_wb_top_months.loc[:, start_month_name:end_month_name]
    new_column_name_sales = f'{start_month_name} - {end_month_name}, % (Продажи)'
    sales_wb_top_months[new_column_name_sales] = selected_columns_sales.sum(axis=1)
    top_sales_values = sales_wb_top_months[new_column_name_sales].nlargest(top_n)
    st.write("Топ категорий по продажвм:", round(top_sales_values, 1))
    
    # Обработка данных для дохода
    revenue_wb_top_months = final_obrabotka(revenue_wb_top)
    selected_columns_revenue = revenue_wb_top_months.loc[:, start_month_name:end_month_name]
    new_column_name_revenue = f'{start_month_name} - {end_month_name}, % (Выручка)'
    revenue_wb_top_months[new_column_name_revenue] = selected_columns_revenue.sum(axis=1)
    top_revenue_values = revenue_wb_top_months[new_column_name_revenue].nlargest(top_n)
    st.write("Топ категорий по выручке:", round(top_revenue_values, 1))

    unique_categories = pd.Index(top_sales_values.index.union(top_revenue_values.index))
    unique_categories = unique_categories.map(lambda x: x.replace('_', '/')).tolist()
    
    selected_category = st.selectbox("Выберите категорию для более подробной информации", unique_categories)
    
    if selected_category:
        st.write(f'Данные для выбранной категории: {selected_category}')
    
        if selected_category in seasonal_results_wb:
            results = seasonal_results_wb[selected_category]
            (monthly_sales_totals_2020, monthly_sales_totals_2021, monthly_sales_totals_2022, monthly_sales_totals_2023,
            total_sales_2020, total_sales_2021, total_sales_2022, total_sales_2023,
            avg_monthly_sales,
            monthly_revenue_totals_2020, monthly_revenue_totals_2021, monthly_revenue_totals_2022, monthly_revenue_totals_2023,
            total_revenue_2020, total_revenue_2021, total_revenue_2022, total_revenue_2023,
            avg_monthly_revenue, share_of_sales_2020, share_of_sales_2021, share_of_sales_2022, share_of_sales_2023,share_of_revenue_2020, share_of_revenue_2021, 
            share_of_revenue_2022, share_of_revenue_2023, avg_monthly_sales_share, avg_monthly_revenue_share, monthly_bills_totals_2020, monthly_bills_totals_2021, monthly_bills_totals_2022, monthly_bills_totals_2023,
            avg_bills_2020, avg_bills_2021, avg_bills_2022, avg_bills_2023,
            deviation_monthly_bills_2020, deviation_monthly_bills_2021, deviation_monthly_bills_2022, deviation_monthly_bills_2023,
            deviation_percent_monthly_bills_2020, deviation_percent_monthly_bills_2021, deviation_percent_monthly_bills_2022, deviation_percent_monthly_bills_2023) = results
            
    
            # Создание DataFrame для продаж
            sales_data = pd.DataFrame({
                '2020': monthly_sales_totals_2020,
                '2021': monthly_sales_totals_2021,
                '2022': monthly_sales_totals_2022,
                '2023': monthly_sales_totals_2023,
                'AVG': avg_monthly_sales
            }, index=months)
        
              # Создание df для доли продаж
            sales_share_data = pd.DataFrame({
                '2020, %': share_of_sales_2020,
                '2021, %': share_of_sales_2021,
                '2022, %': share_of_sales_2022,
                '2023, %': share_of_sales_2023,
                'AVG, %': avg_monthly_sales_share
            }, index = months)
        
            # Создание DataFrame для общей суммы продаж
            total_data = pd.DataFrame({
                'Total Sales': [total_sales_2020, total_sales_2021, total_sales_2022, total_sales_2023],
                'Total Revenue': [total_revenue_2020, total_revenue_2021, total_revenue_2022, total_revenue_2023]
            }, index=[2020, 2021, 2022, 2023])
        
            # Создание DataFrame для выручки
            revenue_data = pd.DataFrame({
                '2020': monthly_revenue_totals_2020,
                '2021': monthly_revenue_totals_2021,
                '2022': monthly_revenue_totals_2022,
                '2023': monthly_revenue_totals_2023,
                'AVG': avg_monthly_revenue
            }, index=months)
        
             # Создание df для доли выручки
            revenue_share_data = pd.DataFrame({
                '2020, %': share_of_revenue_2020,
                '2021, %': share_of_revenue_2021,
                '2022, %': share_of_revenue_2022,
                '2023, %': share_of_revenue_2023,
                'AVG, %': avg_monthly_revenue_share
            }, index = months)


         # Создание DataFrame для средних чеков
            bills_data = pd.DataFrame({
                '2020': monthly_bills_totals_2020, #deviation_monthly_bills_2020, deviation_percent_monthly_bills_2020,
                '2021': monthly_bills_totals_2021, #deviation_monthly_bills_2021, deviation_percent_monthly_bills_2021,
                '2022': monthly_bills_totals_2022, #deviation_monthly_bills_2022, deviation_percent_monthly_bills_2022,
                '2023': monthly_bills_totals_2023  #deviation_monthly_bills_2023, deviation_percent_monthly_bills_2023
            }, index=months)

        
              # Графики
            fig_sales = plot_data(sales_data, 'Распределение продаж по месяцам')
            fig_revenue = plot_data(revenue_data, 'Распределение выручки по месяцам')
            fig_sales_share = plot_data(sales_share_data, 'Распределение продаж по месяцам по долям')
            fig_revenue_share = plot_data(revenue_share_data, 'Распределение выручки по месяцам по долям')
            fig_bills = plot_data(bills_data, 'Значения среднего чека по месяцам')
            fig_total_sales, fig_total_revenue, fig_combined = plot_total_data(total_data)
        
        
            # Вывод DataFrame в Streamlit
            st.write("Продажи:")
            st.dataframe(sales_data)
            st.plotly_chart(fig_sales)
        
            st.write("Продажи по долям:")
            st.dataframe(sales_share_data)
            st.plotly_chart(fig_sales_share)
            
            st.write("Выручка:")
            st.dataframe(revenue_data)
            st.plotly_chart(fig_revenue)
        
            st.write("Выручка по долям:")
            st.dataframe(revenue_share_data)
            st.plotly_chart(fig_revenue_share)

            st.write("Средний чек:")
            st.dataframe(bills_data)
            st.plotly_chart(fig_bills)
        
            st.write("Общая сумма продаж и выручки по годам:")
            st.dataframe(total_data)
            st.plotly_chart(fig_total_sales)
            st.plotly_chart(fig_total_revenue)
            st.plotly_chart(fig_combined)



    # # скрипт с выбором метрики для анализа
    # metric = st.sidebar.radio("Выберите метрику для анализа", ('sales', 'revenue'))
    # sales_wb_top_months = final_obrabotka(sales_wb_top)
    # revenue_wb_top_months = final_obrabotka(revenue_wb_top)
    # if metric == 'sales':
    #     # Выбираем нужные столбцы
    #     selected_columns = sales_wb_top_months.loc[:, start_month_name:end_month_name]
    #     # название промежуточного столбца
    #     new_column_name = f'{start_month_name} - {end_month_name}, %'
    #     # Создаем новый столбец, в котором будут суммы значений по строкам выбранных столбцов
    #     sales_wb_top_months[new_column_name] = selected_columns.sum(axis=1)
    #     # Находим наибольшие значения в столбце
    #     top_values = sales_wb_top_months[new_column_name].nlargest(top_n)
    #     st.write(round(top_values, 1))
    # elif metric == 'revenue':
    #     # Выбираем нужные столбцы
    #     selected_columns = revenue_wb_top_months.loc[:, start_month_name:end_month_name]
    #     # название промежуточного столбца
    #     new_column_name = f'{start_month_name} - {end_month_name}, %'
    #     # Создаем новый столбец, в котором будут суммы значений по строкам выбранных столбцов
    #     revenue_wb_top_months[new_column_name] = selected_columns.sum(axis=1)
    #     # Находим наибольшие значения в столбце
    #     top_values = revenue_wb_top_months[new_column_name].nlargest(top_n)
    #     st.write(round(top_values, 1))
 

 
 # # =====================
elif platform == 'Ozon':
 report_type = st.sidebar.radio("Выберите тип отчета", ['Данные по категории', 'Топовые категории'])
 if report_type == 'Данные по категории':
     if categories_ozon:
         selected_path = st.selectbox('Выберите категорию Ozon:', categories_ozon)
 
     st.write('Данные для выбранной категории:')
     results_ozon = seasonal_results_ozon[selected_path]
 
     # Разбивка результатов на отдельные части
     (monthly_sales_totals_2020_ozon, monthly_sales_totals_2021_ozon, monthly_sales_totals_2022_ozon, monthly_sales_totals_2023_ozon,
     total_sales_2020_ozon, total_sales_2021_ozon, total_sales_2022_ozon, total_sales_2023_ozon,
     avg_monthly_sales_ozon,
     monthly_revenue_totals_2020_ozon, monthly_revenue_totals_2021_ozon, monthly_revenue_totals_2022_ozon, monthly_revenue_totals_2023_ozon,
     total_revenue_2020_ozon, total_revenue_2021_ozon, total_revenue_2022_ozon, total_revenue_2023_ozon,
     avg_monthly_revenue_ozon, share_of_sales_2020_ozon, share_of_sales_2021_ozon, 
     share_of_sales_2022_ozon, share_of_sales_2023_ozon,share_of_revenue_2020_ozon, share_of_revenue_2021_ozon, share_of_revenue_2022_ozon, share_of_revenue_2023_ozon, avg_monthly_sales_share_ozon, avg_monthly_revenue_share_ozon,
     monthly_bills_totals_2020_ozon, monthly_bills_totals_2021_ozon, monthly_bills_totals_2022_ozon, monthly_bills_totals_2023_ozon,
     avg_bills_2020_ozon, avg_bills_2021_ozon, avg_bills_2022_ozon, avg_bills_2023_ozon,
     deviation_monthly_bills_2020_ozon, deviation_monthly_bills_2021_ozon, deviation_monthly_bills_2022_ozon, deviation_monthly_bills_2023_ozon,
     deviation_percent_monthly_bills_2020_ozon, deviation_percent_monthly_bills_2021_ozon, deviation_percent_monthly_bills_2022_ozon, deviation_percent_monthly_bills_2023_ozon) = results_ozon
 
     # Создание DataFrame для продаж
     sales_data = pd.DataFrame({
         '2020': monthly_sales_totals_2020_ozon,
         '2021': monthly_sales_totals_2021_ozon,
         '2022': monthly_sales_totals_2022_ozon,
         '2023': monthly_sales_totals_2023_ozon,
         'AVG': avg_monthly_sales_ozon
     }, index=months)
 
       # Создание df для доли продаж
     sales_share_data = pd.DataFrame({
         '2020, %': share_of_sales_2020_ozon,
         '2021, %': share_of_sales_2021_ozon,
         '2022, %': share_of_sales_2022_ozon,
         '2023, %': share_of_sales_2023_ozon,
         'AVG, %': avg_monthly_sales_share_ozon
     }, index = months)
 
     # Создание DataFrame для общей суммы продаж
     total_data = pd.DataFrame({
         'Total Sales': [total_sales_2020_ozon, total_sales_2021_ozon, total_sales_2022_ozon, total_sales_2023_ozon],
         'Total Revenue': [total_revenue_2020_ozon, total_revenue_2021_ozon, total_revenue_2022_ozon, total_revenue_2023_ozon]
     }, index=[2020, 2021, 2022, 2023])
 
     # Создание DataFrame для выручки
     revenue_data = pd.DataFrame({
         '2020': monthly_revenue_totals_2020_ozon,
         '2021': monthly_revenue_totals_2021_ozon,
         '2022': monthly_revenue_totals_2022_ozon,
         '2023': monthly_revenue_totals_2023_ozon,
         'AVG': avg_monthly_revenue_ozon
     }, index=months)
 
      # Создание df для доли выручки
     revenue_share_data = pd.DataFrame({
         '2020, %': share_of_revenue_2020_ozon,
         '2021, %': share_of_revenue_2021_ozon,
         '2022, %': share_of_revenue_2022_ozon,
         '2023, %': share_of_revenue_2023_ozon,
         'AVG, %': avg_monthly_revenue_share_ozon
     }, index = months)



  # Создание DataFrame для средних чеков
     bills_data = pd.DataFrame({
         '2020': monthly_bills_totals_2020_ozon, #deviation_monthly_bills_2020, deviation_percent_monthly_bills_2020,
         '2021': monthly_bills_totals_2021_ozon, #deviation_monthly_bills_2021, deviation_percent_monthly_bills_2021,
         '2022': monthly_bills_totals_2022_ozon, #deviation_monthly_bills_2022, deviation_percent_monthly_bills_2022,
         '2023': monthly_bills_totals_2023_ozon  #deviation_monthly_bills_2023, deviation_percent_monthly_bills_2023
     }, index=months)
 
       # Графики
     fig_sales = plot_data(sales_data, 'Распределение продаж по месяцам')
     fig_revenue = plot_data(revenue_data, 'Распределение выручки по месяцам')
     fig_sales_share = plot_data(sales_share_data, 'Распределение продаж по месяцам по долям')
     fig_revenue_share = plot_data(revenue_share_data, 'Распределение выручки по месяцам по долям')
     fig_bills = plot_data(bills_data, 'Значения среднего чека по месяцам')
     fig_total_sales, fig_total_revenue, fig_combined = plot_total_data(total_data)
 
 
     # Вывод DataFrame в Streamlit
     st.write("Продажи:")
     st.dataframe(sales_data)
     st.plotly_chart(fig_sales)
 
     st.write("Продажи по долям:")
     st.dataframe(sales_share_data)
     st.plotly_chart(fig_sales_share)
     
     st.write("Выручка:")
     st.dataframe(revenue_data)
     st.plotly_chart(fig_revenue)
 
     st.write("Выручка по долям:")
     st.dataframe(revenue_share_data)
     st.plotly_chart(fig_revenue_share)

     st.write("Средний чек:")
     st.dataframe(bills_data)
     st.plotly_chart(fig_bills)
     
     st.write("Общая сумма продаж и выручки по годам:")
     st.dataframe(total_data)
     st.plotly_chart(fig_total_sales)
     st.plotly_chart(fig_total_revenue)
     st.plotly_chart(fig_combined)    
 
 elif report_type == 'Топовые категории':
      top_n = st.sidebar.selectbox("Выберите количество подкатегорий", [10, 20, 50, 100])
      start_month_name = st.sidebar.selectbox("Выберите начальный месяц", list(month_names.values()))
      end_month_name = st.sidebar.selectbox("Выберите конечный месяц", list(month_names.values()))
  
      start_month = next(key for key, value in month_names.items() if value == start_month_name)
      end_month = next(key for key, value in month_names.items() if value == end_month_name)
  
      
      period_range = list(range(start_month, end_month + 1))
      # Обработка данных для продаж
      sales_ozon_top_months = final_obrabotka(sales_ozon_top)
      selected_columns_sales = sales_ozon_top_months.loc[:, start_month_name:end_month_name]
      new_column_name_sales = f'{start_month_name} - {end_month_name}, % (Продажи)'
      sales_ozon_top_months[new_column_name_sales] = selected_columns_sales.sum(axis=1)
      top_sales_values = sales_ozon_top_months[new_column_name_sales].nlargest(top_n)
      st.write("Топ категорий по продажам:", round(top_sales_values, 1))
      
      # Обработка данных для выручки
      revenue_ozon_top_months = final_obrabotka(revenue_ozon_top)
      selected_columns_revenue = revenue_ozon_top_months.loc[:, start_month_name:end_month_name]
      new_column_name_revenue = f'{start_month_name} - {end_month_name}, % (Выручка)'
      revenue_ozon_top_months[new_column_name_revenue] = selected_columns_revenue.sum(axis=1)
      top_revenue_values = revenue_ozon_top_months[new_column_name_revenue].nlargest(top_n)
      st.write("Топ категорий по выручке:", round(top_revenue_values, 1))

  # Формирование списка категорий для выпадающего списка и графиков===========================
      unique_categories = pd.Index(top_sales_values.index.union(top_revenue_values.index))
      unique_categories = unique_categories.map(lambda x: x.replace('_', '/')).tolist()
      
      selected_category = st.selectbox("Выберите категорию для более подробной информации", unique_categories)
      
      if selected_category:
          st.write(f'Данные для выбранной категории: {selected_category}')
      
          if selected_category in seasonal_results_ozon:
              results_ozon = seasonal_results_ozon[selected_category]
              (monthly_sales_totals_2020_ozon, monthly_sales_totals_2021_ozon, monthly_sales_totals_2022_ozon, monthly_sales_totals_2023_ozon,
               total_sales_2020_ozon, total_sales_2021_ozon, total_sales_2022_ozon, total_sales_2023_ozon,
               avg_monthly_sales_ozon,
               monthly_revenue_totals_2020_ozon, monthly_revenue_totals_2021_ozon, monthly_revenue_totals_2022_ozon, monthly_revenue_totals_2023_ozon,
               total_revenue_2020_ozon, total_revenue_2021_ozon, total_revenue_2022_ozon, total_revenue_2023_ozon,
               avg_monthly_revenue_ozon, share_of_sales_2020_ozon, share_of_sales_2021_ozon, 
               share_of_sales_2022_ozon, share_of_sales_2023_ozon,share_of_revenue_2020_ozon, share_of_revenue_2021_ozon, share_of_revenue_2022_ozon, share_of_revenue_2023_ozon, avg_monthly_sales_share_ozon, avg_monthly_revenue_share_ozon,
               monthly_bills_totals_2020_ozon, monthly_bills_totals_2021_ozon, monthly_bills_totals_2022_ozon, monthly_bills_totals_2023_ozon,
               avg_bills_2020_ozon, avg_bills_2021_ozon, avg_bills_2022_ozon, avg_bills_2023_ozon,
               deviation_monthly_bills_2020_ozon, deviation_monthly_bills_2021_ozon, deviation_monthly_bills_2022_ozon, deviation_monthly_bills_2023_ozon,
               deviation_percent_monthly_bills_2020_ozon, deviation_percent_monthly_bills_2021_ozon, deviation_percent_monthly_bills_2022_ozon, deviation_percent_monthly_bills_2023_ozon) = results_ozon
              
              # Вывод данных в Streamlit
              # Например, отображение общих продаж и выручки
              st.write(f"Общие продажи за 2020: {total_sales_2020_ozon}")
              st.write(f"Общая выручка за 2020: {total_revenue_2020_ozon}")
      
              # Создание DataFrame для продаж
              sales_data = pd.DataFrame({
                  '2020': monthly_sales_totals_2020_ozon,
                  '2021': monthly_sales_totals_2021_ozon,
                  '2022': monthly_sales_totals_2022_ozon,
                  '2023': monthly_sales_totals_2023_ozon,
                  'AVG': avg_monthly_sales_ozon
              }, index=months)
          
                # Создание df для доли продаж
              sales_share_data = pd.DataFrame({
                  '2020, %': share_of_sales_2020_ozon,
                  '2021, %': share_of_sales_2021_ozon,
                  '2022, %': share_of_sales_2022_ozon,
                  '2023, %': share_of_sales_2023_ozon,
                  'AVG, %': avg_monthly_sales_share_ozon
              }, index = months)
          
              # Создание DataFrame для общей суммы продаж
              total_data = pd.DataFrame({
                  'Total Sales': [total_sales_2020_ozon, total_sales_2021_ozon, total_sales_2022_ozon, total_sales_2023_ozon],
                  'Total Revenue': [total_revenue_2020_ozon, total_revenue_2021_ozon, total_revenue_2022_ozon, total_revenue_2023_ozon]
              }, index=[2020, 2021, 2022, 2023])
          
              # Создание DataFrame для выручки
              revenue_data = pd.DataFrame({
                  '2020': monthly_revenue_totals_2020_ozon,
                  '2021': monthly_revenue_totals_2021_ozon,
                  '2022': monthly_revenue_totals_2022_ozon,
                  '2023': monthly_revenue_totals_2023_ozon,
                  'AVG': avg_monthly_revenue_ozon
              }, index=months)
          
               # Создание df для доли выручки
              revenue_share_data = pd.DataFrame({
                  '2020, %': share_of_revenue_2020_ozon,
                  '2021, %': share_of_revenue_2021_ozon,
                  '2022, %': share_of_revenue_2022_ozon,
                  '2023, %': share_of_revenue_2023_ozon,
                  'AVG, %': avg_monthly_revenue_share_ozon
              }, index = months)


           # Создание DataFrame для средних чеков
              bills_data = pd.DataFrame({
                  '2020': monthly_bills_totals_2020_ozon, #deviation_monthly_bills_2020, deviation_percent_monthly_bills_2020,
                  '2021': monthly_bills_totals_2021_ozon, #deviation_monthly_bills_2021, deviation_percent_monthly_bills_2021,
                  '2022': monthly_bills_totals_2022_ozon, #deviation_monthly_bills_2022, deviation_percent_monthly_bills_2022,
                  '2023': monthly_bills_totals_2023_ozon  #deviation_monthly_bills_2023, deviation_percent_monthly_bills_2023
              }, index=months)

          
                # Графики
              fig_sales = plot_data(sales_data, 'Распределение продаж по месяцам')
              fig_revenue = plot_data(revenue_data, 'Распределение выручки по месяцам')
              fig_sales_share = plot_data(sales_share_data, 'Распределение продаж по месяцам по долям')
              fig_revenue_share = plot_data(revenue_share_data, 'Распределение выручки по месяцам по долям')
              fig_bills = plot_data(bills_data, 'Значения среднего чека по месяцам')
              fig_total_sales, fig_total_revenue, fig_combined = plot_total_data(total_data)
          
          
              # Вывод DataFrame в Streamlit
              st.write("Продажи:")
              st.dataframe(sales_data)
              st.plotly_chart(fig_sales)
          
              st.write("Продажи по долям:")
              st.dataframe(sales_share_data)
              st.plotly_chart(fig_sales_share)
              
              st.write("Выручка:")
              st.dataframe(revenue_data)
              st.plotly_chart(fig_revenue)
          
              st.write("Выручка по долям:")
              st.dataframe(revenue_share_data)
              st.plotly_chart(fig_revenue_share)

              st.write("Средний чек:")
              st.dataframe(bills_data)
              st.plotly_chart(fig_bills)
          
              st.write("Общая сумма продаж и выручки по годам:")
              st.dataframe(total_data)
              st.plotly_chart(fig_total_sales)
              st.plotly_chart(fig_total_revenue)
              st.plotly_chart(fig_combined)

if st.button('Выгрузить отчет'):
    st.session_state['is_downloading'] = True  # Установка флага загрузки

    data_to_export = prepare_data_for_excel(platform, report_type)
    
    # Создание файла Excel
    excel_file = BytesIO()  
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        if isinstance(data_to_export, dict):
            for sheet_name, dataframe in data_to_export.items():
                dataframe.to_excel(writer, sheet_name=sheet_name, index=True)
        elif isinstance(data_to_export, pd.DataFrame):
            # Если данные представлены одним DataFrame
            data_to_export.to_excel(writer, sheet_name='Отчет', index=True)

    # Возврат файла пользователю
    excel_file.seek(0)
    category_or_path = selected_category if 'selected_category' in locals() else (selected_path if 'selected_path' in locals() else 'Общий')
    file_name = f"{platform}_{report_type}_{category_or_path}.xlsx".replace(" ", "_").replace('/', '_')
    
    download_button = st.download_button(
        label="Скачать отчет", 
        data=excel_file, 
        file_name=file_name, 
        mime="application/vnd.ms-excel"
    )

    # Если кнопка загрузки была нажата
    if download_button:
        st.success(f"Файл отчета {file_name} успешно загружен")
        st.session_state['is_downloading'] = False  # Сброс флага загрузки

# Проверка состояния загрузки
if 'is_downloading' in st.session_state and st.session_state['is_downloading']:
    st.warning("Файл готовится к загрузке...")





# if st.button('Выгрузить отчет'):
#    st.session_state['is_downloading'] = True  # Установка флага загрузки

#    data_to_export = prepare_data_for_excel(platform, report_type)
   
#    # Создание файла Excel
#    excel_file = BytesIO()  
#    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
#        if isinstance(data_to_export, dict):
#            for sheet_name, dataframe in data_to_export.items():
#                dataframe.to_excel(writer, sheet_name=sheet_name, index=True)
#        elif isinstance(data_to_export, pd.DataFrame):
#            # Если данные представлены одним DataFrame
#            data_to_export.to_excel(writer, sheet_name='Отчет', index=True)

#    # Возврат файла пользователю
#    excel_file.seek(0)
#    download_button = st.download_button(
#        label="Скачать отчет", 
#        data=excel_file, 
#        file_name = f"{platform}_{report_type}_{category_name}.xlsx".replace(" ", "_"), 
#        mime="application/vnd.ms-excel"
#    )

#    # Если кнопка загрузки была нажата
#    if download_button:
#        st.success(f"Файл отчета {file_name} успешно загружен")
#        st.session_state['is_downloading'] = False  # Сброс флага загрузки

# # Проверка состояния загрузки
# if 'is_downloading' in st.session_state and st.session_state['is_downloading']:
#  st.warning("Файл готовится к загрузке...")
