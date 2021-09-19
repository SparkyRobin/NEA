import csv
import tensorflow as tf

def normalise(data):
    data[j].sort()
    min = data[j][0]
    max = data[j][-1]
    for i in range (len(data)):
        data[i] = data[i]/(max-min)
    return data


reader = csv.DictReader(open("historical_BTCUSD_hr.csv"))
open = []
close = []
time = []
percChange = []
gainLoss = []
unix = []
for raw in reader:
    open += [float(raw.get("Open"))]
    close += [float(raw.get("Close"))]
    time += [raw.get("Date")] #Make tu use time of day
    percChange += [(float(raw.get("Close"))-float(raw.get("Open")))/float(raw.get("Open"))]
    #volMeasure
    unix += [raw.get("Unix Timestamp")]
    if float(raw.get("Open")) < float(raw.get("Close")):
        gainLoss += [1]
    elif float(raw.get("Open")) > float(raw.get("Close")):
        gainLoss += [-1]
    else:
        gainLoss += [0]

bsw = [0]*len(gainLoss)
gainLoss.reverse(); open.reverse(); close.reverse(); time.reverse; percChange.reverse(); unix.reverse()
buyFee = 0.001
sellFee = 0.001
i = 0
while i < (len(gainLoss)):
    if gainLoss[i] == 1:
        opener = open[i]
        j = i
        while j < len(gainLoss) and gainLoss[j] != -1:
            closer = close[j]
            j += 1
        if opener*buyFee < closer:
            bsw[i] = 1
            for s in range(i+1, j):
                bsw[s] = 0
        else:
            for s in range(i, j):
                bsw[s] = 0

    elif gainLoss[i] == -1:
        opener = open[i]
        j = i
        while j < len(gainLoss) and gainLoss[j] != 1:
            closer = close[j]
            j += 1
        if opener > closer + opener * sellFee:
            bsw[i] = -1
            for s in range(i + 1, j):
                bsw[s] = 0
        else:
            for s in range(i, j):
                bsw[s] = 0

    else:
        bsw[i] = 0
        j = i+1

    i = j

pcn = normalise(percChange)
roundSeventy = round(len(open) * 0.7)
roundNinety = round(len(open)*0.9)
datasetTraining = [open[:roundSeventy], close[:roundSeventy], percChange[:roundSeventy], bsw[:roundSeventy]]