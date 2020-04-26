import math
import random
import csv
import operator

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
level_value = 1
level_up_value = ""
font = pygame.font.Font('freesansbold.ttf', 20)
game_over = False

high_scores = []
names = []

with open('high_scores.csv') as csvfile:
    reader = csv.reader(csvfile)
    sortedlist = sorted(reader, key=operator.itemgetter(1), reverse=True)
    for i in sortedlist:
        names.append(i[0])
        high_scores.append(i[1])

scoreX = 10
scoreY = 10
levelX = 10
levelY = 40

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
menu_font = pygame.font.Font('freesansbold.ttf', 48)
scores_font = pygame.font.Font('freesansbold.ttf', 45)

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

# Pause Loop

def show_pause():
    paused = True
    while paused:
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))
        pause_title = menu_font.render("PAUSED", True,  (255, 255, 0))
        pauseRect = pause_title.get_rect()
        pauseRect.centerx = screen.get_rect().centerx
        pauseRect.centery = screen.get_rect().centery - 50
        screen.blit(pause_title, pauseRect)

        high_title = menu_font.render("HIGH SCORES", True,  (255, 255, 255))
        highRect = high_title.get_rect()
        highRect.centerx = screen.get_rect().centerx
        highRect.centery = screen.get_rect().centery + 50
        screen.blit(high_title, highRect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                
                if highRect.collidepoint(mpos):
                    show_high_scores_menu()
                    break

        pygame.display.update()

# High Scores Loop

def show_high_scores_menu():
    high_scores_menu = True
    global high_scores, names
    high_scores.clear()
    names.clear()
    with open('high_scores.csv') as csvfile:
        reader = csv.reader(csvfile)
        sortedlist = sorted(reader, key=operator.itemgetter(1), reverse=True)
        for i in sortedlist:
            names.append(i[0])
            high_scores.append(i[1])

    while high_scores_menu:
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))
        high_title = menu_font.render("HIGH SCORES", True,  (255, 255, 0))
        highRect = high_title.get_rect()
        highRect.centerx = screen.get_rect().centerx
        highRect.centery = 100
        screen.blit(high_title, highRect)

        score1 = scores_font.render(names[0] + " : " + str(high_scores[0]), True, (255, 255, 255))
        score1Rect = score1.get_rect()
        score1Rect.centerx = screen.get_rect().centerx
        score1Rect.centery = 250
        screen.blit(score1, score1Rect)
        score2 = scores_font.render(names[1] + " : " + str(high_scores[1]), True, (255, 255, 255))
        score2Rect = score1.get_rect()
        score2Rect.centerx = screen.get_rect().centerx
        score2Rect.centery = 300
        screen.blit(score2, score2Rect)
        score3 = scores_font.render(names[2] + " : " + str(high_scores[2]), True, (255, 255, 255))
        score3Rect = score3.get_rect()
        score3Rect.centerx = screen.get_rect().centerx
        score3Rect.centery = 350
        screen.blit(score3, score3Rect)
        score4 = scores_font.render(names[3] + " : " + str(high_scores[3]), True, (255, 255, 255))
        score4Rect = score4.get_rect()
        score4Rect.centerx = screen.get_rect().centerx
        score4Rect.centery = 400
        screen.blit(score4, score4Rect)
        score5 = scores_font.render(names[4] + " : " + str(high_scores[4]), True, (255, 255, 255))
        score5Rect = score1.get_rect()
        score5Rect.centerx = screen.get_rect().centerx
        score5Rect.centery = 450
        screen.blit(score5, score5Rect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    high_scores_menu = False
                    show_pause()
                    break

        pygame.display.update()

def save_high_scores():
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    name = ""
    while len(name) < 3:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
            
        name = name.upper()
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        high_title = menu_font.render("High Score!", True,  (255, 255, 0))
        highRect = high_title.get_rect()
        highRect.centerx = screen.get_rect().centerx
        highRect.centery = 100
        screen.blit(high_title, highRect)
        
        inpt = font.render("Enter a 3-letter name", True,  (255, 255, 255))
        inptRect = inpt.get_rect()
        inptRect.centerx = screen.get_rect().centerx
        inptRect.centery = 200
        screen.blit(inpt, inptRect)
        namedisplay = menu_font.render(name, True, (255, 255, 255))
        namedisplayRect = namedisplay.get_rect()
        namedisplayRect.center = screen.get_rect().center
        screen.blit(namedisplay, namedisplayRect)
        pygame.display.update()

    #replace lowest 
    lowest = high_scores[0]
    lowest_index = 0
    for i in range(len(high_scores)):
        if high_scores[i] <= lowest:
            lowest = high_scores[i]
            lowest_index = i
    high_scores[lowest_index] = score_value
    names[lowest_index] = name

    with open('high_scores.csv', 'w',newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i in range(len(names)):
                writer.writerow([str(names[i]), str(high_scores[i])])

    show_high_scores_menu()


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
            if event.key == pygame.K_ESCAPE:
                    show_pause()
            


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
            game_over = True
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            if score_value >= int(high_scores[4]):
                save_high_scores()
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

