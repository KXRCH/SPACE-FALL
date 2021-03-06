import os
import pygame
import random
from pygame.locals import *
from pygame.sprite import Sprite
import datetime

pygame.init()
pygame.mixer.init()

'''Основыне переменные'''
shootTiming = 0
score = 0
best_score = 0
FPS = 120
anim = 0
FPS_MODE = False
Money = 0
sound = '1'
'''Переменная ХП'''
strength = 0

invulnerability = 0
shipN = 0

'''Изначальное положение фона'''
bg_y = -800
bg_y1 = -1600
ch_y = 5
ch_y1 = 0
'''Размер экрана'''

WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Fall')

"""Переменные отвечающие за выбранный экран"""
Hard = True
Options = False
Guide = False
Wait_screen = True
Prepair = False
Game = False
LOSE = False

'''Загрузка звуков'''
sound1 = pygame.mixer.Sound('assets/sounds/sfx_wpn_laser6.wav')
sound1.set_volume(0.4)
sound2 = pygame.mixer.Sound('assets/sounds/music1.ogg')
pygame.mixer.music.load('assets/sounds/bg.mp3')
sound2.set_volume(0.1)
lose_sound = pygame.mixer.Sound('assets/sounds/sfx_sounds_negative1.wav')
lose_sound.set_volume(0.2)
dam_sound = pygame.mixer.Sound('assets/sounds/sfx_sounds_damage3.wav')
dam_sound.set_volume(0.6)

'''Загрузка текстур кораблей, мобов, кнопок, фонов'''
exp = [pygame.transform.scale(pygame.image.load(f'assets/\
PNG/expl ({i}).png'), (90, 90))
       for i in range(1, 72)]

ast = [pygame.transform.scale(pygame.image.load(f'assets/\
Asteroids/Mini/{i}.png').convert_alpha(), (85, 85))
       for i in range(1, 13)]

ast2 = [pygame.transform.scale(pygame.image.load(f'assets/\
Asteroids/Mega/asteroidR{i}.png').convert_alpha(), (65, 65))
        for i in range(1, 14)]

shots1 = [pygame.transform.scale(pygame.image.load(f'assets/\
shots/shot_1_{i}.png').convert_alpha(), (35, 35)) for i in range(1, 4)]

shots2 = [pygame.transform.scale(pygame.image.load(f'assets/\
shots/shot_2_{i}.png').convert_alpha(), (35, 35)) for i in range(1, 4)]

shots = [pygame.transform.scale(pygame.image.load(f'assets/\
shots/shot{i}.png').convert_alpha(), (35, 35))
         for i in range(1, 4)]

ships = [pygame.transform.scale(pygame.image.load(f'assets/\
ships/ship ({i}).png'), (95, 95)).convert_alpha()
         for i in range(1, 16)]

ships1 = [pygame.transform.scale(pygame.image.load(f'assets/\
ships/ship ({i}).png'), (150, 150)).convert_alpha()
          for i in range(1, 16)]

fr = [pygame.image.load(f'assets/keys/{i}.gif') for i in range(0, 23)]

keys = pygame.image.load(f'assets/keys/key.png')

lvl1_bg = pygame.image.load(f'assets/Main/game21.jpg')

wait_bg = pygame.image.load(f'assets/Main/bg.png')
wait_text1 = pygame.image.load(f'assets/Main/text1.png')
wait_name1 = pygame.image.load(f'assets/Main/name1.png')

shield = pygame.transform.scale(pygame.image.load(f'assets/ships/shield1.png'),
                                (130, 130))

wait_text1 = pygame.transform.scale(wait_text1, (500, 500))
wait_name1 = pygame.transform.scale(wait_name1, (500, 500))

wait_guide = pygame.image.load(f'assets/Main/guide.png')
wait_guide = pygame.transform.scale(wait_guide, (300, 200))

wait_bg1 = pygame.image.load(f'assets/Main/bg1.png')

wait_back = pygame.image.load(f'assets/Main/back.png')
wait_back = pygame.transform.scale(wait_back, (300, 200))

wait_back1 = pygame.image.load(f'assets/Main/back1.png')
wait_back1 = pygame.transform.scale(wait_back1, (300, 200))

wait_guide1 = pygame.image.load(f'assets/Main/guide1.png')
wait_guide1 = pygame.transform.scale(wait_guide1, (300, 200))

wait_play = pygame.image.load(f'assets/Main/play.png')
wait_play = pygame.transform.scale(wait_play, (300, 200))

