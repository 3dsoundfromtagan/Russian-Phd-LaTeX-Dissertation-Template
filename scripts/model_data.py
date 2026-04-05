# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:53:01 2026

@author: ostap
"""

import numpy as np
from matplotlib import pyplot as plt
import pathlib
import pandas as pd
from brokenaxes import brokenaxes

# def apodization(wl, central = 1030, width = 20, plateau_lvl = 0):
#     return np.exp(-(wl - central)**2 / (2 * width ** 2)) + plateau_lvl

def apodization(wl, central = 1030, width = 20, peak_val = 1):
    return -width * (wl - central)**2 + peak_val
model_data = pd.read_csv('model_data.csv')

def init_spectrum(wl, central=1030, width=0.1):
    return np.where(((wl > central - width / 2) & \
                     (wl < central + width / 2)), 1, 0)


plt.style.use(r'conf.mplstyle')

# %% only pump fm fwm
plateau_lvl = model_data['yb_no_synch'][1]
fig, ax = plt.subplots(figsize=(7, 3), dpi=300, layout='tight')
ax.plot(model_data['yb_wl_corr'],
        plateau_lvl + (-plateau_lvl+38) *\
            init_spectrum(model_data['yb_wl_corr'], central = 1030, width = 0.2), '-',
        linewidth=1, label='Initial')
    
    
ax.plot(model_data['yb_wl_corr'],
        (model_data['yb_no_synch'] - plateau_lvl)*\
            apodization(model_data['yb_wl_corr'], 1030, 0.003) + plateau_lvl, '-',
        linewidth=1, label='Only FMFWM at 1030 nm')
    



ax.set_xlabel('Wavelength, nm')
ax.set_ylabel('Spectral Power, dB')
ax.set_xlim(1020, 1040)
ax.set_ylim(-30, 41)

ax.legend(fontsize=12, framealpha=1)
# fig.savefig(r'../../disser/Dissertation/images/imfwm/fmfwm_1030.pdf')

# %% only fm fwm
plateau_lvl = model_data['yb_no_synch'][1]
fig = plt.figure(figsize=(7, 3),dpi=300, layout='tight')
# ax.plot(model_data['yb_wl_corr'],
#         plateau_lvl + (-plateau_lvl+39) *\
#             init_spectrum(model_data['yb_wl_corr'], central = 1030, width = 0.2), '-',
#         linewidth=1, label='Initial')
    
    
# ax.plot(model_data['yb_wl_corr'],
#         (model_data['yb_no_synch'] - plateau_lvl)*\
#             apodization(model_data['yb_wl_corr'], 1030, 0.003) + plateau_lvl, '-',
#         linewidth=1, label='Only FMFWM at 1030 nm')
    


bax = brokenaxes(xlims=((980, 1060), (1550, 1640)), hspace=0.05)


wl_concat = pd.concat([model_data['yb_wl_corr'], model_data['er_wl_corr']])
bax.plot(wl_concat,
        np.hstack([plateau_lvl + (-plateau_lvl+39) *\
            init_spectrum(model_data['yb_wl_corr'], central = 1030, width = 0.2),
                plateau_lvl + (-plateau_lvl+28) *\
                    init_spectrum(model_data['er_wl_corr'], central = 1560, width = 0.2)]), '-',
        linewidth=1, label='Initial')
    
bax.plot(wl_concat,
        np.hstack([model_data['yb_no_synch']*\
                   np.where((model_data['yb_wl_corr'] < 1040), 1, 200),
                   model_data['er_no_synchr']]), '-',
        linewidth=1, label='FMFWM')


# bax.plot(model_data['er_wl_corr'], np.cos(10 * x), label='FMFWM')


bax.legend(fontsize=12, framealpha=1)
bax.set_xlabel('Wavelength, nm')
bax.set_ylabel('Spectral Power, dB')
bax.set_ylim(-30, 41)
# fig.savefig(r'../../disser/Dissertation/images/imfwm/fmfwm.pdf')

# %% imfwm
plateau_lvl = model_data['yb_no_synch'][1]
fig, ax = plt.subplots(figsize=(7, 3), dpi=300, layout='tight')
ax.plot(model_data['yb_wl_corr'],
        plateau_lvl + (-plateau_lvl+38) *\
            init_spectrum(model_data['yb_wl_corr'], central = 1030, width = 0.2), '-',
        linewidth=1, label='Initial')

ax.plot(model_data['yb_wl_corr']-0.15,
        model_data['yb_no_synch']*\
                   np.where((model_data['yb_wl_corr'] < 1040), 1, 200), '-',
        linewidth=1, label='IMFWM LP$_{01}$')
    
ax.plot(model_data['yb_wl_corr']+0.15,
        model_data['yb_no_synch']*\
                   np.where((model_data['yb_wl_corr'] > 1020), 1, 200), '-',
        linewidth=1, label='IMFWM LP$_{11}$')

ax.set_xlabel('Wavelength, nm')
ax.set_ylabel('Spectral Power, dB')
ax.set_xlim(980, 1080)
ax.set_ylim(-30, 41)

ax.legend(fontsize=12, framealpha=1)
# fig.savefig(r'../../disser/Dissertation/images/imfwm/imfwm.pdf')

