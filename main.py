import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
high_scores = []
level_value = 1
level_up_value = ""
font = pygame.font.Font('freesansbold.ttf', 20)

scoreX = 10
scoreY = 10
levelX = 10
levelY = 40

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
level_font = pygame.font.Font('freesansbold.ttf', 20)

# Starter code functions from forked project
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Added functions

def show_level(x, y):
    level = font.render("Level: " + str(level_value), True, (255, 255, 255))
    screen.blit(level, (x, y))

def level_up_text(x, y):
    level_text = font.render(level_up_value, True,  (255, 255, 0))
    screen.blit(level_text, (x, y))
  

# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    # if player levels up
    if score_value < 10:
        level_value = 1
    elif score_value <= 20:
        level_value = 2
    elif score_value <= 30:
        level_value = 3
    elif score_value <= 40:
        level_value = 4

    if (score_value >= 10 and score_value <= 12):
        level_up_value = "LEVEL UP!"
    elif (score_value >= 20 and score_value <= 22):
        level_up_value = "LEVEL UP!"
    elif (score_value >= 30 and score_value <= 32):
        level_up_value = "LEVEL UP!"
    else:
        level_up_value = ""


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            if score_value < 10:
                enemyX_change[i] = 4
            elif score_value <= 20:
                enemyX_change[i] = 5
            elif score_value <= 30:
                enemyX_change[i] = 6
            else:
                enemyX_change[i] = 7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            if score_value < 10:
                enemyX_change[i] = -4
            elif score_value <= 20:
                enemyX_change[i] = -5
            elif score_value <= 30:
                enemyX_change[i] = -6
            else:
                enemyX_change[i] = -7
            enemyY[i] += enemyY_change[i]
        

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(scoreX, scoreY)
    show_level(levelX, levelY)
    level_up_text(levelX + 100, levelY)
    pygame.display.update()
