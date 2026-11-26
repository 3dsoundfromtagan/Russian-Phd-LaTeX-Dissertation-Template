# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 00:09:26 2026

@author: ostap
"""

import numpy as np
import matplotlib.pyplot as plt

# Функция sinc^2
def sinc2(x):
    return (np.sinc(x / np.pi))**2

X_LIM = 2.2 * np.pi
WIDTH = 4
HEIGHT = 2
arrow_color = (0.3,0.0,0.1)
x = np.linspace(-X_LIM, X_LIM, 1000)

# Настройка осей (толстые линии для иконок)
def setup_ax(ax):
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_linewidth(0)
    ax.spines['bottom'].set_linewidth(0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-X_LIM, X_LIM)
    ax.set_ylim(-0.02, 1.08)

# ==========================================
# 1. Сдвиг кривой (Kinetics shift)
# ==========================================


fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT))
# C0 (было) - правее, C1 (стало) - левее
ax.plot(x, sinc2(x - 1), color='C0', lw=4) 
ax.plot(x, sinc2(x + 1), color='C1', lw=4) 

# Стрелка сдвига (от старого пика к новому)
ax.annotate('', xy=(-1.7, 1.07), xytext=(1.4, 1.07),
            arrowprops=dict(arrowstyle='->', color=arrow_color, lw=5, mutation_scale=20))

setup_ax(ax)
plt.tight_layout()
plt.savefig('../Presentation/images/icon_shift.pdf', transparent=True, bbox_inches='tight', pad_inches=0.05)


# # ==========================================
# # 2. Уменьшение FWHM (Сужение)
# # ==========================================
fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT))
# C0 (было) - шире, C1 (стало) - уже
ax.plot(x, sinc2(x / 1.5), color='C0', lw=4) 
ax.plot(x, sinc2(x*1.6), color='C1', lw=4)
ax.annotate('', xy=(1.05, 0.2), xytext=(3.0, 0.2),
            arrowprops=dict(arrowstyle='->', color=arrow_color, lw=5, mutation_scale=20))

setup_ax(ax)
plt.tight_layout()
plt.savefig('../Presentation/images/icon_fwhm.pdf', transparent=True, bbox_inches='tight', pad_inches=0.05)

# # ==========================================
# # 3. Увеличение пиковой эффективности
# # ==========================================
fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT))
# C0 (было) - ниже, C1 (стало) - выше
ax.plot(x, 0.5 * sinc2(x), color='C0', lw=4) 
ax.plot(x, sinc2(x), color='C1', lw=4)

# Стрелка роста (вертикально вверх от старого пика)
ax.annotate('', xy=(0, 1.0), xytext=(0, 0.5),
            arrowprops=dict(arrowstyle='->', color=arrow_color, lw=5, mutation_scale=20))

setup_ax(ax)
plt.tight_layout()
plt.savefig('../Presentation/images/icon_peak.pdf', transparent=True, bbox_inches='tight', pad_inches=0.05)


print("Done! Icons generated.")