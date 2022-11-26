import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from db import BotDB
from pprint import pprint

BotDB = BotDB('/Users/jcu/Desktop/MyProjects/Company INC/server.db')
dimension_graf_rate = BotDB.vCollector(table='value_main', where='name', meaning='dimension_graf_rate') #размерность данных для графика
# print(BotDB.get_alls('*','graf_rate_usd'))

graf_rate_usd = BotDB.get_alls('*','graf_rate_usd')
graf_rate_btc = BotDB.get_alls('*','graf_rate_btc')


spisok = []
for i in graf_rate_usd:
    time = i[1].split()[0].split(':')
    time = str(int(time[0]))+ ":" + time[1]
    spisok.append({
        'time':time,
        'percent':i[3],
        'rate':i[-1],
        'old_rate':i[2]
    })

spisok2 = []
for i in graf_rate_btc:
    time = i[1].split()[0].split(':')
    time = str(int(time[0]))+ ":" + time[1]
    spisok2.append({
        'time':time,
        'percent':i[3],
        'rate':i[-1],
        'old_rate':i[2]
    })

df = pd.DataFrame(spisok) #формируем Data Frame
df2 = pd.DataFrame(spisok2) #формируем Data Frame

colors = []
for i in spisok:
    if i['percent'] > 0:
        colors.append('green')
    else:
        colors.append('red') 

uprate = spisok[-1]['rate'] - spisok[0]['rate']
perc_uprate = round((spisok[0]['rate'] * 100) / spisok[-1]['rate'],2)


if uprate > 0:
    sign ='↑'
    text_perc_uprate =sign + str(perc_uprate) + '%'
else:
    sign = '↓'
    text_perc_uprate =sign + str(perc_uprate) + '%'

maxy = max([i['rate'] for i in spisok]) + 20

# Plot Line1 (Left Y Axis)
fig, ax1 = plt.subplots(1,1,figsize=(16,9), dpi= 80)
ax1.plot(df.get('time'), df.get('rate'), color='tab:red')

# Plot Line2 (Right Y Axis)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot(df.get('time'), df2.get('rate'), color='tab:blue')

# Decorations
# ax1 (left Y axis)
ax1.set_xlabel('Время', fontsize=20)
ax1.tick_params(axis='x', rotation=0, labelsize=12)
ax1.set_ylabel('USD', color='tab:red', fontsize=20)
ax1.tick_params(axis='y', rotation=0, labelcolor='tab:red' )
ax1.grid(alpha=.4)

# ax2 (right Y axis)
ax2.set_ylabel("BTC", color='tab:blue', fontsize=20)
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.set_xticks(df.get('time'))
ax2.set_xticklabels(df.get('time'), rotation=90, fontdict={'fontsize':10})
ax2.set_title("Доллар и Биткоин", fontsize=22)
fig.tight_layout()
plt.show()