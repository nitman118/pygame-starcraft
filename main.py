import pygame
import random
import math

# Initialize pygame
pygame.init()
FPS = 60

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
# Background
background = pygame.image.load('background.png')


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 400
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(10):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)


# Bullet
# ready - you can't see the bullet on the screen
# fire - fired from spaceship

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_X = 250
game_over_Y = 300


def show_score(x, y, score_val):
    score = font.render(f'Score: {score_val}', True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y, bullet_state):
    bullet_state = 'fire'
    screen.blit(bulletImg, (x+16, y+10))
    return bullet_state


def game_over_text(x, y):
    game_over = game_over_font.render(f'GAME OVER', True, (255, 255, 255))
    screen.blit(game_over, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):

    distance = math.sqrt(math.pow(enemyX - bulletX, 2) +
                         math.pow(enemyY - bulletY, 2))

    if distance < 27:
        return True
    return False


    # Game Loop
running = True
while running:
    clock.tick(FPS)
    # RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4

            if event.key == pygame.K_RIGHT:
                playerX_change = 4

            if event.key == pygame.K_UP:
                pass

            if event.key == pygame.K_DOWN:
                pass

            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    # Get the current X coordinate of the spaceship
                    bulletX = playerX
                    bullet_state = fire_bullet(bulletX, bulletY, bullet_state)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0

            if event.key == pygame.K_RIGHT:
                playerX_change = 0

    if playerX <= 0:
        playerX = 0

    if playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]

        if enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        if enemyY[i] >= 480:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text(game_over_X, game_over_Y)

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    # Bullet Movement
    if bullet_state is 'fire':
        bullet_state = fire_bullet(bulletX, bulletY, bullet_state)
        bulletY -= bulletY_change

    playerX += playerX_change
    show_score(textX, textY, score_value)
    player(playerX, playerY)
    pygame.display.update()
