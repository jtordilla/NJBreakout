import pygame as pg
from pygame.locals import *
from pygamelib import *
import pygame.gfxdraw

pg.init()

#set screen and window 
screenWidth = 1200
screenHeight = 700
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption('NjBreakout')

#game loop
clock = pg.time.Clock()
running = True

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (179, 217, 255)
background = BLUE

#paddle variables
paddleLength = 200
paddleHeight = 30
paddleColor = WHITE
paddleX = screenWidth/2 - paddleLength/2
paddleY = screenHeight - (paddleHeight*2)
paddleVel = 15
paddleImage = pg.image.load('paddle.png').convert()

#ball variables
ballSize = 40
ballColor = WHITE
ballX = screenWidth/3
ballY = screenHeight/2
ballVelX = 15
ballVelY = 15
#erase default black background
ballImage = pg.image.load('ball.png').convert_alpha()

#brick variables
brickLength = 200
brickHeight = 30
brickColor = BLACK
brickImage = pg.image.load('brick.png').convert()
brickCoords = [[55, 20], [55, 60], [55, 100], [55, 140], [55, 180],
               [275, 20], [275, 60], [275, 100], [275, 140], [275, 180],
               [495, 20], [495, 60], [495, 100], [495, 140], [495, 180],
               [715, 20], [715, 60], [715, 100], [715, 140], [715, 180],
               [935, 20], [935, 60], [935, 100], [935, 140], [935, 180]]

#paddle class
class Paddle():
    def __init__(self):
        self.length = paddleLength
        self.height = paddleHeight
        self.color = paddleColor
        self.x = paddleX
        self.y = paddleY
        self.vel = paddleVel

    #blit a rect from paddle image and set coords to the paddle 
    def draw(self):
        rect = paddleImage.get_rect()
        rect.x = self.x
        rect.y = self.y
        rect.w = self.length
        rect.h = self.height
        screen.blit(paddleImage, rect)

        '''
        pg.draw.rect(screen, self.color, (self.x, self.y, self.length,
                                          self.height))'''

    def update(self):
        key = pg.key.get_pressed()
        #if paddle is touching the right wall
        if self.x >= screenWidth - paddleLength:
            self.x -= 2
        #if paddle is touching the left wall
        if self.x <= 0:
            self.x += 2
        #if A pressed move left at velocity
        elif (key[pg.K_a] and (self.x <= screenWidth - paddleLength)
            and (self.x > 0)):
            self.x -= self.vel
        #if D pressed move right at velocity
        elif (key[pg.K_d] and (self.x <= screenWidth - paddleLength)
            and (self.x > 0)):
            self.x += self.vel

class Ball():
    def __init__(self):
        self.size = ballSize
        self.color = ballColor
        self.x = ballX
        self.y = ballY
        self.velX = ballVelX
        self.velY = ballVelY

    #blit a rect from ball image and set coords to the ball 
    def draw(self):
        rect = ballImage.get_rect()
        rect.x = self.x
        rect.y = self.y
        rect.w = self.size
        rect.h = self.size
        screen.blit(ballImage, rect)
        
        '''
        pg.draw.ellipse(screen, WHITE, (self.x, self.y, self.size,
                                        self.size))'''

    def update(self):
        #move in x and y directions at start
        self.x += self.velX
        self.y += self.velY

class Brick():
    def __init__(self):
        self.length = brickLength
        self.height = brickHeight
        self.color = brickColor

    def draw(self):
        #iterate brick coords, check if colliding with ball, otherwise draw
        i = 0
        while i < len(brickCoords):
            if ((nBall.x >= brickCoords[i][0]) and
                (nBall.x <= brickCoords[i][0] + brickLength) and
                (nBall.y >= brickCoords[i][1]) and
                (nBall.y < brickCoords[i][1] + brickHeight)):
                    #delete item from list if collided
                    del brickCoords[i]
                    #send ball in opposite y direction
                    nBall.velY = -nBall.velY
                    
            else:
                #blit a rect from brick image and set coords to the brick 
                rect = brickImage.get_rect()
                rect.x = brickCoords[i][0]
                rect.y = brickCoords[i][1]
                rect.w = self.length
                rect.h = self.height
                screen.blit(brickImage, rect)
                '''
                pg.draw.rect(screen, brickColor, (brickCoords[i][0],
                                             brickCoords[i][1],
                                             self.length, self.height))'''

                i += 1
                
    def update(self):
        pass

#game objects
jPaddle = Paddle()
nBall = Ball()
jBrick = Brick()

class NjBreakout():
    
    def __init__(self):
        self.running = running

    def draw(self):
        jPaddle.draw()
        nBall.draw()
        jBrick.draw()

    def update(self):
        jPaddle.update()
        nBall.update()
        jBrick.update()

    def collisionDetect(self):
        #if ball collided with paddle
        if ((nBall.x >= jPaddle.x - (nBall.size/1.5)) and
            (nBall.x <= jPaddle.x + jPaddle.length + (nBall.size/1.5))
            and (nBall.y >= jPaddle.y - nBall.size) and
            (nBall.y <= jPaddle.y + jPaddle.height)):
            nBall.velY = -nBall.velY
        #if ball collided with side walls
        if ((nBall.x >= screenWidth - nBall.size) or (nBall.x <= 0)): 
            nBall.velX = -nBall.velX
        #if ball collided with ceiling
        if (nBall.y <=0): 
            nBall.velY = -nBall.velY
        #if ball collided with floor
        if (nBall.y >= screenHeight - nBall.size):
            self.running = False
            pg.quit()
        #if all bricks broken
        if (len(brickCoords) == 0):
            nBall.velX = 0
            nBall.velY = 0

    #game loop
    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()

            screen.fill(background)
            self.update()
            self.draw()
            self.collisionDetect()
            pg.display.update()
            clock.tick(60)

#game loop
if __name__ == '__main__':
    NjBreakout().run()

