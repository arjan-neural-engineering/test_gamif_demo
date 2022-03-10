import os
import pygame
from pygame import time as pg_time
import time
import random
import PyRTMA3 as PyRTMA
import message_defs as mdefs

from models.ship import Player, StimShip, enemy_ship_group, \
    LeftStimShip, \
    RightStimShip, \
    Enemy
from models.explosion import Explosion, explosion_group
from utils.collide import collide
from utils.resource_path import resource_path
from .controls import audio_cfg, display_cfg
from .background import bg_obj

from constants import WIDTH, \
    HEIGHT, \
    CANVAS, \
    heartImage, \
    score_list, \
    framespersec, \
    FPS, \
    FONT_PATH, \
    MENU_MUSIC_PATH, \
    GAME_MUSIC_PATH, \
    EXP2_SOUND, \
    BLADE_RUNNER_PATH, \
    tablet_L, \
    tablet_R


# # Code for custom user events
# RCV_L = 1
# RCV_R = 2
#
# tablet_L = pygame.event.Event(pygame.USEREVENT, myEvent=RCV_L)
# tablet_R = pygame.event.Event(pygame.USEREVENT, myEvent=RCV_R)

MMM_IP = "localhost:7111"

ME = 11

print("MMM_IP: " + MMM_IP)
mod = PyRTMA.RTMA_Module(ME, 0)
mod.ConnectToMMM("localhost:7111")
mod.Subscribe(mdefs.MT_GO_L)
mod.Subscribe(mdefs.MT_GO_R)

rtma_L = False
rtma_R = False


