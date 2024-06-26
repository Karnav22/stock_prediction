import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import datetime

st.title('Stock Trend Prediction')
user_input = st.text_input('Enter Stock Ticker', 'AAPL')

start='2010-01-01'#st.date_input(label='Start', value=None, min_value=None, max_value=None, key=None, help=None, on_change=None, args=None, kwargs=None, format="YYYY/MM/DD", disabled=False, label_visibility="visible")
#'2010-01-01'
end='2019-12-31'#st.date_input(label='End', value=None, min_value=None, max_value=None, key=None, help=None, on_change=None, args=None, kwargs=None, format="YYYY/MM/DD", disabled=False, label_visibility="visible")
#'2019-12-31'

df = data.DataReader(user_input, data_source='stooq', start=start, end=end)

# Describing data
st.subheader('Data From 2010 to 2019')
st.write(df.describe())

# Visualizations
st.subheader('Closing Price V/S Time Chart')
fig = plt.figure(figsize=(12, 6))
plt.plot(df['Close'])
st.pyplot(fig)

st.subheader('Closing Price V/S Time Chart with 100 Days Moving Average')
ma100 = df['Close'].rolling(100).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100, 'r')
plt.plot(df['Close'], 'g')
st.pyplot(fig)

st.subheader('Closing Price V/S Time Chart with 100 Days Moving Average & 200 Days Moving Average')
ma200 = df['Close'].rolling(200).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100, 'r')
plt.plot(ma200, 'g')
plt.plot(df['Close'], 'b')
st.pyplot(fig)

# Splitting data into training and testing
data_training = df['Close'][:int(len(df) * 0.70)]
data_testing = df['Close'][int(len(df) * 0.70):]

scaler = MinMaxScaler(feature_range=(0, 1))

data_training_array = scaler.fit_transform(np.array(data_training).reshape(-1, 1))

# Splitting data into x_train & y_train
x_train = []
y_train = []

for i in range(100, data_training_array.shape[0]):
    x_train.append(data_training_array[i - 100:i, 0])
    y_train.append(data_training_array[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)

# Load the model
model = load_model('keras_model.h5')

# Testing Part
past_100_days = data_training.tail(100)
final_df = past_100_days._append(data_testing, ignore_index=True)
input_data = scaler.transform(np.array(final_df).reshape(-1, 1))

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i - 100:i, 0])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)

# Predictions
y_predicted = model.predict(x_test)

y_predicted = y_predicted.reshape(-1, 1)
y_predicted = scaler.inverse_transform(y_predicted).flatten()
y_test = y_test.reshape(-1, 1)
y_test = scaler.inverse_transform(y_test).flatten()

# Final Graph
st.subheader('Predictions V/S Original Graph')
fig2 = plt.figure(figsize=(12, 6))
plt.plot(y_test, 'b', label='Original Price')
plt.plot(y_predicted, 'r', label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)
