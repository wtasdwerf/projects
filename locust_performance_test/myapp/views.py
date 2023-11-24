from django.shortcuts import render
import numpy as np
import pandas as pd
from django.http import JsonResponse

df = pd.read_csv('data/test_data.CSV', encoding='cp949')

def getAverage(data_list):
    age_sum = 0
    for data in data_list:
        if data != 'NULL':
            age_sum += data
    
    return age_sum/len(data_list)

# Create your views here.
def problem_a(request):
    # CSV 파일 위치
    data = df.to_dict('records')
    return JsonResponse({ 'dat': data }, json_dumps_params={ 'ensure_ascii': False })


def problem_b(request):
    # CSV 파일 위치
    df.fillna('NULL', inplace=True)
    data = df.to_dict('records')
    return JsonResponse({ 'dat': data }, json_dumps_params={ 'ensure_ascii': False })


def problem_c(request):
    # CSV 파일 위치
    df.fillna('NULL', inplace=True)
    age_avg = getAverage(df['나이'])
    
    temp_list = []
    for idx, age in enumerate(df['나이']):
        if age != 'NULL':
            temp_list.append((abs(age_avg-age), idx))
    temp_list.sort()
    
    new_list = []
    for i in range(10):
        new_list.append(df.loc[temp_list[i][1]])
    
    new_df = pd.DataFrame(new_list)
    
    data = new_df.to_dict('records')
    return JsonResponse({ 'dat': data }, json_dumps_params={ 'ensure_ascii': False })


def problem_d(request):
    pass