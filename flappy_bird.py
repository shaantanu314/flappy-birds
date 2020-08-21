import pygame
import random
import math

pygame.init()
screen_height = 620
screen_width  = 500
fps=30
score = 0
gameWindow = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
pygame.display.set_caption("flappy bird")
pygame.display.update()

exit_game = False
start_game = False
game_over = False
font = pygame.font.SysFont(None, 30, bold=False, italic=False)

# ASSETS
player = [
    pygame.image.load('assets/sprites/bird_down.png').convert_alpha(),
    pygame.image.load('assets/sprites/bird_mid.png').convert_alpha(),
    pygame.image.load('assets/sprites/bird_up.png').convert_alpha(),
    pygame.image.load('assets/sprites/bird_mid.png').convert_alpha(),
]
SOUND = {
    'point': pygame.mixer.Sound('assets/audio/point.wav'),
    'wing': pygame.mixer.Sound('assets/audio/wing.wav'),
    'hit': pygame.mixer.Sound('assets/audio/hit.wav'),
    'die': pygame.mixer.Sound('assets/audio/die.wav'),
}
messageImg = pygame.image.load('assets/sprites/message.png').convert_alpha()

scoreImg = [
    pygame.image.load('assets/sprites/0.png').convert_alpha(),
    pygame.image.load('assets/sprites/1.png').convert_alpha(),
    pygame.image.load('assets/sprites/2.png').convert_alpha(),
    pygame.image.load('assets/sprites/3.png').convert_alpha(),
    pygame.image.load('assets/sprites/4.png').convert_alpha(),
    pygame.image.load('assets/sprites/5.png').convert_alpha(),
    pygame.image.load('assets/sprites/6.png').convert_alpha(),
    pygame.image.load('assets/sprites/7.png').convert_alpha(),
    pygame.image.load('assets/sprites/8.png').convert_alpha(),
    pygame.image.load('assets/sprites/9.png').convert_alpha(),
]
digit_width = scoreImg[0].get_width()

# BASE CHARACTERISTICS
baseImg = pygame.image.load('assets/sprites/base.png').convert_alpha()
backgroundImg = pygame.image.load('assets/sprites/background.png').convert_alpha()
base_height = baseImg.get_height()
base_width  = baseImg.get_width()

# PIPES
pipeGap = 160
max_shift = 250
pipe_speed = 7
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
wing_sound = 0



def get_current_time():

    return pygame.time.get_ticks()


def blit_scene(gameWindow):
    global bird_state
    global wing_sound

    # blit background
    gameWindow.blit(backgroundImg , (0,0))

    # blit pipes
    for pipe in UP_PIPE:
        gameWindow.blit(upPipeImg , pipe)
    for pipe in DOWN_PIPE:
        gameWindow.blit(downPipeImg , pipe)


    # blit bird
    curr_bird = player[bird_state/2]
    curr_bird = pygame.transform.rotate(curr_bird , bird_dir)
    if start_game:
        gameWindow.blit(curr_bird, (bird_x,bird_y))
    bird_state += 1
    if bird_state == 8:
        if wing_sound and start_game:
            SOUND['wing'].play()
            wing_sound = 0
        else :
            wing_sound = 1
    bird_state %= 8
    

    #blit base
    gameWindow.blit(baseImg , (0,screen_height - base_height))
    gameWindow.blit(baseImg , (base_width,screen_height - base_height))

def get_newPipe():
    
    new_down_pipeY = screen_height-base_height-pipe_height + random.randint(0,max_shift)
    new_up_pipeY = new_down_pipeY - pipeGap - pipe_height

    return {'new_down_pipeY': new_down_pipeY , 'new_up_pipeY': new_up_pipeY}


def collideWall():
    global exit_game

    for pipe in UP_PIPE:
        if (bird_x + player[0].get_width())>pipe[0] and (bird_x + player[0].get_width())<pipe[0]+pipe_width and bird_y < (pipe[1] + pipe_height):
            exit_game = True
    for pipe in DOWN_PIPE:
        if (bird_x + player[0].get_width())>pipe[0] and (bird_x + player[0].get_width())<pipe[0]+pipe_width and bird_y > (pipe[1] ):
            exit_game = True


def dispScore(gameWindow , score):
    curr_x = screen_width/2 + digit_width
    s = score
    while s!=0:
        gameWindow.blit(scoreImg[s%10] , [curr_x,screen_height/4])
        curr_x -= digit_width
        s/=10




# Initiallize the pipes so that we have two pipes at the start
new_pipes = get_newPipe()
UP_PIPE.append([screen_width,new_pipes['new_up_pipeY']])
DOWN_PIPE.append([screen_width,new_pipes['new_down_pipeY']])
new_pipes = get_newPipe()
UP_PIPE.append([3*screen_width/2,new_pipes['new_up_pipeY']])
DOWN_PIPE.append([3*screen_width/2,new_pipes['new_down_pipeY']])

def Start_Screen(gameWindow):
    global exit_game
    global start_game
    while not start_game:
        clock.tick(fps)
        blit_scene(gameWindow)
        gameWindow.blit(messageImg,[50,50])
        # gameWindow.blit(backgroundImg,(0,0))
        screen_text = font.render("PRESS SPACE TO PLAY", True ,(0,0,0))
        gameWindow.blit(screen_text , [screen_width/6-30,screen_height/3])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    start_game = True
            



if __name__ == "__main__":
    Start_Screen(gameWindow)
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


        # SCORE MANAGEMENT
        if  bird_x - UP_PIPE[0][0] < 5 and bird_x - UP_PIPE[0][0] > -4 :
            score += 1
            SOUND['point'].play()

        
        dispScore(gameWindow,score)

        # COLLISION DETECTION
        if bird_y > screen_height - base_height:
            SOUND['die'].play()
            exit_game = True
        
        if collideWall():
            SOUND['die'].play()
            exit_game = True

        

        pygame.display.update()

    pygame.quit()   
    quit()