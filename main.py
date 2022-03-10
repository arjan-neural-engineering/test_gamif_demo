import os
import pygame
import argparse
import importlib.util
# spec = importlib.util.spec_from_file_location("rtma-master", "C:/git/rtma-master/lang/python/PyRTMA3.py")
# getmod = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(getmod)
# import sys
# sys.path.append("C:/git/rtma-master/") # lang/python/PyRTMA3.py
import PyRTMA3 as PyRTMA
#
from PyRTMA3 import copy_to_msg, copy_from_msg

# import climber_config as md
import message_defs as mdefs


from screens.game import game
from screens.controls import audio_cfg, display_cfg, controls
from screens.score_board import score_board
from screens.background import slow_bg_obj
from models.button import Button
from models.icon_button import IconButton
from utils.resource_path import resource_path

from constants import TITLE,\
    BOSS_SHIP,\
    PLAYER_SPACE_SHIP,\
    PLAYER_LASER,\
    WHITE,\
    controlImage,\
    trophyImage,\
    CANVAS, \
    framespersec, \
    FPS, \
    FONT_PATH, \
    MENU_MUSIC_PATH, \
    center_x,\
    center_y, \
    BLADE_RUNNER_PATH

# parsing arguments
ag = argparse.ArgumentParser()
ag.add_argument("--mute", help="disable all sounds", action="store_true")
args = vars(ag.parse_args())

if args["mute"]:
    audio_cfg.toggle_mute()

pygame.font.init()

pygame.display.set_caption(TITLE)

# sysConfig = md.loadLocalSysConfig()
# MMM_IP = "localhost:7111"
#
# ME = 11
#
# print("MMM_IP: " + MMM_IP)
# mod = PyRTMA.RTMA_Module(ME, 0)
# mod.ConnectToMMM("localhost:7111")
# mod.Subscribe(mdefs.MT_GO_L)
# mod.Subscribe(mdefs.MT_GO_R)


# rtma_L = False
# rtma_R = False

def main():

    title_font = pygame.font.Font(resource_path(
        os.path.join(FONT_PATH, 'edit_undo.ttf')), 82)
    # sub_title_font = pygame.font.Font(resource_path(
    #     os.path.join(FONT_PATH, 'neue.ttf')), 30)
    # control_font = pygame.font.Font(resource_path(
    #     os.path.join(FONT_PATH, 'neue.ttf')), 36)

    # audio_cfg.play_music(MENU_MUSIC_PATH)
    audio_cfg.play_music(BLADE_RUNNER_PATH)

    # window_width = CANVAS.get_width()
    background_width = slow_bg_obj.rectBGimg.width
    starting_x = center_x - background_width//2
    ending_x = center_x + background_width//2

    mouse_btn = Button((7, 8, 16), (255, 255, 255),
                       (center_x - 210, center_y + 22), (195, 66), "MOUSE")
    keyboard_btn = Button((7, 8, 16), (255, 255, 255),
                          (center_x + 15, center_y + 22), (195, 66), "TABLET")
    control_btn = IconButton(controlImage, (starting_x + 30, 15))
    trophy_btn = IconButton(trophyImage, (ending_x - 85, 25))

    run = True
    while run:

        # msg = PyRTMA.CMessage()
        # mod.ReadMessage(msg, 0.0001)    # blocking read
        # # the second argument is a refresh rate
        # print("Received message ", msg.GetHeader().msg_type)

        # if msg.GetHeader().msg_type == mdefs.MT_GO_L:
        #     rtma_L = True
        #     print(" Pressed L key")
        # if msg.GetHeader().msg_type == mdefs.MT_GO_R:
        #     rtma_R = True
        #     print(" Pressed R key")


        pygame.mouse.set_visible(True)
        slow_bg_obj.update()
        slow_bg_obj.render(CANVAS)

        mouse_btn.draw()
        keyboard_btn.draw()

        title_label = title_font.render('RNEL GAMIFIED TASK', 1, WHITE)
        CANVAS.blit(title_label, (center_x -
                    title_label.get_width()//2, center_y-title_label.get_height() + 5))

        # Ships
        CANVAS.blit(BOSS_SHIP, (starting_x + 285, 75))
        CANVAS.blit(PLAYER_SPACE_SHIP, (center_x - 50, 575))
        CANVAS.blit(PLAYER_LASER, (center_x - 50, 475))

        # Control Page
        control_btn.draw()

        # ScoreBoard Page
        trophy_btn.draw()

        audio_cfg.display_volume(CANVAS)
        pygame.display.update()
        framespersec.tick(FPS)  # capping frame rate to 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Keyboard events
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    audio_cfg.toggle_mute()
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    audio_cfg.inc_volume(5)
                if event.key == pygame.K_MINUS:
                    audio_cfg.dec_volume(5)
                if event.key == pygame.K_f:
                    display_cfg.toggle_full_screen()

            # Handle mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse_btn.isOver():
                        game(True)
                    if keyboard_btn.isOver():
                        game()
                    if control_btn.isOver():
                        controls()
                    if trophy_btn.isOver():
                        score_board()

            # Mouse hover events
            if event.type == pygame.MOUSEMOTION:
                if mouse_btn.isOver():
                    mouse_btn.outline = "onover"
                else:
                    mouse_btn.outline = "default"

                if keyboard_btn.isOver():
                    keyboard_btn.outline = "onover"
                else:
                    keyboard_btn.outline = "default"

                if control_btn.isOver():
                    control_btn.outline = "onover"
                else:
                    control_btn.outline = "default"

                if trophy_btn.isOver():
                    trophy_btn.outline = "onover"
                else:
                    trophy_btn.outline = "default"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
            run = False

        if keys[pygame.K_c]:
            controls()

        if keys[pygame.K_s]:
            score_board()

    pygame.quit()


main()
