# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 02:15:36 2026

@author: ostap
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 16

# Параметры
t0 = 1.0
h = 1.0
deltah = 0.9

# Данные: два горизонтальных участка
t = [0.0, t0, t0, 2*t0]
y = [h + deltah/2, h + deltah/2, h - deltah/2, h - deltah/2]

# График
fig, ax = plt.subplots(figsize=(3.5, 1.8))
ax.plot(t, y, color="C0", lw=4)

# Оформление
# ax.set_xlabel("Время, t")
# ax.set_ylabel("Коэффициент теплоотдачи, h")
ax.set_xlim(0, 2*t0)
ax.set_ylim(h - deltah/1.5, h + deltah/1.5)
ax.set_xticks([0, t0])
ax.set_xticklabels(["0", r"$t_0$"])

ax.set_yticks([h-deltah/2, h, h+deltah/2])
ax.set_yticklabels([r"$h-\Delta h/2$",r"$h$",r"$h+\Delta h/2$"])

ax.grid(True, ls=":", alpha=0.6)
ax.axvline(t0, color="gray", ls="--", lw=1)

ax.axhline(h, color="black", ls="--", lw=3)


plt.tight_layout()
fig.savefig(r'../../disser/Presentation/images/h_vs_t.pdf')
plt.show()