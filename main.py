import os
import sys
import pygame


pygame.init()
size = width, height = 1700, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ESCAPE из гауптвахты")
clock = pygame.time.Clock()
fps = 30

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


class Elephant(pygame.sprite.Sprite):
    image = load_image("elephant.png", colorkey=-1)
    image1 = load_image("elephant1.png", colorkey=-1)
    image2 = load_image("elephant2.png", colorkey=-1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Elephant.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 550
        self.moving = False

    def update(self, tot_time):
        if self.moving:
            if 0 <= tot_time <= 500:
                self.image = Elephant.image
            else:
                self.image = Elephant.image1
        else:
            self.image = Elephant.image2
        if True in list(pygame.key.get_pressed()):
            if list(pygame.key.get_pressed()).index(True) == 82:
                self.rect = self.rect.move(0, -3)
                self.moving = True
            elif list(pygame.key.get_pressed()).index(True) == 81:
                self.rect = self.rect.move(0, 3)
                self.moving = True
            elif list(pygame.key.get_pressed()).index(True) == 79:
                self.rect = self.rect.move(3, 0)
                self.moving = True
            elif list(pygame.key.get_pressed()).index(True) == 80:
                self.rect = self.rect.move(-3, 0)
                self.moving = True
        else:
            self.moving = False


all_sprites = pygame.sprite.Group()
running = True
Elephant(all_sprites)
total_time = 0
bg = pygame.transform.scale(load_image(r'C:\Users\1\PycharmProjects\platformer\data\background.png'), (1700, 800))
screen.blit(bg, (0, 0))
while running:
    all_sprites.update(total_time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #screen.fill(pygame.Color("white"))
    screen.blit(bg, (0, 0))
    total_time += clock.get_time()
    if total_time >= 1000:
        total_time = 0
    clock.tick(fps)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()