# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 15:51:35 2022
TABLET TEST
@author: arjan
"""

import pygame as pg
from pygame.locals import *
import PyRTMA3 as PyRTMA
from sys import exit
# import climber_config as md
import message_defs as mdefs
from constants import center_x, center_y
from models.button import Button
import os

os.environ['SDL_MOUSE_TOUCH_EVENTS'] = '1'

pg.init()
pg.font.init()

screen = pg.display.set_mode((640, 480), 0, 32)
WHITE = pg.Color(255,255,255)
screen.fill(WHITE)

font = pg.font.SysFont("arial", 32)
font_height = font.get_linesize()
alpha = 255

L_btn = Button((7, 8, 16), (255, 255, 255),
    (center_x - 210, center_y - 52), (195, 66), "LEFT")
R_btn = Button((7, 8, 16), (255, 255, 255),
    (center_x + 15, center_y - 52), (195, 66), "RIGHT")

MY_ID = 12

mod = PyRTMA.RTMA_Module(MY_ID,0)
mod.ConnectToMMM("localhost:7111")
# mod.Subscribe(mdefs.MT_TEST_DATA)
pressed_key_text = []
a = 0

# will constrain mouse to box limits and set it invisible
# pg.event.set_grab(True)
# pg.mouse.set_visible(False)


running = True
while running:
    top_text_surface = font.render("Simulate tablet", True, (0,0,0))
    screen.blit(top_text_surface, (30,30))

    L_btn.draw()
    R_btn.draw()

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            exit()
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_LEFT:
                om_L = PyRTMA.CMessage(mdefs.MT_GO_L)
                payload = mdefs.MDF_GO_L()
                payload.pressedL = 1
                PyRTMA.copy_to_msg(payload, om_L)
                mod.SendMessage(om_L)
                print("sent L")
                L_text_surface = font.render("Left key pressed", True, (0,0,0))
                screen.blit(L_text_surface, (80,90))
                L_btn.outline = "onover"
                pg.display.flip()
                pg.event.pump()
                pg.time.wait(100)
                screen.fill(WHITE)
                screen.blit(top_text_surface, (30,30))
                L_btn.draw()
                R_btn.draw()
                L_btn.outline = "default"
                # L_text_blank = font.render("Left key pressed", True, (255,255,255))
                # screen.blit(L_text_blank, (80,90))
                # L_text_surface.fill((255, 255, 255, alpha), special_flags=pg.BLEND_RGBA_MULT)
            elif e.key == pg.K_RIGHT:
                om_R = PyRTMA.CMessage(mdefs.MT_GO_R)
                payload = mdefs.MDF_GO_R()
                payload.pressedR = 1
                PyRTMA.copy_to_msg(payload, om_R)
                mod.SendMessage(om_R)
                print("sent R")
                R_text_surface = font.render("Right key pressed", True, (0,0,0))
                screen.blit(R_text_surface, (80,120))
                R_btn.outline = "onover"
                pg.display.flip()
                pg.event.pump()
                pg.time.wait(100)
                screen.fill(WHITE)
                screen.blit(top_text_surface, (30,30))
                L_btn.draw()
                R_btn.draw()
                R_btn.outline = "default"
        elif e.type == pg.FINGERDOWN:
            print("gesture received!")
        elif e.type == pg.FINGERMOTION:
            print("detected finger motion")
        elif e.type == pg.FINGERUP:
            print("got to finger up")
        elif ((e.type == pg.KEYDOWN and e.key in (pg.K_q, pg.K_ESCAPE))
                or e.type == pg.QUIT):
                running = False
                # R_text_blank = font.render("Right key pressed", True, (255,255,255))
                # screen.blit(R_text_blank, (80,120))
                # R_text_surface.fill((255, 255, 255, alpha), special_flags=pg.BLEND_RGBA_MULT)
    
    # screen.fill(WHITE)
    pg.display.update()

                

    pressed_keys = pg.key.get_pressed()
    y = font_height
    
    for key_constant, pressed in enumerate(pressed_keys):
        if pressed:
            key_name = pg.key.name(key_constant)
            # text_surface = font.render(key_name+ " pressed ", True, (0,0,0))
            # screen.blit(text_surface, (8,y))
            y += font_height
            
        pg.display.update()


mod.DisconnectFromMMM()