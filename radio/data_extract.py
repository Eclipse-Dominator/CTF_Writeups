from pwn import *
import numpy as np
import matplotlib.pyplot as plt


def getData(blk_num):  # extract data in 5 chunks
    conn = remote("challs1.nusgreyhats.org", 5213)
    text = conn.recvuntil(b'seperated by space :', drop=True).decode('utf-8')
    text = text.split("\n")
    for line in text:

        if line.startswith("Frequency"):
            frequency = float(line.split("=")[1].strip()[:-5])
        elif line.startswith("Total signal time "):
            time_total = float(line.split("=")[1].strip()[:-4])

    blk = 1 / frequency * 5
    interval = blk / 1000
    timestamp = []
    for i in range(1000):
        timestamp.append(blk_num * blk + i * interval)
    timestamp = [k for k in timestamp if k < time_total]
    queryString = " ".join([f"{k}" for k in timestamp])
    queryString += "\n"
    conn.send(bytes(queryString, "utf-8"))
    text = conn.recvuntil(b'~~', drop=True).decode('utf-8')
    conn.close()
    return timestamp, [float(d) for d in text.split("\n")[2].split()]


data = []
for i in range(76):
    _, data_t = getData(i)
    data.extend(data_t)

with open("data.dat", 'w+') as f:
    f.write(",".join((str(s) for s in data)))
plt.plot(data)
plt.grid()
plt.show()