def game(isMouse=False):
    lives = 5
    level = 0
    laser_vel = 10

    main_font = pygame.font.Font(resource_path(
        os.path.join(FONT_PATH, "edit_undo.ttf")), 50)
    sub_font = pygame.font.Font(resource_path(
        os.path.join(FONT_PATH, "neue.ttf")), 40)
    sub_small_font = pygame.font.Font(resource_path(
        os.path.join(FONT_PATH, "neue.ttf")), 35)
    lost_font = pygame.font.Font(resource_path(
        os.path.join(FONT_PATH, "edit_undo.ttf")), 55)
    win_font = pygame.font.Font(resource_path(
        os.path.join(FONT_PATH, "edit_undo.ttf")), 55)

    # load and play ingame music
    # audio_cfg.play_music(GAME_MUSIC_PATH)
    # audio_cfg.play_music(BLADE_RUNNER_PATH)
    audio_cfg.play_music(MENU_MUSIC_PATH)

    enemies = []
    wave_length = 0
    enemy_vel = 1

    # max_left_x = random.randrange(150, WIDTH / 2 - 200)
    # max_right_x = random.randrange(WIDTH / 2 + 200 , WIDTH - 100)
    #
    # start_y = random.randrange(-200, -100)

    player = Player(300, 585, mouse_movement=isMouse)
    pygame.mouse.set_visible(False)

    lost = False
    win = False
    boss_entry = True
    pause = False
    # swappedYet = False

    explosion_group.empty()
    enemy_ship_group.empty()

    def redraw_window(pause=False):
        if not pause:
            bg_obj.update()
        bg_obj.render(CANVAS)

        window_width = CANVAS.get_width()
        background_width = bg_obj.rectBGimg.width
        screen_rect = CANVAS.get_rect()
        center_x = screen_rect.centerx
        starting_x = center_x - background_width // 2
        ending_x = center_x + background_width // 2

        # Draw Text
        level_label = sub_small_font.render(f'stim trial: {level}', 1, (0, 255, 255))
        # score_label = sub_font.render(f'{player.get_score()}', 1, (0, 255, 0))

        player.draw(CANVAS)

        for enemyShip in enemies:
            enemyShip.draw(CANVAS)

        # blit player stats after enemyShips to prevent the latter
        # from being drawn over the stats

        # Lives
        # for index in range(1, lives + 1):
        #     CANVAS.blit(heartImage, (starting_x + 37 * index - 10, 20))

        # blit stats
        CANVAS.blit(level_label, (starting_x + 35, 75))
        # CANVAS.blit(score_label, (ending_x - score_label.get_width() - 30, 20))

        if win:
            score_list.append(player.get_score())
            win_label = win_font.render('WINNER :)', 1, (0, 209, 0))
            CANVAS.blit(win_label, (window_width // 2 -
                                    win_label.get_width() // 2, 350))

        if lost:
            score_list.append(player.get_score())
            lost_label = lost_font.render('GAME OVER ;(', 1, (255, 0, 0))
            CANVAS.blit(lost_label, (window_width // 2 -
                                     lost_label.get_width() // 2, 350))

        if level >= 10 and boss_entry:
            last_label = lost_font.render('BOSS LEVEL!!', 1, (255, 0, 0))
            CANVAS.blit(last_label, (window_width // 2 -
                                     last_label.get_width() // 2, 350))


        if pause:
            # if paused display the "game is paused" screen
            pause_label = main_font.render('Game Paused', 1, (0, 255, 255))
            CANVAS.blit(pause_label, (window_width // 2 -
                                      pause_label.get_width() // 2, 350))

            key_msg = sub_font.render('Press [p] to unpause', 1, (0, 0, 255))
            CANVAS.blit(key_msg, (window_width // 2 -
                                  key_msg.get_width() // 2, 400))

        # explosion group
        explosion_group.draw(CANVAS)
        explosion_group.update()

        # enemy ship group
        enemy_ship_group.draw(CANVAS)
        enemy_ship_group.update()

        audio_cfg.display_volume(CANVAS)
        pygame.display.update()
        framespersec.tick(FPS)

    timer = time.time()
    start_clock = 0

    # GAME LOOP
    while player.run:
        msg = PyRTMA.CMessage()
        mod.ReadMessage(msg, 0.0001)    # blocking read
        # the second argument is a refresh rate
        # print("Received message ", msg.GetHeader().msg_type)

        if msg.GetHeader().msg_type == mdefs.MT_GO_L:

            player.rtma_L = True
            pygame.event.post(tablet_L)
            print(" Pressed L key")
        if msg.GetHeader().msg_type == mdefs.MT_GO_R:
            player.rtma_R = True
            pygame.event.post(tablet_R)
            print(" Pressed R key")

        # clock.tick()
        redraw_window()
        if lives > 0:
            if player.health <= 0:
                lives -= 1
                player.health = 100
        else:
            lost = True
            redraw_window()
            time.sleep(3)
            player.run = False
            pygame.mouse.set_visible(True)

        if level == 10 and boss_entry:
            redraw_window()
            time.sleep(2)
            boss_entry = False
        elif level > 10:
            win = True
            redraw_window()
            time.sleep(3)
            player.run = False

        if len(enemies) == 0:
            level += 1
            # wave_length += 4

            # max_left_x = random.randrange(50, WIDTH / 2 - 50)
            # max_right_x = random.randrange(WIDTH / 2 + 50, WIDTH - 100)
            max_left_x = 100
            max_right_x = 600

            l_start_y = random.randrange(-300, -100)
            r_start_y = random.randrange(-600, -500)

            leftEnemy = Enemy(max_left_x, l_start_y, 'stimoff')
            rightEnemy = Enemy(max_right_x, l_start_y, 'stimoff' if level < 10 else 'boss', False, False)

            # endless loop until boss fight
            # if wave_length == 0:
            #     leftEnemy = Enemy(max_left_x, l_start_y, 'stimoff' if level < 10 else 'boss')
            #     rightEnemy = Enemy(max_right_x, r_start_y, 'stimoff' if level < 10 else 'boss', False, True)
            #     wave_length += 1
            # elif wave_length % 2 != 0:
            #     leftEnemy = Enemy(max_left_x, l_start_y, 'stimon' if level < 10 else 'boss')
            #     rightEnemy = Enemy(max_right_x, r_start_y, 'stimoff' if level < 10 else 'boss', False, True)
            #     wave_length += 1
            # else:
            #     leftEnemy = Enemy(max_left_x, l_start_y, 'stimoff' if level < 10 else 'boss')
            #     rightEnemy = Enemy(max_right_x, r_start_y, 'stimon' if level < 10 else 'boss', False, True)
            #     wave_length += 1
            # leftEnemy = Enemy(max_left_x, start_y, 'stimoff')
            # rightEnemy = Enemy(max_right_x, start_y, 'stimoff')

            enemies.append(leftEnemy)
            enemies.append(rightEnemy)
            # leftEnemy = LeftStimShip()
            # rightEnemy = RightStimShip()
            # enemy_ship_group.add(leftEnemy)
            # enemy_ship_group.add(rightEnemy)

            # for i in range(wave_length if level < 10 else 1):
            #     enemies.append(Enemy(
            #         random.randrange(50, WIDTH - 100),
            #         random.randrange(-1200, -100),
            #         random.choice(['easy', 'medium', 'hard']) if level < 10 else 'boss')
            #     )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.USEREVENT:
                if event.myEvent == tablet_L:
                    print("Successful L, playa!!!")
                elif event.myEvent == tablet_R:
                    print("Successful R, pimp!!!")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pygame.mouse.set_visible(True)
                    pause = True
                if event.key == pygame.K_m:
                    audio_cfg.toggle_mute()
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    audio_cfg.inc_volume(5)
                if event.key == pygame.K_MINUS:
                    audio_cfg.dec_volume(5)
                if event.key == pygame.K_f:
                    display_cfg.toggle_full_screen()

        while pause:
            # create a fresh screen
            redraw_window(pause)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        player.run = False
                        pause = False
                        audio_cfg.play_music(BLADE_RUNNER_PATH)
                        break
                    if event.key == pygame.K_m:
                        audio_cfg.toggle_mute()
                    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        audio_cfg.inc_volume(5)
                    if event.key == pygame.K_MINUS:
                        audio_cfg.dec_volume(5)
                    if event.key == pygame.K_p:
                        pygame.mouse.set_visible(False)
                        pause = False
                        break

        player.move(leftEnemy.x)

        # leftEnemy.change_color()
        # leftEnemy.draw(CANVAS)



        for enemy in enemies:

            if enemy.y > HEIGHT:
                EXP2_SOUND.play()
                enemy.kill()

            # enemy_ship_group.update()
            enemy.move(enemy_vel/1.5)
            enemy.move_lasers(laser_vel, player)


            if enemy.left:
                if 75 <= enemy.y <= 76 and not enemy.swapped:
                    enemy.change_color()
                    start_clock = time.time()
                    # clock.tick()
                    enemy.swapped = True

                if enemy.swapped and (time.time() - start_clock) >= 1:
                    enemy.change_color()
                    enemy.swapped = False

                    # enemy.swapped = False
            if not enemy.left:
                if enemy.y >= HEIGHT/2 - 100 and not enemy.swapped:

                    enemy.change_color()

                    enemy.swapped = True

                if enemy.swapped and (time.time() - start_clock) >= 1:
                    enemy.change_color()
                    enemy.swapped = False



            if random.randrange(0, 2 * FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.SCORE += 50
                if enemy.ship_type == 'boss':
                    if enemy.boss_max_health - 5 <= 0:
                        # note: this is not seen as game is paused as soon as boss health reaches zero
                        # should be fixed in future with a short delay in pausing
                        boss_crash = Explosion(player.x, player.y, size=100)
                        explosion_group.add(boss_crash)

                        enemies.remove(enemy)
                        enemy.boss_max_health = 100
                        player.health -= 100
                    else:
                        enemy.boss_max_health -= 5
                        player.health -= 100
                        # player death explosion
                        crash = Explosion(player.x, player.y)
                        explosion_group.add(crash)
                else:
                    player.health -= 10
                    crash = Explosion(enemy.x, enemy.y)
                    explosion_group.add(crash)
                    enemies.remove(enemy)
            elif enemy.y + enemy.get_height() / 2 > HEIGHT:
                # lives -= 1
                enemies.remove(enemy)



        player.move_lasers(-laser_vel, enemies)
