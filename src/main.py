import random

from volleyballClasses import *

#Всплывающее окно
def draw_popup(message):
    popup_width = 500
    popup_height = 200
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    #Прямоугольник всплывающего окна
    pygame.draw.rect(screen, POPUP_COLOR, (popup_x, popup_y, popup_width, popup_height))

    #Текст внутри всплывающего окна
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height // 2))
    screen.blit(text, text_rect)

# Инициализация Pygame
pygame.init()

font = pygame.font.Font(None, 36)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Volleyball")

clock = pygame.time.Clock()

# Создание персонажей, мяча
p1 = Spiker()
p2 = Setter()
bot1 = BotSpiker()
bot2 = BotSetter()
ball = Ball()

running = True
k = 0
ball_flag = False
flag_two_touch = False
popup_window = False
pause = False
score_updated = False

teams_score = [0, 0]

#Отображение первого персонажа
def draw_player1(player, rec_flag):
    player.draw_head(screen, rec_flag)
    player.draw_legs(screen, rec_flag)
    player.draw_body(screen, rec_flag)
    player.draw_arms(screen, rec_flag)

#Отображение второго персонажа
def draw_player2(player, pas_flag):
    player.draw_head(screen)
    player.draw_legs(screen)
    player.draw_body(screen)
    player.draw_arm(screen, pas_flag)

#Отображение первого бота
def draw_bot1(player, rec_flag):
    player.draw_head(screen, rec_flag)
    player.draw_legs(screen, rec_flag, -1)
    player.draw_body(screen, rec_flag)
    player.draw_arms(screen, rec_flag, -1)

#Отображение второго бота
def draw_bot2(player, pas_flag):
    player.draw_head(screen)
    player.draw_legs(screen)
    player.draw_body(screen)
    player.draw_arm(screen, pas_flag, -1)

