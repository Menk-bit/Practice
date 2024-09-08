# -*- coding: utf-8 -*-
"""Phân lô bán nền công nghệ lõi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pkdW3KwpfWIGyD-o4YTCXDSABQYnvAHX
"""

from google.colab import drive
drive.mount("/content/gdrive")

import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

data = pd.read_csv("/content/gdrive/MyDrive/dataset.csv")
data.head(5)

data.info()

df = data

# Convert Unix time to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

# Resample to daily frequency
df_daily = df.resample('D', on='Timestamp').mean()

# remove Null values
df_daily['Open'].ffill(inplace=True)
df_daily['High'].ffill(inplace=True)
df_daily['Low'].ffill(inplace=True)
df_daily['Close'].ffill(inplace=True)

df_daily.head()

historical_df = df_daily
historical_df = historical_df.drop(["Volume_(BTC)","Volume_(Currency)","Weighted_Price"],axis = 1)

sb.pairplot(historical_df)

for i in range(1,8):
    historical_df["Open_past_"+str(i)] = df_daily['Open'].shift(i)
    historical_df["High_past_"+str(i)] = df_daily['High'].shift(i)
    historical_df["Low_past_"+str(i)]  = df_daily['Low'].shift(i)
    historical_df["Close_past_"+str(i)]= df_daily['Close'].shift(i)
historical_df = historical_df.dropna()
print(historical_df.shape)
historical_df.head(7)

historical_df["NEXT_CLOSE"] = historical_df['Close'].shift(-1)
historical_df = historical_df.dropna()
print(historical_df.shape)
historical_df.tail(7)

X_train = historical_df.iloc[0:len(historical_df)*7//10,0:32].values
X_test = historical_df.iloc[len(historical_df)*7//10:,0:32].values
y_train = historical_df.iloc[0:len(historical_df)*7//10,32].values
y_test = historical_df.iloc[len(historical_df)*7//10:,32].values

rf = RandomForestRegressor(n_estimators = 1000, random_state = 10)
rf.fit(X_train, y_train);
test_result = rf.predict(X_test)
RMSD = np.sqrt(np.mean(np.square(test_result.reshape(-1,1) - y_test.reshape(-1,1) )))
print("Root-mean-square error: ", RMSD)

Timestamp_collector_df = historical_df[len(historical_df) - len(y_test):]
df_Result = pd.DataFrame(y_test, index = Timestamp_collector_df.index, columns=["NEXT_CLOSE"])
df_Result['Predicted'] = test_result
print(df_Result.shape)
df_Result.tail(15)

plt.figure(figsize=(100,15), dpi=80, facecolor='w', edgecolor='w')
ax = plt.gca()
ax.set_facecolor("#201c24")
plt.plot(df_Result['NEXT_CLOSE'], color = 'red', label = 'Real BTC Price', linewidth = 10.0)
plt.plot(df_Result['Predicted'], color = 'green', label = 'Predicted BTC Price', linewidth = 7.0)
plt.title('BTC Price Prediction', fontsize=40)
df_test = df_Result.reset_index()
plt.xlabel('Time', fontsize=40)
plt.ylabel('BTC Price(USD) [Closed]', fontsize=40)
plt.legend(loc=2, prop={'size': 25})
plt.show()