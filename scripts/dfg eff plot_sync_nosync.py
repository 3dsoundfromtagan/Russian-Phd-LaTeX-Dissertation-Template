# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:53:01 2026

@author: ostap
"""

import numpy as np
from matplotlib import pyplot as plt
import pathlib
import pandas as pd

lengths =  np.arange(1.5, 5.1, 0.5)

sync = np.array([0.99634, 0.98032, 0.97369, 0.89024, 0.71975, 0.54594, 0.26133, 0.1649])
no_sync = np.array([0.99469, 0.98971, 0.98833, 0.97369, 0.96401, 0.92395, 0.85791, 0.6763])


plt.style.use(r'conf.mplstyle')

fig, ax = plt.subplots(figsize=(6, 3), dpi=300, layout='tight')
ax.plot(lengths, no_sync, '.',
        markersize=7, label='Несинхронизированные импульсы', color='black')
ax.plot(lengths, sync, '.',
        markersize=7, label='Синхронизированные импульсы', color=[0.8, 0, 0])


ax.set_ylim(0,1.05)
ax.set_xlabel('Длина ОВ, м')
ax.set_ylabel('Нормированная\nэффективность')


ax.legend(fontsize=12, framealpha=1)
fig.savefig(r'../../disser/Dissertation/images/imfwm/dfg_eff_plot_sync_nosync.pdf')


