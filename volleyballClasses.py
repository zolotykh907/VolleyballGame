import time
import math
import pygame

from mathOperations import calculate_y, height_to_angle
from constants import *

# Класс игрока, от которого наследуются все остальные
class Player:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.speed = 5
        self.body_width = 30
        self.body_height = 60
        self.legs_width = 10
        self.legs_height = 60
        self.arms_width = 8
        self.arms_height = 50
        self.jump_force = 20
        self.gravity = 0.7
        self.speed_y = 0
        self.bottom = self.y
        self.flag_jump = False
        self.flag_hit2 = False
        self.arm_points = []
        self.body_color = None

    #Обновление до начальной позиции
    def reload(self, x_start, y_start):
        self.x = x_start
        self.y = y_start
        self.arm_points.clear()

    #Движение
    def move(self, k):
        self.x += self.speed * k

    #Прыжок
    def jump(self):
        self.flag_jump = True
        self.speed_y += self.gravity
        self.y += self.speed_y
        if self.y > GLOBAL_Y:
            self.y = GLOBAL_Y
            self.speed_y = 0
            self.flag_jump = False
            self.flag_hit2 = False

    #Отображение тела
    def draw_body(self, screen, rec_flag = False):
        points_body = (self.x, self.y, self.body_width, self.body_height)
        if rec_flag:
            points_body = (self.x, self.y + 10, self.body_width, self.body_height)
        pygame.draw.rect(screen, self.body_color, pygame.Rect(points_body))

    #Отображение ног
    def draw_legs(self, screen, rec_flag = False, direction = 1):
        x_left = self.x + 5 - 1
        x_right = self.x + 25 - 1

        y1_legs = self.y + self.body_height
        y2_legs = y1_legs + self.legs_height

        points_left = [(x_left, y1_legs), (x_left, y2_legs)]
        points_right = [(x_right, y1_legs), (x_right, y2_legs)]

        #Если персонаж находится в приеме
        if rec_flag:
            points_left = [(x_left, y1_legs + 10), (x_left + direction*20, y1_legs + 40), (x_left, y2_legs)]
            points_right = [(x_right, y1_legs + 10), (x_right + direction*20, y1_legs + 40), (x_right, y2_legs)]

        pygame.draw.lines(screen, LEGS_COLOR, False, points_left, self.legs_width)
        pygame.draw.lines(screen, LEGS_COLOR, False, points_right, self.legs_width)

    #Отображение головы
    def draw_head(self, screen, rec_flag = False):
        circle_radius = 13
        circle_x, circle_y = self.x + self.body_width / 2 - 1, self.y - circle_radius

        #Если персонаж находится в приеме
        if rec_flag:
            circle_y += 10

        pygame.draw.circle(screen, HEAD_COLOR, (circle_x, circle_y), circle_radius)

    #Проверка на касание сетки
    def chek_touch_net(self):
        if self.x + self.body_width/2 >= WIDTH/2:
            return True
        return None

#Класс нападающего персонажа
class Spiker(Player):
    def __init__(self):
        super().__init__()
        self.flag_hit = 0
        self.body_color = BODY1_COLOR

    #Отображение рук
    def draw_arms(self, screen, rec_flag = False, direction = 1):
        y_right = self.y + 10
        x_right = self.x + self.body_width / 2 - 1

        points_right = [(x_right, y_right), (x_right - 6*direction, y_right + 20), (x_right, y_right + self.arms_height)]

        #Если персонаж находится в приеме
        if rec_flag:
            points_right = [(x_right + 3, y_right + 10), (x_right + direction * (self.arms_height + 3), y_right + 15)]

        #Если персонаж прыгнул, и совершил нападение
        if self.flag_jump and not self.flag_hit2:
            points_right = [(x_right, y_right + 10), (x_right - 15, y_right - self.arms_height - 3)]

        #Если персонаж совершил нападение
        if self.flag_hit:
            points_right = [(x_right, y_right + 10), (x_right + direction*40, y_right - self.arms_height - 3)]
            self.flag_hit2 = True

        self.arm_points = points_right
        pygame.draw.lines(screen, ARMS_COLOR, False, points_right, self.arms_width)
        self.flag_hit = False

    #Нападение
    def hit(self):
        self.flag_hit = True

    #Получение координат рук для обработки касаний с мячом во время приема
    def get_arm_rect(self):
        x = self.arm_points[0][0]
        y = self.arm_points[0][1]
        w = self.arm_points[1][0] - self.arm_points[0][0]
        h = self.arms_width

        arm_rect = pygame.Rect(x, y, w, h)
        return arm_rect

    #Получение координат конечной точки руки во время нападения для обработки удара
    def get_end_arm_coordinates(self):
        x = self.arm_points[1][0]
        y = self.arm_points[1][1]

        return x, y

