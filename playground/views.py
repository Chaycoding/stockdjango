from rest_framework.decorators import api_view
from rest_framework.response import Response
import yahoo_fin.stock_info as yhi
from yahoo_fin.stock_info import get_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from django.http import FileResponse
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates


zz = False
tinker = False


@api_view(['GET'])
def tinkerSetter(request,pk):
  global zz
  global tinker
  global check
  try:
    zz= get_data(pk, start_date="15/02/2014", index_as_date = True)
    zz['Date'] = list(zz.index)
    tinker = pk
    return Response('yes')
  except:
    check = True 
    return Response('no')


@api_view(['GET'])
def normchart(request, pk):
  plt.figure(figsize=(15, 5), facecolor='#111827')
  ax = sns.lineplot(data=zz, x='Date', y='close', color='white')
  plt.title(f'{tinker} close Price', fontsize=15)

  plt.ylabel('Price in dollars')

  ax.set_facecolor('#111827')
  ax.spines['bottom'].set_color('white')
  ax.spines['top'].set_color('white') 
  ax.spines['right'].set_color('white')
  ax.spines['left'].set_color('white')
  ax.tick_params(axis='x', colors='white')
  ax.tick_params(axis='y', colors='white')
  ax.yaxis.label.set_color('white')
  ax.xaxis.label.set_color('white')
  ax.title.set_color('white')

  plt.savefig('thing.jpg')

  img = open('./thing.jpg', 'rb')

  response = FileResponse(img)

  return response
# return Response(zz.tail(1))

# @api_view(['GET'])
def candle(request, pk):

  data = zz
  ohlc = data.loc[:, ['Date', 'open', 'high', 'low', 'close']]
  ohlc['Date'] = pd.to_datetime(ohlc['Date'])
  ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
  ohlc = ohlc.astype(float)
  plt.rcParams["figure.figsize"] = [7.50, 3.50]
  plt.rcParams["figure.autolayout"] = True
  plt.rcParams["axes.edgecolor"] = "black"
  plt.rcParams["axes.linewidth"] = 2.50
  fig, ax = plt.subplots(figsize=(12, 6), facecolor='#111827')
  candlestick_ohlc(ax, ohlc.values, width=0.6,
                  colorup='green', colordown='red', alpha=0.8)

  ax.set_xlabel('Date')
  ax.set_ylabel('Price')
  
  ax.grid(color = 'lightgrey')
  ax.spines['bottom'].set_color('white')
  ax.spines['top'].set_color('white') 
  ax.spines['right'].set_color('white')
  ax.spines['left'].set_color('white')
  ax.tick_params(axis='x', colors='white')
  ax.tick_params(axis='y', colors='white')
  ax.yaxis.label.set_color('white')
  ax.xaxis.label.set_color('white')

  fig.suptitle(f'Candlestick Chart of {tinker}', color='white')
  
  date_format = mpl_dates.DateFormatter('%Y-%m')
  ax.xaxis.set_major_formatter(date_format)
  fig.autofmt_xdate()
  fig.tight_layout()
  fig.savefig('thing2.jpg')
  img = open('./thing2.jpg', 'rb')

  response = FileResponse(img)

  return response



