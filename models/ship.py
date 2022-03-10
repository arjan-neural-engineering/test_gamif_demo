import pygame
import os
import random
from utils.resource_path import resource_path
from utils.collide import collide
from pygame.sprite import Sprite
from models.laser import Laser
from models.explosion import Explosion, explosion_group
from screens.background import slow_bg_obj
from screens.controls import audio_cfg
from constants import HEIGHT, \
    CANVAS, \
    WIDTH, \
    SHIPS_PATH, \
    FRIEND_SHIP, \
    ENEMY_SHIP, \
    STIM_ON_SHIP, \
    STIM_OFF_SHIP, \
    EASY_SPACE_SHIP, \
    MEDIUM_SPACE_SHIP, \
    HARD_SPACE_SHIP, \
    PLAYER_SPACE_SHIP, \
    BOSS_SHIP, \
    PLAYER_LASER, \
    RED_LASER, \
    BLUE_LASER, \
    GREEN_LASER, \
    FLAME_LASER, \
    PLAYER_LASER_SOUND, \
    ENEMY_LASER_SOUND, \
    MENU_MUSIC_PATH, \
    BLADE_RUNNER_PATH, \
    tablet_L, \
    tablet_R

enemy_ship_group = pygame.sprite.Group()


class Ship(Sprite):
    CoolDown = 10
    boss_max_health = 99
    SCORE = 0

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        # drawing lasers before the ship so that it doesn't appear
        # like the lasers appear from above the ship
        for laser in self.lasers:
            laser.draw(window)

        # making ship's coordinates centered in the sprite
        background_width = slow_bg_obj.rectBGimg.width
        screen_rect = window.get_rect()
        center_x = screen_rect.centerx
        starting_x = center_x - background_width // 2
        x_offset, y_offset = self.ship_img.get_size()
        window.blit(self.ship_img, (starting_x + self.x -
                                    x_offset / 2, self.y - y_offset / 2))

    def move_lasers(self, vel, obj):
        self.coolDown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def coolDown(self):
        if self.cool_down_counter >= self.CoolDown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            PLAYER_LASER_SOUND.play()
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def get_score(self):
        return self.SCORE


class Player(Ship):
    def __init__(self, x, y, health=100, mouse_movement=False):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SPACE_SHIP
        self.laser_img = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.mouse_movement = mouse_movement
        self.run = True
        self.vel = 5
        self.rtma_L = False
        self.rtma_R = False

    def move_with_keyboard(self, pos):
        pygame.init()
        keys = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT:
                if e.myEvent == tablet_L:
                    pygame.event.post(tablet_L)
                    self.rtma_L = True
                elif e.myEvent == tablet_R:
                    pygame.event.post(tablet_R)
                    self.rtma_R = True

        action = {'LEFT': keys[pygame.K_a],  # keys[pygame.K_LEFT] or keys[pygame.K_a]
                  'RIGHT': keys[pygame.K_d],  # keys[pygame.K_RIGHT] or keys[pygame.K_d]
                  'UP': keys[pygame.K_UP] or keys[pygame.K_w],
                  'DOWN': keys[pygame.K_DOWN] or keys[pygame.K_s],
                  'SHOOT': keys[pygame.K_SPACE],
                  'QUIT': keys[pygame.K_BACKSPACE]}

        # Return to main page
        if action['QUIT']:
            audio_cfg.play_music(BLADE_RUNNER_PATH)
            self.run = False
        # Left Key action['LEFT'] or
        if self.rtma_L and (self.x - self.vel) > self.get_width() / 2:
            # self.x = pos
            print("reached rtma_L code")
            while self.x != pos:
                self.x -= self.vel
                if self.x == pos:
                    self.rtma_L = False
                    self.shoot()
                    break
            # # self.x -= self.vel
        # Right Key action['RIGHT'] or
        if self.rtma_R and (self.x + self.vel + self.get_width() / 2) < WIDTH:
            print("reached rtma_R code")
            while self.x != 600:
                self.x += self.vel
                if self.x == 600:
                    self.rtma_R = False
                    self.shoot()
                    break
            # self.x = 600
            # self.x += self.vel
        # Up Key
        if action['UP'] and (self.y - self.vel) > 0:
            self.y -= self.vel
        # Down Key
        if action['DOWN'] and (self.y + self.vel + self.get_height()) < HEIGHT:
            self.y += self.vel
        # Shoot Laser
        if action['SHOOT']:
            self.shoot()

    def move_with_mouse(self):
        cx, cy = pygame.mouse.get_pos()
        button = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        # Movement
        if self.get_width() / 2 < cx < WIDTH - self.get_width() / 2 \
                and 0 < cy < HEIGHT:
            self.x = cx
            self.y = cy
        # Shoot Laser
        if button[0] or keys[pygame.K_SPACE]:
            self.shoot()
        # Return to main page if right click
        # if button[2] or keys[pygame.K_BACKSPACE]:
        #     audio_cfg.play_music(BLADE_RUNNER_PATH)
        #     self.run = False

    def move(self, pos):
        if self.mouse_movement:
            self.move_with_mouse()
        else:
            self.move_with_keyboard(pos)

    def move_lasers(self, vel, objs):
        self.coolDown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        self.SCORE += 50
                        if obj.ship_type == 'boss':
                            if self.boss_max_health - 10 <= 0:
                                objs.remove(obj)
                                self.boss_max_health = 100
                            else:
                                self.boss_max_health -= 10
                        else:
                            # enemy ship death explosion
                            explosion = Explosion(obj.x, obj.y)
                            explosion_group.add(explosion)
                            objs.remove(obj)

                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthBar(window)

    def healthBar(self, window):
        background_width = slow_bg_obj.rectBGimg.width
        screen_rect = window.get_rect()
        center_x = screen_rect.centerx
        starting_x = center_x - background_width // 2
        x_offset, y_offset = self.ship_img.get_size()
        pygame.draw.rect(window, (255, 0, 0), (starting_x + self.x - x_offset / 2,
                                               self.y + y_offset / 2 + 10,
                                               int(self.ship_img.get_width()),
                                               10))
        pygame.draw.rect(window, (0, 255, 0), (starting_x + self.x - x_offset / 2,
                                               self.y + y_offset / 2 + 10,
                                               int(self.ship_img.get_width() *
                                                   (self.health / self.max_health)),
                                               10))

    def reset(self):
        self.rtma_L = False
        self.rtma_R = False


