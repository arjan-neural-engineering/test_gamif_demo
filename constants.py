import pygame
import os

from utils.resource_path import resource_path
# from screens.background import slow_bg_obj

# ROOT VARS
TITLE = 'GAMIFIED CALIBRATION TASK'
WIDTH = 750
HEIGHT = 750

# Define some colors
BLACK = (0, 0, 0)
black = (0, 0, 0)
WHITE = (255, 255, 255)
white = (255, 255, 255)
GREEN = (0, 255, 0)
green = (0, 255, 0)
RED = (255, 0, 0)
red = (255, 0, 0)
BLUE = (0, 0, 255)
blue = (0, 0, 255)

# Canvas Dimensions
CANVAS = pygame.display.set_mode((WIDTH, HEIGHT))

screen_rect = CANVAS.get_rect()
center_x = screen_rect.centerx
center_y = screen_rect.centery

# Load Background Image
backgroundImage = pygame.image.load(resource_path(os.path.join(
    'assets', 'graphics', 'background-black.png')))

# Set Background Dimensions
BG = pygame.transform.scale(backgroundImage, (WIDTH, HEIGHT))

FPS = 60
framespersec = pygame.time.Clock()

score_list = []

# list of all game sounds
soundList = []

# Initialize Sound System
pygame.mixer.init()

# PATH VARS
FONT_PATH = os.path.join('assets', 'fonts')
EXPLOSION_PATH = os.path.join('assets', 'graphics', 'explosion')
SHIPS_PATH = os.path.join('assets', 'graphics', 'stimships')

# Load Controls Image
controlImage = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'joystick.png')))
trophyImage = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'trophy.png')))

goBackImage = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'back2.png')))
# goBackImage = pygame.transform.scale()
goBackImage = pygame.transform.scale(goBackImage, (34*2.4, 19*2.4))

# Load Hearts
heartImage = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'heart.png')))

# Load Enemy Ships
EASY_SPACE_SHIP = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'easy.png')))
MEDIUM_SPACE_SHIP = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'medium.png')))
HARD_SPACE_SHIP = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'hard.png')))
BOSS_SHIP = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'boss.png')))

FRIEND_SHIP = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'friend.png')))
ENEMY_SHIP = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'enemy.png')))
STIM_OFF_SHIP = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'stim_off.png')))
STIM_ON_SHIP = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'stim_on.png')))


# Load Player
PLAYER_SPACE_SHIP = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'spaceship2.png')))
PLAYER_LASER = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'pixel_laser_cosmic.png')))

# Load Lasers
RED_LASER = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'pixel_laser_red.png')))
BLUE_LASER = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'pixel_laser_blue.png')))
GREEN_LASER = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'pixel_laser_green.png')))
FLAME_LASER = pygame.image.load(resource_path(
    os.path.join('assets', 'graphics', 'pixel_laser_flame.png')))

# load music
GAME_MUSIC_PATH = resource_path(os.path.join('assets', 'sounds', 'ingame.wav'))
MENU_MUSIC_PATH = resource_path(os.path.join('assets', 'sounds', 'menu.wav'))
BLADE_RUNNER_PATH = resource_path(os.path.join('assets', 'sounds', '2049.wav'))

# SFX VARS
PLAYER_LASER_SOUND = pygame.mixer.Sound(resource_path(
    os.path.join('assets', 'sounds', 'img_laser.wav')))
ENEMY_LASER_SOUND = pygame.mixer.Sound(resource_path(
    os.path.join('assets', 'sounds', 'enemylaser.wav')))
EXPLODE_SOUND = pygame.mixer.Sound(resource_path(
    os.path.join('assets', 'sounds', 'explode.wav')))
LASER_HIT_SOUND = pygame.mixer.Sound(resource_path(
    os.path.join('assets', 'sounds', 'laser_hit.wav')))
BLADE_RUNNER_SOUND = pygame.mixer.Sound(resource_path(
    os.path.join('assets', 'sounds', '2049.wav')))

EXP2_SOUND = pygame.mixer.Sound(resource_path(
    os.path.join('assets', 'sounds', 'img_explosion2.wav')))
EXP2_SOUND.set_volume(0.75)

# adding sounds to the list
soundList.append(PLAYER_LASER_SOUND)
soundList.append(ENEMY_LASER_SOUND)
soundList.append(EXPLODE_SOUND)
soundList.append(LASER_HIT_SOUND)
soundList.append(EXP2_SOUND)
soundList.append(BLADE_RUNNER_SOUND)



#EVENTS
# Code for custom user events
RCV_L = 1
RCV_R = 2

tablet_L = pygame.event.Event(pygame.USEREVENT, myEvent=RCV_L)
tablet_R = pygame.event.Event(pygame.USEREVENT, myEvent=RCV_R)
