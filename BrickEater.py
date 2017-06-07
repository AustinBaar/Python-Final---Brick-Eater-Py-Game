import pygame
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

display_width = 600
display_height = 400

gameDisplay = pygame.display.set_mode((display_width,display_height)) 
pygame.display.set_caption('BrickEater')

clock = pygame.time.Clock()

block_size = 10
FPS= 15

smallfont = pygame.font.SysFont("comicsansms", 12)
medfont = pygame.font.SysFont("comicsansms", 20)
largefont = pygame.font.SysFont("comicsansms", 30)

def pause():

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Paused",
                          black,
                          -100,
                          "large")

        message_to_screen("Press A to continue or Q to quit.",
                         red,
                         25,
                         "medium")
        
        pygame.display.update()
        clock.tick(5)
        


def score(score):
    text = medfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])

def game_intro():

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quite()

        
        gameDisplay.fill(white)
        message_to_screen("Welcome to BrickEater",
                          green,
                          -120,
                          "large")
        
        message_to_screen("The objective of the game is to eat red bricks and grow!",
                          blue,
                          -30,
                          "small")
        
        message_to_screen("Use keys W, A, S, D, to move your black brick around",
                          black,
                          10,
                          "small")
        
        message_to_screen("Press the P key to pause the game",
                          black,
                          30,
                          "small")
        
        message_to_screen("If you run into yourself or the edges of play, you die",
                          red,
                          70,
                          "small")
        
        message_to_screen("Press A to Play or Q to quit",
                          red,
                          120,
                          "medium")
        

        
        pygame.display.update()
        clock.tick(5)
        

def snake(block_size, snakelist):
    for XnY in snakelist:
        pygame.draw.rect(gameDisplay, black, [XnY[0],XnY[1],block_size,block_size]) 
    
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    
    return textSurface, textSurface.get_rect()
    

def message_to_screen(msg,color, y_displace=0, size = "medium"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randPowerUpX = round(random.randrange(0, display_width-block_size)/10.0)*10.0
    randPowerUpY = round(random.randrange(0, display_height-block_size)/10.0)*10.0
    
    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over man, Game over.", red, -50, size="large")
            message_to_screen("Press A to play again or Q to quit",black, 50, size="medium") 
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_a:
                        gameLoop() 

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_d:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_w:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_s:
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True 
            
        
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    lead_x_change = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    lead_y_change = 0
                    

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, green, [randPowerUpX, randPowerUpY, block_size,block_size]) 

        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        
        snake(block_size, snakeList)

        score(snakeLength-1)

        
        pygame.display.update()

        if lead_x == randPowerUpX and lead_y == randPowerUpY:
            randPowerUpX = round(random.randrange(0, display_width-block_size)/10.0)*10.0
            randPowerUpY = round(random.randrange(0, display_height-block_size)/10.0)*10.0
            snakeLength += 1
    

        clock.tick(FPS)

    pygame.quit()
    quit()
    
game_intro()
gameLoop()