class Enemy(Ship):
    TYPE_MODE = {
        'easy': (EASY_SPACE_SHIP, RED_LASER, 10),
        'medium': (MEDIUM_SPACE_SHIP, BLUE_LASER, 18),
        'hard': (HARD_SPACE_SHIP, GREEN_LASER, 25),
        'boss': (BOSS_SHIP, FLAME_LASER, 100),

        'friend': (FRIEND_SHIP, FLAME_LASER, 10),
        'enemy': (ENEMY_SHIP, BLUE_LASER, 18),
        'stimoff': (STIM_OFF_SHIP, GREEN_LASER, 25),
        'stimon': (STIM_ON_SHIP, FLAME_LASER, 100)
    }

    ship_type = ''

    def __init__(self, x, y, ship_type, swapped=False, left=True, health=100):
        super().__init__(x, y, health)
        self.ship_type = ship_type
        self.ship_img, self.laser_img, self.damage = self.TYPE_MODE[self.ship_type]
        self.size = self.ship_img.get_size()
        self.ship_img = pygame.transform.scale(
            self.ship_img, (int(self.size[0] * 0.35), int(self.size[1] * 0.35)))
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.swapped = swapped
        self.left = left

    def move(self, vel):
        self.y += vel

    def move_lasers(self, vel, obj):
        self.coolDown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                # display collisions if enemy lasers hit the player
                sm_explosion = Explosion(laser.x, laser.y, size=60)
                explosion_group.add(sm_explosion)
                obj.health -= self.damage
                self.lasers.remove(laser)

    def shoot(self):
        if self.cool_down_counter == 0 and self.y > 0:
            ENEMY_LASER_SOUND.play()
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def change_color(self):
        keep_x = self.x
        keep_y = self.y
        if self.ship_type == 'stimoff':
            self.ship_type = 'stimon'
            self.ship_img = pygame.image.load("stim_1.png").convert_alpha()
        elif self.ship_type == 'stimon':
            self.ship_type = 'stimoff'
            self.ship_img = pygame.image.load("stim_0.png").convert_alpha()
        # resize alien sprite
        self.size = self.ship_img.get_size()
        self.ship_img = pygame.transform.scale(
            self.ship_img, (int(self.size[0] * 0.35), int(self.size[1] * 0.35)))
        self.rect = self.ship_img.get_rect()
        self.rect.center = [keep_x, keep_y]

    def reset(self):
        pass


# Inherit from sprite
# JUNK WORK
class StimShip(pygame.sprite.Sprite):
    TYPE = {
        'friend': (FRIEND_SHIP, FLAME_LASER, 10),
        'enemy': (ENEMY_SHIP, BLUE_LASER, 18),
        'stimoff': (STIM_OFF_SHIP, GREEN_LASER, 25),
        'stimon': (STIM_ON_SHIP, FLAME_LASER, 100)
    }

    def __init__(self, x, y, size=75):
        super(StimShip, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(0, 1):
            img = pygame.image.load(resource_path(os.path.join(
                SHIPS_PATH, f"stim_{num}.png"))).convert_alpha()
            img = pygame.transform.scale(img, (size, size))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.counter = 0
        self.x = x
        self.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def collision(self, obj):
        return collide(self, obj)

    def update(self):
        self.rect.x += self.move_direction
        self.rect.y += 1
        self.move_counter += 1
        if abs(self.move_counter > 175) or self.rect.right > WIDTH or \
                self.rect.left < 0:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        if self.rect.bottom > HEIGHT:
            self.kill()

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()


max_left_x = random.randrange(50, WIDTH / 2 - 50)
max_right_x = random.randrange(WIDTH / 2 + 50, WIDTH - 100)
start_y = random.randrange(-300, -100)


class LeftStimShip(StimShip):
    global max_left_x
    global start_y

    def __init__(self, x, y):
        super(StimShip, self).__init__()
        pygame.sprite.Sprite.__init__(x, y)
        # super().__init__(self, x, y, size)

    def update(self):
        if HEIGHT / 2 - 5 > self.y > 100:
            self.index += 1
            self.image = self.images[self.index]
        else:
            self.index = 0
            self.image = self.images[self.index]


class RightStimShip(StimShip):
    global max_left_x
    global start_y

    def __init__(self, x, y):
        super(StimShip, self).__init__()
        pygame.sprite.Sprite.__init__(self, x, y)
        # super().__init__(self, x, y, size)
        # self.x = max_right_x
        # self.y = start_y

    def update(self):
        if HEIGHT / 2 - 5 < self.y < HEIGHT:
            self.index += 1
            self.image = self.images[self.index]
        else:
            self.index = 0
            self.image = self.images[self.index]
