import random
import sys
import pygame
from pygame.locals import *

from pygame import mixer

pygame.mixer.init()

# Defining Colors

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255,255,51)
green = (51,255,51)

# Global Variables for game 

FPS = 50
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
GROUNDY = SCREEN_HEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER ='gallery/sprites/bird.png'
BACKGROUND ='gallery/sprites/bg.png'
PIPE ='gallery/sprites/pipe.png'


def game_over() :
    SCREEN.fill(white)
    SCREEN.blit(GAME_SPRITES['messege'],(0,0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            exit_game = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                mainGame()



def welcomeScreen():
    """
    shows welcome screen
    """

    playerx = int(SCREEN_WIDTH/5)

    playery = int((SCREEN_HEIGHT - GAME_SPRITES['player'].get_height())/2)

    messegex = int((SCREEN_WIDTH - GAME_SPRITES['messege'].get_width()))

    messegey = int(SCREEN_HEIGHT*0.01)

    basex = 0

    while True :

        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) :
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE  or event.key == K_UP) :
                return

            else :
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['messege'],(messegex,messegey))
                

                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():

    score  = 0
    playerx = int(SCREEN_WIDTH/5)
    playery = int(SCREEN_WIDTH/2)
    basex = 0

    # Creating 2 pipes for blitting on the screen

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # My list of upper pipes 

    upperPipes = [
        {'x': SCREEN_WIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREEN_WIDTH+200 + (SCREEN_WIDTH/2), 'y': newPipe2[0]['y']},

    ]

    # My list of lower pipes

    lowerPipes = [
        {'x': SCREEN_WIDTH+200, 'y': newPipe1[1]['y']},
        {'x': SCREEN_WIDTH+200 + (SCREEN_WIDTH/2), 'y': newPipe2[1]['y']},

    ]

    pipeVelocityX = -4
    playerVelocity_Y = -9
    playerMaxVelocity_Y = 10
    playerMinVelocity_Y = -8
    playerAccelerationY = 1

    playerFlapAccv = -8  # Velocity while flapping
    playerFlapeed  = False # It is true only when the bird is flapping


    while True :

        for event in pygame.event.get() :

            if event.type == QUIT or (event.type ==KEYDOWN and event.key ==K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key ==K_SPACE or event.key == K_UP):

                if playery > 0 :
                    playerVelocity_Y = playerFlapAccv
                    playerFlapeed = True
                    GAME_SOUNDS['wing'].play()

        
        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes) # This function will return true if the player is crashed


        if crashTest :
            return


        # Check for score

        playerMidPos = (playerx + GAME_SPRITES['player'].get_width())/2

        for pipe in upperPipes:
            pipMidPos = (pipe['x'] + GAME_SPRITES['pipe'][0].get_width())/2

            if pipMidPos <= playerMidPos < pipMidPos+4 :

                score = score + 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()


        if playerVelocity_Y < playerMaxVelocity_Y and not playerFlapeed :
            playerVelocity_Y = playerVelocity_Y + playerAccelerationY

          
        if playerFlapeed :
            playerFlapeed = False


        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery +  min(playerVelocity_Y , GROUNDY - playery - playerHeight)


        # MOVES PIPE TO THE LEFT

        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):

            upperPipe['x'] = upperPipe['x']  + pipeVelocityX
            lowerPipe['x'] = lowerPipe['x'] + pipeVelocityX
            

        # Add a new pipe whwn first pipe is about to cross the leftmost part of the screen

        if 0<upperPipes[0]['x']<5 :

            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


        # If the pipe is out of the screen remove it

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():

            upperPipes.pop(0)
            lowerPipes.pop(0)


        # Lets blit our srites now

        SCREEN.blit(GAME_SPRITES['background'],(0,0))

        for upperPipe , lowerPipe in zip(upperPipes , lowerPipes) :
            
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'] , (basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        # For blitting score

        myDigits = [int(x) for x  in list(str(score))]

        width = 0

        for digit in myDigits :

            width += GAME_SPRITES['numbers'][digit].get_width()

            Xoffset = (SCREEN_WIDTH - width)/2


        for digit in myDigits :

            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset , SCREEN_HEIGHT*0.12))

            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def  isCollide(playerx,playery,upperPipes,lowerPipes):

    if playery > GROUNDY -25 or playery < 0 :

        GAME_SOUNDS['hit'].play()

        game_over()

        return True


    for pipe in upperPipes :

        pipeHeight = GAME_SPRITES['pipe'][0].get_height()

        if (playery < pipeHeight + pipe['y'] and  abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):

            GAME_SOUNDS['hit'].play()

            game_over()

            return True

        
    for pipe  in lowerPipes :

        if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):

            GAME_SOUNDS['hit'].play()

            game_over()

            return True

        


    return False

           
def getRandomPipe():

    """
    Generating position of 2 pipes (one bottom straight and upper rotated) for blitting on
    the screen
    """

    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT/3
    y2 = offset + random.randrange(int(SCREEN_HEIGHT - GAME_SPRITES['base'].get_height()-(1.2*offset)))
    pipeX = SCREEN_WIDTH + 10
    y1 = pipeHeight - y2 + offset

    pipe = [

        {'x': pipeX,'y': -y1}, #upper pipe
        {'x': pipeX,'y': y2} #lower pipe
    ]

    return pipe 


if __name__ == "__main__":  
    
    # The main starting point of our game
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird with Ovi')

    GAME_SPRITES['numbers'] = (

        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['messege'] = pygame.image.load('gallery/sprites/messege.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (

        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()        
    )


    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True :
        welcomeScreen()
        mainGame()




