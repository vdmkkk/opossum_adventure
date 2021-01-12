import pygame as pg

pg.init()

WIDTH = 1000
HEIGHT = 1000
TILE_SIZE = 50
game_over = False

undg_bg = pg.image.load('source/undg_bg.png')
out_bg = pg.image.load('source/out_bg.png')

clock = pg.time.Clock()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('opossum adventure')


map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


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
                if tile == 1:
                    img = pg.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pg.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    redish = Redish(col_count * TILE_SIZE, row_count * TILE_SIZE + (TILE_SIZE // 2))
                    redishes.add(redish)
                col_count += 1
            row_count += 1

    def update(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pg.image.load(f'source/opossum{num}.png')
            img_right = pg.transform.scale(img_right, (100, 60))
            img_right.convert()
            img_left = pg.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pg.transform.flip(self.images_right[0], False, True)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.on_ground = True
        self.dir = 0

    def update(self):

        dx = 0
        dy = 0
        walk_cooldown = 20

        global game_over
        if not game_over:
            key = pg.key.get_pressed()

            # keys
            if key[pg.K_LEFT]:
                dx -= 4
                self.counter += 1
                self.dir = -1
                self.image = self.images_left[self.index]
            if key[pg.K_RIGHT]:
                dx += 4
                self.dir = 1
                self.counter += 1
                self.image = self.images_right[self.index]
            if key[pg.K_UP] and self.on_ground:
                self.vel_y = -20
                self.on_ground = False
            if not key[pg.K_UP]:
                self.on_ground = True
            if not key[pg.K_LEFT] and not key[pg.K_RIGHT]:
                self.counter = 0
                self.index = 0

            # gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # collision
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            # collision with redish
            if pg.sprite.spritecollide(self, redishes, False):
                game_over = True

            # animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.dir == 1:
                    self.image = self.images_right[self.index]
                if self.dir == -1:
                    self.image = self.images_left[self.index]

            # update
            self.rect.x += dx
            self.rect.y += dy
        elif game_over:
            self.image = self.dead_image

        screen.blit(self.image, self.rect)


class Redish(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('source/redish.png')
        self.image = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


redishes = pg.sprite.Group()
world = World(map)
player = Player(100, HEIGHT - 300)


running = True
while running:
    clock.tick(120)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.blit(undg_bg, (0, 0))
    world.update()
    redishes.draw(screen)
    player.update()
    pg.display.update()
pg.quit()