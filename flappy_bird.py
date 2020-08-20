import pygame
import random
import math

pygame.init()
screen_height = 700
screen_width  = 500
fps=30
gameWindow = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
pygame.display.set_caption("snake game")
pygame.display.update()

exit_game = False
game_over = False
font = pygame.font.SysFont(None, 50, bold=False, italic=False)

# ASSETS
player = [
    pygame.image.load('assets/sprites/bird_down.png').convert_alpha(),
    pygame.image.load('assets/sprites/bird_mid.png').convert_alpha(),
    pygame.image.load('assets/sprites/bird_up.png').convert_alpha(),
    pygame.image.load('assets/sprites/bird_mid.png').convert_alpha(),
]
baseImg = pygame.image.load('assets/sprites/base.png').convert_alpha()
backgroundImg = pygame.image.load('assets/sprites/background.png').convert_alpha()


# BASE CHARACTERISTICS
base_height = baseImg.get_height()
base_width  = baseImg.get_width()



# BIRD VARIABLES
bird_state = 0
bird_dir = 30
bird_x = screen_width/5
bird_y = screen_height/2
jump_velocity = -15
velocity_y = jump_velocity
acceleration_y = 1.5



def get_current_time():

    return pygame.time.get_ticks()


def blit_bird(gameWindow):
    global bird_state

    # blit base and background
    gameWindow.blit(backgroundImg , (0,0))
    gameWindow.blit(baseImg , (0,screen_height - base_height))
    gameWindow.blit(baseImg , (base_width,screen_height - base_height))
    

    # blit bird
    curr_bird = player[bird_state/2]
    curr_bird = pygame.transform.rotate(curr_bird , bird_dir)
    gameWindow.blit(curr_bird, (bird_x,bird_y))
    bird_state += 1
    bird_state %= 8


while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                velocity_y = jump_velocity
        
    clock.tick(fps)

    gameWindow.fill((0,0,0))
    
    
    # BIRD KINEMATICS:
    blit_bird(gameWindow)
    bird_dir = 30 - 0.3*velocity_y*(velocity_y - (jump_velocity))
    bird_y += velocity_y
    if velocity_y < 15:
        velocity_y += acceleration_y
    
    if bird_y > screen_height - base_height:
        exit_game = True



    pygame.display.update()

pygame.quit()
quit()