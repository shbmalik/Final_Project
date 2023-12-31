# -*- coding: utf-8 -*-
"""Air Polution Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UsMAIzrghC3JHdzeNPsNcNwWDf2QyTYk
"""

import sys
import csv
import glob
import pandas as pd
import matplotlib.pyplot as plt

import keras
from keras.models import Sequential
from keras import datasets, layers, models
#from keras.utils import np_utils
from keras import regularizers
from keras.layers import Dense, Dropout, BatchNormalization
from random import shuffle
import tensorflow as tf
from skimage.measure import block_reduce
from tensorflow import image
from sklearn.metrics import classification_report

from tensorflow.keras import activations
from keras.models import load_model
from keras.callbacks import EarlyStopping
import numpy as np


#Normalising data
from sklearn.preprocessing import MinMaxScaler

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd '/content/drive/MyDrive/CAMS_PM2.5/Air Quality N data'
!ls

"""# Importing data"""

Aotizhongxin = pd.read_csv('./PRSA_Data_Aotizhongxin_20130301-20170228.csv')
Changping = pd.read_csv('./PRSA_Data_Changping_20130301-20170228.csv')
Dingling = pd.read_csv('./PRSA_Data_Dingling_20130301-20170228.csv')
Dongsi = pd.read_csv('./PRSA_Data_Dingling_20130301-20170228.csv')
Guanyuan = pd.read_csv('./PRSA_Data_Guanyuan_20130301-20170228.csv')
Gucheng = pd.read_csv('./PRSA_Data_Gucheng_20130301-20170228.csv')
Huairou = pd.read_csv('./PRSA_Data_Huairou_20130301-20170228.csv')
Nongzhanguan = pd.read_csv('./PRSA_Data_Nongzhanguan_20130301-20170228.csv')
Shunyi = pd.read_csv('./PRSA_Data_Shunyi_20130301-20170228.csv')
Tiantan = pd.read_csv('./PRSA_Data_Tiantan_20130301-20170228.csv')
Wanliu = pd.read_csv('./PRSA_Data_Wanliu_20130301-20170228.csv')
Wanshouxigong = pd.read_csv('./PRSA_Data_Wanshouxigong_20130301-20170228.csv')

"""# Filling NaN values"""

Aotizhongxin = Aotizhongxin.interpolate(method='linear')

Changping['PM2.5']=Changping['PM2.5'].interpolate(method='linear', axis=0)
Dingling['PM2.5']=Dingling['PM2.5'].interpolate(method='linear', axis=0)
Dongsi['PM2.5']=Dongsi['PM2.5'].interpolate(method='linear', axis=0)
Guanyuan['PM2.5']=Guanyuan['PM2.5'].interpolate(method='linear', axis=0)
Gucheng['PM2.5']=Gucheng['PM2.5'].interpolate(method='linear', axis=0)
Huairou['PM2.5']=Huairou['PM2.5'].interpolate(method='linear', axis=0)
Nongzhanguan['PM2.5']=Nongzhanguan['PM2.5'].interpolate(method='linear', axis=0)
Shunyi['PM2.5']=Shunyi['PM2.5'].interpolate(method='linear', axis=0)
Tiantan['PM2.5']=Tiantan['PM2.5'].interpolate(method='linear', axis=0)
Wanliu['PM2.5']=Wanliu['PM2.5'].interpolate(method='linear', axis=0)
Wanshouxigong['PM2.5']=Wanshouxigong['PM2.5'].interpolate(method='linear', axis=0)

Aotizhongxin['wd']==22.5

"""# Encoding Categorical Variable"""

for i in range(len(Aotizhongxin['wd'])):
  temp = Aotizhongxin['wd'][i]
  final_temp = 0
  if (temp == 'N'):
    final_temp = 0
  if (temp == 'NNE'):
    final_temp = 22.5
  if (temp == 'NE'):
    final_temp = 45
  if (temp == 'ENE'):
    final_temp = 67.5
  if (temp == 'E'):
    final_temp = 90
  if (temp == 'ESE'):
    final_temp = 112.5
  if (temp == 'SE'):
    final_temp = 135
  if (temp == 'SSE'):
    final_temp = 157.5
  if (temp == 'S'):
    final_temp = 180
  if (temp == 'SSW'):
    final_temp = 202.5
  if (temp == 'SW'):
    final_temp = 225
  if (temp == 'WSW'):
    final_temp = 247.5
  if (temp == 'W'):
    final_temp = 270
  if (temp == 'WNW'):
    final_temp = 292.5
  if (temp == 'NW'):
    final_temp = 315
  if (temp == 'NNW'):
    final_temp = 337.5

  Aotizhongxin['wd'][i] = final_temp