wait_play1 = pygame.image.load(f'assets/Main/play1.png')
wait_play1 = pygame.transform.scale(wait_play1, (300, 200))

wait_cont1 = pygame.image.load(f'assets/Main/cont1.png')
wait_cont1 = pygame.transform.scale(wait_cont1, (300, 200))

wait_cont = pygame.image.load(f'assets/Main/cont.png')
wait_cont = pygame.transform.scale(wait_cont, (300, 200))

wait_opt1 = pygame.image.load(f'assets/Main/options1.png')
wait_opt1 = pygame.transform.scale(wait_opt1, (300, 200))

opt_music = pygame.image.load(f'assets/Main/MT.png')

opt_music1 = pygame.image.load(f'assets/Main/MF.png')

arrow1 = pygame.image.load(f'assets/Main/arrow1.png')
arrow2 = pygame.image.load(f'assets/Main/arrow2.png')

wait_opt = pygame.image.load(f'assets/Main/options.png')
wait_opt = pygame.transform.scale(wait_opt, (300, 200))

start_bt = pygame.image.load(f'assets/Main/start.png')
start_bt = pygame.transform.scale(start_bt, (300, 200))
start_bt1 = pygame.image.load(f'assets/Main/start1.png')
start_bt1 = pygame.transform.scale(start_bt1, (300, 200))

lose_scr = pygame.image.load(f'assets/Main/LOSE.png')

"""Загрузка настроек и сохранений из файла"""
if os.path.exists('user.config'):
    with open('user.config', 'r', encoding='utf-8') as f:
        i = f.read()
        i = i.split()
        if i == []:
            with open('user.config', 'w', encoding='utf-8') as f:
                f.write(f'0\n0\nFalse\n1')
                pygame.mixer.music.play(-1)
        else:
            if i[3] == '1':
                sound = '1'
                pygame.mixer.music.play(-1)
            else:
                sound = '0'
            if i[2] == 'True':
                FPS_MODE = True
            else:
                FPS_MODE = False
            best_score = i[0]
            Money = i[1]
else:
    with open('user.config', 'w', encoding='utf-8') as f:
        f.write(f'0\n0\nFalse\n1')
        pygame.mixer.music.play(-1)

