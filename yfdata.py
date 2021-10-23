# downloads historical data from given assets from yahoo finance, then processes them using Tensorflow.

import yfinance as yf
import pandas as pd
from sklearn import preprocessing
import re
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import BatchNormalization
from matplotlib import pyplot

pd.options.mode.chained_assignment = None  # default='warn'

tickersIndex = ["^NDXT"]
tickersStocks = ["MSFT", "AAPL", "FB", "AMZN", "GOOGL"]  # will collect data for these tickers
tickers = tickersIndex + tickersStocks
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

#creates a model for each stock ticker, then saves under ticker name
#currently does not produce a good model.
#NEEDS WORK DONE. MODEL DOES NOT GENERALISE
def model(features, labels, valX, valY, ticker):
    #defining model
    model = Sequential()
    model.add(LSTM(128, activation='tanh', return_sequences=True, dropout=0.2,  input_shape=(features.shape[1], features.shape[2])))
    model.add(BatchNormalization())
    model.add(LSTM(128, activation='tanh', dropout=0.1))
    model.add(BatchNormalization())
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mae', metrics=["accuracy"]) #needs to do stuff properly

    # fit model
    hist = model.fit(features, labels, validation_data=(valX, valY), epochs=20) #change number of epochs later

    # plot loss during training
    # pyplot.title('Loss / Mean Squared Error')
    # pyplot.plot(hist.history['loss'], label='train')
    # pyplot.plot(hist.history['val_loss'], label='test')
    # pyplot.legend()
    # pyplot.show()
    model.save(f"{ticker}")

#separates data and runs model function for each ticker using indexes and particular stock data
def all_models(features, labels, valX, valY, tickersIndex, tickersStocks):
    for i in range(len(tickersStocks)):
        featuresTemp = np.concatenate((features[:, :, :(2*len(tickersIndex))], features[:, :, (2*len(tickersIndex)+3*i):(2*len(tickersIndex)+3*(i+1))]), axis=2)
        #labelsTemp = np.concatenate((labels[:, :(2*len(tickersIndex))], labels[:, (2*len(tickersIndex)+3*i):(2*len(tickersIndex)+3*(i+1))]), axis=1)
        labelsTemp = labels[:, 2*len(tickersIndex)+3*i+2]
        valXTemp = np.concatenate((valX[:, :, :(2*len(tickersIndex))], valX[:, :, (2*len(tickersIndex)+3*i):(2*len(tickersIndex)+3*(i+1))]), axis=2)
        #valYTemp = np.concatenate((valY[:, :(2*len(tickersIndex))], valY[:, (2*len(tickersIndex)+3*i):(2*len(tickersIndex)+3*(i+1))]), axis=1)
        valYTemp = valY[:, 2*len(tickersIndex)+3*i+2]
        model(featuresTemp, labelsTemp, valXTemp, valYTemp, tickersStocks[i])

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

all_models(trainX, trainY, valX, valY, tickersIndex, tickersStocks)
