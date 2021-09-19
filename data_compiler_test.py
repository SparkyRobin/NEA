import requests
import json
import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from matplotlib.widgets import Slider, Button, RadioButtons
import sqlite3

response = requests.get("https://api.btctools.io/api/fear-greed-chart?period=1y")
def jprint(x):
    print(json.dumps(x, sort_keys=True, indent=4))

da = response.json()["data"]

xyz = []
abc = []
for d in da:
    v = d["v"]
    xyz.append(v)
    t = d["t"]
    abc.append(t)

y_filtered = savgol_filter(xyz, 31, 5)


fig = plt.figure()
ax = fig.subplots()
p = ax.plot(abc, xyz, '-*')
p, = ax.plot(abc, y_filtered, 'g')
#p2 = ax.plot(abc, y_filtered, '-*')
plt.subplots_adjust(bottom=0.25)

axa = plt.axes([0.25, 0.15, 0.65, 0.03])
axb = plt.axes([0.25, 0.1, 0.65, 0.03])
a = Slider(axa, 'a', 11, 31.0, 19, valstep = 2)
b = Slider(axb, 'b', 0.0, 20.0, 3, valstep = 1)

def update(val):
    y_filtered = savgol_filter(xyz, int(a.val), int(b.val))
    p, = ax.plot(abc, y_filtered, 'g')
    plt.draw()

a.on_changed(update)
b.on_changed(update)

plt.show()