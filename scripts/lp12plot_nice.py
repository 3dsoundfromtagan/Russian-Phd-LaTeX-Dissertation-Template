# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:53:01 2026

@author: ostap
"""

import numpy as np
from matplotlib import pyplot as plt
import pathlib
import pandas as pd

colnames = ['col1', 'col2', 'length', 'eff']
df_oi = pd.read_csv('lp01.csv', header=None, names=colnames)
df_ii = pd.read_csv('lp11.csv', header=None, names=colnames)


plt.style.use(r'conf.mplstyle')

fig, ax = plt.subplots(figsize=(5, 2.5), dpi=300, layout='tight')
ax.plot(df_oi['length'],
        df_oi['eff'], '-',
        linewidth=2, label='LP$_{01}$')
ax.plot(df_ii['length'],
        df_ii['eff'], '-',
        linewidth=2, label='LP$_{11}$')
# ax.plot(lengths_theory, theory, '.',
#         markersize=7, label='Estimated (from output spectra)')

ax.set_xlabel('MF length, cm')
ax.set_ylabel('Transmittance, %')
ax.set_xlim(-0, 10)
ax.set_ylim(-0.5, 105)

ax.legend(fontsize=12, framealpha=1)
fig.savefig(r'../../disser/Dissertation/images/imfwm/mf_eff_plot.pdf')


