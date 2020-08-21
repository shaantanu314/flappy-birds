import pygame
import random
import math

pygame.init()
screen_height = 620
screen_width  = 500
fps=30
gameWindow = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
pygame.display.set_caption("flappy bird")
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

# BASE CHARACTERISTICS
baseImg = pygame.image.load('assets/sprites/base.png').convert_alpha()
backgroundImg = pygame.image.load('assets/sprites/background.png').convert_alpha()
base_height = baseImg.get_height()
base_width  = baseImg.get_width()

# PIPES
pipeGap = 120
max_shift = 250
pipe_speed = 8
downPipeImg = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
upPipeImg = pygame.transform.rotate(downPipeImg , 180)
pipe_height = downPipeImg.get_height()
pipe_width  = downPipeImg.get_width()
UP_PIPE = list()
DOWN_PIPE = []


# BIRD VARIABLES
bird_state = 0
bird_dir = 30
bird_x = screen_width/5
bird_y = screen_height/2
jump_velocity = -14
velocity_y = jump_velocity
acceleration_y = 1.6



def get_current_time():

    return pygame.time.get_ticks()


def blit_scene(gameWindow):
    global bird_state

    # blit background
    gameWindow.blit(backgroundImg , (0,0))

    

    # blit bird
    curr_bird = player[bird_state/2]
    curr_bird = pygame.transform.rotate(curr_bird , bird_dir)
    gameWindow.blit(curr_bird, (bird_x,bird_y))
    bird_state += 1
    bird_state %= 8
    
    # blit pipes
    for pipe in UP_PIPE:
        gameWindow.blit(upPipeImg , pipe)
    for pipe in DOWN_PIPE:
        gameWindow.blit(downPipeImg , pipe)

    #blit base
    gameWindow.blit(baseImg , (0,screen_height - base_height))
    gameWindow.blit(baseImg , (base_width,screen_height - base_height))

def get_newPipe():
    
    new_down_pipeY = screen_height-base_height-pipe_height + random.randint(0,max_shift)
    new_up_pipeY = new_down_pipeY - pipeGap - pipe_height

    print(new_down_pipeY)
    print(new_up_pipeY)
    return {'new_down_pipeY': new_down_pipeY , 'new_up_pipeY': new_up_pipeY}


def collideWall():
    pass

# Initiallize the pipes so that we have two pipes at the start
new_pipes = get_newPipe()
UP_PIPE.append([screen_width/2,new_pipes['new_up_pipeY']])
DOWN_PIPE.append([screen_width/2,new_pipes['new_down_pipeY']])
new_pipes = get_newPipe()
UP_PIPE.append([screen_width,new_pipes['new_up_pipeY']])
DOWN_PIPE.append([screen_width,new_pipes['new_down_pipeY']])





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
    blit_scene(gameWindow)
    bird_dir = 30 - 0.3*velocity_y*(velocity_y - (jump_velocity))
    bird_y += velocity_y
    if velocity_y < 15:
        velocity_y += acceleration_y  
    

    # PIPE MOTION :
    for pipe in UP_PIPE:
        pipe[0] -= pipe_speed
    for pipe in DOWN_PIPE:
        pipe[0] -= pipe_speed
        
    if UP_PIPE[0][0] +  pipe_width <0:
        new_pipes = get_newPipe()
        UP_PIPE.append([screen_width,new_pipes['new_up_pipeY']])
        DOWN_PIPE.append([screen_width,new_pipes['new_down_pipeY']])
        UP_PIPE.pop(0)
        DOWN_PIPE.pop(0)


    # COLLISION DETECTION
    if bird_y > screen_height - base_height:
        exit_game = True
    
    if collideWall():
        exit_game = True

    pygame.display.update()

pygame.quit()
quit()