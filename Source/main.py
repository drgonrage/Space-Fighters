# Imports
import pygame as pg, os, time as tm, random as rd, sys

# Initializing
pg.init()
pg.font.init()
pg.mixer.init()


# Main Window
WIDTH, HEIGHT = 900, 500

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("SpaceFighters")
BORDER = pg.Rect((WIDTH // 2), 0, 10, HEIGHT)

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0,100,200)


# HITREG EVENTS
YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2

# SHIP
SHIP_WIDTH = 60
SHIP_HEIGHT = 50
VEL = 8
HEALTH_FONT = pg.font.SysFont("impact", 30)
DEATH_FONT = pg.font.SysFont("impact", 100)
PAUSE_FONT = pg.font.SysFont("cascadia", 140)

pause_text = PAUSE_FONT.render("PAUSED", True, BLUE)

# BULLET
BULLET_VEL = 25
MAX_BULLETS = 3


# IMPORT ASSETS
YELLOW_SPACESHIP = pg.image.load(os.path.join("Source/Assets", "spaceship_yellow (Custom).png"))

"""YELLOW_SPACESHIP = pg.transform.rotate(
    pg.transform.scale(YELLOW_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), (270)
)"""

RED_SPACESHIP = pg.image.load(os.path.join("Source/Assets", "spaceship_red (Custom).png"))
"""RED_SPACESHIP = pg.transform.rotate(
    pg.transform.scale(RED_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), (90)
)"""

BACKGROUND_IMAGE = pg.image.load(os.path.join("Source/Assets", "space.jpeg"))
BACKGROUND = pg.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
BULLET_SOUND = pg.mixer.Sound(os.path.join("Source/Assets", "Gun.mp3"))
YELLOW_BULLET = pg.image.load(os.path.join("Source/Assets", "YellowBullets.png"))
RED_BULLET = pg.image.load(os.path.join("Source/Assets", "RedBullets.png"))
HIT_SOUND = pg.mixer.Sound(os.path.join("Source/Assets", "Hit.mp3"))
DEATH_SOUND = pg.mixer.Sound(os.path.join("Source/Assets", "death.mp3"))

# Pause-Menu
def pause_menu(paused):
    if paused:
        pause_text = PAUSE_FONT.render("PAUSED", True, YELLOW)
        WIN.blit(pause_text,((WIDTH - pause_text.get_width()) // 2,(HEIGHT - pause_text.get_height()) // 2))
        pg.display.update()



# Draw Window
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.fill(WHITE)
    WIN.blit(BACKGROUND, (0, 0))
    pg.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Drawing Bullets
    for bullet in red_bullets:
        pg.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pg.draw.rect(WIN, YELLOW, bullet)
    pg.display.update()


# Draw Winner
def draw_winner(text):
    if text == "YELLOW WINS":
        draw_text = DEATH_FONT.render(text, 1, YELLOW)
        WIN.blit(
            draw_text,
            (
                WIDTH / 2 - draw_text.get_width() / 2,
                HEIGHT / 2 - draw_text.get_height() / 2,
            ),
        )
        pg.display.update()
    elif text == 'RED WINS':
        draw_text = DEATH_FONT.render(text, 1, RED)
        WIN.blit(
            draw_text,
            (
                WIDTH / 2 - draw_text.get_width() / 2,
                HEIGHT / 2 - draw_text.get_height() / 2,
            ),
        )
        pg.display.update()
    elif text == 'DRAW':
        draw_text = DEATH_FONT.render(text, 1, (0,255,0))
        WIN.blit(
            draw_text,
            (
                WIDTH / 2 - draw_text.get_width() / 2,
                HEIGHT / 2 - draw_text.get_height() / 2,
            ),
        )
        pg.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pg.K_a] and (yellow.x - VEL) > 0:
        yellow.x -= VEL
    if keys_pressed[pg.K_d] and (yellow.x + VEL + yellow.width) < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pg.K_w] and (yellow.y - (VEL / 2)) > 0:
        yellow.y -= VEL
    if keys_pressed[pg.K_s] and (yellow.y + VEL + yellow.height) < HEIGHT + 3.4:
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pg.K_LEFT] and (red.x - VEL) > (BORDER.x + BORDER.width):
        red.x -= VEL
    if keys_pressed[pg.K_RIGHT] and (red.x + VEL + VEL + red.width) < WIDTH + 10:
        red.x += VEL
    if keys_pressed[pg.K_UP] and (red.y - VEL) > -3:
        red.y -= VEL
    if keys_pressed[pg.K_DOWN] and (red.y + VEL + red.height) < HEIGHT + 4.5:
        red.y += VEL


# Bullet Handler
def bullet_handler(yellow_bullets, red_bullets, red, yellow):
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


# Logic
def main():
    FPS:int = 60
    PAUSED:bool = False
    PLAYING:bool = True
    red_health:int = 10
    yellow_health:int = 10
    yellow_bullets:list = []
    red_bullets:list = []
    yellow_random_y = rd.randint(20, HEIGHT - SHIP_HEIGHT)
    red_random_y = rd.randint(20, HEIGHT - SHIP_HEIGHT)
    red = pg.Rect(840, red_random_y, 50, SHIP_HEIGHT)
    yellow = pg.Rect(10, yellow_random_y, 50, SHIP_HEIGHT)
    # CLOCK
    clock = pg.time.Clock()

    while PLAYING:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                PLAYING = False
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if not PAUSED:
                    if event.key == pg.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                        bullet = pg.Rect(
                            yellow.x + yellow.width,
                            yellow.y + yellow.height // 2 - 3,
                            8,
                            5,
                        )
                        yellow_bullets.append(bullet)
                        BULLET_SOUND.play()

                    if event.key == pg.K_j and len(red_bullets) < MAX_BULLETS:
                        bullet = pg.Rect(
                            red.x - red.width / 2, red.y + red.height // 2 - 3, 8, 5
                        )
                        red_bullets.append(bullet)
                        BULLET_SOUND.play()
                    
                if event.key == pg.K_ESCAPE:
                    if not PAUSED:
                        PAUSED = True
                        pause_menu(PAUSED)
                    else:
                        PAUSED = False
                        pause_menu(PAUSED)

            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                
        winner_text = ""
        if yellow_health <=0 and red_health <= 0:
            winner_text = 'DRAW'    
        elif red_health <= 0 and yellow_health > 0:
            winner_text = "YELLOW WINS"
            DEATH_SOUND.play()
        elif yellow_health <= 0 and red_health > 0:
            winner_text = "RED WINS"
            DEATH_SOUND.play()

        if winner_text != "":
            draw_winner(winner_text)
            break
        YELLOW_HIT, RED_HIT
        keys_pressed = pg.key.get_pressed()

        # function-calls
        if not PAUSED:
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
            yellow_handle_movement(keys_pressed, yellow)
            red_handle_movement(keys_pressed, red)
            bullet_handler(yellow_bullets, red_bullets, red, yellow)
    pg.time.delay(1000)
    main()


if __name__ == "__main__":
    main()
