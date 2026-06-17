# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 23:34:13 2023
create funny _dick_pick to iclo 2024
@author: ostap
"""

import pandas as pd
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from scipy.optimize import fsolve
import math

font = {
        'size'   : 16}
plt.rc('font', **font)

def exp_heat(t, tau = 100, T0 = 1, t_heat_start = 0):
    return T0 * (1-np.exp(-(t-t_heat_start)/tau))
    
def exp_cool(t, tau = 100, T0 = 1, t_cool_start = 0, t_heat_start = 0): 
    return T0 * (np.exp(-(t-t_cool_start)/tau)-np.exp(-(t-t_heat_start)/tau))


def func(t, tau = 100, T0 = 1, t_cool_start = 0, t_heat_start = 0):
    return exp_heat(t, tau, T0, t_heat_start)-\
        exp_cool(t, tau, T0, t_cool_start, t_heat_start)

def heat_deriv(t, tau = 100, T0 = 1, t_heat_start = 0):
    return T0 / tau * np.exp(-(t - t_heat_start) / tau)

def cool_deriv(t, tau = 100, T0 = 1, t_cool_start = 0, t_heat_start = 0):
    return T0 / tau * (np.exp(-(t - t_heat_start) / tau) - 
                       np.exp(-(t - t_cool_start) / tau)) 

def straight_heat(t, t0, tau=100, T0=1, t_heat_start=0):

    return exp_heat(t0, tau, T0, t_heat_start) +\
        heat_deriv(t0, tau, T0, t_heat_start) * (t - t0)

def straight_cool(t, t0, tau=100, T0=1, t_heat_start=0,
                  t_cool_start=0):

    return exp_cool(t0, tau, T0, t_cool_start, t_heat_start) +\
        cool_deriv(t0, tau, T0, t_cool_start, t_heat_start) * (t - t0)


th = 100
tc = 150
tau = 100
T0 = 1.6
N = 1000
MAX_TIME = th + tc

default_args = {'tau' : tau, 'T0' : T0, 't_heat_start' : 0}
time = np.linspace(0, MAX_TIME, N)

colors = {"cool": "#3AE6CA",
          "heat": "#E6AC0C"
    }

fig, ax = plt.subplots()
fig.set_size_inches(6.1, 3.3)

f = lambda t: exp_heat(t, tau=tau, T0=T0) - exp_cool(t, tau=tau, T0=T0, t_cool_start=th)
cross_time = fsolve(f, x0=1)[0]
cross_temp = exp_heat(cross_time, tau=tau, T0=T0, t_heat_start=0)

plt.plot(time[time < th], exp_heat(time[time < th], T0 = T0, tau = tau), color = colors["heat"])
plt.plot(time[time > th], exp_heat(time[time > th], T0 = T0, tau = tau), '--',
         color = colors["heat"])

plt.plot(time[(time < th) & (time > th/2)], exp_cool(time[(time < th) & (time > th/2)],
            T0 = T0, tau = tau, t_cool_start = th, t_heat_start = 0),'--',
         color = colors["cool"])
plt.plot(time[time > th], exp_cool(time[time > th], T0 = T0, tau = tau, t_cool_start = th,\
                                   t_heat_start = 0),color = colors["cool"])

#draw derivatives
lvl = 0.8
plusminus_cool = 25
plusminus_heat = 28
touching_temp = cross_temp * lvl
touching_time = time[np.nonzero(
    np.abs(exp_heat(time, tau=tau, T0=T0, t_heat_start=0) - touching_temp) < 0.01)][-1]
touching_time_heat = touching_time
plt.plot(time[(time < touching_time + plusminus_heat)\
              & (time > touching_time - plusminus_heat)],\
         straight_heat(time[(time < touching_time + plusminus_heat) &\
                            (time > touching_time - plusminus_heat)],\
                       touching_time, tau=tau, T0=T0, 
                        t_heat_start=0), color='black')

touching_time = time[np.nonzero(
    np.abs(exp_cool(time, tau=tau, T0=T0, t_heat_start=0, t_cool_start=th) -\
           touching_temp) < 0.01)][-1]

touching_time_cool = touching_time

plt.plot((touching_time_heat, touching_time_cool), 
           (touching_temp, touching_temp), '--', color='gray')

plt.plot(time[(time < touching_time + plusminus_cool)\
              & (time > touching_time - plusminus_cool)],\
         straight_cool(time[(time < touching_time + plusminus_cool)\
                            & (time > touching_time - plusminus_cool)],\
                       touching_time, tau=tau, T0=T0, 
                        t_heat_start=0, t_cool_start=th), color='black')


#arrow annotation
plt.annotate('', xy=(touching_time_heat, touching_temp), 
             xytext=(touching_time_cool, touching_temp), 
             arrowprops={'arrowstyle' : '<|-|>', 
                         'connectionstyle' : 'arc3,rad=-0.65',
                         'facecolor' : 'black'})
plt.text(65, 0.45, 'Градиентный', bbox={'boxstyle' : 'round4', 
                                      'facecolor' : 'white',
                                      'edgecolor' : 'none',
                                      'pad' : 0.2},
         size = "medium") 

plt.text(47, 0.83, r'$\left(\frac{dT}{dt}\right)_{_{h}}$', size='large', 
         rotation=38)
plt.text(119, 0.715, r'$\left(\frac{dT}{dt}\right)_{_{c}}$', size='large',
         rotation=-40)
    
    
#plt.plot(time, 0.5 + 0.0048 * (time - touching_time))
# deriv_heat = np.gradient(exp_heat(time[time < th], T0 = T0, tau = tau))\
    # [(exp_heat(time[time < th], T0 = T0, tau = tau) > 0.4)]

# plt.axvline(th/2, linestyle='--', markersize=0, zorder=-1000,
#                 linewidth=1, arrow_head=True)





#T ext
myArrow = FancyArrowPatch(posA=(th/2, 0), 
                          posB=(th/2, exp_cool(th/2, tau=tau, T0=T0, t_cool_start=th)), 
                          arrowstyle='<|-|>',
                          mutation_scale=20, shrinkA=0, shrinkB=0, color=colors["cool"])

ax.add_artist(myArrow)
plt.annotate('$T(t_0/2)$', (th / 2 * 0.24,  T0 / 2.2), color=colors["cool"],
             size = 'medium')

#Exponential and pulsed
plt.annotate('Экспоненциальный', ((th + tc) * 0.504,  T0 * 0.65), size = 'medium',
            color = colors["heat"])

plt.annotate('Импульсный', (th / 1.65, T0 * 0.945), size = 'medium',
            color = colors["cool"])

#t0
plt.plot([th] * 2,  (cross_temp, 0), '--', color='gray')
plt.annotate('$t_0$', xy=(th * 1.02, 0.07), size='medium')
plt.annotate(r'$t_0 / 2$', xy=(th / 2 * 1.08, 0.07), size='medium',
             color=colors["cool"])

plt.xlabel('t, с')
plt.ylabel('$\Delta$T, \u2103')

plt.xlim(0, th+tc)
plt.ylim(0, exp_cool(th/2, tau=tau, T0=T0, t_cool_start=th))
# plt.tight_layout()
plt.subplots_adjust(left = 0.14, bottom=0.17, top = 0.99)
# plt.savefig(r'../../disser/Dissertation/images/review/illustrative_example.pdf')
# fig.savefig(r'../../disser/Dissertation/images/imfwm/dfg_eff_plot.pdf')