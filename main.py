import os
import sys
import pygame
from pygame import *


pygame.init()
pygame.key.set_repeat(200, 70)
size = WIDTH, HEIGHT = 1560, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ESCAPE из гауптвахты")
clock = pygame.time.Clock()
fps = 60
g = 10
# Загрузка музыки
pygame.mixer.music.load(r"C:\Users\1\PycharmProjects\my_test_of_project\music\zoo.mp3")
pygame.mixer.music.play()

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
    new_player, x, y = Elephant(), None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('deep', x, y)
            if level[y][x] == '#':
                Tile('dirt', x, y)
    return x, y

class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        # вычислим координату клитки, если она уехала влево за границу экрана
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        # вычислим координату клитки, если она уехала вправо за границу экрана
        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        # вычислим координату клитки, если она уехала вверх за границу экрана
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        # вычислим координату клитки, если она уехала вниз за границу экрана
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        print(self.image.get_rect())
        if tile_type == "deep":
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        else:
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        print(self.rect, pos_x, "TILE RECTANGLE")

class Elephant(pygame.sprite.Sprite):
    image = load_image("elephant.png", colorkey=-1)
    image1 = load_image("elephant1.png", colorkey=-1)
    image2 = load_image("elephant2.png", colorkey=-1)
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
        self.image = Elephant.image
        self.rect = self.image.get_rect()
        self.image = Elephant.image
        self.rect.x = 800
        self.rect.y = 530
        self.moving = False
        self.cur_image = Elephant.image2
        self.mask = pygame.mask.from_surface(self.image)
        print("START:", self.fall, self.down, self.uskor_y, self.uskor_x)


    def update(self, tot_time):
        if pygame.sprite.spritecollideany(self, tiles_group) and self.fall:
            print(pygame.sprite.spritecollideany(self, tiles_group).rect.y)
            print("RECT", self.rect)
            #print(pygame.sprite.collide_mask(self, pygame.sprite.spritecollideany(self, tiles_group)))
            if pygame.sprite.spritecollideany(self, tiles_group).rect.y > self.rect.y:
                self.rect = self.rect.move(self.uskor_x // 100, self.uskor_y // 100)
                self.fall = False
                self.uskor_y = 0
            #if pygame.sprite.spritecollideany(self, tiles_group).rect.y - self.rect.y < self.rect[0] - self.rect[1]:
                #print(pygame.sprite.spritecollideany(self, tiles_group).rect.y - self.rect.y)
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
                    self.cur_image = self.image2
                elif list(pygame.key.get_pressed()).index(True) == 80:
                    self.cur_image = pygame.transform.flip(self.image2, True, False)
            if self.right:
                if 0 <= tot_time <= 500:
                    self.image = Elephant.image
                else:
                    self.image = Elephant.image1
            else:
                if 0 <= tot_time <= 500:
                    self.image = pygame.transform.flip(Elephant.image, True, False)
                else:
                    self.image = pygame.transform.flip(Elephant.image1, True, False)
        else:
            self.image = self.cur_image

        if max(list(pygame.key.get_pressed())):
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


all_sprites = pygame.sprite.Group()
earth = pygame.sprite.Group()
running = True
pleer = Elephant(all_sprites)
pleer.earth = earth
total_time = 0

tiles_group = pygame.sprite.Group()
tile_images = {'dirt': load_image('dirt.png', colorkey=-1), 'deep': load_image('deep.png', colorkey=-1)}
tile_width = 141
tile_height = 64
level_x, level_y = generate_level(load_level("1.txt"))
print(level_x, level_y, "LEVELS")
print(level_x, "LEVELX")
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
            pleer.down = True
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            pleer.up = False
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            pleer.right = False
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            pleer.left = False
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            pleer.down = False

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
