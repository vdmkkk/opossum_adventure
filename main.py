import pygame as pg

pg.init()

WIDTH = 1000
HEIGHT = 1000
TILE_SIZE = 200

clock = pg.time.Clock()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('opossum adventure')


map = [[2, 2, 2, 2, 2],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1]]


class World():
    def __init__(self, map):

        self.tile_list = []

        dirt_img = pg.image.load('source/dirt_tile.jpg')
        grass_img = pg.image.load('source/grass_tile.jpg')
        images = [dirt_img, grass_img]

        row_count = 0
        for row in map:
            col_count = 0
            for tile in row:
                img = pg.transform.scale(images[tile - 1], (TILE_SIZE, TILE_SIZE))
                img_rect = img.get_rect()
                img_rect.x = col_count * TILE_SIZE
                img_rect.y = row_count * TILE_SIZE
                self.tile_list.append((img, img_rect))
                col_count += 1
            row_count += 1

    def update(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Player():
    def __init__(self, x, y):
        img = pg.image.load('source/opossum.png')
        self.image = pg.transform.scale(img, (150, 150))
        self.image.convert()
        colorkey = self.image.get_at((1, 1))
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = True

    def update(self):

        dx = 0
        dy = 0

        key = pg.key.get_pressed()

        if key[pg.K_LEFT]:
            dx -= 6
        if key[pg.K_RIGHT]:
            dx += 6
        if key[pg.K_UP] and self.on_ground:
            self.vel_y = -25
            self.on_ground = False
        if not key[pg.K_UP]:
            self.on_ground = True

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            dy = 0

        screen.blit(self.image, self.rect)




world = World(map)
player = Player(100, HEIGHT - 200)

running = True
while running:
    clock.tick(120)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    world.update()
    player.update()
    pg.display.update()
pg.quit()