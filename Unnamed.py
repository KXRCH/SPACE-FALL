import os
import pygame
import random
from pygame.locals import *
from pygame.sprite import Sprite


pygame.init()
pygame.mixer.init()

shootTiming = 0
score = 0
n = -800
n1 = -1600
FPS = 60
bg_y = -800
bg_y1 = -1600
ch_y = 5
ch_y1 = 0
WIDTH = 600
HEIGHT = 800
x, y = 248, 690
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
anim = 0
pygame.display.set_caption('Space Fall')
Hard = True
Options = False
Guide = False
wait_screen = True
Prepair = False
game = False
RIGHT = False
DOWN = False
UP = False
LEFT = False
seconds = 0
shipN = 0
x1 = 0
y1 = 0
sound1 = pygame.mixer.Sound('assets/sounds/Pew__005.ogg')
sound2 = pygame.mixer.Sound('assets/sounds/music1.ogg')
sound2.set_volume(0.3)
ast = [pygame.transform.scale(pygame.image.load(f'assets/Asteroids/Mini/{i}.png').convert_alpha(), (85, 85))\
       for i in range(1, 13)]
shots = [pygame.transform.scale(pygame.image.load(f'assets/shots/shot{i}.png').convert_alpha(), (35, 35))\
         for i in range(1, 4)]
lvl1_bg = pygame.image.load(f'assets/game21.jpg')
wait_bg = pygame.image.load(f'assets/bg.png')
fr = [pygame.image.load(f'assets/keys/{i}.gif') for i in range(0, 23)]
ships = [ pygame.transform.scale(pygame.image.load(f'assets/ships/ship ({i}).png'), (95, 95)).convert_alpha() for i in range(1, 16)]
wait_text1 = pygame.image.load(f'assets/text1.png')
wait_name1 = pygame.image.load(f'assets/name1.png')
wait_text1 = pygame.transform.scale(wait_text1, (500, 500))
wait_name1 = pygame.transform.scale(wait_name1, (500, 500))

wait_guide = pygame.image.load(f'assets/guide.png')
wait_guide = pygame.transform.scale(wait_guide, (300, 200))

wait_bg1 = pygame.image.load(f'assets/bg1.png')

wait_back = pygame.image.load(f'assets/back.png')
wait_back = pygame.transform.scale(wait_back, (300, 200))

wait_back1 = pygame.image.load(f'assets/back1.png')
wait_back1 = pygame.transform.scale(wait_back1, (300, 200))

wait_guide1 = pygame.image.load(f'assets/guide1.png')
wait_guide1 = pygame.transform.scale(wait_guide1, (300, 200))

wait_play = pygame.image.load(f'assets/play.png')
wait_play = pygame.transform.scale(wait_play, (300, 200))

wait_play1 = pygame.image.load(f'assets/play1.png')
wait_play1 = pygame.transform.scale(wait_play1, (300, 200))

wait_cont1 = pygame.image.load(f'assets/cont1.png')
wait_cont1 = pygame.transform.scale(wait_cont1, (300, 200))

wait_cont = pygame.image.load(f'assets/cont.png')
wait_cont = pygame.transform.scale(wait_cont, (300, 200))

wait_opt1 = pygame.image.load(f'assets/options1.png')
wait_opt1 = pygame.transform.scale(wait_opt1, (300, 200))

opt_music = pygame.image.load(f'assets/MT.png')

opt_music1 = pygame.image.load(f'assets/MF.png')

arrow1 = pygame.image.load(f'assets/arrow1.png')
arrow2 = pygame.image.load(f'assets/arrow2.png')

wait_opt = pygame.image.load(f'assets/options.png')
wait_opt = pygame.transform.scale(wait_opt, (300, 200))
pygame.mixer.music.load('assets/sounds/bg.mp3')