'''Класс астеройдов'''


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if random.randint(0, 1) == 1:
            self.image_original = ast[random.randint(0, 11)]
            self.image = self.image_original.copy()
            self.speedy = random.randrange(2, 3)
            self.radius = 22
        else:
            self.image_original = ast2[random.randint(0, 12)]
            self.image = self.image_original.copy()
            self.speedy = random.randrange(1, 2)
            self.radius = 28
        self.rect = self.image.get_rect()
        self.radius = 22
        self.rect.x = random.randint(0, WIDTH - 70)
        self.rect.y = random.randrange(-200, -40)
        self.speedx = random.randrange(-1, 1)
        self.rot = 0
        self.rot_speed = random.randrange(-5, 5)
        self.last_update = pygame.time.get_ticks()

    # Анимация вращения астеройдов

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(
                self.image_original, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.rect.bottom >= -100:
            self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top >= HEIGHT:
            self.kill()


'''Класс выстрелов'''


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if shipN in [4, 11, 12]:
            self.image = shots1[random.randint(0, len(shots1) - 1)]
        elif shipN in [13, 8, 6]:
            self.image = shots2[random.randint(0, len(shots2) - 1)]
        else:
            self.image = shots[random.randint(0, len(shots) - 1)]
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -4

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom <= 0:
            self.kill()


'''Класс игрока'''


class Player(pygame.sprite.Sprite):
    def __init__(self):
        global strength
        pygame.sprite.Sprite.__init__(self)
        self.image = ships[shipN]
        self.rect = self.image.get_rect()
        self.radius = 40
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 0
        '''Задаётся разная скорость движения для всех кораблей'''
        if shipN in [0, 1, 3, 9]:
            self.speed = 3
            strength = 3
        elif shipN in [2, 7, 8, 5, 6]:
            self.speed = 2
            strength = 4
        elif shipN in [4, 10, 11, 12, 13]:
            self.speed = 1
            strength = 5
        elif shipN == 14:
            self.speed = 5
            strength = 9
        self.speedx = 0
        self.speedY = 0

    def update(self):
        self.speedx = 0
        self.speedY = 0
        '''Движение игрока'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -self.speed
        if keys[pygame.K_RIGHT]:
            self.speedx = self.speed
        if keys[pygame.K_UP]:
            self.speedY = -self.speed
        if keys[pygame.K_DOWN]:
            self.speedY = self.speed
        self.rect.x += self.speedx
        self.rect.y += self.speedY
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
        if self.rect.top < HEIGHT // 2:
            self.rect.top = HEIGHT // 2

    def shoot(self):
        """Задаётся стрельба из 2 орудий для определённых кораблей"""
        if shipN in [4, 11, 12, 13, 8, 6, 13]:
            bullet1 = Bullet(self.rect.centerx - 25, self.rect.top)
            bullet2 = Bullet(self.rect.centerx + 25, self.rect.top)
            all_sprites.add(bullet1, bullet2)
            bullets.add(bullet1, bullet2)
        else:
            bullet = Bullet(self.rect.centerx, self.rect.top + 15)
            all_sprites.add(bullet)
            bullets.add(bullet)


def new():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


'''Функция главного экрана'''


def draw_wait_screen():
    screen.blit(wait_name1, (50, -150))
    # Анимация смены цвета кнопки
    if Guide is False and Wait_screen is True and \
            210 <= pygame.mouse.get_pos()[0] <= 400 and \
            530 <= pygame.mouse.get_pos()[1] <= 570:
        screen.blit(wait_opt1, (150, 450))
    else:
        screen.blit(wait_opt, (150, 450))

    # Анимация смены цвета кнопки
    if Guide is False and Wait_screen is True and \
            210 <= pygame.mouse.get_pos()[0] <= 400 and \
            480 <= pygame.mouse.get_pos()[1] <= 520:
        screen.blit(wait_play1, (150, 400))
    else:
        screen.blit(wait_play, (150, 400))

    # Анимация смены цвета кнопки
    if Guide is False and Wait_screen is True and \
            210 <= pygame.mouse.get_pos()[0] <= 400 and \
            580 <= pygame.mouse.get_pos()[1] <= 620:
        screen.blit(wait_guide1, (150, 500))
    else:
        screen.blit(wait_guide, (150, 500))
    if FPS_MODE:
        draw_text(screen, str(int(clock.get_fps())), 15, 10, 0)

    pygame.display.update()


'''Функция проигрыша'''


def LOSE():
    global Money
    screen.blit(lose_scr, (0, 40))
    draw_text(screen, (f'Galactic dollars +{int(score) // 7}'), 35,
              WIDTH / 2, 250)
    lose_sound.play()
    sound2.stop()
    Money = int(Money) + int(score) // 7
    pygame.display.update()


'''Функция экрана с обучением'''


def guide_screen():
    global anim
    if anim + 1 >= FPS:
        anim = 0
    screen.blit(wait_text1, (0, 25))
    screen.blit(pygame.transform.scale(fr[anim // 6].convert_alpha(),
                                       (300, 300)), (150, 350))
    draw_text(screen, ('For shooting use SPACE'), 35, WIDTH / 2, 10)
    if Guide is True and 15 <= pygame.mouse.get_pos()[0] <= 200 and \
            745 <= pygame.mouse.get_pos()[1] <= 785:
        screen.blit(wait_back1, (-50, 665))
    else:
        screen.blit(wait_back, (-50, 665))
    anim += 1
    if FPS_MODE:
        draw_text(screen, str(int(clock.get_fps())), 15, 10, 0)
    pygame.display.update()


'''Функция экрана настроек'''


def options_screen():
    # Анимация смены цвета кнопки
    if Options is True and 15 <= pygame.mouse.get_pos()[0] <= 200 and \
            745 <= pygame.mouse.get_pos()[1] <= 785:
        screen.blit(wait_back1, (-50, 665))
    else:
        screen.blit(wait_back, (-50, 665))

    if FPS_MODE:
        draw_text(screen, str(int(clock.get_fps())), 15, 10, 0)
    # Анимация при включении/выключении музыки
    if sound == '1':
        screen.blit(pygame.transform.scale(opt_music, (600, 150)), (50, 150))
    else:
        screen.blit(pygame.transform.scale(
            opt_music1, (600, 150)), (50, 150))
    pygame.display.update()


'''Функция экрана подготовки'''


def prepair_screen():
    global shipN
    screen.blit(wait_bg1, (0, 0))
    if FPS_MODE:
        draw_text(screen, str(int(clock.get_fps())), 15, 10, 0)
    '''Анимация смены цвета кнопки'''
    if Prepair is True and 15 <= pygame.mouse.get_pos()[0] <= 200 and \
            745 <= pygame.mouse.get_pos()[1] <= 785:
        screen.blit(wait_back1, (-50, 665))
    else:
        screen.blit(wait_back, (-50, 665))

    '''Анимация смены цвета кнопки'''
    if Prepair is True and 395 <= pygame.mouse.get_pos()[0] <= 585 and \
            745 <= pygame.mouse.get_pos()[1] <= 785:
        screen.blit(start_bt1, (335, 665))
    else:
        screen.blit(start_bt, (335, 665))
    draw_text(screen, (f'Money: {Money}'), 25, WIDTH - 100, 10)
    screen.blit(pygame.transform.scale(arrow1, (45, 50)), (380, 393))
    screen.blit(pygame.transform.scale(arrow2, (45, 50)), (170, 400))
    screen.blit(pygame.transform.scale(
        ships1[shipN], (150, 150)), (225, 350))

    '''Требования для открытия корабля'''
    if shipN == 3 and int(Money) < 1500:
        draw_text(screen, (f'Price: 1500 Galactic Dollars'),
                  25, WIDTH / 2, 500)
    elif shipN == 4 and int(Money) < 2250:
        draw_text(screen, (f'Price: 2250 Galactic Dollars'),
                  25, WIDTH / 2, 500)
    elif shipN == 5 and int(Money) < 3150:
        draw_text(screen, (f'Price: 3150 Galactic Dollars'),
                  25, WIDTH / 2, 500)
    elif shipN == 7 and int(Money) < 4261:
        draw_text(screen, (f'Price: 4261 Galactic Dollars'),
                  25, WIDTH / 2, 500)
    elif shipN == 9 and int(Money) < 6456 or shipN == 10 and \
            int(Money) < 6456:
        draw_text(screen, (f'Price: 6456 Galactic Dollars'),
                  25, WIDTH / 2, 500)
    elif shipN == 12 and int(Money) < 7001 or shipN == 13 and \
            int(Money) < 7001:
        draw_text(screen, (f'Price: 7001 Galactic Dollars'),
                  25, WIDTH / 2, 500)
    elif shipN == 14 and int(Money) < 25003:
        draw_text(screen, (f'Price: 25003 Galactic Dollars'),
                  25, WIDTH / 2, 500)
    elif shipN == 8 and int(Money) < 8981:
        draw_text(screen, (f'Price: 8441 Galactic Dollars'),
                  25, WIDTH / 2, 500)
    elif shipN == 11 and int(Money) < 15574:
        draw_text(screen, (f'Price: 15574 Galactic Dollars'),
                  25, WIDTH / 2, 500)
    elif shipN == 6 and int(Money) < 9452:
        draw_text(screen, (f'Price: 9452 Galactic Dollars'),
                  25, WIDTH / 2, 500)

    pygame.display.update()


def game_lvl1():
    global anim
    score_last = 0
    if score == 2500:
        for i in range(random.randint(1, 3)):
            score_last = score
    if anim + 1 >= FPS:
        anim = 0
    if anim == 71:
        anim = 0
    """Спавн мобов"""
    if len(mobs) >= 3:
        pass
    else:
        if score >= 250:
            for i in range(random.randint(3, 12)):
                new()

    all_sprites.update()
    screen.blit(pygame.transform.scale(lvl1_bg, (600, 1600)), (0, bg_y1))
    screen.blit(pygame.transform.scale(lvl1_bg, (600, 1600)), (0, bg_y))
    all_sprites.draw(screen)
    '''отрисовка счёта и жизней'''
    if FPS_MODE:
        draw_text(screen, str(int(clock.get_fps())), 15, 10, 0)
    draw_text(screen, (f'Score: {score}'), 25, WIDTH / 2, 10)
    draw_text(screen, (f'Best score: {best_score}'), 25, WIDTH / 2, 40)
    draw_text(screen, (f'Strength: {strength}'), 25, WIDTH - 100, 10)
    all_sprites.update()
    if invulnerability != 0 and score - invulnerability <= 50:
        screen.blit(shield, (player.rect.centerx - 95 // 2 - 21,
                             player.rect.centery - 95 // 2 - 10))
    pygame.display.flip()


'''Функция отрисовки текста'''


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('assets/Main/aesymatt.ttf', size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


all_sprites = pygame.sprite.Group()
player = Player()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

'''Игровой цикл'''
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and Game is True:
            '''Проверка нажатия на кнопку выход'''
            if event.key == pygame.K_ESCAPE:
                '''Сброс параметров'''
                Game = False
                Wait_screen = True
                score = 0
                mobs = pygame.sprite.Group()
                all_sprites = pygame.sprite.Group()
                sound2.stop()
                if sound == '1':
                    pygame.mixer.music.play(-1)
                shootTiming = 0
                invulnerability = 0

            '''Проверка нажатия на кнопку стрельбы'''
            if event.key == pygame.K_SPACE:
                '''Проверка на возможность стрельбы'''
                if score - shootTiming >= 15:
                    sound1.play()
                    player.shoot()
                    '''В shootTiming записывается кадр последнего выстрела,
                    чтобы сделать задержку между выстрелами'''
                    shootTiming = score

        if event.type == pygame.KEYDOWN and Game is False:
            '''Проверка на нажатие кнопки ЗАНОВО после проигрыша'''
            if event.key == pygame.K_TAB:
                '''Сброс параметров'''
                Game = True
                for i in mobs:
                    i.kill()
                bg_y = -800
                bg_y1 = -1600
                ch_y = 5
                ch_y1 = 0
                score = 0
                shootTiming = 0
                """Проверка включена ли музыка в настройках"""
                if sound == '1':
                    sound2.play(-1)
                player.rect.centerx = WIDTH / 2
                player.rect.bottom = HEIGHT - 10
                if shipN in [0, 1, 3, 9, 14]:
                    player.speed = 3
                    strength = 3
                elif shipN in [2, 7, 8, 5, 6]:
                    player.speed = 2
                    strength = 4
                elif shipN in [4, 10, 11, 12, 13]:
                    player.speed = 1
                    strength = 5

        if event.type == pygame.MOUSEBUTTONDOWN:
            '''Проверка нажатия на кнопку Guide'''
            if Guide is False and Options is False and Wait_screen is True and \
                    Prepair is False and \
                    210 <= pygame.mouse.get_pos()[0] <= 400 and \
                    580 <= pygame.mouse.get_pos()[1] <= 620:
                Guide = True
                Wait_screen = False
                anim = 0

            '''Проверка нажатия на кнопку Back'''
            if Guide is True and 5 <= pygame.mouse.get_pos()[0] <= 195 and \
                    755 <= pygame.mouse.get_pos()[1] <= 795:
                Guide = False
                Wait_screen = True

            '''Проверка нажатия на кнопку Options'''
            if Options is False and Wait_screen is True and Guide is False and \
                    210 <= pygame.mouse.get_pos()[0] <= 400 and \
                    530 <= pygame.mouse.get_pos()[1] <= 570:
                Options = True
                Wait_screen = False

            '''Проверка нажатия на кнопку Back'''
            if Options is True and 15 <= pygame.mouse.get_pos()[0] <= 200 and \
                    745 <= pygame.mouse.get_pos()[1] <= 785:
                Options = False
                Wait_screen = True

            '''Проверка нажатия на кнопку вкл/выкл музыки и
            запись параметра в файл'''
            if Options is True and 115 <= pygame.mouse.get_pos()[0] <= 530 and \
                    210 <= pygame.mouse.get_pos()[1] <= 255:
                if sound == '1':
                    sound = '0'
                else:
                    sound = '1'
                if sound == '1':
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
                with open('assets/st.txt', 'w', encoding='utf-8') as f:
                    f.write(f'{best_score};0;{sound};')

            '''Проверка нажатия на кнопку Play'''
            if Guide is False and Wait_screen is True and Options is False and \
                    210 <= pygame.mouse.get_pos()[0] <= 400 and \
                    480 <= pygame.mouse.get_pos()[1] <= 520:
                screen.fill(pygame.Color("black"))
                Wait_screen = False
                Prepair = True

            '''Проверка нажатия на кнопку Back'''
            if Prepair is True and Guide is False and Options is False and \
                    Wait_screen is False and \
                    15 <= pygame.mouse.get_pos()[0] <= 200 and \
                    745 <= pygame.mouse.get_pos()[1] <= 785:
                Wait_screen = True
                Prepair = False

            '''Проверка нажатия на кнопку Выбора корабля влево'''
            if Prepair is True and Guide is False and Options is False and \
                    Wait_screen is False and \
                    170 <= pygame.mouse.get_pos()[0] <= 210 and \
                    405 <= pygame.mouse.get_pos()[1] <= 440:
                if shipN - 1 >= 0:
                    shipN -= 1
            '''Проверка нажатия на кнопку Выбора корабля вправо'''
            if Prepair is True and Guide is False and \
                    Options is False and Wait_screen is False and \
                    380 <= pygame.mouse.get_pos()[0] <= 425 and \
                    400 <= pygame.mouse.get_pos()[1] <= 435:
                if shipN == 14:
                    pass
                else:
                    screen.fill((0, 0, 0))
                    shipN += 1

            '''Проверка нажатия на кнопку Start'''
            if Prepair is True and Guide is False and \
                    Options is False and Wait_screen is False and \
                    395 <= pygame.mouse.get_pos()[0] <= 585 and \
                    745 <= pygame.mouse.get_pos()[1] <= 785:
                """Проверка на наличие достаточного кол-во очков,
                чтобы использовать корабль"""
                if shipN == 3 and int(Money) >= 1500:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)
                elif shipN == 4 and int(Money) >= 2250:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)
                elif shipN == 5 and int(Money) >= 3150:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)
                elif shipN == 7 and int(Money) >= 4261:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)
                elif shipN == 9 and int(Money) >= 6456 or \
                        shipN == 10 and int(Money) >= 6456:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)
                elif shipN == 12 and int(Money) >= 7001 or shipN == 13 and \
                        int(Money) >= 7001:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)
                elif shipN == 14 and int(Money) >= 25003:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)
                elif shipN == 8 and int(Money) >= 8981:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)
                elif shipN == 11 and int(Money) >= 15574:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)
                elif shipN == 6 and int(Money) >= 9452:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)
                elif shipN == 0 or shipN == 1 or shipN == 2:
                    '''запус игрового экрана'''
                    pygame.mixer.music.stop()
                    Prepair = False
                    Game = True
                    player = Player()
                    if sound == '1':
                        sound2.play(-1)
                    all_sprites.add(player)

    '''Проверка столкновения пули и моба'''
    all_sprites.update()
    if len(mobs) != 0:
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True,
                                          pygame.sprite.collide_circle)
        for hit in hits:
            new()

    '''Проверка столкновения игрока и моба'''
    hits1 = pygame.sprite.spritecollide(player, mobs, True,
                                        pygame.sprite.collide_circle)
    for hit in hits1:
        '''Проверка на кол-во ХП у игрока'''
        if strength >= 1:
            '''Переменная invulnerability нужна, чтобы сделать игрока неязвимым
            после столкновения на некторое время '''
            if invulnerability == 0:
                invulnerability = score
                strength -= 1
                new()
                dam_sound.play()
            else:
                if score - invulnerability >= 75:
                    strength -= 1
                    new()
                    dam_sound.play()
                    invulnerability = score
        else:
            '''Проигрыш'''
            Game = False
            invulnerability = 0
            LOSE()

    all_sprites.update()

    '''Проверка на включенный в данным момент экран'''
    if Wait_screen and Guide is False and Options is False and \
            Prepair is False and Game is False:
        screen.blit(wait_bg, (-1250, 0))
        draw_wait_screen()
    if Guide:
        screen.blit(wait_bg1, (0, 0))
        guide_screen()
    elif Options:
        screen.blit(wait_bg1, (0, 0))
        options_screen()
    elif Prepair:
        prepair_screen()
    elif Game:
        '''Движение заднего фона'''
        if bg_y + 5 >= 0:
            ch_y1 = 5
        if bg_y + 5 >= 800:
            bg_y = -1600
            ch_y = 0
        if bg_y1 + 5 >= 0:
            ch_y = 5
        if bg_y1 + 5 >= 800:
            bg_y1 = -1600
            ch_y1 = 0
        game_lvl1()
        score += 1
        bg_y += ch_y
        bg_y1 += ch_y1
        '''Если счёт достиг лучшего счёта, то мы их приравниваем'''
        if score >= int(best_score):
            best_score = score
    else:
        '''Сброс фона в исходное положение'''
        bg_y = -800
        bg_y1 = -1600
        ch_y = 5
        ch_y1 = 0

    '''Запись лучшего счёта в файл'''
    with open('user.config', 'w', encoding='utf-8') as f:
        f.write(f'{best_score}\n{Money}\n{FPS_MODE}\n{sound}')

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
with open('user.config', 'w', encoding='utf-8') as f:
    f.write(f'{best_score}\n{Money}\n{FPS_MODE}\n{sound}\n\
{datetime.datetime.now()}')
