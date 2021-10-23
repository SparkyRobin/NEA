# downloads historical data from given assets from yahoo finance, then processes them using Tensorflow.

import yfinance as yf
import pandas as pd
from sklearn import preprocessing
import re
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

pd.options.mode.chained_assignment = None  # default='warn'

tickers = ["^NDXT", "MSFT", "AAPL", "FB", "AMZN", "GOOGL"]  # will collect data for these tickers
samplePeriod = "60d"  # length of time historic data gathered over
sampleInterval = "1h"  # interval historic data gathered at
predictTime = 1  # how many hours ahead it will predict
splitPerc = 0.8  # percentage split training to validation data

hist = pd.DataFrame()


def increase(current, future):
    if future > current:
        return 1
    else:
        return 0


# data is a pandas dataframe
# lents default to 30, but can be changed when called
# returns arrays with values for close volume and increase for all tickers for each time period
def process(data, lents=30):
    for col in data.columns:

        # delete future price as irrelevant
        if re.search("._future$", str(col)):
            data = data.drop(columns=str(col))

        # normalises data not already in normalised format.
        elif not re.search("._increase$", str(col)):
            if sum(data[col].values) != 0:
                data[col] = data[col].pct_change()
                data[col].dropna(inplace=True)
                data[col] = preprocessing.scale(data[col].values)

            # drops columns where all values are 0, as these are indexes which have no market volume
            else:
                data = data.drop(columns=str(col))
    data.dropna(inplace=True)

    xseries = []
    yseries = []
    i = 0

    while i + lents < int(list(data.shape)[0]):
        xsubseries = []
        ysubseries = []
        for col in data.columns:
            xsubseries.append(data[col].values[i:i+lents-1])
            ysubseries.append(data[col].values[i+lents])
        xseries.append(xsubseries)
        yseries.append(ysubseries)
        i += 1
    return xseries, yseries

def model(features, labels, valX, valY):
    model = Sequential()
    model.add(LSTM(128, activation='relu', return_sequences=True, input_shape=(29, 17)))
    model.add(LSTM(128, activation='relu'))
    model.add(Dense(17))
    model.compile(optimizer='adam', loss='mse', metrics=["accuracy"]) #needs to do stuff properly
    # fit model
    model.fit(features, labels, validation_data=(valX, valY), epochs=400) #change later

# collect close prices and volumes for each of ticker into one dataframe
for ticker in tickers:
    sTicker = yf.Ticker(ticker)
    history = sTicker.history(period=f"{samplePeriod}", interval=f"{sampleInterval}")
    history.rename(columns={"Close": f"{ticker}_close", "Volume": f"{ticker}_volume"}, inplace=True)
    if len(hist) == 0:
        hist = history[[f"{ticker}_close", f"{ticker}_volume"]]
    else:
        hist = hist.join(history[[f"{ticker}_close", f"{ticker}_volume"]])

    # adding new columns for each stock for if price increases over predictTime intervals
    tempFuture = history[f"{ticker}_close"].shift(-predictTime)
    tempDF = pd.DataFrame(data={f"{ticker}_future": history[f"{ticker}_close"].shift(-predictTime), f"{ticker}_increase": list(map(increase, history[f"{ticker}_close"], tempFuture))})
    hist = hist.join(tempDF)
    del tempDF

hist.dropna(inplace=True)  # remove all rows with NaN

# split all into training and validation data
allLen = int(list(hist.shape)[0])
split = int((allLen*splitPerc)//1)
allTrain = hist.head(split)
allVal = hist.tail(allLen - split)

# processing training and validation data
trainX, trainY = process(allTrain)
valX, valY = process(allVal)

trainX = np.array(trainX)
trainX = np.swapaxes(trainX, 1, 2)
trainY = np.array(trainY)

valX = np.array(valX)
valX = np.swapaxes(valX, 1, 2)
valY = np.array(valY)

model(trainX, trainY, valX, valY)