with open('assets/st.txt', 'r', encoding='utf-8') as f:
    i = f.read()
    i = i.split(';')
    if i[0] == '0':
        Hard = False
    else:
        Hard = True
    if i[2] == '1':
        sound = '1'

        pygame.mixer.music.play(-1)
    else:
        sound = '0'


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ast[random.randint(0, 11)]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-200, -40)
            self.speedy = random.randrange(3, 5)
        if self.rect.top >= HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = shots[random.randint(0, len(shots) - 1)]
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -8

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom <= 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ships[shipN]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedY = 0

    def update(self):
        self.speedx = 0
        self.speedY = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -5
        if keys[pygame.K_RIGHT]:
            self.speedx = 5
        if keys[pygame.K_UP]:
            self.speedY = -5
        if keys[pygame.K_DOWN]:
            self.speedY = 5
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
        sound1.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

def draw_wait_screen():
    screen.blit(wait_name1, (50, -150))
    if Hard == False:
        if Guide == False and wait_screen == True and \
                210 <= pygame.mouse.get_pos()[0] <= 400 and 430 <= pygame.mouse.get_pos()[1] <= 470:
            screen.blit(wait_cont1, (150, 350))
        else:
            screen.blit(wait_cont, (150, 350))
    if Guide == False and wait_screen == True and \
                    210 <= pygame.mouse.get_pos()[0] <= 400 and 530 <= pygame.mouse.get_pos()[1] <= 570:
        screen.blit(wait_opt1, (150, 450))
    else:
        screen.blit(wait_opt, (150, 450))
    if Guide == False and wait_screen == True and \
                    210 <= pygame.mouse.get_pos()[0] <= 400 and 480 <= pygame.mouse.get_pos()[1] <= 520:
        screen.blit(wait_play1, (150, 400))
    else:
        screen.blit(wait_play, (150, 400))
    if Guide == False and wait_screen == True and \
                    210 <= pygame.mouse.get_pos()[0] <= 400 and 580 <= pygame.mouse.get_pos()[1] <= 620:
        screen.blit(wait_guide1, (150, 500))
    else:
        screen.blit(wait_guide, (150, 500))

    pygame.display.update()


