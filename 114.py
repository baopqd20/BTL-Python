 #1 - Import library
import pygame
from pygame.locals import *
import math
import random
pygame.display.set_caption('114')
# 2 - Initialize the game
def Start():
    pygame.init() 
    width, height = 640, 480
    screen=pygame.display.set_mode((width, height))
    keys = [False, False, False, False, False, False]
    playerpos=[100,100]
    acc=[0,0]
    waters=[]
    timer=100
    timer1=0
    fires=[[640,100]]
    healthvalue=194
    game_font = pygame.font.Font('resources/04B_19.ttf', 40)
    pygame.mixer.init()

    # 3 - Load image
    player = pygame.image.load("resources/images/firemancv1.png")
    bg = pygame.image.load("resources/images/bgcv.png")
    house = pygame.image.load("resources/images/housecv.png")
    water = pygame.image.load("resources/images/watercv.png")
    fireimg1 = pygame.image.load("resources/images/firecv.png")
    fireimg=fireimg1
    healthbar = pygame.image.load("resources/images/healthbar.png")
    health = pygame.image.load("resources/images/health.png")
    logo = pygame.image.load("resources/images/firemancv1.png")
    pygame.display.set_icon(logo)
    # 3.1 - Load audio
    hit = pygame.mixer.Sound("resources/audio/firehouse.wav")
    enemy = pygame.mixer.Sound("resources/audio/splash.wav")
    shoot = pygame.mixer.Sound("resources/audio/splashhit.wav")
    endgame = pygame.mixer.Sound("resources/audio/gameover.wav")
    endgame.set_volume(0.2)
    hit.set_volume(0.2)
    enemy.set_volume(0.05)
    shoot.set_volume(0.05)
    pygame.mixer.music.load('resources/audio/nhacnen.WAV')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.1)

    # 4 - keep looping through

    running = 1
    exitcode = 0
    while running:
        timer-=1
        # 5 - clear the screen before drawing it again
        screen.fill(0)
        # 6.1 - draw the BG on the screen at X:100, Y:100
        for x in range(int(width/bg.get_width())+1):
            for y in range(int(height/bg.get_height())+1):
                screen.blit(bg,(x*100,y*100))
        # 6.2 - draw house
        screen.blit(house,(0,10))
        screen.blit(house,(0,135))
        screen.blit(house,(0,250))
        screen.blit(house,(0,370 ))
        # 6.3 - Set player position and rotation
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
        playerrot = pygame.transform.rotate(player, 360-angle*57.29)
        playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
        screen.blit(playerrot, playerpos1)
        playerrotrect =pygame.Rect(playerrot.get_rect())
        # 6.4 - Draw water
        for bullet in waters:
            index=0
            velx=math.cos(bullet[0])*10
            vely=math.sin(bullet[0])*10
            bullet[1]+=velx
            bullet[2]+=vely
            if bullet[1]<=-64 or bullet[1]>=640 or bullet[2]<=-64 or bullet[2]>=480:
                waters.pop(index)
            index+=1
            for projectile in waters:
                water1 = pygame.transform.rotate(water, 360-projectile[0]*57.29)
                screen.blit(water1, (projectile[1], projectile[2]))
        # 6.5 - Draw fires
        if timer==0:
            fires.append([640, random.randint(30,430)])
            timer=100-(timer1 * 2)
            if timer1>=35:
                timer1=35
            else:
                timer1+=1
        index=0
        for fire in fires:
            if fire[0]<-64:
                fires.pop(index)
            fire[0]-=1
            # 6.5.1 - Attack house
            badrect=pygame.Rect(fireimg.get_rect())
            badrect.top=fire[1]
            badrect.left=fire[0]
            if badrect.left<64:
                hit.play()
                healthvalue -= random.randint(20,50)
                fires.pop(index)
            #6.5.2 - Check for collisions
            index1=0
            for bullet in waters:
                bullrect=pygame.Rect(water.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    acc[0]+=1
                    fires.pop(index)
                    waters.pop(index1)
                index1+=1
            # 6.5.3 - Next fire
            index+=1
        for fire in fires:
            screen.blit(fireimg, fire)
        #6.6 - Draw score
        if healthvalue<=0:
            running=0
            exitcode=0
        if acc[1] !=0:
            score+=0.05
        else:
            score=0
        font = pygame.font.Font('resources/04B_19.ttf', 40)
        score_surface = font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(topright = (600,5))
        screen.blit(score_surface, score_rect)
        # 6.7 - Draw health bar
        screen.blit(healthbar, (5,5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1+8,8))
        # 7 - update the screen
        pygame.display.flip()
        # 8 - loop through the events
        for event in pygame.event.get():
            # check if the event is the X button 
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key==K_w or event.key == K_UP:
                    keys[0]=True
                elif event.key==K_a or event.key == K_LEFT:
                    keys[1]=True
                elif event.key==K_s or event.key == K_DOWN:
                    keys[2]=True
                elif event.key==K_d or event.key == K_RIGHT:
                    keys[3]=True
                elif event.key == K_F1:
                    keys[4] =True
                elif event.key==K_ESCAPE:
                    exit()
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_w or event.key == K_UP:
                    keys[0]=False
                elif event.key==pygame.K_a or event.key == K_LEFT:
                    keys[1]=False
                elif event.key==pygame.K_s or event.key == K_DOWN:
                    keys[2]=False
                elif event.key==pygame.K_d or event.key == K_RIGHT:
                    keys[3]=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                shoot.play()
                position=pygame.mouse.get_pos()
                acc[1]+=1
                waters.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
                    
        # 9 - Move player
        if keys[0] and playerpos[1] >= 10:
            playerpos[1]-=1
        elif keys[2] and playerpos[1] <= 450:
            playerpos[1]+=1
        if keys[1] and playerpos[0] >= 100:
            playerpos[0]-=1
        elif keys[3] and playerpos[0] <= 630:
            playerpos[0]+=1
    # 11 - Gameover display        
    if exitcode==0:
        pygame.font.init()
        pygame.mixer.music.stop()
        endgame.play()
        font = pygame.font.Font('resources/04B_19.ttf', 40)
        text = font.render("Score: "+str(int(score)), True, (0,255,255))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+50
        font1 = pygame.font.Font('resources/04B_19.ttf', 80)
        over = font1.render("GAME OVER", True, (255,0,0))
        overRect = over.get_rect()
        overRect.centerx = screen.get_rect().centerx
        overRect.centery = screen.get_rect().centery-50
        screen.blit(over, overRect)
        screen.blit(text, textRect)
        font2 = pygame.font.Font('resources/04B_19.ttf', 20)
        reset = font2.render("space to restart", True, (255,255,255))
        resetRect = reset.get_rect()
        resetRect.centerx = screen.get_rect().centerx
        resetRect.centery = screen.get_rect().centery+200
        screen.blit(reset, resetRect)
Start()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                Start()
            elif event.key == K_ESCAPE:
                exit()
    pygame.display.update()



