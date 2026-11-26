import numpy as np
import matplotlib.pyplot as plt

# --- Параметры ---
t0 = 5           # Длительность импульса мощности
t_start = -1   # Отрицательное время (чтобы был виден ноль до импульса)
t_end = 10         # Конец временной оси
Gamma = 1.0        # Коэффициент теплоотдачи
Q_bar = 1        # Плотность теплового потока
P0 = 1.0           # Уровень мощности

# Массив времени
t = np.linspace(t_start, t_end, 500)

# --- 1. Мощность P(t) ---
P = np.zeros_like(t)
# Прямоугольный импульс от 0 до t0
P[(t >= 0) & (t <= t0)] = P0

# --- 2. Температура T(t) ---
T = np.zeros_like(t)
mask1 = (t >= 0) & (t <= t0)
mask2 = t > t0

# Формула из скрина (для t >= 0)
T[mask1] = (Q_bar / Gamma) * (1 - np.exp(-Gamma * t[mask1]))
T[mask2] = (Q_bar / Gamma) * np.exp(-Gamma * t[mask2]) * (np.exp(Gamma * t0) - 1)
# Для t < 0 температура равна нулю (начальные условия)

# --- 3. Построение графика ---
fig, ax = plt.subplots(figsize=(6, 3)) 

# Рисуем красную кривую температуры (толстую)
ax.plot(t, T, color='#ff0000', linewidth=4)

# Рисуем синюю линию мощности (толстую)
ax.plot(t, P, color='#0000ff', linewidth=4)

# --- Настройка осей ---
# Убираем рамки
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)

# Настраиваем оси
for spine in ['bottom']:
    ax.spines[spine].set_linewidth(2)
    ax.spines[spine].set_color('black')

# Деления на оси X: только 0 и t0
ax.set_xticks([0, t0])
ax.set_xticklabels(['0', '$t_0$'], fontsize=28)

# Деления на оси Y: 0 и P0 (подписываем P)
# ax.set_yticks([0, P0])
# ax.set_yticklabels(['0', 'P'], fontsize=28)

ax.set_yticks([])
ax.set_yticklabels([])

# Настраиваем параметры тиков (размер шрифта и длина)
ax.tick_params(axis='both', direction='out', length=8, width=2, labelsize=28)

# Добавляем стрелочку на конце оси X
ax.annotate('', xy=(t_end + 0.2, 0), xytext=(t_end - 0.6, 0),
            arrowprops=dict(
                arrowstyle='fancy,head_length=0.8,head_width=0.8,tail_width=0.1', # Налаштовуємо пропорції
                lw=0,               # Обов'язково 0, щоб прибрати небажану обводку!
                color='black',
                mutation_scale=25   # Загальний масштаб стрілки
            ))
ax.text(t_end + 0.6, -0.05, 't', fontsize=32)

# --- 4. Подписи ---
ax.text(t0 * 1.2, max(T) * 0.8, 'T', fontsize=32, color='#ff0000',
        ha='center', va='center')

ax.text(t0 * 0.15, max(T) * 0.8, 'P', fontsize=32, color='#0000ff',
        ha='center', va='center')

ax.set_ylim([0, P0*1.03])
ax.set_xlim([-0.4, t_end+0.3])


# Убираем лишние отступы
plt.tight_layout()

# Показываем график
# plt.show()

plt.savefig('../Presentation/images/T_P_lc.pdf', transparent=True, bbox_inches='tight', pad_inches=0.05)