Aotizhongxin['wd']=Aotizhongxin['wd'].interpolate(method='linear', axis=0)

"""# Nomarlization"""

Max_Aotizhongxin_pm = Aotizhongxin['PM2.5'].max()
Min_Aotizhongxin_pm = Aotizhongxin['PM2.5'].min()

for i in range(len(Aotizhongxin['PM2.5'])):
  temp = (Aotizhongxin['PM2.5'][i] - Min_Aotizhongxin_pm) / (Max_Aotizhongxin_pm - Min_Aotizhongxin_pm)
  Aotizhongxin['PM2.5'][i] = temp

Max_Changping_pm = Changping['PM2.5'].max()
Min_Changping_pm = Changping['PM2.5'].min()

for i in range(len(Changping['PM2.5'])):
  temp = (Changping['PM2.5'][i] - Min_Changping_pm) / (Max_Changping_pm - Min_Changping_pm)
  Changping['PM2.5'][i] = temp

Max_Dingling_pm = Dingling['PM2.5'].max()
Min_Dingling_pm = Dingling['PM2.5'].min()

for i in range(len(Dingling['PM2.5'])):
  temp = (Dingling['PM2.5'][i] - Min_Dingling_pm) / (Max_Dingling_pm - Min_Dingling_pm)
  Dingling['PM2.5'][i] = temp

Max_Dongsi_pm = Dongsi['PM2.5'].max()
Min_Dongsi_pm = Dongsi['PM2.5'].min()

for i in range(len(Dongsi['PM2.5'])):
  temp = (Dongsi['PM2.5'][i] - Min_Dongsi_pm) / (Max_Dongsi_pm - Min_Dongsi_pm)
  Dongsi['PM2.5'][i] = temp

Max_Guanyuan_pm = Guanyuan['PM2.5'].max()
Min_Guanyuan_pm = Guanyuan['PM2.5'].min()

for i in range(len(Guanyuan['PM2.5'])):
  temp = (Guanyuan['PM2.5'][i] - Min_Guanyuan_pm) / (Max_Guanyuan_pm - Min_Guanyuan_pm)
  Guanyuan['PM2.5'][i] = temp

Max_Gucheng_pm = Gucheng['PM2.5'].max()
Min_Gucheng_pm = Gucheng['PM2.5'].min()

for i in range(len(Gucheng['PM2.5'])):
  temp = (Gucheng['PM2.5'][i] - Min_Gucheng_pm) / (Max_Gucheng_pm - Min_Gucheng_pm)
  Gucheng['PM2.5'][i] = temp

Max_Huairou_pm = Huairou['PM2.5'].max()
Min_Huairou_pm = Huairou['PM2.5'].min()

for i in range(len(Huairou['PM2.5'])):
  temp = (Huairou['PM2.5'][i] - Min_Huairou_pm) / (Max_Huairou_pm - Min_Huairou_pm)
  Huairou['PM2.5'][i] = temp

Max_Nongzhanguan_pm = Nongzhanguan['PM2.5'].max()
Min_Nongzhanguan_pm = Nongzhanguan['PM2.5'].min()

for i in range(len(Nongzhanguan['PM2.5'])):
  temp = (Nongzhanguan['PM2.5'][i] - Min_Nongzhanguan_pm) / (Max_Nongzhanguan_pm - Min_Nongzhanguan_pm)
  Nongzhanguan['PM2.5'][i] = temp

Max_Shunyi_pm = Shunyi['PM2.5'].max()
Min_Shunyi_pm = Shunyi['PM2.5'].min()

for i in range(len(Shunyi['PM2.5'])):
  temp = (Shunyi['PM2.5'][i] - Min_Shunyi_pm) / (Max_Shunyi_pm - Min_Shunyi_pm)
  Shunyi['PM2.5'][i] = temp

Max_Tiantan_pm = Tiantan['PM2.5'].max()
Min_Tiantan_pm = Tiantan['PM2.5'].min()

