# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 16:55:56 2025

2. 	Дан кварцевый аксиально-симметричный световод со следующими параметрами:
ступенчатый профиль показателя преломления, диаметр жилы 8.4 мкм,
Delta n = 5.5*{10}^{-3}. Найти такую длину волны, на которой будет
существовать мода LP22. Построить 2-D распределение поля и интенсивности всех
мод более низкого порядка, чем LP22. В каком порядке по мере уменьшения длины
волны появляются эти поперечные моды?

@author: Nick
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import scipy.special as bes

def plot_mode_2d(r, radial_profile, phi_profile_func, l, extent_um=10e-6, N=500):
    """
    Построение 2D картинки моды.
    
    Параметры:
    r — радиальная сетка (1D)
    radial_profile — радиальный профиль поля (1D)
    phi_profile_func — функция угловой части, принимает phi и возвращает поле
    m — азимутальный индекс (для заголовка)
    extent_um — размер области отображения в мкм (по умолчанию ±10 мкм)
    N — разрешение сетки
    """
    # Декартова сетка
    x = np.linspace(-extent_um, extent_um, N)
    y = np.linspace(-extent_um, extent_um, N)
    X, Y = np.meshgrid(x, y)
    
    # Полярные координаты
    R = np.sqrt(X**2 + Y**2)
    Phi = np.arctan2(Y, X)
    
    # Угловая часть
    angular = phi_profile_func(Phi, l)
    
    # Радиальная часть (интерполяция)
    radial_2d = np.interp(R.flatten(), r, radial_profile, left=0, right=0)
    radial_2d = radial_2d.reshape(R.shape)
    
    # Полное поле
    field = radial_2d * angular
    
    return X, Y, field


def angle_part(phi, m=0):
    return np.cos(m * phi)

def uw(r_core, n_core, n_clad, beta, k):
    u = r_core * np.sqrt(n_core ** 2 * k ** 2 - beta ** 2)
    w = r_core * np.sqrt(beta ** 2 - n_clad ** 2 * k ** 2)
    return u, w


def characteristic_function(r_core, n_core, n_clad, beta, k, L=0):
    u, w = uw(r_core, n_core, n_clad, beta, k)
    return bes.jv(L, u) * (- w) * bes.kvp(L, w) - (- bes.kv(L, w)) \
        * u * bes.jvp(L, u)


def calc_mode(r, r_core, n_core, n_clad, k, L=0, brac=0):
    if brac == 0:
        brac = (ncore-1e-9, nclad+1e-9)
    neff = sc.optimize.root_scalar(
        lambda neff: characteristic_function(rcore, ncore, nclad, neff * k, k,
                                             L), bracket=brac).root
    beta = neff * k
    u, w = uw(rcore, ncore, nclad, beta, k)
    C = bes.jv(L, u) / bes.kv(L, w)
    R = np.zeros(len(r))
    R[r < rcore] = bes.jv(L, u * r[r < rcore] / rcore)
    R[r > rcore] = C * bes.kv(L, w * r[r > rcore] / rcore)
    return neff, R


def search_neffs(r, rcore, ncore, nclad, k, L=0):
    ns = np.linspace(nclad+1e-9, ncore-1e-9)
    dn = ns[1] - ns[0]
    char_v = characteristic_function(rcore, ncore, nclad, ns*k, k, L)
    hehe = char_v > 0
    hehe1 = hehe ^ np.roll(hehe, 1)
    hehe1[0] = False
    return ns[hehe1], dn


def search_modes(r, rcore, ncore, nclad, k, L=0):
    ns, dn = search_neffs(r, rcore, ncore, nclad, k, L)
    neffs = []
    Rs = []
    for n in ns:
        neff, R = calc_mode(r, rcore, ncore, nclad, k, L, (n-dn, n+dn))
        neffs += [neff]
        Rs += [R]
    return neffs, Rs


# %% initial parameters

nclad = 1.45
dn = 5.5e-3
ncore = nclad + dn
rcore = 4.2e-6
wavelength = 1.03e-6
k = 2*np.pi/wavelength
r = np.linspace(0, rcore * 10, 1000)

# %% search for LP22 mode

wavelengths = np.linspace(470e-9, 480e-9, 10000)
for wavelength in wavelengths[::-1]:
    k = 2*np.pi/wavelength
    ns, dn = search_neffs(r, rcore, ncore, nclad, k, L=2)
    if np.size(ns) == 2:
        break
print(wavelength*1e9)

# %% plot of the every mode at found wavelength

k = 2*np.pi/wavelength
L = 0
phi = np.linspace(0, 2*np.pi, 1000)
neffs, Rs = search_modes(r, rcore, ncore, nclad, k, L)

while np.size(neffs) > 0:
    for m, R in enumerate(Rs):
        if (L == 1) and (m == 0):
            X, Y, field = plot_mode_2d(
                r=r,
                radial_profile=R,
                phi_profile_func=angle_part,
                l=L,
                extent_um=7e-6,  # размер в мкм, подберите под свой масштаб
                N=500
            )
            plt.figure()
            plt.imshow(field**2, cmap = 'gray')
            # plt.title(f'l={L}, m={m}')
            plt.axis('off')  
            plt.tight_layout()
            plt.savefig(r'..//Dissertation/images/fibershg/calc_lp12.pdf',
                        bbox_inches='tight', pad_inches=0)
        # plt.plot(r, R, label = f'm = {m}')

        # plt.legend()
    L += 1
    neffs, Rs = search_modes(r, rcore, ncore, nclad, k, L)


# %% plot of the every mode at found wavelength

k = 2*np.pi/wavelength
L = 0
neffs, Rs = search_modes(r, rcore, ncore, nclad, k, L)
while np.size(neffs) > 0:
    fig, ax = plt.subplots()
    for m, R in enumerate(Rs):        
        plt.plot(r, R, label = f'm = {m}')
        plt.title(f'l={L}')
        plt.legend()
    L += 1
    neffs, Rs = search_modes(r, rcore, ncore, nclad, k, L)

# %% search of mode to wavelength dependence
wavelengths = np.linspace(343e-9, 1550e-9, 1000)
mode = []
mode_w = []
prev = 0

for L in range(5):
    for wavelength in wavelengths[::-1]:
        k = 2*np.pi/wavelength
        ns, dn = search_neffs(r, rcore, ncore, nclad, k, L)
        if np.size(ns) > prev:
            prev += 1
            mode += [f'LP {L}{prev}']
            mode_w += [wavelength*1e9]
    prev = 0
# %%

hehe = np.argsort(mode_w)
mode = np.array(mode)
mode_w = np.array(mode_w)

for i in range(len(mode_w)):
    print(mode[hehe][i] + f' {mode_w[hehe][i]:.5}')

# %%
"""
Направления для улучшения:
Я опять слишком ленивый для того чтобы рисовать красивые 2д графики, и то что
это буквально требование задания мне всё равно;

Поиск длины волны можно сделать и пооптимальней, енто так то пиздец;
"""