#Класс связующего
class Setter(Player):
    def __init__(self):
        super().__init__()
        self.jump_force = 15
        self.body_color = BODY1_COLOR

    #Отображение рук
    def draw_arm(self, screen, pas_flag, direction = 1):
        y_right = self.y + 10
        x_right = self.x + self.body_width / 2 - 1

        points_right = [(x_right, y_right), (x_right - direction*6, y_right + 20), (x_right, y_right + self.arms_height)]

        #Если персонаж пасует
        if pas_flag:
            points_right = [(x_right, y_right), (x_right, y_right - self.arms_height)]

        self.arm_points = points_right
        pygame.draw.lines(screen, ARMS_COLOR, False, points_right, self.arms_width)

    #Получение коориднат рук для обработки касания с мячом во время паса
    def get_arm_rect(self):
        x = self.arm_points[0][0] - self.arms_width/2 + 1
        y = self.arm_points[0][1] - self.arms_height
        w = self.arms_width
        h = 10

        arm_rect = pygame.Rect(x, y, w, h)
        return arm_rect

#Первый бот, нападающий
class BotSpiker(Spiker):
    def __init__(self):
        super().__init__()
        self.receive = False
        self.high_ball = False
        self.count_jump = 0
        self.body_color = BODY2_COLOR

    #Движение бота к мячу
    def move_to_ball(self, ball):
        if ball.x > WIDTH/2 and ball.count_touches == 0 and not ball.serve:
            if ball.y < HEIGHT/1.2 and ball.final_touch == 1:
                if not ball.serve:
                    self.receive = True
                d = self.x - ball.x
                if  d > 0 and d > 5:
                    self.move(-2)
                elif d < 0 and abs(d) > 5:
                    self.move(4)

    #Прием
    def receive_ball(self, ball):
        if self.receive:
            arm_rect = self.get_arm_rect()
            ball_rect = pygame.Rect(ball.x - ball.r, ball.y - ball.r, ball.r * 2, ball.r * 2)

            if ball_rect.colliderect(arm_rect) and ball.count_touches == 0:
                arm_end_x = arm_rect[0]
                ball.count_touches += 1
                ball.bounce((ball.x, ball.y), (700 - (abs(arm_end_x - ball.x)) * 1.2, HEIGHT))
        if ball.count_touches >= 1:
            self.receive = False

    #Прыжок
    def jump_bot(self, ball):
        if ball.count_touches == 2 and ball.final_touch == 1:
            if self.x - ball.x > 10:
                self.move(-2)
            if ball.y <= 100:
                self.high_ball = True
            if self.y >= GLOBAL_Y and ball.y > 115 and self.count_jump < 1 and self.high_ball:
                self.high_ball = False
                self.speed_y = -self.jump_force
                self.count_jump += 1

            end_arm = self.get_end_arm_coordinates()
            ball_rect = pygame.Rect(ball.x - ball.r - 10, ball.y - 20 - ball.r, ball.r * 2 + 20, ball.r * 2 + 20)

        #pygame.draw.rect(screen, BLACK, ball_rect)

            if ball_rect.collidepoint(end_arm):
                self.hit()
                ball.attack(direction=-1)

#Второй бот, связующий
class BotSetter(Setter):
    def __init__(self):
        super().__init__()
        self.body_color = BODY2_COLOR
        self.pas = False

    #Движение бота к мячу
    def move_to_ball(self, ball):
        if ball.x > WIDTH/2 and ball.count_touches == 1:
            if ball.y < HEIGHT/1.2 and ball.final_touch == 1:
                self.pas = True
                d = self.x - ball.x
                if ball.y > 100:
                    if d > 0 and d > 5:
                        self.move(-2)
                    elif d < 0 and abs(d) > 5:
                        self.move(2)
        if ball.count_touches == 2:
            self.pas = False

    #Пас
    def pas_ball(self, ball):
        if self.pas:
            arm_rect = self.get_arm_rect()
            ball_rect = pygame.Rect(ball.x - ball.r, ball.y - ball.r, ball.r * 2, ball.r * 2)

            if ball_rect.colliderect(arm_rect):
                ball.second_bounce()

