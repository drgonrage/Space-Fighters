#==========================Imports=========================#
import pygame as pg
import os
import time as tm
import ffmpeg
#==========================Imports=========================#

#===================Initializing================#
pg.init()
pg.font.init()
pg.mixer.init()
#===================Initializing================#

#=========================Main-Window=========================#
WIDTH, HEIGHT = 900, 500
BORDER = pg.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
WIN = pg.display.set_mode((WIDTH, HEIGHT)) 
pg.display.set_caption('Blyat')
#=========================Main-Window=========================#                    

#=========================Color=========================#
WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)  
#=========================Color=========================#

#=========================FPS-Limit=========================#
FPS = 60
PLAYING = True
#=========================FPS-Limit=========================#

#=========================HITREG-EVENTS=========================#
YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2
#=========================SHIP=========================#
SHIP_WIDTH = 60
SHIP_HEIGHT = 50  
VEL = 6.76
HEALTH_FONT = pg.font.SysFont('comicsans', 40)
#=========================SHIP=========================#

#---------------------BULLET----------------#  
BULLET_VEL = 15
MAX_BULLETS = 3  
#---------------------BULLET----------------# 

#----------------------IMPORT-ASSETS--------------------# 
YELLOW_SPACESHIP_IMAGE = pg.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pg.transform.rotate(pg.transform.scale(YELLOW_SPACESHIP_IMAGE , (SHIP_WIDTH,SHIP_HEIGHT)), (270))
RED_SPACESHIP_IMAGE = pg.image.load(os.path.join('Assets', 'spaceship_red.png')) 
RED_SPACESHIP = pg.transform.rotate(pg.transform.scale(RED_SPACESHIP_IMAGE , (SHIP_WIDTH,SHIP_HEIGHT)), (90))
BACKGROUND_IMAGE = pg.image.load(os.path.join('Assets', 'space.jpeg')) 
BACKGROUND = pg.transform.scale(BACKGROUND_IMAGE,(WIDTH,HEIGHT))
BULLET_SOUND = pg.mixer.Sound(os.path.join('Assets', 'Gun.mp3'))
HIT_SOUND = pg.mixer.Sound(os.path.join('Assets', 'death.mp3'))
#----------------------IMPORT-ASSETS--------------------# 
            
#=========================================================Draw-Window============================================#    
def draw_window(red, yellow, red_bullets,yellow_bullets, red_health, yellow_health):
    WIN.fill(WHITE)     
    WIN.blit(BACKGROUND, (0,0))
    pg.draw.rect(WIN,BLACK,BORDER)
    
    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
#--------------------Drawing-Bullets-----------------#
    for bullet in red_bullets:
        pg.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pg.draw.rect(WIN, YELLOW, bullet)
#--------------------Drawing-Bullets-----------------#
    pg.display.update()
#=============================Draw-Winner========================#
def draw_winner(text):
    draw_text = HEALTH_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2,
                         HEIGHT/2 - draw_text.get_width()/2))
    pg.display.update() 
    pg.time.delay(1000)
      
     
#=========================================================Draw-Window============================================#    
           
#------------------------Player1-Handling------------------------#    
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pg.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pg.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pg.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pg.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pg.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pg.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pg.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pg.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL
#------------------------Player2-Handling--------------------------#

#-------------------BULLET-HANDLER----------------------#
def bullet_handler(yellow_bullets,red_bullets,red,yellow):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            HIT_SOUND.play()
            pg.event.post(pg.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
        
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            HIT_SOUND.play()
            pg.event.post(pg.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x < 0:
            red_bullets.remove(bullet)
 #-------------------BULLET-HANDLER----------------------#  
          
#--------------------------------------------Logic--------------------------------------------------#
def main():
    playing = True
    red_health = 10
    yellow_health = 10 
    yellow_bullets = []
    red_bullets = []
    red = pg.Rect(840, 240, SHIP_WIDTH,SHIP_HEIGHT)
    yellow = pg.Rect(10, 240, SHIP_WIDTH,SHIP_HEIGHT)

#---------------------CLOCK----------------------#
    clock = pg.time.Clock() 
#---------------------CLOCK----------------------#   
    
    while playing:
        clock.tick(FPS)  
         
        for event in pg.event.get():
            if event.type == pg.QUIT:
               playing = False
            
            if event.type == pg.KEYDOWN:
                if keys_pressed == [pg.K_j]:
                    yellow_bullets.append()
                    BULLET_SOUND.play()
                if keys_pressed == [pg.K_RSHIFT]:
                    red_bullets.append()
                    BULLET_SOUND.play()
                    
            if event.type == RED_HIT:
                red_health -= 1
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
            winner_text = ''
            if red_health <= 0:
                winner_text = 'YELLOW WINS'
                
            if yellow_health <= 0:
                winner_text = 'RED WINS'
            
            if winner_text != '':
                draw_winner(winner_text)
                pg.time.delay(2000) 
            
            
            YELLOW_HIT,RED_HIT
            keys_pressed = pg.key.get_pressed()
#--------------------------------------------Logic--------------------------------------------------#


#-----------------------------------fucntion-calls-------------------------------#  
        yellow_handle_movement(keys_pressed, yellow)        
        red_handle_movement(keys_pressed, red)
        draw_window(red,yellow,red_bullets,yellow_bullets, red_health, yellow_health)
        bullet_handler(yellow_bullets,red_bullets,red,yellow)  
#-----------------------------------fucntion-calls-------------------------------#                 

if __name__ == '__main__':                  
    main()

