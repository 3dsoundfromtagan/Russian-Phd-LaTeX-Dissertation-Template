# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:53:01 2026

@author: ostap
"""

import numpy as np
from matplotlib import pyplot as plt
import pathlib
import pandas as pd

lengths_theory =  np.arange(1.5, 5.1, 0.5)

lengths_exp = np.array([2.3, 2.77, 3, 3.33,
                        3.63, 3.82, 4.1, 4.4,
                        4.7, 5])
theory = np.array([1.0, 0.98, 0.95, 0.89,
                   0.72, 0.535, 0.25, 0.17])
exp = np.array([1.0, 0.99, 0.98, 0.9, 0.75,
                 0.55, 0.35, 0.19, 0.10, 0.07])


plt.style.use(r'conf.mplstyle')

fig, ax = plt.subplots(figsize=(6, 3), dpi=300, layout='tight')
ax.plot(lengths_exp, exp, '.',
        markersize=7, label='Measured')
ax.plot(lengths_theory, theory, '.',
        markersize=7, label='Estimated (from output spectra)')

ax.set_xlabel('OF length, m')
ax.set_ylabel('Normalized efficiency')


ax.legend(fontsize=12, framealpha=1)
# fig.savefig(r'../../disser/Dissertation/images/imfwm/dfg_eff_plot.pdf')


