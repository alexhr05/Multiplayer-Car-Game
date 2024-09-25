import sys

import pygame
import random
import math
from pygame.locals import *
from pygame import mixer


pygame.init()

width_screen = 600
height_screen = 600

#my_font = pygame.font.SysFont("monospace", 30)

screen = pygame.display.set_mode((width_screen, height_screen))
pygame.display.set_caption("F1 car")

bg = pygame.image.load("image/roadImage.jpg")

player_1 = pygame.image.load("image/car_1.jpg")
width_player_1_car = 40
height_player_1_car = 100
player_1 = pygame.transform.scale(player_1, (width_player_1_car, height_player_1_car))

player_2 = pygame.image.load("image/car_7.png")
width_player_2_car = 40
height_player_2_car = 100
player_2 = pygame.transform.scale(player_2, (width_player_2_car, height_player_2_car))

obs_pic = ""
font_name = pygame.font.match_font("arial")

FPS = 60
player_vel_1 = 10
clock = pygame.time.Clock()
x_pl_1 = 200
y_pl_1 = 400

player_vel_2 = 10
x_pl_2 = 400
y_pl_2 = 400

obs_speed = 3
obs_width = 40
obs_height = 100

max_index_obs = int(20)
obs_x = [0]*max_index_obs
obs_y = [0]*max_index_obs
obs_visible = []
obs_fileName = ["","","","",""]
obs_type = [0,0,0,0,0,0,0]


background_speed = int(2.5)
current_score_pl_1 = int(0)
current_score_pl_2 = int(0)
high_score_pl_1 = int(7)
high_score_pl_2 = int(8)
index_of_array = int(0)

game_over_player_1 = False
game_over_player_2 = False

mixer.music.load('music/backgroundMusic.mp3')

def redraw_window(j,x_pl_1,y_pl_1,x_pl_2,y_pl_2, ticks):
    #screen.fill((0,0,0))
    screen.blit(bg, (0, j))
    screen.blit(bg, (0, j - height_screen ))
    screen.blit(player_1, (x_pl_1, y_pl_1))
    screen.blit(player_2, (x_pl_2, y_pl_2))

    for i in range(0,max_index_obs):
        if obs_visible[i] == True:
            obs_pic = pygame.image.load(obs_fileName[i])
            #obs_pic = pygame.transform.scale(obs_fileName[i], (obs_width, obs_height))
            obs_pic = pygame.transform.scale(obs_pic , (obs_width, obs_height))
            screen.blit( obs_pic, (obs_x[i], obs_y[i]))
            draw_text(screen, i, 18, obs_x[i]+10, obs_y[i]+10)
            obs_y[i] += obs_speed
            if (obs_y[i] >= height_screen - 0 and obs_y[i] <= (height_screen + 200)):
                obs_visible[i] = False

    draw_text(screen, "Time:", 18, width_screen - 570, height_screen - 300)
    draw_text(screen, round(ticks / 10), 18, width_screen - 540, height_screen - 300)

    draw_text(screen, "Score player 1:", 18, width_screen - 540, height_screen - 580)
    draw_text(screen, str(current_score_pl_1), 18, width_screen - 480, height_screen - 580)

    draw_text(screen, "Score player 2:", 18, width_screen - 80, height_screen - 580)
    draw_text(screen, str(current_score_pl_2), 18, width_screen - 30, height_screen - 580)

    pygame.display.update()

def new_obstacles ():
    # Search for free index
    i = int(0)
    while obs_visible[i] != False and i < max_index_obs:
        i+=1
    first_free_index = i
    index_of_array = i

    print("first_free_index=",first_free_index)
    print("NEW CAR+++++++++++++++++++++++++++++++++++++++++++++++NEW CAR")

    obs_x[first_free_index] = random.randint(0,width_screen - 100)
    obs_y[first_free_index] = -(obs_height)
    obs_visible[first_free_index] = True
    obs_type[first_free_index] = random.randint(1,5)
    obs_type[first_free_index] = random.randint(1,5)

    if obs_type[first_free_index] == 1:
        obs_fileName[first_free_index] = "image/car_1.jpg"
    elif obs_type[first_free_index] == 2:
        obs_fileName[first_free_index] = "image/enemyCar.jfif"
    elif obs_type[first_free_index] == 3:
        obs_fileName[first_free_index] = "image/diamond.jfif"
    elif obs_type[first_free_index] == 4:
        obs_fileName[first_free_index] = "image/diamond_2.jfif"
    elif obs_type[first_free_index] == 5:
        obs_fileName[first_free_index] = "image/lamborghini.png"
    pygame.display.update()

