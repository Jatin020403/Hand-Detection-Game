import pygame
import random

import cv2 as cv
import numpy as np
import mediapipe as mp
import time
import HandTrackingModule as htm

#pygame
pygame.init()

X = 1280
Y = 720

screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Ball part')
screen.fill((0,160,70))

cam_empty_dist = [-100, -100]
playerX = cam_empty_dist[0]
playerY = cam_empty_dist[1]
playerImg = pygame.draw.circle(screen, (0,0,0), (int(playerX),
                                                 int(playerY)), 20)
playerChange = 10

ballImg = []
ballX = []  # Bad Ball Black  ||  Good Ball Green
ballY = []  
velX = []
velY = []
ballVel = 9
ball_num = 10

Enemy_ball_share = 5 
score = 0
callState = 'No'
radius = 40
clrChange = 1


def randomness():  #Randomness of balls
    velX = 0
    velY = random.random()*ballVel+1
    pX = random.randrange(80, 1200)
    pY = 90
    List = [velX, velY, pX, pY]
    return List 

def player(x,y, screen):
    playerImg = pygame.draw.circle(screen, (0, 0, 255), (int(playerX),
                                                         int(playerY)), 20)

def ball(x, y, i): #BallX, BallY
    if i< Enemy_ball_share:
        img = pygame.draw.circle(screen, (255,0,0), (int(x[i]),
                                                       int(y[i])), 20)
    if i>= Enemy_ball_share:
        img = pygame.draw.circle(screen, (0,255,0), (int(x[i]),
                                                        int(y[i])), 20)    

def callChk(Bx, By, Px = playerX, Py = playerY):
    global callState
    dist = ((Bx-Px)**2 + (By-Py)**2)**(1/2)
    if dist < radius:
        if callState == 'No':
            callState = 'Yes'
        #print(dist)
        return True
    else:
        callState = 'No'
        return False
        

def ball_move(ballX, ballY, velX, velY, i, Px, Py):
    global check, score
    check = 1
    if ballX <= 20 or ballX >=X - 20:
        velX*=-1
    if ballY >= Y - 20:
        ballX = randomness()[2]
        ballY = randomness()[3]
        ###
    ballX = ballX + velX
    ballY = ballY + velY
    callChkAns = callChk(ballX, ballY, Px, Py)
    if i >= (Enemy_ball_share) and callChkAns:
        score+=1
        ballX = randomness()[2]
        ballY = randomness()[3]
        callState = False
        check = True
        #print('Yeyy1')
        # add callstate to where you display

    #print(score)
        
    if i < (Enemy_ball_share) and callChkAns:
        check = False
        #print('Yeyy2')
    return (ballX, ballY, velX, velY, check)
    
            
for i in range(ball_num):
    velX.append(randomness()[0])
    velY.append(randomness()[1])
    ballX.append(randomness()[2])
    ballY.append(randomness()[3])

    if i<Enemy_ball_share:
        img = pygame.draw.circle(screen, (255, 255, 0), (int(ballX[i]),
                                                         int(ballY[i])), 20)
    if i>=Enemy_ball_share:
        img= pygame.draw.circle(screen, (212,175,55), (int(ballX[i]),
                                                       int(ballY[i])), 20)
    ballImg.append(img)

#webcam
pTime = 0

cap = cv.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
detector = htm.handDetector(detectionCon=0.6)


#The Loop

running = 1

while running and cap.isOpened():
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
            cv.destroyAllWindows
            print('End1')
            break
    
        
    #screen.fill((120,120,120))        

    #Screen Ready, reading from camera

    success, img = cap.read()
    img = cv.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList) !=0:
        #print(lmList[9])
        playerX = lmList[9][1]
        playerY = lmList[9][2]
        
    else:
        #print(cam_empty_dist)
        playerX = cam_empty_dist[0]
        playerY = cam_empty_dist[1]

    #Balls
    for i in range(ball_num):
        ballX[i], ballY[i], velX[i], velY[i], check = ball_move(ballX[i],
                                                                ballY[i],
                                                                velX[i],
                                                                velY[i],
                                                                i,
                                                                playerX,
                                                                playerY)
        ball(ballX, ballY, i)
        if check == False:
            cv.destroyAllWindows
            running = 0
            print('End 2')
            break
        
    #print(playerX, playerY)
    player(playerX, playerY, screen)
    pygame.display.update()
    
    cTime = time.time()
    fps = int(1/(cTime - pTime))
    pTime = cTime

    screen.fill((120,120,120))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, X, 70))
    fpsss = pygame.font.Font('freesansbold.ttf', 32).render('FPS : ' + str(fps),
                                                        True, (255, 255, 255))
    
    screen.blit(fpsss, (10, 10))
    scoreDisp = pygame.font.Font('freesansbold.ttf', 32).render('Score' + str(score),
                                                            True, (255, 255, 255))
    screen.blit(scoreDisp, (1080, 10))
    if clrChange%3==0:
        Name = pygame.font.Font('freesansbold.ttf', 40).render('Game',
                                                                True, (255, 0, 0))
    if clrChange%3==1:
        Name = pygame.font.Font('freesansbold.ttf', 40).render('Game',
                                                                True, (0, 255, 0))
    if clrChange%3==2:
        Name = pygame.font.Font('freesansbold.ttf', 40).render('Game',
                                                                True, (0, 0, 255))
    screen.blit(Name, (540, 10))
    clrChange+=1
    if clrChange == 7:
        clrChange = 1
        
    

    
    
    
    cv.putText(img, str(int(fps)), (10, 70),
                cv.FONT_HERSHEY_PLAIN, 3,
               (255, 0, 255), 3)
    
    cv.imshow('Screen', img)
    
    
    cv.waitKey(1)
    

cv.destroyAllWindows
pygame.quit()

print(score)
        
    

        