#Отображение счета
def draw_score(screene, score_team1, score_team2):

    score_block_x = (WIDTH - SCORE_BLOCK_WIDTH) // 2
    score_block_y = 20

    pygame.draw.rect(screen, TABLO_COLOR, (score_block_x, score_block_y, SCORE_BLOCK_WIDTH, SCORE_BLOCK_WIDTH))

    score_text_team1 = f"{score_team1}"
    score_text_team2 = f"{score_team2}"
    separator = "|"

    score_text_team1_rendered = font.render(score_text_team1, True, BLACK)
    score_text_team2_rendered = font.render(score_text_team2, True, BLACK)
    separator_rendered = font.render(separator, True, BLACK)

    score_text_team1_pos = (score_block_x + 10,
                            score_block_y + SCORE_BLOCK_WIDTH // 2 - score_text_team1_rendered.get_height() // 2)
    separator_pos = (score_block_x + SCORE_BLOCK_WIDTH // 2 - separator_rendered.get_width() // 2,
                     score_block_y + SCORE_BLOCK_WIDTH // 2 - separator_rendered.get_height() // 2)
    score_text_team2_pos = (score_block_x + SCORE_BLOCK_WIDTH - 10 - score_text_team2_rendered.get_width(),
                            score_block_y + SCORE_BLOCK_WIDTH // 2 - score_text_team2_rendered.get_height() // 2)

    screen.blit(score_text_team1_rendered, score_text_team1_pos)
    screen.blit(separator_rendered, separator_pos)
    screen.blit(score_text_team2_rendered, score_text_team2_pos)


#Основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    receiving_flag = False
    hit_flag = False
    pas_flag = False

    # Получение нажатых клавиш
    keys = pygame.key.get_pressed()

    #Управление первым персонажем
    if keys[pygame.K_a]:
        k = -1
        p1.move(k)
    if keys[pygame.K_d]:
        k = 1
        p1.move(k)
    if keys[pygame.K_w] and p1.y >= GLOBAL_Y:
        p1.speed_y = -p1.jump_force
    if keys[pygame.K_s]:
        receiving_flag = True
    if keys[pygame.K_SPACE]:
        hit_flag = True

    #Управление вторым персонажем
    if keys[pygame.K_LEFT]:
        k = -1
        p2.move(k)
    if keys[pygame.K_RIGHT]:
        k = 1
        p2.move(k)
    if keys[pygame.K_UP] and p2.y >= GLOBAL_Y:
        p2.speed_y = -p2.jump_force
    if keys[pygame.K_DOWN]:
        pas_flag = True

    #Начало игры, подача
    if keys[pygame.K_f]:
        ball_flag = True

    #Снятие с паузы после проигранного мяча
    if keys[pygame.K_ESCAPE]:
        pause = False

    screen.fill(WHITE)

    if not pause:
    #Если мяч в игре
        if ball.in_game:
            p1.jump()
            p2.jump()
            bot1.jump()
            if hit_flag:
                p1.hit()

            #Обработка действий ботов и игроков
            bot1.move_to_ball(ball)
            bot2.move_to_ball(ball)

            draw_player1(p1, receiving_flag)
            draw_player2(p2, pas_flag)
            draw_bot1(bot1, bot1.receive)
            draw_bot2(bot2, bot2.pas)

            bot1.receive_ball(ball)
            bot1.jump_bot(ball)
            bot2.pas_ball(ball)


            #Подача
            if ball_flag:
                ball.reload()
                ball.serve = True
                ball.dx, ball.dy = random.randint(-50, 150), random.randint(-35, 15)
                ball_flag = False

            #Прием
            if receiving_flag:
                arm_rect = p1.get_arm_rect()
                ball_rect = pygame.Rect(ball.x - ball.r, ball.y - ball.r, ball.r * 2, ball.r * 2)
                if ball_rect.colliderect(arm_rect):
                    arm_end_x = arm_rect[0]

                    #ball.bounce((ball.x, ball.y), (ball.x + 400, ball.y + 120))
                    ball.bounce((ball.x, ball.y), (500-(arm_end_x-ball.x)*1.2,HEIGHT))
                    ball_flag = False

            #Пас
            if pas_flag:
                arm_rect = p2.get_arm_rect()
                ball_rect = pygame.Rect(ball.x - ball.r, ball.y - ball.r, ball.r * 2, ball.r * 2)
                if ball_rect.colliderect(arm_rect):
                    ball.second_bounce()
                    ball_flag = False

            #Атака
            if hit_flag:
                end_arm = p1.get_end_arm_coordinates()
                ball_rect = pygame.Rect(ball.x - ball.r - 10, ball.y - 20 - ball.r, ball.r * 2 + 20, ball.r * 2 + 30)
                #pygame.draw.rect(screen, BLACK, ball_rect)

                if ball_rect.collidepoint(end_arm):
                    ball.attack()

            ball.draw_ball(screen)
        #Перезапуск
        else:
            ball.reload()
            p1.reload(120, GLOBAL_Y)
            p2.reload(400, GLOBAL_Y)
            bot1.reload(WIDTH-300, GLOBAL_Y)
            bot2.reload(650, GLOBAL_Y)
            bot1.count_jump = 0
            score_updated = False

    #Обработка проигранных мячей
    message, team_id = ball.check()
    if message:
        pause = True
        draw_popup(message)
        if not score_updated:
            teams_score[team_id - 1] += 1
            score_updated = True
        ball.in_game = False
    elif p1.chek_touch_net() or p2.chek_touch_net():
        pause = True
        draw_popup('Вы коснулись сетки')
        if not score_updated:
            teams_score[1] += 1
            score_updated = True
        ball.in_game = False


    #Сетка
    pygame.draw.line(screen, BLACK, (WIDTH // 2, HEIGHT), (WIDTH // 2, HEIGHT / 1.3), 15)
    pygame.draw.line(screen, GRAY, (WIDTH // 2, HEIGHT/1.3), (WIDTH // 2, HEIGHT / 1.8), 10)

    #Поле
    pygame.draw.line(screen, GREEN, (WIDTH*0.1, HEIGHT), (WIDTH * 0.9, HEIGHT), 20)
    pygame.draw.line(screen, AUT, (0, HEIGHT), (WIDTH * 0.1, HEIGHT), 20)
    pygame.draw.line(screen, AUT, (WIDTH * 0.9, HEIGHT), (WIDTH, HEIGHT), 20)

    #Обновление счета
    draw_score(screen, teams_score[0], teams_score[1])
    if teams_score[0] == 15:
        draw_popup('Команда слева победила!')
        teams_score[0] = teams_score[1] = 0
    elif teams_score[1] == 15:
        draw_popup('Команда справа победила!')
        teams_score[0] = teams_score[1] = 0

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()



