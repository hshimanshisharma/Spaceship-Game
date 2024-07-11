import pygame
import os    #operating system to help define the path of the images 

pygame.init()


WIDTH,HEIGHT = 900,500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Spaceship Game!")  #to give title to the window

FPS = 60   #frame per second to make sure gmae runs at same speed at different computers
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
Winner_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT ))   #Resizes the image
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP,90)                                          #Rotates the spaceship by 90 degrees

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT )),270)

SPACE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),(WIDTH,HEIGHT))

BORDER = pygame.Rect(WIDTH//2-5 ,0 ,10 ,HEIGHT)

def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    # WIN.fill((255,255,255))  #White
    WIN.blit(SPACE_IMAGE,(0,0))
    pygame.draw.rect(WIN,(0,0,0),BORDER)

    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, (255,255,255))
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health), 1, (255,255,255))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))     #we use blit when we want to draw somw surface on the screen, the images when they get loaded on pygame are called surfaces
                    #always draw  everything after fill cause cause before it will just get covered by fill color
    WIN.blit(RED_SPACESHIP,(red.x,red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, (255,255,0), bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, (255,0,0), bullet)

    pygame.display.update()

def draw_winner(text):
    tx = Winner_FONT.render(text, 1, (255,255,255))
    WIN.blit(tx, (WIDTH/2 - tx.get_width()/2, HEIGHT/2 - tx.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_movements(key_pressed,yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:  #LEFT
        yellow.x -= VEL 
    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 10:  #Right
        yellow.x += VEL 
    if key_pressed[pygame.K_w] and yellow.y-VEL > 0:  #UP
        yellow.y -= VEL 
    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  #Down
        yellow.y += VEL 

def red_movements(key_pressed,red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  #LEFT
        red.x -= VEL 
    if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 15:  #Right
        red.x += VEL 
    if key_pressed[pygame.K_UP] and red.y - VEL > 0:  #UP
        red.y -= VEL 
    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  #Down
        red.y += VEL 

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    red = pygame.Rect(650,200,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(200,200,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets=[]

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)      #makes sure while loop runs maximum at the speed of FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2-2, 10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2-2, 10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

        key_pressed = pygame.key.get_pressed()
        yellow_movements(key_pressed, yellow)
        red_movements(key_pressed, red)

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        # print(yellow_bullets, red_bullets)
        

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)

    main()

if __name__ == "__main__":
    main()