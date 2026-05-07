# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:53:01 2026

@author: ostap
"""

import numpy as np
from matplotlib import pyplot as plt
import pathlib
import pandas as pd

file = pathlib.Path(r'../../fibershg/raw data/3564/2/from power  LOT OF TIMES/'
                    + r'202410031417.csv')

df = pd.read_csv(file)
df.loc[:, 'power'] = df['power'].rolling(5).median()
up = df.iloc[: int(len(df)//2)]
down = df.iloc[int(len(df)//2):]

plt.style.use(r'../../fibershg/conf67/conf.mplstyle')

fig, ax = plt.subplots(figsize=(7, 3.5), dpi=300, layout='tight')
podgon_sh_power = 1 / 1.5
ax.plot(up['power']/10, up['green'] / up['power'] * 100 / 1000 * podgon_sh_power, '.',
        markersize=3, label='Увеличение мощности')
ax.plot(down['power']/10, down['green'] / down['power'] * 100 / 1000 * podgon_sh_power, '.',
        markersize=3, label='Уменьшение мощности')
ax.set_xlabel('Пиковая мощность накачки, кВт')
ax.set_ylabel('Эффективность ГВГ, %')
ax.axvline(x=0.05, color='#B62C0C', linestyle='--',
           linewidth=2, label='Уровень измерения КФС')

ax.legend(fontsize=12, framealpha=1)
# fig.savefig(r'../../disser/Dissertation/images/fibershg/vac.pdf')