def guide_screen():
    global anim
    if anim + 1 >= FPS:
        anim = 0
    screen.blit(wait_text1, (0, 25))
    screen.blit(pygame.transform.scale(fr[anim // 5].convert_alpha(), (300, 300)), (150, 350))
    if Guide == True and 15 <= pygame.mouse.get_pos()[0] <= 200 and 745 <= pygame.mouse.get_pos()[1] <= 785:
        screen.blit(wait_back1, (-50, 665))
    else:
        screen.blit(wait_back, (-50, 665))
    anim += 1
    pygame.display.update()

def options_screen():
    if Options == True and 15 <= pygame.mouse.get_pos()[0] <= 200 and 745 <= pygame.mouse.get_pos()[1] <= 785:
        screen.blit(wait_back1, (-50, 665))
    else:
        screen.blit(wait_back, (-50, 665))
    if sound == '1':
        screen.blit(pygame.transform.scale(opt_music, (600, 150)), (50, 150))
    else:
        screen.blit(pygame.transform.scale(opt_music1, (600, 150)) , (50, 150))
    pygame.display.update()

def prepair_screen():
    global  shipN
    if Prepair == True and 15 <= pygame.mouse.get_pos()[0] <= 200 and 745 <= pygame.mouse.get_pos()[1] <= 785:
        screen.blit(wait_back1, (-50, 665))
    else:
        screen.blit(wait_back, (-50, 665))


    screen.blit(pygame.transform.scale(arrow1, (45, 50)), (380, 393))
    screen.blit(pygame.transform.scale(arrow2, (45, 50)), (170, 400))
    screen.blit(pygame.transform.scale(ships[shipN], (150, 150)), (225, 350))
    pygame.display.update()

def game_lvl1():

    if len(mobs) != 0:
        pass
    else:
        if score >= 250:
            for i in range(random.randint(2, 10)):
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)
    all_sprites.update()
    all_sprites.draw(screen)

    screen.blit(pygame.transform.scale(lvl1_bg, (600, 1600)), (0, bg_y1))
    screen.blit(pygame.transform.scale(lvl1_bg, (600, 1600)), (0, bg_y))
    all_sprites.draw(screen)
    pygame.display.update()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game is True:
            if event.key == pygame.K_ESCAPE:
                game = False
                wait_screen = True
                score = 0
                mobs = set()
                all_sprites = pygame.sprite.Group()
                sound2.stop()
                shootTiming = 0
            if event.key == pygame.K_SPACE:
                if score - shootTiming >= 15:
                    player.shoot()
                    shootTiming = score
        if event.type == pygame.KEYDOWN and game is False:
            if event.key == pygame.K_TAB:
                game = True
                for i in mobs:
                    i.kill()
                x, y = 248, 690
                bg_y = -800
                bg_y1 = -1600
                ch_y = 5
                ch_y1 = 0
    if event.type == pygame.MOUSEBUTTONDOWN:
            if Guide == False and Options == False and wait_screen == True and Prepair == False and \
                    210 <= pygame.mouse.get_pos()[0] <= 400 and 580 <= pygame.mouse.get_pos()[1] <= 620:
                Guide = True
                wait_screen = False
                anim = 0

            if Guide == True and 5 <= pygame.mouse.get_pos()[0] <= 195 and 755 <= pygame.mouse.get_pos()[1] <= 795:
                Guide = False
                wait_screen = True
            if Options == False and wait_screen == True and Guide == False and \
                    210 <= pygame.mouse.get_pos()[0] <= 400 and 530 <= pygame.mouse.get_pos()[1] <= 570:
                Options = True
                wait_screen = False

            if Options == True and 15 <= pygame.mouse.get_pos()[0] <= 200 and 745 <= pygame.mouse.get_pos()[1] <= 785:
                Options = False
                wait_screen = True
            if Options == True and 115 <= pygame.mouse.get_pos()[0] <= 530 and 210 <= pygame.mouse.get_pos()[1] <= 255:
                if sound == '1':
                    sound = '0'
                else:
                    sound = '1'
                if sound == '1':
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
                with open('assets/st.txt', 'w', encoding='utf-8') as f:
                    f.write(f'0;0;{sound};')
            if Guide == False and wait_screen == True and Options == False and \
                    210 <= pygame.mouse.get_pos()[0] <= 400 and 480 <= pygame.mouse.get_pos()[1] <= 520:
                seconds = 0
                screen.fill(pygame.Color("black"))
                wait_screen = False
                Prepair = True

            if Prepair == True and Guide == False and Options == False and wait_screen == False and \
                    15 <= pygame.mouse.get_pos()[0] <= 200 and 745 <= pygame.mouse.get_pos()[1] <= 785:
                Prepair = False
                wait_screen = True

            if Prepair == True and Guide == False and Options == False and wait_screen == False and \
                    170 <= pygame.mouse.get_pos()[0] <= 210 and 405 <= pygame.mouse.get_pos()[1] <= 440:
                if shipN - 1 < 0:
                    pass
                else:
                    shipN -= 1
                print(shipN)

            if Prepair == True and Guide == False and Options == False and wait_screen == False and \
                    380 <= pygame.mouse.get_pos()[0] <= 425 and 400 <= pygame.mouse.get_pos()[1] <= 435:
                if shipN == 14:
                    pass
                else:
                    pygame.mixer.music.stop()
                    shipN += 1
                    game = True
                    Prepair = False
                    player = Player()
                    sound2.play(-1)
                    all_sprites.add(player)

    all_sprites.update()
    if wait_screen and Guide == False and Options == False and Prepair == False and game == False:
        screen.blit(wait_bg, (-1250, 0))
        draw_wait_screen()
    if Guide:
        screen.blit(wait_bg1, (0, 0))
        guide_screen()
    elif Options:
        screen.blit(wait_bg1, (0, 0))
        options_screen()
    elif Prepair:
        screen.blit(wait_bg1, (0, 0))
        prepair_screen()
    elif game:
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
    else:
        x, y = 248, 690
        bg_y = -800
        bg_y1 = -1600
        ch_y = 5
        ch_y1 = 0

    bg_y += ch_y
    bg_y1 += ch_y1
    print(all_sprites, shipN)
    print(pygame.mouse.get_pos(), int(clock.get_fps()), len(mobs), score)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