for i in range(len(Tiantan['PM2.5'])):
  temp = (Tiantan['PM2.5'][i] - Min_Tiantan_pm) / (Max_Tiantan_pm - Min_Tiantan_pm)
  Tiantan['PM2.5'][i] = temp

Max_Wanliu_pm = Wanliu['PM2.5'].max()
Min_Wanliu_pm = Wanliu['PM2.5'].min()

for i in range(len(Wanliu['PM2.5'])):
  temp = (Wanliu['PM2.5'][i] - Min_Wanliu_pm) / (Max_Wanliu_pm - Min_Wanliu_pm)
  Wanliu['PM2.5'][i] = temp

Max_Wanshouxigong_pm = Wanshouxigong['PM2.5'].max()
Min_Wanshouxigong_pm = Wanshouxigong['PM2.5'].min()

for i in range(len(Wanshouxigong['PM2.5'])):
  temp = (Wanshouxigong['PM2.5'][i] - Min_Wanshouxigong_pm) / (Max_Wanshouxigong_pm - Min_Wanshouxigong_pm)
  Wanshouxigong['PM2.5'][i] = temp

"""# Pearson correlation"""

Pm25_list = pd.DataFrame(
    {'PM2.5': Aotizhongxin['PM2.5'],
     'PM2.5_Wans': Wanshouxigong['PM2.5'],
     'PM2.5_wanl':  Wanliu['PM2.5'],
     'PM2.5_Tian':  Tiantan['PM2.5'],
     'PM2.5_Shun':  Shunyi['PM2.5'],
     'PM2.5_Guch':  Gucheng['PM2.5'],
     'PM2.5_Huai':  Huairou['PM2.5'],
     'PM2.5_Guan':  Guanyuan['PM2.5'],
     'PM2.5_Dong':  Dongsi['PM2.5'],
     'PM2.5_Nong':  Nongzhanguan['PM2.5'],
     'PM2.5_Ding':  Dingling['PM2.5'],
     'PM2_Chan':  Changping['PM2.5']
    })

import seaborn as sb
corr = Pm25_list.corr(method='pearson')
fig, ax = plt.subplots(figsize=(8,5))
sb.heatmap(corr, cmap="RdPu", annot=True,linewidths=.5, ax=ax)



"""# Making Excel"""

Excel_df = pd.DataFrame(
    {'No': Aotizhongxin['No'],
     'year': Aotizhongxin['year'],
     'month':  Aotizhongxin['month'],
     'day':  Aotizhongxin['day'],
     'hour':  Aotizhongxin['hour'],
     'PM2.5_Wans': Wanshouxigong['PM2.5'],
     'PM2.5_wanl':  Wanliu['PM2.5'],
     'PM2.5_Tian':  Tiantan['PM2.5'],
     'PM2.5_Shun':  Shunyi['PM2.5'],
     'PM2.5_Guch':  Gucheng['PM2.5'],
     'PM2.5_Huai':  Huairou['PM2.5'],
     'PM2.5_Guan':  Guanyuan['PM2.5'],
     'PM2.5_Dong':  Dongsi['PM2.5'],
     'PM2.5_Nong':  Nongzhanguan['PM2.5'],
     'PM2.5_Ding':  Dingling['PM2.5'],
     'PM2.5_Chan':  Changping['PM2.5'],
     'PM10_Aotizh': Aotizhongxin['PM10'],
     'CO_Aotizh': Aotizhongxin['CO'],
     'TEMP_Aotizh': Aotizhongxin['TEMP'],
     'PRES_Aotizh': Aotizhongxin['PRES'],
     'DEWP_Aotizh': Aotizhongxin['DEWP'],
     'RAIN_Aotizh': Aotizhongxin['RAIN'],
     'WSPM_Aotizh': Aotizhongxin['WSPM'],
     'wd_Aotizh': Aotizhongxin['wd'],
     'PM2.5_Aotizh': Aotizhongxin['PM2.5'],
    })

Excel_df.to_csv('/content/drive/MyDrive/CAMS_PM2.5/Feature_selection.csv', encoding='utf-8', index=False)

"""## Train and Test Split"""

Excel_df

"""## Lag = 1 days"""

