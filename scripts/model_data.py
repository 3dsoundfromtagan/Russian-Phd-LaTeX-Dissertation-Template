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
fig, ax = plt.subplots(figsize=(7.5, 3), dpi=300, layout='tight')
ax.plot(model_data['yb_wl_corr'],
        plateau_lvl + (-plateau_lvl+38) *\
            init_spectrum(model_data['yb_wl_corr'], central = 1030, width = 0.2), '-',
        linewidth=1, label='Изначальная')
    
    
ax.plot(model_data['yb_wl_corr'],
        (model_data['yb_no_synch'] - plateau_lvl)*\
            apodization(model_data['yb_wl_corr'], 1030, 0.003) + plateau_lvl, '-',
        linewidth=1, label='Учёт ОМЧВС на 1030 nm')
    



ax.set_xlabel('$\lambda$, нм')
ax.set_ylabel('Спектральная плот-\nность мощности, дБ')
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
    


bax = brokenaxes(xlims=((980, 1060), (1550, 1640)),
                 hspace=0.02,
                 wspace=0.07, despine=False)


wl_concat = pd.concat([model_data['yb_wl_corr'], model_data['er_wl_corr']])
bax.plot(wl_concat,
        np.hstack([plateau_lvl + (-plateau_lvl+39) *\
            init_spectrum(model_data['yb_wl_corr'], central = 1030, width = 0.2),
                plateau_lvl + (-plateau_lvl+28) *\
                    init_spectrum(model_data['er_wl_corr'], central = 1560, width = 0.2)]), '-',
        linewidth=1, label='Изначальная')
    
bax.plot(wl_concat,
        np.hstack([model_data['yb_no_synch']*\
                   np.where((model_data['yb_wl_corr'] < 1040), 1, 200),
                   model_data['er_no_synchr']]), '-',
        linewidth=1, label='Учёт ОМЧВС')


# bax.plot(model_data['er_wl_corr'], np.cos(10 * x), label='FMFWM')


bax.legend(fontsize=12, framealpha=1)
bax.set_xlabel('$\lambda$, нм')
bax.set_ylabel('Спектральная плот-\nность мощности, дБ')
bax.set_ylim(-30, 41)
# fig.savefig(r'../../disser/Dissertation/images/imfwm/fmfwm.pdf')

# %% the same wo bax

plt.rcParams.update({'font.size': 11})
plateau_lvl = model_data['yb_no_synch'][1]

# Создаём ДВА графика рядом
fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(9, 3.5), dpi=300, sharey=True)

# Настраиваем разные диапазоны X (разрыв между 1060 и 1550)
ax_left.set_xlim(980, 1060)
ax_right.set_xlim(1550, 1640)

# Объединяем данные
wl_concat = pd.concat([model_data['yb_wl_corr'], model_data['er_wl_corr']])
y_initial = np.hstack([
    plateau_lvl + (-plateau_lvl+39) * init_spectrum(model_data['yb_wl_corr'], central=1030, width=0.2),
    plateau_lvl + (-plateau_lvl+28) * init_spectrum(model_data['er_wl_corr'], central=1560, width=0.2)
])

y_with_fwm = np.hstack([
    model_data['yb_no_synch'] * np.where((model_data['yb_wl_corr'] < 1040), 1, 200),
    model_data['er_no_synchr']
])

# Рисуем данные на ОБОИХ графиках
ax_left.plot(wl_concat[:len(model_data['yb_wl_corr'])], 
             y_initial[:len(model_data['yb_wl_corr'])], '-',
             linewidth=1, label='Изначальная')
ax_left.plot(wl_concat[:len(model_data['yb_wl_corr'])], 
             y_with_fwm[:len(model_data['yb_wl_corr'])], '-',
             linewidth=1, label='Учёт ОМЧВС')

ax_right.plot(wl_concat[len(model_data['yb_wl_corr']):], 
              y_initial[len(model_data['yb_wl_corr']):], '-',
              linewidth=1)
ax_right.plot(wl_concat[len(model_data['yb_wl_corr']):], 
              y_with_fwm[len(model_data['yb_wl_corr']):], '-',
              linewidth=1)

# Настройка внешнего вида
ax_left.set_ylabel('Спектральная плот-\nность мощности, дБ')
ax_left.set_xlabel('')
ax_right.set_xlabel('')

# ОДНА подпись X по центру всего рисунка
fig.text(0.5, 0.02, '$\lambda$, нм', 
         va='center', ha='center', fontsize=14)

# Одинаковый диапазон по Y
ax_left.set_ylim(-30, 41)

ax_left.yaxis.set_major_locator(plt.MaxNLocator(4))

# Убираем внутренние рамки (чтобы создать видимость разрыва)
ax_left.spines['right'].set_visible(False)
ax_right.spines['left'].set_visible(False)

# Убираем подписи Y у правого графика (они одинаковые)
ax_right.tick_params(axis='y', labelleft=False)

# НАСТРАИВАЕМ РАССТОЯНИЕ МЕЖДУ ГРАФИКАМИ (решает проблему с чёрточками!)
plt.subplots_adjust(wspace=0.04)  # уменьшите до 0.02 если нужно ещё ближе

# Рисуем диагональные чёрточки (разрыв) между графиками
d = 0.015  # длина чёрточек

# Правый верхний угол левого графика
ax_left.plot((1-d, 1+d), (1-d, 1+d), transform=ax_left.transAxes, 
             color='k', clip_on=False, linewidth=1)
ax_left.plot((1-d, 1+d), (-d, d), transform=ax_left.transAxes, 
             color='k', clip_on=False, linewidth=1)

# Левый верхний угол правого графика
ax_right.plot((-d, d), (1-d, 1+d), transform=ax_right.transAxes, 
              color='k', clip_on=False, linewidth=1)
ax_right.plot((-d, d), (-d, d), transform=ax_right.transAxes, 
              color='k', clip_on=False, linewidth=1)

# Легенда (только на левом графике)
ax_left.legend(fontsize=12, framealpha=1)
ax_right.tick_params(axis='y', labelleft=False, left=False)

# Сохранить (раскомментируйте если нужно)
# fig.savefig(r'../../disser/Dissertation/images/imfwm/fmfwm.pdf')



# %% imfwm
plateau_lvl = model_data['yb_no_synch'][1]
fig, ax = plt.subplots(figsize=(7, 3), dpi=300, layout='tight')
ax.plot(model_data['yb_wl_corr'],
        plateau_lvl + (-plateau_lvl+38) *\
            init_spectrum(model_data['yb_wl_corr'], central = 1030, width = 0.2), '-',
        linewidth=1, label='Изначальная')

ax.plot(model_data['yb_wl_corr']-0.15,
        model_data['yb_no_synch']*\
                   np.where((model_data['yb_wl_corr'] < 1040), 1, 200), '-',
        linewidth=1, label='Учёт ММЧВС LP$_{01}$')
    
ax.plot(model_data['yb_wl_corr']+0.15,
        model_data['yb_no_synch']*\
                   np.where((model_data['yb_wl_corr'] > 1020), 1, 200), '-',
        linewidth=1, label='Учёт ММЧВС LP$_{11}$')

ax.set_xlabel('$\lambda$, нм')
ax.set_ylabel('Спектральная плот-\nность мощности, дБ')
ax.set_xlim(980, 1080)
ax.set_ylim(-30, 41)

ax.legend(fontsize=12, framealpha=1)
# fig.savefig(r'../../disser/Dissertation/images/imfwm/imfwm.pdf')

