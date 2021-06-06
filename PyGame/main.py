import pygame
import random
from math import pow, sqrt
from pygame import mixer

# Inicjalizowanie
pygame.init()
# Tworzenie okienka
screen = pygame.display.set_mode((800, 600))
# Tytul i Ikona
pygame.display.set_caption('Podbój w Kosmosie')
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
# Background
background1 = pygame.image.load('space_stars.jpg')
# Background music
mixer.music.load('background_music.mp3')
mixer.music.play(-1)
# Gracz
player1 = pygame.image.load('player.png')
player_X = 400
player_Y = 500
change_X = 0
change_Y = 0


def player(x, y):
    screen.blit(player1, (x, y))


# Pociski
bullet = pygame.image.load('bullet.png')
bullet_X = 0
bullet_y = player_Y
bullet_change_y = 0.5
bullet_state = "ready"
pocisk_y = 0
pocisk_x = 0

# Wynik
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
font_x = 10
font_y = 10
# Game over
game_over = pygame.font.Font('freesansbold.ttf', 32)
is_hit = False


def font_show(x, y):
    score_show = font.render("Wynik wynosi: " + str(score), True, (255, 255, 255))
    screen.blit(score_show, (x, y))


def game_over_text(x, y):
    game_over_show = game_over.render("KONIEC GRY", True, (255, 255, 255))
    screen.blit(game_over_show, (x, y))


def bullet_Fire(x, y):
    global bullet_state
    bullet_state = "fire"

    screen.blit(bullet, (x + 16, y))


def Colissions(x1, x2, y1, y2):
    distance = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
    if distance < 27:
        return True
    else:
        return False


# Przeciwnik_czaszka
enemy1 = []
enemy_X = []
enemy_Y = []
enemy_change_X = []
enemy_change_Y = []
number_of_opp = 2
for i in range(number_of_opp):
    enemy1.append(pygame.image.load('enemy.png'))
    enemy_X.append(random.randint(0, 764))
    enemy_Y.append(random.randint(10, 60))
    enemy_change_X.append(0.1)
    enemy_change_Y.append(100)


def enemy(x, y, i):
    screen.blit(enemy1[i], (x, y))


# Gierka
running = True
while running:
    screen.fill((0, 0, 0))  # Wypelnienie ekranu kolorem
    screen.blit(background1, (0, 0))  # Dodanie tła
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Wylaczanie programu na QUIT
            running = False
        if event.type == pygame.KEYDOWN:  ## przypisanie co robią klawisze
            if event.key == pygame.K_LEFT:
                change_X -= 0.2
            if event.key == pygame.K_RIGHT:
                change_X += 0.2
            if event.key == pygame.K_DOWN:
                change_Y += 0.1
            if event.key == pygame.K_UP:
                change_Y -= 0.25
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.mp3')
                    mixer.Sound.play(bullet_sound)

                    bullet_Fire(player_X, player_Y)
                    pocisk_y = player_Y
                    pocisk_x = player_X

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change_X = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                change_Y = 0

    player_X += change_X
    player_Y += change_Y

    if player_X < 0:  # Ustawianie granic ekranu
        player_X = 0
    elif player_X > 736:
        player_X = 736
    if player_Y < 0:
        player_Y = 0
    elif player_Y > 536:
        player_Y = 536
    for i in range(number_of_opp):
        is_hit = Colissions(enemy_X[i], player_X, enemy_Y[i], player_Y)
        if is_hit:
            for j in range(number_of_opp):
                enemy_Y[j] = 2000
            break
        enemy_X[i] += enemy_change_X[i]
        if enemy_X[i] > 764:
            enemy_change_X[i] = -0.25
            enemy_Y[i] += enemy_change_Y[i]
        elif enemy_X[i] < 0:
            enemy_change_X[i] = 0.25
            enemy_Y[i] += enemy_change_Y[i]
        is_col = Colissions(enemy_X[i], pocisk_x, enemy_Y[i], pocisk_y)
        if is_col:
            col_sound = mixer.Sound('explosion.mp3')
            mixer.Sound.play(col_sound)
            pocisk_y = player_Y
            bullet_state = "ready"
            score += 100
            enemy_X[i] = random.randint(0, 764)
            enemy_Y[i] = random.randint(10, 60)
            # Jezeli trafiony to podwaja przeciwnika:
            if number_of_opp <= 20:
                number_of_opp += 1
                enemy1.append(pygame.image.load('enemy.png'))
                enemy_X.append(random.randint(0, 764))
                enemy_Y.append(random.randint(10, 60))
                enemy_change_X.append(0.1)
                enemy_change_Y.append(30)
            if number_of_opp > 20:  # Zwiększanie predkosci gdy jest wiecej niz 20
                enemy_change_X[i] += 0.01

        if enemy_Y[i] <= 564:
            enemy(enemy_X[i], enemy_Y[i], i)

    # Pociski
    if pocisk_y <= 0:
        pocisk_y = player_Y
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet_Fire(pocisk_x, pocisk_y)
        pocisk_y -= bullet_change_y

    if is_hit:
        game_over_text(200, 250)

    font_show(font_x, font_y)

    player(player_X, player_Y)

    pygame.display.update()