def to_supervised(train):
  window_size = 24
  X = []
  Y = []
  i=0
  for i in range(window_size, len(train)):
    X.append(train[i-window_size:i,5:25])
    Y.append(train[i,-1])

  return X,Y

X, Y = to_supervised(values)
X = np.asarray(X).astype('float32')
Y = np.asarray(Y).astype('float32')
print('Y' ,Y.shape)
print('X' ,X.shape)

n_train = 6988
X_train, X_test = X[n_train:,] , X[:n_train,]
print('X_train' ,X_train.shape)
print('X_test' ,X_test.shape)

Y_train, Y_test = Y[n_train:,] , Y[:n_train,]
print('Y_train' ,Y_train.shape)
print('Y_test' ,Y_test.shape)

"""CNN-LSTM Network"""

model = Sequential()
model.add(layers.Conv1D(64, 3, padding='causal',activation="relu", input_shape=(X_train.shape[1],
                                                                                X_train.shape[2])))
model.add(layers.BatchNormalization())

model.add(layers.Conv1D(64, 3, padding='causal',activation="relu"))
model.add(layers.BatchNormalization())

model.add(layers.Conv1D(32, 3, padding='causal',activation="relu"))

model.add(layers.MaxPooling1D(pool_size=3))


model.add(tf.keras.layers.LSTM(units=100,dropout=0.2,return_sequences = True))
model.add(tf.keras.layers.LSTM(units=50,dropout=0.3))
model.add(layers.Dense(units=1, activation="relu"))
model.summary()

opt = keras.optimizers.Adam(learning_rate=0.001,decay=0.0001)
model.compile(loss='mean_squared_error', optimizer=opt)
es = EarlyStopping(min_delta = 1e-3,patience = 50)
model.fit(X_train, Y_train, batch_size=32, epochs=200, callbacks=[es])

Y_pred = model.predict(X_test)
print(Y_pred.shape)
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(Y_test, Y_pred)

rmse = np.sqrt(mse)

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(Y_test, Y_pred)

from sklearn.metrics import r2_score
r2 = r2_score(Y_test, Y_pred)

print("rmse = "+str(rmse))
print("mae = "+str(mae))
print("R2 = "+str(r2))

"""## Lag = 7 days"""

def to_supervised(train):
  window_size = 7*24
  X = []
  Y = []
  i=0
  for i in range(window_size, len(train)):
    X.append(train[i-window_size:i,5:25])
    Y.append(train[i,-1])

  return X,Y

X, Y = to_supervised(values)
X = np.asarray(X).astype('float32')
Y = np.asarray(Y).astype('float32')
print('Y' ,Y.shape)
print('X' ,X.shape)

n_train = 6988
X_train, X_test = X[n_train:,] , X[:n_train,]
print('X_train' ,X_train.shape)
print('X_test' ,X_test.shape)

Y_train, Y_test = Y[n_train:,] , Y[:n_train,]
print('Y_train' ,Y_train.shape)
print('Y_test' ,Y_test.shape)

model = Sequential()
model.add(layers.Conv1D(64, 3, padding='causal',activation="relu", input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(layers.BatchNormalization())

model.add(layers.Conv1D(64, 3, padding='causal',activation="relu"))
model.add(layers.BatchNormalization())

model.add(layers.Conv1D(32, 3, padding='causal',activation="relu"))

model.add(layers.MaxPooling1D(pool_size=3))


model.add(tf.keras.layers.LSTM(units=100,dropout=0.2,return_sequences = True))
model.add(tf.keras.layers.LSTM(units=50,dropout=0.3))
model.add(layers.Dense(units=1, activation="relu"))
model.summary()

opt = keras.optimizers.Adam(learning_rate=0.001,decay=0.0001)
model.compile(loss='mean_squared_error', optimizer=opt)
es = EarlyStopping(min_delta = 1e-3,patience = 50)
model.fit(X_train, Y_train, batch_size=32, epochs=200, callbacks=[es])

Y_pred = model.predict(X_test)
print(Y_pred.shape)
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(Y_test, Y_pred)

rmse = np.sqrt(mse)

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(Y_test, Y_pred)

from sklearn.metrics import r2_score
r2 = r2_score(Y_test, Y_pred)

print("rmse = "+str(rmse))
print("mae = "+str(mae))
print("R2 = "+str(r2))

