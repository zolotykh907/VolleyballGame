import numpy as np
import math

#Получение значения угла отскока мяча во время удара в зависимости от высоты съема
def height_to_angle(height):
    height_max = 400
    angle_max = -50

    k = 0.002

    angle = angle_max * math.exp(-k * (height_max - height))

    return angle

#Определение траектории полета мяча по параболе во время приема и подачи
def calculate_y(start, end, ball_pos, ball_speed, dx=0, dy=0, coeff=1, peak_height = 400):
    # Определение вершины параболы
    x0, y0 = start
    x1, y1 = end
    xv = (x0 + x1) / 2

    if coeff == -1:
        peak_height += dy
        x1 += dx

    yv = min(y0, y1) - peak_height

    #Решаем уравнения для получения нужных коэффициентов
    A = np.array([
        [x0 ** 2, x0, 1],
        [x1 ** 2, x1, 1],
        [xv ** 2, xv, 1]
    ])
    B = np.array([y0, y1, yv])

    a, b, c = np.linalg.solve(A, B)

    def get_y(x):
        return a * x ** 2 + b * x + c

    # Обновление позиции мяча
    if coeff == 1:
        ball_pos[0] += ball_speed
        if ball_pos[0] >= x1:
            ball_pos[0] = x1
        ball_pos[1] = get_y(ball_pos[0])
    else:
        ball_pos[0] += ball_speed*coeff
        if ball_pos[0] < x1:
            ball_pos[0] = x1
        ball_pos[1] = get_y(ball_pos[0])

    return ball_pos