#Класс мяча
class Ball:
    def __init__(self):
        self.in_game = False
        self.x = WIDTH - 50
        self.y = HEIGHT - 200
        self.r = 13
        self.speed_x = 2
        self.speed_y = 0
        self.speed_attack = 10
        self.gravity = 0.07
        self.first_bouncing = False
        self.bounce_start = None
        self.bounce_end = None
        self.count_touches = 0
        self.second_bouncing = False
        self.hitting = False
        self.angle = 0
        self.serve = False
        self.dx, self.dy = 0, 0
        self.final_touch = None

        self.last_bounce_time = 0

    #Обновление до начального состояния
    def reload(self):
        self.x = WIDTH - 50
        self.y = HEIGHT - 200
        self.in_game = True
        self.speed_y = 0
        self.count_touches = 0
        self.angle = 0
        self.hitting = False
        self.first_bouncing = False
        self.second_bouncing = False
        self.serve = False
        self.final_touch = None

    #Проверка на различные условия выхода из игры и обработку кол-ва касаний
    def check(self):
        if self.x < WIDTH / 2 and self.count_touches == 3:
            self.count_touches = 0
            self.final_touch = 1
        if self.x > WIDTH / 2 and self.count_touches == 3:
            self.count_touches = 0
            self.final_touch = 2

        if self.y > HEIGHT - self.r and self.x > WIDTH/2 and self.x <= WIDTH*0.9:
            self.in_game = False
            return "Вы забили", 1
        elif self.y > HEIGHT - self.r and self.x > WIDTH/2 and self.x > WIDTH*0.9 + self.r:
            self.in_game = False
            return "Вы попали в аут", 2
        elif (self.y > (NET_HEIGHT + self.r - 1)) and (self.x < WIDTH/2) and self.final_touch == 1:
            self.in_game = False
            return 'У вас сетка', 2
        elif self.count_touches > 3:
            self.in_game = False
            return 'У вас больше трех касаний', 2
        elif (self.y > HEIGHT - self.r) and (self.x < WIDTH * 0.1 + self.r):
            self.in_game = False
            return 'Соперник попал в аут', 1
        elif self.x <= WIDTH/2 and self.y > HEIGHT - self.r:
            self.in_game = False
            return 'Мяч упал на вашей стороне', 2
        else:
            return None, None

    #Отображения мяча, с учетом того, кто коснулся последний и какое действие совершил
    def draw_ball(self, screen):
        if self.in_game:
            if self.first_bouncing and self.final_touch == 1:
                self.x, self.y = calculate_y(self.bounce_start, self.bounce_end, [self.x, self.y],
                                             self.speed_x-1.5, coeff=-1)
                self.serve = False
            elif self.first_bouncing:
                self.x, self.y = calculate_y(self.bounce_start, self.bounce_end, [self.x, self.y], self.speed_x)
                self.serve = False
            elif self.second_bouncing:
                self.y += self.speed_y
                self.speed_y += self.gravity
                if self.hitting:
                    self.second_bouncing = False
            elif self.hitting:
                self.update_position()
            elif self.serve:
                self.x, self.y = calculate_y((WIDTH-50, HEIGHT - 200), (100, HEIGHT), [self.x, self.y],
                                             self.speed_x + 5, self.dx, self.dy, -1, 200)

            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.r)

    #Обновление позиции во время нападающего удара
    def update_position(self):
        self.x += self.speed_attack * math.cos(math.radians(self.angle))
        self.y -= self.speed_attack * math.sin(math.radians(self.angle))

    #Отскок мяча во время приемя
    def bounce(self, start, end):
        self.first_bouncing = True
        self.bounce_start = start
        self.bounce_end = end
        self.check_delay()

    #Отскок мяча во время паса
    def second_bounce(self):
        self.hitting = False
        self.first_bouncing = False
        self.second_bouncing = True
        if self.y <= NET_HEIGHT:
            self.speed_y = -3
        else:
            self.speed_y = -7
        self.check_delay()

    #Отскок мяча во время атаки, чем выше съем - тем острее угол
    def attack(self, direction = 1):
        self.hitting = True
        h = HEIGHT - self.y
        self.angle = height_to_angle(h)
        if direction == -1:
            self.angle = height_to_angle(h) - 90
        self.check_delay()

    #Обработка касаний, чтобы несколько быстрых касаний засчитывались как одно
    def check_delay(self):
        current_time = time.time()
        if current_time - self.last_bounce_time > 1:
            self.last_bounce_time = current_time
            self.count_touches += 1