def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(str(text), True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
    #pygame.display.update()


def crash(x_pl_1,y_pl_1,x_pl_2,y_pl_2):
    # check conditions
    global current_score_pl_1,current_score_pl_2
    global game_over_player_1, game_over_player_2

    for i in range(0, max_index_obs):

        if obs_visible[i] == True:

            if (y_pl_1 + height_player_1_car) > obs_y[i] and y_pl_1 < (obs_y[i] + obs_height):
                if ((x_pl_1 > obs_x[i] and x_pl_1 < (obs_x[i] + obs_width)) or ((x_pl_1 + width_player_1_car) > obs_x[i]  and (x_pl_1 + width_player_1_car) < (obs_x[i] + obs_width))):

                    if obs_type[i] == 1:   # crash with enemy
                        game_over_player_1 = True
                        game_over(game_over_player_1, game_over_player_2)
                    elif obs_type[i] == 2:  # crash with enemy
                        game_over_player_1 = True
                        game_over(game_over_player_1, game_over_player_2)
                    elif obs_type[i] == 3: # get diamond
                        current_score_pl_1 += 1
                        obs_visible[i] = False
                    elif obs_type[i] == 4:  # get diamond 2
                        current_score_pl_1 += 1
                        obs_visible[i] = False
                    elif obs_type[i] == 5:  # crash with enemy
                        game_over_player_1 = True
                        game_over(game_over_player_1, game_over_player_2)
                        
            if (y_pl_2 + height_player_2_car) > obs_y[i] and y_pl_2 < (obs_y[i] + obs_height):

                if ((x_pl_2 > obs_x[i] and x_pl_2 < (obs_x[i] + obs_width)) or ((x_pl_2 + width_player_2_car) > obs_x[i]  and (x_pl_2 + width_player_2_car) < (obs_x[i] + obs_width))):

                    if obs_type[i] == 1:   # crash with enemy
                        game_over_player_2 = True
                        game_over(game_over_player_1, game_over_player_2)
                    elif obs_type[i] == 2:  # crash with enemy
                        game_over_player_2 = True
                        game_over(game_over_player_1, game_over_player_2)
                    elif obs_type[i] == 3: # get diamond
                        current_score_pl_2 += 1
                        obs_visible[i] = False
                    elif obs_type[i] == 4:  # get diamond
                        current_score_pl_2 += 1
                        obs_visible[i] = False
                    elif obs_type[i] == 5:  # crash with enemy
                        game_over_player_2 = True
                        game_over(game_over_player_1, game_over_player_2)


def show_go_screen():
    with open("score.txt", "r") as file:
        global high_score_pl_1
        global high_score_pl_2
        content = file.readlines()
        high_score_pl_1 = int(content[5])
        high_score_pl_2 = int(content[7])

    for i in range(0, max_index_obs):
        obs_visible.append(False)

    draw_text(screen, "Play survival cars!", 68, width_screen / 2, height_screen / 6)
    draw_text(screen, "Press any key to begin again", 24, width_screen / 2, height_screen - 100)

    mainScreenImage = pygame.image.load("image/mainScreenImage.jpg")
    mainScreenImage = pygame.transform.scale(mainScreenImage, (200, 200))
    screen.blit(mainScreenImage, (width_screen-400, height_screen-400))
    pygame.display.flip()
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                 waiting = False
                 mixer.music.play(-1)

def game_over(game_over_player_1, game_over_player_2):
    mixer.music.stop()

    screen.fill((0, 0,0))

    winImage = pygame.image.load("image/winImage.jpg")
    winImage = pygame.transform.scale(winImage, (200, 200))

    loseImage = pygame.image.load("image/loseImage.jpg")
    loseImage = pygame.transform.scale(loseImage, (200, 200))
    if game_over_player_1 == True:
        draw_text(screen, "Player 1 LOST", 30, width_screen - 440, height_screen - 500)
        screen.blit(loseImage, (width_screen - 550, height_screen - 400))
    else:
        draw_text(screen, "Player 1 WIN", 30, width_screen - 440, height_screen - 500)
        screen.blit(winImage, (width_screen - 550, height_screen - 400))

    if  game_over_player_2 == True:
        draw_text(screen, "Player 2 LOST", 30, width_screen - 180, height_screen - 500)
        screen.blit(loseImage, (width_screen - 250, height_screen - 400))
    else:
        draw_text(screen, "Player 2 WIN", 30, width_screen - 180, height_screen - 500)
        screen.blit(winImage, (width_screen - 250, height_screen - 400))

    draw_text(screen, "Press any key to exit", 24, width_screen / 2, height_screen - 100)

    pygame.display.flip()
    pygame.display.update()

    with open("score.txt", "w") as file:
        file.write("Current score player 1:" + "\n" + str(current_score_pl_1) + "\n")
        file.write("Current score player 2:" + "\n" + str(current_score_pl_2) + "\n")
        if int(high_score_pl_1) < current_score_pl_1:
            file.write("High score player 1:" + "\n" + str(current_score_pl_1) + "\n")
        else:
            file.write("High score player 1:" + "\n" + str(high_score_pl_1) + "\n")
        if int(high_score_pl_2) < current_score_pl_2:
            file.write("High score player 2:" + "\n" + str(current_score_pl_2) + "\n")
        else:
            file.write("High score player 2:" + "\n" + str(high_score_pl_2) + "\n")

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
                sys.exit()

def main(x_pl_1,y_pl_1,x_pl_2,y_pl_2,game_over_player_1,game_over_player_2):

    j = int(0)

# start of init
    show_go_screen()
# end of init
    running = True
    spawn_interval  = 30
    start_ticks = round(pygame.time.get_ticks()/100)
    while running:

        ticks = round(pygame.time.get_ticks()/100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #running = False
                sys.exit()

        redraw_window(j,x_pl_1,y_pl_1,x_pl_2,y_pl_2,ticks)

        if ticks-start_ticks > spawn_interval:
            new_obstacles()
            start_ticks = ticks

        if y_pl_1 > height_screen:
            game_over_player_1 = True
            game_over(game_over_player_1, game_over_player_2)
        if y_pl_2 > height_screen:
            game_over_player_2 = True
            game_over(game_over_player_1, game_over_player_2)



        if j == width_screen:
            screen.blit(bg, (0, j - height_screen ))

            j = 0
        j += 2
        y_pl_1 += background_speed
        y_pl_2 += background_speed
        clock.tick(FPS)

        key = pygame.key.get_pressed()

        #player 1 key move
        if key[pygame.K_a] and x_pl_1 > 0:
            x_pl_1 -= player_vel_1
        if key[pygame.K_d] and x_pl_1 < width_screen - width_player_1_car:
            x_pl_1 += player_vel_1
        if key[pygame.K_w] and y_pl_1 > 0:
            y_pl_1 -= player_vel_1
        if key[pygame.K_s] and y_pl_1  < height_screen:
            y_pl_1 += player_vel_1

        # player 2 key move
        if key[pygame.K_LEFT] and x_pl_2 > 0:
            x_pl_2 -= player_vel_2
        if key[pygame.K_RIGHT] and x_pl_2 + width_player_2_car < width_screen:
            x_pl_2 += player_vel_2
        if key[pygame.K_UP] and y_pl_2 > 0:
            y_pl_2 -= player_vel_2
        if key[pygame.K_DOWN] and y_pl_2:
            y_pl_2 += player_vel_2

        crash(x_pl_1,y_pl_1, x_pl_2,y_pl_2)

        if (current_score_pl_1+current_score_pl_2) <= 4:
            spawn_interval = 30
        elif (current_score_pl_1 + current_score_pl_2) <= 6:
            spawn_interval = 25
        elif (current_score_pl_1 + current_score_pl_2) <= 8:
            spawn_interval = 18
        elif (current_score_pl_1 + current_score_pl_2) <= 10:
            spawn_interval = 12
        else:
            spawn_interval = 8



    pygame.quit()

main(x_pl_1,y_pl_1,x_pl_2,y_pl_2,game_over_player_1,game_over_player_2)