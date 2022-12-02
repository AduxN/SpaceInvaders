import pygame
from pygame import mixer
from random import randint
from math import sqrt, pow

pygame.init()

# Initializing
screen = pygame.display.set_mode((800, 600))
mixer.music.load("sound/background.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.2)
# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('img/spaceship.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('img/player.png')
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0
speed = 3

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemies = 2
for i in range(enemies):
    enemy_img.append(pygame.image.load('img/enemy.png'))
    enemy_x.append(randint(0, 735))
    enemy_y.append(randint(50, 150))
    enemy_x_change.append(2)
    enemy_y_change.append(0.5)


def enemy(x, y, q):
    screen.blit(enemy_img[q], (x, y))


# Bullet
bullet_img = pygame.image.load('img/bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 10
bullet_y_change = 10
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))


def is_collision(en_x, en_y, bul_x, bul_y):
    distance = sqrt((pow(en_x-bul_x, 2)) + (pow(en_y-bul_y, 2)))
    if distance < 27:
        return True
    return False


# Game loop
running = True
while running:
    # Background
    screen.blit(pygame.image.load("img/bg.jpg"), (0, 0))

    for event in pygame.event.get():

        # Quit Game
        if event.type == pygame.QUIT:
            running = False

        # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_x_change = -speed
            if event.key == pygame.K_d:
                player_x_change = speed
            if event.key == pygame.K_w:
                player_y_change = -speed
            if event.key == pygame.K_s:
                player_y_change = speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("sound/laser.wav")
                    bullet_sound.play()
                    bullet_sound.set_volume(0.4)
                    bullet_x = player_x+8
                    bullet_y = player_y
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player_x_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player_y_change = 0

    # Applying movement changes
    player_x += player_x_change
    player_y += player_y_change
    for i in range(enemies):
        enemy_x[i] += enemy_x_change[i]
        enemy_y[i] += enemy_y_change[i]

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Boundaries
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    if player_y <= 0:
        player_y = 0
    elif player_y >= 536:
        player_y = 536

    for i in range(enemies):
        # Game Over
        if enemy_y[i] > 440:
            for j in range(enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        if enemy_x[i] <= 0:
            enemy_x_change[i] = 2
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -2
        if enemy_y[i] <= 0:
            enemy_y_change[i] = 1
        elif enemy_y[i] >= 536:
            enemy_y_change[i] = -1

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("sound/explosion.wav")
            explosion_sound.set_volume(0.3)
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = randint(0, 735)
            enemy_y[i] = randint(50, 150)
        enemy(enemy_x[i], enemy_y[i], i)

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
