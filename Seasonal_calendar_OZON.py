#!/usr/bin/env python
# coding: utf-8


import requests
import json
import csv

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

# from openpyxl import Workbook, load_workbook
# from openpyxl.utils.dataframe import dataframe_to_rows
# from openpyxl.drawing.image import Image
# from openpyxl.styles import NamedStyle
# from openpyxl.styles import Color, PatternFill, Font


import math
from datetime import datetime
import os
import glob
import streamlit as st

st.title('Сезонный календарь OZON')
# Список категорий
# **********************************************************************************************************************************
@st.cache_data
def podkluchenie_k_api():
    url = 'http://mpstats.io/api/oz/get/categories'  #oz/get/categories
    headers = {
        'X-Mpstats-TOKEN': '64ee0e4f67a005.746995831774b14d378d3e3022e4e2f8a3698042',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        formatted_data = [
            {
                "url": category.get("url"),
                "name": category.get("name"),
                "path": category.get("path")
            }
            for category in data
        ]
        
        filtered_data = [item for item in formatted_data if item['path'].count('/') == 1 and  not item['path'].startswith('Акции')]   
        # если берем все подкатегории, то убрать условие выше
    
        # csv_filename = "Категории OZON второго уровня без акций.csv"
        # with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        #     fieldnames = ['url', 'name', 'path']
        #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
        #     writer.writeheader()
        #     for row in filtered_data: # если берем всё, а не только короткие названия, то изм на formatted_data 
        #         writer.writerow(row)
            
        # print(f"Данные успешно записаны в CSV файл: '{csv_filename}'")
        st.write(filtered_data)
        st.write(formatted_data)
    else:
        st.write(f"Запрос не отработан: {response.status_code}")
    return filtered_data
    
def poluchenie_categoriy(list1):
    # Создаем выпадающий список для 'name'
    selected_name = st.selectbox('Выберите категорию по названию:', [item['name'] for item in filtered_data])
    
    # Создаем выпадающий список для 'path' на основе выбранного 'name'
    selected_data = next(item for item in filtered_data if item['name'] == selected_name)
    selected_path = st.selectbox('Выберите путь категории:', [selected_data['path']])
    
    # Выводим выбранные значения
    st.write('Выбранное название:', selected_name)
    st.write('Выбранный путь:', selected_path)
    

# **********************************************************************************************************************************
# Функции
data_api = podkluchenie_k_api()
# poluchenie_categoriy(data_api)

# **********************************************************************************************************************************

# # Загружаем файл категорий
# # categories = pd.read_csv('/Users/iv18s/Desktop/Champ Commerce/Категории OZON второго уровня без акций.csv', sep = ',')  #iv18s\Desktop\Champ Commerce
# # разделитель - запятая!


# # In[5]:


# categories


# # In[5]:


# pip install xlsxwriter


# # In[7]:


# # Обращение за данными катеории по api без функции
# import xlsxwriter
# from xlsxwriter import Workbook

# index_column = 'Дата'   # кажется, эта строка ни на что не влияет

# url = 'https://mpstats.io/api/oz/get/category/by_date'
# categories_data = categories.to_dict(orient='records')

# data_dict = {}

# for category_data in categories_data:
#     category_path = category_data['path']
#     category_name = category_path.split('/')[0]
#     subcategory_name = category_path.split('/')[1] if len(category_path.split('/')) > 1 else 'No Subcategory'
    
#     if category_name != 'Бытовая техника': #and category_name != 'Аксессуары':
#         continue  # Пропускаем категории, отличные указанных
    
#     params = {
#         'd1': '2020-01-01',
#         'd2': '2022-12-31',
#         'path': category_path
#     }
    
#     headers = {
#         'X-Mpstats-TOKEN': '64ee0e4f67a005.746995831774b14d378d3e3022e4e2f8a3698042',
#         'Content-Type': 'application/json'
#     }
    
#     response = requests.get(url, params=params, headers=headers)
    
#     if response.status_code == 200:
#         data = response.json()
#         if data:
#             if category_name not in data_dict:
#                 data_dict[category_name] = {'subcategories': {}}
#                 print(f"Данные категории {category_name} обрабатываются")
#             data_dict[category_name]['subcategories'][subcategory_name] = data
#         else:
#             print(f"Нет доступных данных для подкатегории '{category_path}' за выбранный период.")

# # Создание Excel-файла с разными листами для каждой подкатегории
# for category_name, category_data in data_dict.items():
#     excel_filename = f"Категория {category_name}.xlsx"
#     with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
#         for subcategory_name, data in category_data['subcategories'].items():
#             if subcategory_name == 'No Subcategory':
#                 subcategory_name = 'Без подкатегории'
                
#             df = pd.DataFrame(data)
            
#             df = df.T  # Транспонируем таблицу
#             df.index.rename('Date', inplace= True)  # Переименовываем столбец индексов. Он уже в формате Дата
         
            
#             #  df['Date'] = pd.to_datetime(df['Date'])  # Преобразование в объект datetime
#             #  df.set_index('Date', inplace=True)  # Делаем 'Date' индексом
            
#             # Удаление всех колонок, кроме 'sales' и 'period'
# ##            df = df[['sales', 'revenue']]

#             df.to_excel(writer, sheet_name=subcategory_name[:25])

#     print(f"Файл '{excel_filename}' успешно создан!")
    


# # In[9]:


# df.head()


# # In[10]:


# print(df.keys())


# # In[11]:


# data_posled = list(data.keys())
# data_posled


# # In[12]:


# data.items()


# # In[ ]:





# # In[ ]:





# # In[ ]:





# # # РАБОТАЕТ ТРОЙНОЕ ОБРАЩЕНИЕ К СЛОВАРЮ

# # In[22]:


# # data_proba = data['2022-10-28']['fbs']['sales']
# # data_proba


# # In[ ]:





# # In[ ]:





# # Получим данные по sales

# # In[23]:


# # Создаем пустые списки для значений 'sales'
# sales_fbo = []
# sales_fbs = []
# sales_crossborder = []
# sales_retail = []


# poisk_1 = 'sales'
# poisk_2 = 'items'
# poisk_3 = 'revenue'

# # Итерируемся по словарям внутри словаря
# # sales в fbo
# for date, values in data.items():
#     if poisk_1 in values:
#         sales_fbo.append(values[poisk_1])
#     elif 'fbo' in values and poisk_1 in values['fbo']:
#         sales_fbo.append(values['fbo'][poisk_1])

# # sales в fbs
# for date, values in data.items():
#     if poisk_1 in values:
#         sales_fbs.append(values[poisk_1])
#     elif 'fbs' in values and poisk_1 in values['fbs']:
#         sales_fbs.append(values['fbs'][poisk_1])        
        
# # sales в crossborder
# for date, values in data.items():
#     if poisk_1 in values:
#         sales_crossborder.append(values[poisk_1])
#     elif 'crossborder' in values and poisk_1 in values['crossborder']:
#         sales_crossborder.append(values['crossborder'][poisk_1])
        
# # sales в retail
# for date, values in data.items():
#     if poisk_1 in values:
#         sales_retail.append(values[poisk_1])
#     elif 'retail' in values and poisk_1 in values['retail']:
#         sales_retail.append(values['retail'][poisk_1])        
        
        

# # # Выводим данные по Sales
# # print("Данные по Sales fbo:", sales_fbo)
# # print('*' * 115)
# # print("Данные по Sales fbs:", sales_fbs)
# # print('*' * 115)
# # print("Данные по Sales crossborder:", sales_crossborder)
# # print('*' * 115)
# # print("Данные по Sales retail:", sales_retail)


# # In[24]:


# # Создаем пустые списки для значений 'items'
# items_fbo = []
# items_fbs = []
# items_crossborder = []
# items_retail = []


# poisk_1 = 'sales'
# poisk_2 = 'items'
# poisk_3 = 'revenue'

# # Итерируемся по словарям внутри словаря
# # items в fbo
# for date, values in data.items():
#     if poisk_2 in values:
#         items_fbo.append(values[poisk_2])
#     elif 'fbo' in values and poisk_2 in values['fbo']:
#         items_fbo.append(values['fbo'][poisk_2])

# # items в fbs
# for date, values in data.items():
#     if poisk_2 in values:
#         items_fbs.append(values[poisk_2])
#     elif 'fbs' in values and poisk_2 in values['fbs']:
#         items_fbs.append(values['fbs'][poisk_2])        
        
# # items в crossborder
# for date, values in data.items():
#     if poisk_2 in values:
#         items_crossborder.append(values[poisk_2])
#     elif 'crossborder' in values and poisk_2 in values['crossborder']:
#         items_crossborder.append(values['crossborder'][poisk_2])
        
# # items в retail
# for date, values in data.items():
#     if poisk_2 in values:
#         items_retail.append(values[poisk_2])
#     elif 'retail' in values and poisk_2 in values['retail']:
#         items_retail.append(values['retail'][poisk_2])        
        
        

# # # Выводим данные по items
# # print("Данные по items fbo:", items_fbo)
# # print('*' * 115)
# # print("Данные по items fbs:", items_fbs)
# # print('*' * 115)
# # print("Данные по items crossborder:", items_crossborder)
# # print('*' * 115)
# # print("Данные по items retail:", items_retail)


# # In[25]:


# # Создаем пустые списки для значений 'revenue'
# revenue_fbo = []
# revenue_fbs = []
# revenue_crossborder = []
# revenue_retail = []


# poisk_1 = 'sales'
# poisk_2 = 'items'
# poisk_3 = 'revenue'

# # Итерируемся по словарям внутри словаря
# # revenue в fbo
# for date, values in data.items():
#     if poisk_3 in values:
#         revenue_fbo.append(values[poisk_3])
#     elif 'fbo' in values and poisk_3 in values['fbo']:
#         revenue_fbo.append(values['fbo'][poisk_3])

# # revenue в fbs
# for date, values in data.items():
#     if poisk_3 in values:
#         revenue_fbs.append(values[poisk_3])
#     elif 'fbs' in values and poisk_3 in values['fbs']:
#         revenue_fbs.append(values['fbs'][poisk_3])        
        
# # revenue в crossborder
# for date, values in data.items():
#     if poisk_3 in values:
#         revenue_crossborder.append(values[poisk_3])
#     elif 'crossborder' in values and poisk_3 in values['crossborder']:
#         revenue_crossborder.append(values['crossborder'][poisk_3])
        
# # revenue в retail
# for date, values in data.items():
#     if poisk_3 in values:
#         revenue_retail.append(values[poisk_3])
#     elif 'retail' in values and poisk_3 in values['retail']:
#         revenue_retail.append(values['retail'][poisk_3])        
        
        

# # # Выводим данные по revenue
# # print("Данные по revenue fbo:", revenue_fbo)
# # print('*' * 115)
# # print("Данные по revenue fbs:", revenue_fbs)
# # print('*' * 115)
# # print("Данные по revenue crossborder:", revenue_crossborder)
# # print('*' * 115)
# # print("Данные по revenue retail:", revenue_retail)


# # Создаем датафрейм с полученными значениями

# # In[45]:


# dict_category = {
#     'Date': data_posled, 
#     'Items fbo': items_fbo, 'Items fbs': items_fbs, 'Items crossborder': items_crossborder, 'Items retail': items_retail, 
#     'Sales fbo': sales_fbo, 'Sales fbs': sales_fbs, 'Sales crossborder': sales_crossborder, 'Sales retail': sales_retail,
#     'Revenue fbo': revenue_fbo, 'Revenue fbs': revenue_fbs, 'Revenue crossborder': revenue_crossborder, 'Revenue retail': revenue_retail
#                 }

# df_category = pd.DataFrame(dict_category)
# df_category['Date'] = pd.to_datetime(df_category['Date'])
# df_category = df_category.set_index('Date')

# df_category['Total Items'] = df_category['Items fbo'] + df_category['Items fbs'] + df_category['Items crossborder'] + df_category['Items retail']
# df_category['Total Sales'] = df_category['Sales fbo'] + df_category['Sales fbs'] + df_category['Sales crossborder'] + df_category['Sales retail']
# df_category['Total Revenue'] = df_category['Revenue fbo'] + df_category['Revenue fbs'] + df_category['Revenue crossborder'] + df_category['Revenue retail']
# df_category['Avg price'] = df_category['Total Revenue'] / df_category['Total Sales']

# df_categoty_total = df_category.iloc[:, 12:16]

# print(df_categoty_total.sort_index(ascending=True))


# # In[ ]:


# # monthly_sales_totals_2020
# # monthly_sales_totals_2021
# # monthly_sales_totals_2022
# # total_sales_2020
# # total_sales_2021
# # total_sales_2022
# # avg_monthly_sales


# # In[43]:


# monthly_sales_2020 = {month: [0] for month in range(1, 13)}
# monthly_sales_2021 = {month: [0] for month in range(1, 13)}
# monthly_sales_2022 = {month: [0] for month in range(1, 13)}
# # avg_monthly_sales = [[],[]]

# for index, row in df_categoty_total.iterrows():
#     year = index.year
#     month = index.month
#     sales = row['Total Sales']
#     revenue = row['Total Revenue']

#     if year == 2020:
#         monthly_sales_2020[month][0] += sales
#     elif year == 2021:
#         monthly_sales_2021[month][0] += sales
#     else:
#         monthly_sales_2022[month][0] += sales

# print(monthly_sales_2020)
# print(monthly_sales_2021)
# print(monthly_sales_2022)

# monthly_sales_totals_2020 = [monthly_sales_2020[month][0] for month in range(1, 13)]
# print("Сумма продаж за каждый месяц 2020 года: ", monthly_sales_totals_2020)
# print('\n')
    
# monthly_sales_totals_2021 = [monthly_sales_2021[month][0] for month in range(1, 13)]
# print("Сумма продаж за каждый месяц 2021 года: ", monthly_sales_totals_2021)
# print('\n')
    
# monthly_sales_totals_2022 = [monthly_sales_2022[month][0] for month in range(1, 13)]
# print("Сумма продаж за каждый месяц 2022 года: ", monthly_sales_totals_2022)
# print('\n')
    
# total_sales_2020 = sum(monthly_sales_totals_2020)
# total_sales_2021 = sum(monthly_sales_totals_2021)
# total_sales_2022 = sum(monthly_sales_totals_2022)
# print("Сумма продаж за 2020 год: ", total_sales_2020)
# print("Сумма продаж за 2021 год: ", total_sales_2021)
# print("Сумма продаж за 2022 год: ", total_sales_2022)
# print('\n')

# total_sales_for_3_years = total_sales_2020 + total_sales_2021 + total_sales_2022
# print('Сумма продаж за 2020-2022 годы: ', total_sales_for_3_years)
# print('\n')

# avg_monthly_sales = [(monthly_sales_2020[month][0] + monthly_sales_2021[month][0] + monthly_sales_2022[month][0]) / 3 for month in range(1, 13)]

# print("Средние значения продаж по месяцам за три года:")
# for month in range(1, 13):
#     print(f"Средняя продажа за месяц {month}:", avg_monthly_sales[month - 1].round(0))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




