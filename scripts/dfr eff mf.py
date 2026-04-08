# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:53:01 2026

@author: ostap
"""

import numpy as np
from matplotlib import pyplot as plt
import pathlib
import pandas as pd



lengths = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3, 3.5, 4])
no_mf = np.array([1, 0.98, 0.96, 0.94, 0.9, 0.63673, 0.42384, 0.29042])
mf = np.array([1, 1, 0.99, 0.98, 0.95, 0.87461, 0.60724, 0.40433])


plt.style.use(r'conf.mplstyle')

fig, ax = plt.subplots(figsize=(6, 3), dpi=300, layout='tight')

ax.plot(lengths, mf, '.',
        markersize=7, label='With MF')
ax.plot(lengths, no_mf, '.',
        markersize=7, label='Without MF')

ax.set_xlabel('OF length, m')
ax.set_ylabel('Normalized efficiency')


ax.legend(fontsize=12, framealpha=1)
fig.savefig(r'../../disser/Dissertation/images/imfwm/dfg_eff_mf.pdf')


