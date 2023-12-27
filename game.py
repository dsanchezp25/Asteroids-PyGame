import math, os, pygame, random, sys
from pygame.locals import *

# init pygame
pygame.init()
fps = pygame.time.Clock()

# sounds
pygame.mixer.pre_init()
pygame.init()

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# globals
WIDTH = 800
HEIGHT = 600
time = 0

# canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Asteroids')

# load images
bg = pygame.image.load(os.path.join('images', 'bg.jpg'))
debris = pygame.image.load(os.path.join('images', 'debris2_brown.png'))
ship = pygame.image.load(os.path.join('images', 'ship.png'))
ship_thrusted = pygame.image.load(os.path.join('images', 'ship_thrusted.png'))
asteroids = pygame.image.load(os.path.join('images', 'asteroid.png'))
shot = pygame.image.load(os.path.join('images', 'shot2.png'))
explosion = pygame.image.load(os.path.join('images', 'explosion_blue.png'))

# load sounds
#   missile sound
missile_sound = pygame.mixer.Sound(os.path.join('sounds', 'missile.ogg'))
missile_sound.set_volume(1)

#   thrust sound
thruster_sound = pygame.mixer.Sound(os.path.join('sounds', 'thrust.ogg'))
thruster_sound.set_volume(1)

#   thrust sound
explosion_sound = pygame.mixer.Sound(os.path.join('sounds', 'explosion.ogg'))
explosion_sound.set_volume(1)

#   background score
pygame.mixer.music.load(os.path.join('sounds', 'game.ogg'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

# set variable
ship_x = WIDTH / 2 - 50
ship_y = HEIGHT / 2 - 50
ship_angle = 0
ship_is_rotating = False
ship_is_forward = False
ship_direction = 0
ship_speed = 0

asteroid_x = [0, 0, 0, 0, 0]  # random.randint(0,WIDTH)
asteroid_y = [0, 0, 0, 0, 0]  # random.randint(0,HEIGHT)
asteroid_angle = []
asteroid_speed = 2
num_asteroids = 5

bullet_x = []
bullet_y = []
bullet_angle = []
num_bullets = 0

score = 0
game_over = False

for i in range(0, num_asteroids):
    asteroid_x.append(random.randint(0, WIDTH))
    asteroid_y.append(random.randint(0, HEIGHT))
    asteroid_angle.append(random.randint(0, 365))


# rot_center function
def rot_center(image, angle):
    """rotate a Surface, maintaining position"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


# draw game function
def draw(canvas):
    global time
    global ship_is_forward
    global bullet_x, bullet_y
    global score

    canvas.fill(BLACK)
    canvas.blit(bg, (0, 0))
    canvas.blit(debris, (time * .3, 0))
    canvas.blit(debris, (time * .3 - WIDTH, 0))

    time += 1

    for i in range(0, num_bullets):
        canvas.blit(shot, (bullet_x[i], bullet_y[i]))

    for i in range(0, num_asteroids):
        canvas.blit(rot_center(asteroids, time), (asteroid_x[i], asteroid_y[i]))

    if ship_is_forward:
        canvas.blit(rot_center(ship_thrusted, ship_angle), (ship_x, ship_y))
    else:
        canvas.blit(rot_center(ship, ship_angle), (ship_x, ship_y))

    # draw Score
    myfont1 = pygame.font.SysFont("Comic Sans MS", 40)
    label1 = myfont1.render("Score : " + str(score), 1, (255, 255, 0))
    canvas.blit(label1, (50, 20))

    if game_over:
        myfont2 = pygame.font.SysFont("Comic Sans MS", 40)
        label2 = myfont2.render("GAME OVER MAKINA ", 1, (255, 255, 255))
        canvas.blit(label2, (WIDTH / 2 - 150, HEIGHT / 2 - 40))


# handle_input function
def handle_input():
    global ship_angle, ship_is_rotating, ship_direction
    global ship_x, ship_y, ship_speed, ship_is_forward
    global bullet_x, bullet_angle, bullet_y, num_bullets
    global thruster_sound, missile_sound

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                ship_is_rotating = True
                ship_direction = 0
            elif event.key == K_LEFT:
                ship_is_rotating = True
                ship_direction = 1
            elif event.key == K_UP:
                ship_is_forward = True
                ship_speed = 10
                thruster_sound.play()
            elif event.key == K_SPACE:
                bullet_x.append(ship_x + 50)
                bullet_y.append(ship_y + 50)
                bullet_angle.append(ship_angle)
                num_bullets += 1
                missile_sound.play()
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                ship_is_rotating = False
            else:
                ship_is_forward = False
                thruster_sound.stop()

    if ship_is_rotating:
        if ship_direction == 0:
            ship_angle -= 10
        else:
            ship_angle += 10

    if ship_is_forward or ship_speed > 0:
        ship_x = (ship_x + math.cos(math.radians(ship_angle)) * ship_speed)
        ship_y = (ship_y + -math.sin(math.radians(ship_angle)) * ship_speed)
        if not ship_is_forward:
            ship_speed = ship_speed - 0.2


# update_screen function
def update_screen():
    pygame.display.update()
    fps.tick(60)


# isCollision function
def isCollision(enemyX, enemyY, bulletX, bulletY, dist):
    distancia = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distancia < dist:
        return True
    else:
        return False


# game_logic function
def game_logic():
    global bullet_x, bullet_angle, bullet_y, num_bullets
    global asteroid_x, asteroid_y
    global score, game_over

    for i in range(0, num_bullets):
        bullet_x[i] = (bullet_x[i] + math.cos(math.radians(bullet_angle[i])) * 10)
        bullet_y[i] = (bullet_y[i] + -math.sin(math.radians(bullet_angle[i])) * 10)

    for i in range(0, num_asteroids):
        asteroid_x[i] = (asteroid_x[i] + math.cos(math.radians(asteroid_angle[i])) * asteroid_speed)
        asteroid_y[i] = (asteroid_y[i] + -math.sin(math.radians(asteroid_angle[i])) * asteroid_speed)

        if asteroid_y[i] < 0:
            asteroid_y[i] = HEIGHT

        if asteroid_x[i] > HEIGHT:
            asteroid_y[i] = 0

        if asteroid_x[i] < 0:
            asteroid_x[i] = WIDTH

        if asteroid_x[i] > WIDTH:
            asteroid_x[i] = 0

        if isCollision(ship_x, ship_y, asteroid_x[i], asteroid_y[i], 17):
            game_over = True

    for i in range(0, num_bullets):
        for j in range(0, num_asteroids):
            if isCollision(bullet_x[i], bullet_y[i], asteroid_x[j], asteroid_y[j], 50):
                asteroid_x[j] = (random.randint(0, WIDTH))
                asteroid_y[j] = (random.randint(0, HEIGHT))
                asteroid_angle[j] = (random.randint(0, 360))
                explosion_sound.play()
                score += 1


# asteroids game loop
while True:
    draw(window)
    handle_input()
    if not game_over:
        game_logic()
    update_screen()
