import os
import sys
import pygame
import math as matematics
import random
from pygame import *

pygame.init()
pygame.key.set_repeat(200, 70)
size = WIDTH, HEIGHT = 1560, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ESCAPE из гауптвахты")
clock = pygame.time.Clock()
fps = 120
g = 10


# Загрузка музыки
# pygame.mixer.music.load(r"C:\Users\1\PycharmProjects\my_test_of_project\music\zoo.mp3")
# pygame.mixer.music.play()

def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print("файл не существует")
        sys.exit()
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_map(name):
    fullname = os.path.join("maps", name)
    if not os.path.isfile(fullname):
        print("файл не существует")
        sys.exit()
    else:
        maps = open(fullname)
    return maps


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        s = [True, 0, 0] # s[0]-системное s[1]-начало s[2]-длина
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('deep', x, y)
            if level[y][x] == '#':
                Tile('dirt', x, y)
            if level[y][x] == "!":
                Tile("barrier", x, y)
            if level[y][x] == 'f':
                Tile("finish", x, y)
    return x, y


class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        # print(type(obj) == Spoody, "TYPE")
        obj.rect.x += self.dx
        # вычислим координату клeтки, если она уехала вверх за границу экрана
        if type(obj) != Bullet:
            if obj.rect.y < -obj.rect.height:
                obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
            # вычислим координату клeтки, если она уехала вниз за границу экрана
            if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
                obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target):
        # if type(target) == Elephant:
        # if target.changed_x != True:
        # print("THIS")
        # self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        # else:
        # if pleer.changed_x != True:
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        if type(target) != Bullet:
            self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.pos_x = pos_x * tile_width
        self.pos_y = pos_y * tile_height
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Elephant(pygame.sprite.Sprite):
    image = load_image("elephant.png", colorkey=-1)
    image1 = load_image("elephant1.png", colorkey=-1)
    image2 = load_image("elephant2.png", colorkey=-1)
    image_hit = load_image("elephant_attack.png", colorkey=-1)
    image_move_hit1 = load_image("elephant_move_attack1.png", colorkey=-1)
    image_move_hit2 = load_image("elephant_move_attack2.png", colorkey=-1)
    uskor_x = 0
    uskor_y = 0
    fall = False
    right = False
    up = False
    left = False
    right = False
    down = False

    def __init__(self, *group):
        super().__init__(*group)
        # self.image = Elephant.image
        self.image = Elephant.image
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 440
        self.pos_x = 200
        self.pos_y = 440
        self.moving = False
        self.cur_image = Elephant.image2
        self.mask = pygame.mask.from_surface(self.image)
        self.hit = False
        self.changed_x = False
        self.im1 = Elephant.image1
        self.im2 = Elephant.image2

    def update(self, tot_time):
        platform = pygame.sprite.spritecollideany(self, tiles_group)
        if platform:
            print('"координаты"', platform.pos_x,  self.pos_x)
            if 80 > matematics.fabs(self.rect.y - platform.rect.y):
                self.uskor_x = -self.uskor_x


        if pygame.sprite.spritecollideany(
                self, tiles_group) and self.fall:  # обработка соприкосновений с блоками по вертикали
            if pygame.sprite.spritecollideany(self, tiles_group).rect.y > self.rect.y:
                self.rect = self.rect.move(self.uskor_x // 100, self.uskor_y // 100)
                self.pos_x += self.uskor_y // 100
                self.pos_y += self.uskor_x // 100
                self.fall = False
                self.uskor_y = 0
            elif pygame.sprite.spritecollideany(self, tiles_group).rect.y < self.rect.y and \
                    self.rect.y - pygame.sprite.spritecollideany(self,
                                                                 tiles_group).rect.y < pygame.sprite.spritecollideany(
                self, tiles_group).rect.height:
                self.fall = True
                self.rect.y = pygame.sprite.spritecollideany(self, tiles_group).rect.y + pygame.sprite.spritecollideany(
                    self, tiles_group).rect.height
                self.uskor_y = 0  # /= 2
        else:
            self.fall = True
            self.rect = self.rect.move(self.uskor_x // 100, self.uskor_y // 100)
        if self.rect.y > 900:
            self.rect.y = 0
        if self.fall:
            self.uskor_y = self.uskor_y + g
            if self.uskor_x > 0:
                self.uskor_x -= 1
            elif self.uskor_x < 0:
                self.uskor_x += 1
        if self.uskor_y > 500:
            self.uskor_y = 500

        if self.moving:
            if True in list(pygame.key.get_pressed()):
                if list(pygame.key.get_pressed()).index(True) == 79:
                    self.cur_image = self.im2
                elif list(pygame.key.get_pressed()).index(True) == 80:
                    self.cur_image = pygame.transform.flip(self.im2, True, False)
            if self.right:
                if 0 <= tot_time <= 500:
                    self.image = Elephant.image
                else:
                    self.image = Elephant.image1
            else:
                if 0 <= tot_time <= 500:
                    self.image = pygame.transform.flip(Elephant.image, True, False)
                else:
                    self.image = pygame.transform.flip(self.im1, True, False)
        else:
            self.image = self.cur_image

        if max(list(pygame.key.get_pressed())):
            if list(pygame.key.get_pressed()).index(True) == 44:
                if self.cur_image == self.im2 and not self.right:
                    self.image = Elephant.image_hit
                    self.changed_x = False
                elif self.cur_image != self.im2 and not self.left:
                    self.image = pygame.transform.flip(Elephant.image_hit, True, False)
                    if not self.changed_x:
                        if pygame.sprite.spritecollideany(self, tiles_group):
                            # if not self.moving:
                            self.rect.x -= Elephant.image_hit.get_rect().width - Elephant.image2.get_rect().width
                            self.changed_x = True
            if self.up and not self.fall:
                self.uskor_y = -500
                self.fall = True
                self.moving = True
            elif self.down:
                self.uskor_y = 0
                self.fall = False
                self.moving = True
            else:
                self.moving = False
            if self.right:
                self.right = True
                self.uskor_x = 300
                self.moving = True
            elif self.left:
                self.right = False
                self.uskor_x = -300
                self.moving = True
            else:
                self.uskor_x = 0
        else:
            self.uskor_x = self.uskor_x * self.fall
            self.moving = False
            if self.changed_x and pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.x += Elephant.image_hit.get_rect().width - Elephant.image2.get_rect().width
                self.changed_x = False


class Spoody(pygame.sprite.Sprite):
    image_go = load_image("spoody.png", colorkey=-1)
    image_attack = load_image("spoody_atack.png", colorkey=-1)
    image_go_back = pygame.transform.flip(image_go, True, False)
    image_attack_back = pygame.transform.flip(image_attack, True, False)

    def __init__(self, x, lim, *group):  # x - номер блока, который является нулём по оcи X для данного объекта спуди
        super().__init__(*group)
        self.x = x
        self.image = self.image_go
        self.rect = self.image.get_rect()
        self.start_y = 385
        try:
            self.start_x = list(tiles_group)[self.x].rect.x
        except:
            self.start_x = 50
            print(self.x)
        self.rect.x = self.start_x
        self.rect.y = 465
        self.limit = lim
        self.a_y = -4
        self.a_x = 4

    def update(self, tot_time):
        # print("current", list(tiles_group)[20].rect.x,
        # "SPOODY", self.rect.x, self.start_x + self.limit, self.start_x - self.limit)
        self.start_y = 385  # list(tiles_group)[20].rect.y
        self.start_x = list(tiles_group)[self.x].rect.x
        self.rect = self.rect.move(self.a_x, self.a_y)
        if self.rect.x > self.start_x + self.limit:
            self.a_x = -4
        elif self.rect.x < self.start_x - self.limit:
            # print("по ОСИ")
            self.a_x = 4
            self.image = Spoody.image_go_back
        if self.rect.y < self.start_y - 5:
            self.a_y = 4
        elif self.rect.y >= self.start_y + 20:
            self.a_y = -4

        # атака
        if 0 < self.rect.x - pleer.rect.x < 150 and self.a_x < 0:
            self.image = Spoody.image_attack
        elif -150 < self.rect.x - pleer.rect.x < 0 and self.a_x > 0:
            self.image = Spoody.image_attack_back
        else:
            if self.a_x < 0:
                self.image = Spoody.image_go
            else:
                self.image = Spoody.image_go_back


class Vonni(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, x_cord):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        # print(list(tiles_group)[x_cord].rect.y - 225, list(tiles_group)[x_cord].rect.y, x_cord, "VONNI COORDS")
        self.rect.y = list(tiles_group)[x_cord].rect.y - 225
        self.rect.x = list(tiles_group)[x_cord].rect.x
        self.rect = self.rect.move(x, y)
        self.counter = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, tot_time):
        if tot_time > 800:
            self.counter += 1
        if self.counter == 50:
            self.counter = 0
            Honey(self.rect.x, self.rect.y + 60)
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Honey(pygame.sprite.Sprite):
    image = load_image("honey.png", colorkey=-1)

    def __init__(self, x_got, y_got):
        super().__init__(all_sprites)
        self.image = Honey.image
        self.rect = self.image.get_rect()
        self.start_pos = x_got
        self.rect.x = x_got
        self.rect.y = y_got
        # print("GOT:", y_got)

    def update(self, tot_time):
        self.rect = self.rect.move(-5, 0)
        if self.start_pos - self.rect.x > 300:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    image = load_image("bullet.png", colorkey=-1)

    def __init__(self, x, y, dim):
        super().__init__(all_sprites)
        self.start_pos = x
        self.dim = dim
        if self.dim == "left":
            self.im = Bullet.image
        else:
            self.im = pygame.transform.flip(Bullet.image, True, False)
        self.rect = self.im.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, tot_time):
        if self.dim == "left":
            self.rect = self.rect.move(-7, 0)
            if self.start_pos - self.rect.x > 300:
                self.kill()
        else:
            self.rect = self.rect.move(7, 0)
            if self.rect.x - self.start_pos > 300:
                self.kill()


