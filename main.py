import pygame as pg
from levels import *

pg.init()

# game values
WIDTH = 1000
HEIGHT = 1000
TILE_SIZE = 50
game_over = False
score = 0

# screen
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('opossum adventure')

# images
undg_bg = pg.image.load('source/undg_bg.png')
out_bg = pg.image.load('source/out_bg.png')
restart_img = pg.image.load('source/restart_img.png')
menu_bg = pg.image.load('source/menu_bg.png')
results_bg = pg.image.load('source/results_bg.png')
hint1 = pg.image.load('source/hint1.png')
hint2 = pg.image.load('source/hint2.png')
end_img = pg.image.load('source/end.png')
end_img = pg.transform.scale(end_img, (40, 120))

# font
font = pg.font.SysFont('Aerial', 60)
color = (255, 255, 255)

# sounds
sound1 = pg.mixer.Sound('source/music.wav')
sound1.set_volume(0.01)


# button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pg.mouse.get_pressed()[0]:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action


# right top corner info about score
def draw_score(score, x, y):
    img = font.render(score, True, color)
    worm = pg.image.load('source/worm.png')
    worm = pg.transform.scale(worm, (40, 40))
    screen.blit(worm, (x - 50, y - 5))
    screen.blit(img, (x, y))


# first screen
def menu():
    global current_bg, start_btn, exit_btn
    current_bg = menu_bg
    start_btn = Button(580, 425, pg.image.load('source/play.png'))
    exit_btn = Button(215, 425, pg.image.load('source/exit.png'))
    return {'map': 0, 'finish': 0}


# last screen
def results():
    global current_bg
    current_bg = results_bg
    return {'map': 0, 'finish': 0, 'bg': 0}


clock = pg.time.Clock()

# level system
levels = [menu(), level1(), level2(), level3(), level4(), level5(), level6(), level7(), results()]
level_index = 0
current_lvl = levels[level_index]['map']
current_finish = levels[level_index]['finish']
current_bg = undg_bg


# restart of the level
def new_attempt():
    global redishes, world, player, restart_btn, worms, old_score
    redishes = pg.sprite.Group()
    worms = pg.sprite.Group()
    world = World(current_lvl)
    player = Player(100, HEIGHT - 300, current_finish)
    old_score = score

    restart_btn = Button(370, 500, restart_img)


# switch to the next level
def next_level():
    global level_index, current_lvl, current_finish, current_bg
    if levels[level_index + 1]['bg'] != 0:
        level_index += 1
        current_lvl = levels[level_index]['map']
        current_finish = levels[level_index]['finish']
        if levels[level_index]['bg'] == 'undg':
            current_bg = undg_bg
        else:
            current_bg = out_bg
        new_attempt()
    else:
        results()


# class of level
class World():
    def __init__(self, map):

        self.tile_list = []

        dirt_img = pg.image.load('source/dirt_tile.jpg')
        grass_img = pg.image.load('source/grass_tile.jpg')
        images = [dirt_img, grass_img]

        row_count = 0

        # tiles upload
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
                if tile == 4:
                    worm = Worm(col_count * TILE_SIZE, row_count * TILE_SIZE + (TILE_SIZE // 2))
                    worms.add(worm)
                if tile == 5:
                    img = pg.transform.scale(hint2, (150, 150))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 6:
                    img = pg.transform.scale(hint1, (200, 140))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    # tiles render
    def update(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


# player class
class Player():
    def __init__(self, x, y, finish):
        # downloading several images for animations
        self.images_right = []
        self.images_left = []
        self.finish = finish
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
        self.can_jump = False

    # render of the player
    def update(self):

        dx = 0
        dy = 0
        walk_cooldown = 20

        global game_over

        # while player alive
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
            if key[pg.K_UP] and self.on_ground and self.can_jump:
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
            self.can_jump = False
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.can_jump = True
                        self.vel_y = 0

            # collision with reddish
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

        # if player is dead
        elif game_over:
            self.image = self.dead_image
        # if player completed the level
        if self.rect.x >= self.finish[0] and self.rect.y <= self.finish[1]:
            next_level()
        screen.blit(self.image, self.rect)


# enemy class of reddish
class Redish(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('source/redish.png')
        self.image = pg.transform.scale(img, (TILE_SIZE - 20, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x + 10
        self.rect.y = y


# coin class of a worm
class Worm(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load('source/worm.png')
        self.image = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# first screen must be the menu screen
menu()

running = True
while running:
    clock.tick(120)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.blit(current_bg, (0, 0))

    # what to render if it is menu
    if current_bg == menu_bg:
        if start_btn.draw():
            pg.init()
            next_level()
        if exit_btn.draw():
            break

    # what to render if it is results screen
    elif current_bg == results_bg:
        draw_score('Your score is: ' + str(score), 370, 490)

    # rendering levels themselves
    else:
        sound1.play()
        world.update()
        screen.blit(end_img, (current_finish[0] + 105, current_finish[1] - 70))
        redishes.draw(screen)
        worms.draw(screen)
        # checking for coin collision
        if pg.sprite.spritecollide(player, worms, True):
            score += 1
        draw_score(str(score), 910, 70)
        player.update()

        # restarting the level
        if game_over:
            if restart_btn.draw():
                game_over = False
                score = old_score
                new_attempt()
    pg.display.update()
pg.quit()