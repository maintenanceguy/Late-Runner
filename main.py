import pygame, sys, random
from pygame.locals import *

# Scoring timer method
def point_display():
    real_time_score = int(pygame.time.get_ticks() /1000) - init_point_score
    point_surface = font.render(f"Point: {real_time_score}", False, "black")
    display.blit(point_surface, (35,20))
    return real_time_score

#Obstacle (enemy) movement method
def obstacle_movement(obstacle_list, frame_1, frame_2, real_time_score):
    if obstacle_list:
        for obstacle_box in obstacle_list:
            obstacle_speed = 6 + (real_time_score // 10)
            obstacle_box.left -= obstacle_speed
            
            if obstacle_box.bottom == 300:
                display.blit(frame_1, obstacle_box)
            else:
                display.blit(frame_2, obstacle_box)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.left > -100]

        return obstacle_list
    else: return []

#Collison method
def collison(player, obstacles):
    if obstacles:
        for obstacle_box in obstacles:
            if player.colliderect(obstacle_box):
                return False
    return True

#Player animation
def player_animation():

    global player, player_position_index

    if player_box.bottom < 300:
        player = player_jumping

    else:
        player_position_index += 0.3
        if player_position_index >= len(player_walking):
            player_position_index = 0

        player = player_walking[int(player_position_index)]

#Game init variable
start = True
game_state = False
init_point_score = 0
final_score = 0
player_gravity = 0
high_score = 0
pygame.init()

#Display variables
screen_height = 400
screen_width = 800
game_name = "Late Runner"

#Screen
display = pygame.display.set_mode((screen_width,screen_height))
title = pygame.display.set_caption(game_name)
FPS = pygame.time.Clock()

#text
font = pygame.font.Font("Fonts/PixelifySans-SemiBold.ttf", 25)

#background surface
sky = pygame.image.load('Images/sky.png')
ground = pygame.image.load("Images/ground.png") 

#sound
game_sound = pygame.mixer.Sound("audio/music.wav")
game_sound.play(loops= -1)
game_sound.set_volume(0.2)

#Player sound
player_jump_sound = pygame.mixer.Sound("audio/jump.mp3")
player_jump_sound.set_volume(0.1)

#obstacles:
obstacle_box_list = []

#snail frames (Enemy_1)
enemy_1_frame_1 = pygame.image.load("Images/snail1.png")
enemy_1_frame_2 = pygame.image.load("Images/snail2.png")
enemy_1_frames = [enemy_1_frame_1, enemy_1_frame_2]

#snail surface & index
enemy_1_position_index = 0
enemy_1 = enemy_1_frames[enemy_1_position_index]
enemy_1_box = enemy_1.get_rect(bottomright = (600,300))

#fly frames (Enemy_2)
enemy_2_frame_1 = pygame.image.load("Images/fly1.png")
enemy_2_frame_2 = pygame.image.load("Images/fly2.png")
enemy_2_frames = [enemy_2_frame_1, enemy_2_frame_2]

#fly surface & index
enemy_2_position_index = 0
enemy_2 = enemy_2_frames[enemy_2_position_index] 

#player frames (walking, jumping)
player_walk_1 = pygame.image.load("Images/player_walk_1.png")
player_walk_2 =pygame.image.load("Images/player_walk_2.png")
player_walking = [player_walk_1,player_walk_2]
player_jumping = pygame.image.load("Images/jump.png")

#player surface & index
player_position_index = 0
player = player_walking[player_position_index]
player_box = player.get_rect(bottomleft = (30,300))


#intro screen
player_init_position = pygame.image.load("Images/player_stand.png")
player_init_position_box = player_init_position.get_rect(center = (400,200))
intro_name = font.render("Late Runner", False, (248, 222, 34))
how_to_start = font.render("Press space to start", False, (248, 222, 34))

#Enemy spawn Timer system
obstacle_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_spawn_timer, 2500)

enemy_1_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_1_animation_timer, 500)

enemy_2_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy_2_animation_timer, 200)

#Game logic
while start:

    #display window
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            start = False
            pygame.quit()
            sys.exit()

        #Restart game state
        if game_state:

        #Input mechanics & Player gravity
            if events.type == pygame.KEYDOWN:
                if events.key ==pygame.K_SPACE:
                    if player_box.bottom >= 300:
                        player_gravity = -22
                        player_jump_sound.play()
        
        #Restart mechanics            
        else:
            if events.type == pygame.KEYDOWN:
                if events.key == K_SPACE:
                    game_state = True
                    init_point_score = int(pygame.time.get_ticks() /1000)

        #obstacle spawning logic
        if events.type == obstacle_spawn_timer:
            if game_state:
                if random.randint(0,1):
                    obstacle_box_list.append(enemy_1.get_rect(bottomright = (random.randint(1100, 1400),300)))
                else:
                    obstacle_box_list.append(enemy_2.get_rect(bottomright = (random.randint(900, 1100),210)))

        #Enemy Animation timer logic
        if game_state:
            if events.type == enemy_1_animation_timer:
                if enemy_1_position_index == 0:
                    enemy_1_position_index = 1
                else:
                    enemy_1_position_index = 0
                enemy_1 = enemy_1_frames[enemy_1_position_index]
            
            if events.type == enemy_2_animation_timer:
                if enemy_2_position_index == 0:
                    enemy_2_position_index = 1
                else:
                    enemy_2_position_index = 0
                enemy_2 = enemy_2_frames[enemy_2_position_index]

    #Game state & Game over mechanics
    if game_state:

        #Display surfaces
        display.blit(sky, (0,0))
        display.blit(ground, (0,300))
        final_score = point_display()

        #Player gravity & Jumping mechanics
        player_gravity += 1
        player_box.y += player_gravity

        #player floor mechanics on the ground
        if player_box.bottom > 300: 
            player_box.bottom = 300
        player_animation()
        display.blit(player, player_box)

        #Enemy spawning logic
        obstacle_box_list = obstacle_movement(obstacle_box_list, enemy_1, enemy_2, final_score)

        #Collison system & failed game state
        game_state = collison(player_box, obstacle_box_list)

    else:
        display.fill((64, 96, 147))
        
        display.blit(player_init_position, player_init_position_box)
        display.blit(intro_name, (330, 80))
        obstacle_box_list.clear()
        player_box.bottomleft = (80,300)
        player_gravity = 0

        if final_score > high_score:
            high_score = final_score
        game_over_message = font.render(f"Your score is: {final_score}", False, (248, 222, 34))

        #Game over Screen       
        if final_score == 0:
            display.blit(how_to_start, (280, 280))
        else:
            display.blit(game_over_message, (290, 290))
            high_score_message = font.render(f"Best: {high_score}", False, (248, 222, 34))
            display.blit(high_score_message, (350, 250))
        

    pygame.display.update()
    FPS.tick(60)