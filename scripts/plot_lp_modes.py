# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:26:51 2026

@author: ostap
"""

import lpmodes
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

dn = 3e-3
cladding_n = 1.45
core_n = cladding_n + dn
core_radius = 5
wavelength = 0.33

modes = lpmodes.find_modes(core_radius, core_n, cladding_n, wavelength)


grid_size = 300        # pixels
max_plot_radius = 9   # microns

# for mode in modes:

#     mode_plot = mode.plot_amplitude(grid_size, max_plot_radius)
    
#     plt.figure(dpi=150)
#     max_val = np.max(np.abs(mode_plot))
#     plt.imshow(mode_plot, cmap = lpmodes.ampcol(), vmin = -max_val, vmax = max_val)
    
n_rows = 3
n_cols = 4

fig = plt.figure(figsize=(15, 9), dpi=300)
gs = gridspec.GridSpec(n_rows, n_cols, wspace=0.05, hspace=0.05)

for idx, mode in enumerate(sorted(modes, key=lambda mode: mode.n_eff, reverse=True)):
    row = idx // n_cols
    col = idx % n_cols
    ax = fig.add_subplot(gs[row, col])
    
    mode_plot = mode.plot_amplitude(grid_size, max_plot_radius)
    max_val = np.max(np.abs(mode_plot))
    ax.imshow(mode_plot, cmap=lpmodes.ampcol(), vmin=-max_val, vmax=max_val)
    ax.axis('off')
    ax.set_title(f"LP$_{{{mode.l}{mode.m}}}$", fontsize=24, pad=0, y=0.95)

plt.subplots_adjust(left=0.00, right=1.00, top=0.98, bottom=0.00, wspace=0.05, hspace=0.05)
plt.show()

fig.savefig(r'../../disser/Dissertation/images/review/lp_modes.pdf', 
            dpi=300, bbox_inches='tight', pad_inches=0.0)