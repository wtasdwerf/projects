from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import numpy as np
from datetime import datetime

plt.switch_backend('Agg')
csv_path = 'weathers/data/austin_weather.csv'
df = pd.read_csv(csv_path, index_col='Date', parse_dates=True)

# Create your views here.
def problem1(request):  
    context = {
        'df': df,
    }
    return render(request, 'weathers/problem1.html', context)



def problem2(request):
    # # # 날짜를 날짜형으로 변환
    # df['date']= pd.to_datetime(df['date'])

    # # 날짜를 인덱스로 설정
    # df.set_index('Date', inplace=True)

    # 그래프 그리기
    plt.figure(figsize=(10, 6))

    # 선 그래프 그리기
    plt.plot(df.index, df['TempHighF'], label='High Temperature')
    plt.plot(df.index, df['TempAvgF'], label='Average Temperature')
    plt.plot(df.index, df['TempLowF'], label='Low Temperature')
    
    # 그래프에 제목과 레이블 추가
    plt.title('Temperature Variation')
    plt.xlabel('Date')
    plt.ylabel('Temperature(Farenheit)')

    # 범례 추가
    plt.legend()

     # 비어있는 버퍼를 생성
    buffer = BytesIO()

    # 버퍼에 그래프를 저장
    plt.savefig(buffer, format='png')

    # 버퍼의 내용을 base64 로 인코딩
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    
    # 버퍼를 닫아줌
    buffer.close()

    # 이미지를 웹 페이지에 표시하기 위해
    # URI 형식(주소 형식)으로 만들어진 문자열을 생성
    context = {
        # chart_image: 저장된 이미지의 경로
        'chart_image': f'data:image/png;base64,{image_base64}',
    }

    return render(request, 'weathers/problem2.html', context)



def problem3(request):
    df = pd.read_csv(csv_path)

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # NaN 값이 있는 행 제거
    df = df.dropna(subset=['Date'])

    # '-' 값을 NaN으로 처리
    df.replace('-', pd.NaT, inplace=True)

    # 그래프 그리기
    plt.figure(figsize=(10, 6))

    df_new = df.groupby(['Date']).mean()

    # Debugging: 인덱스 출력
    print(df_new.index)

    try:
        # 인덱스를 datetime 형식으로 변환
        df_new.index = pd.to_datetime(df_new.index)
    except Exception as e:
        # 변환 실패 시 에러 메시지 출력
        print(f"Error during datetime conversion: {e}")

    # Debugging: 변환 후 인덱스 다시 출력
    print(df_new.index)

    plt.plot(df_new.index, df_new['TempHighF'], label='TempHighF')
    plt.plot(df_new.index, df_new['TempAvgF'], label='TempAvgF')
    plt.plot(df_new.index, df_new['TempLowF'], label='TempLowF')
    
    # 그래프에 제목과 레이블 추가
    plt.title('Temperature Variation')
    plt.xlabel('Date')
    plt.ylabel('Temperature(Farenheit)')

    # 범례 추가
    plt.legend()

     # 비어있는 버퍼를 생성
    buffer = BytesIO()

    # 버퍼에 그래프를 저장
    plt.savefig(buffer, format='png')

    # 버퍼의 내용을 base64 로 인코딩
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    
    # 버퍼를 닫아줌
    buffer.close()

    # 이미지를 웹 페이지에 표시하기 위해
    # URI 형식(주소 형식)으로 만들어진 문자열을 생성
    context = {
        # chart_image: 저장된 이미지의 경로
        'chart_image': f'data:image/png;base64,{image_base64}',
    }

    return render(request, 'weathers/problem3.html', context)




def problem4(request):
    context ={
        
    }
    return render(request, 'weathers/problem4.html', context)
