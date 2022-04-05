import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import matplotlib.patches as patches
from db import BotDB
from pprint import pprint

BotDB = BotDB('/Users/jcu/Desktop/MyProjects/Company INC/server.db')
dimension_graf_rate = BotDB.vCollector(table='value_main', where='name', meaning='dimension_graf_rate') #размерность данных для графика
# print(BotDB.get_alls('*','graf_rate_usd'))

graf_rate_usd = BotDB.get_alls('*','graf_rate_usd')
graf_rate_btc = BotDB.get_alls('*','graf_rate_btc')


spisok = []
for i in graf_rate_usd:
    spisok.append({
        'time':i[1].split()[0],
        'percent':i[3],
        'rate':i[-1]
    })

df = pd.DataFrame(spisok) #формируем Data Frame


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

fig, ax = plt.subplots(figsize=(16,10), facecolor='white', dpi= 80)
ax.vlines(x=df.index, ymin=0, ymax=df.get('rate'), color=colors, alpha=0.7, linewidth=12.5)
# ax.vlines(x=df.index, ymin=0, ymax=df.get('quantity'), color='#c7c91e', alpha=0.2, linewidth=13.5)

# Annotate Text
for i, cty in enumerate(df.get('percent')):
    heigh = [i for i in df.get('rate')]
    ax.text(i, heigh[i]+1, round(cty, 2), horizontalalignment='center')

ax.text(-0.5, maxy - 10, f'Рост курса за последние {dimension_graf_rate} мин: {spisok[-1]["rate"]} $ ({text_perc_uprate})', horizontalalignment='left', verticalalignment='center', fontdict={'size':15, 'weight':600})


# Title, Label, Ticks and Ylim
ax.set_title(f'BANK {spisok[0]["time"]} - {spisok[-1]["time"]}', fontdict={'size':22,'weight':700})
ax.set(ylim=(0,maxy))
plt.ylabel(ylabel='USD',fontdict={'size':17,'weight':500})
plt.xticks(df.index, df.get('time'), horizontalalignment='center', fontsize=12)

plt.show()