def start_screen():
    intro_text = ["Мега платформер: ESCAPE из гауптвахты", "",
                  "Правила игры:",
                  "Для движения вправо использовать стрелку ->",
                  "Для движения влево использовать стрелку <-",
                  "                                                           ^",
                  "Для прыжка использовать стрелку |",
                  "Для удара использовать пробел ",
                  "(БИТЬ ВРАГА НЕВОЗМОЖНО ПРИ ДВИЖЕНИИ)"
                  "", "", "", "",
                  "Ну что, народ, погнали?!",
                  "Для начала игры нажмите любую клавишу"]

    fon = pygame.transform.scale(load_image('intro.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    text_coord = 80
    for l in range(len(intro_text)):
        line = intro_text[l]
        if l == 0:
            font = pygame.font.Font(None, 40)
            string_rendered = font.render(line, 1, pygame.Color('black'))
        else:
            font = pygame.font.Font(None, 30)
            string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 380
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


start_screen()

all_sprites = pygame.sprite.Group()
earth = pygame.sprite.Group()
running = True
pleer = Elephant(all_sprites)
lvl = 1
pleer.earth = earth
total_time = 0
tiles_group = pygame.sprite.Group()
tile_images = {'dirt': load_image('dirt.png', colorkey=-1), 'deep': load_image('deep.png', colorkey=-1),
               "barrier": load_image("barrier.png", colorkey=-1), "finish": load_image("final_flag.png", colorkey=-1)}
tile_width = 141
tile_height = 64
level_x, level_y = generate_level(load_level("1.txt"))

# Генерация врагов
# генерация Спуди
spoodies = [(56, 350), (69, 200), (79, 200), (91, 150)]
for spoody in spoodies:
    Spoody(spoody[0], spoody[1], all_sprites)

# генерация Вонни
vonnis = [74, 18, 85, 14, 108]
for vonni in vonnis:
    Vonni(load_image("vonni2.png", colorkey=-1), 16, 6, 50, 50, vonni)

camera = Camera((level_x, level_y))
bg = pygame.transform.scale(load_image('background.png'), (1700, 800))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            pleer.up = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            pleer.left = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            pleer.right = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            try:
                for i in all_sprites:
                    i.kill()
                level_x, level_y = generate_level(load_level(str(lvl) + ".txt"))
                pleer = Elephant(all_sprites)
            except:
                lvl = 0
            lvl += 1
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            pleer.up = False
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            pleer.right = False
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            pleer.left = False
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            print(pleer.moving, "PLEER")
            if pleer.moving:
                print("HITTING")

    camera.update(pleer)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.blit(bg, (0, 0))
    total_time += clock.get_time()
    if total_time >= 1000:
        total_time = 0
    clock.tick(fps)

    all_sprites.update(total_time)
    tiles_group.draw(screen)
    earth.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
