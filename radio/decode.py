import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import numpy as np
from scipy.signal import lfilter


class dataChunk:
    def __init__(self, data) -> None:
        data = data[200:-200]
        self.data = np.array(data)
        self.dataLen = len(data)
        self.amplitude = max(self.data)
        self.norm_data = self.data / self.amplitude
        self.period = 200
        self.phaseDiff = self.findFirstPeak() / self.period * 2 * np.pi

        # calculate phase diff with cosine

    def calphaseCos(self):

        return self.findFirstPeak(i) / self.period * 2 * np.pi

    def findFirstPeak(self):

        data = self.norm_data[:self.period]
        index = -1
        max_num = -2
        for i, dat in enumerate(data):
            if dat > max_num:
                max_num = dat
                index = i
        return index

    def getConstellCord(self, maxAmp):
        return self.amplitude / maxAmp * np.sin(self.phaseDiff), self.amplitude / maxAmp * np.cos(self.phaseDiff)


with open("data.dat", 'r') as f:
    data = f.read().split(",")


data = [float(x) for x in data]
data_length = 800
# assuming t = 200

plt.plot(data)
plt.show()


subData = []
amp = 0
for i in range(0, len(data), data_length):
    subData.append(dataChunk(data[i:i + data_length]))
    peak = subData[-1].amplitude
    if peak > amp:
        amp = peak


coordx = []
coordy = []
constellation = [["0000", "0100", "1100", "1000"],
                 ["0001", "0101", "1101", "1001"],
                 ["0011", "0111", "1111", "1011"],
                 ["0010", "0110", "1110", "1010"]]
res = ""
xl = []
yl = []
for d in subData:
    x, y = d.getConstellCord(amp)
    xl.append(x)
    yl.append(y)
    x = int(x / 0.4 + 2)
    y = int(y / 0.4 + 2)
    res += constellation[3 - y][x]
plt.scatter(xl, yl)
plt.show()
print(res)
