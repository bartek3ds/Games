import pygame
import numpy as np

pygame.init()
# Wartosci ekranu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
# Ekran i nazwa
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kamień, papier i nożyce")
# Muzyka w tle
pygame.mixer.music.load('music/background_music.mp3')
pygame.mixer.music.play(-1)
# Ikona
icon = pygame.image.load('img/stone.png')
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)
# FPS
FPS = 60
clock = pygame.time.Clock()
# napis
napis = pygame.font.Font("freesansbold.ttf", 16)
wynik_og = pygame.font.Font("freesansbold.ttf", 20)  # Czcionka do pokazywania wyniku
index = 3  # Startowy indeks
# KOniec gry
game_over = True
# Restart gry
restart = False


# Klasa przedmiot
class Przedmiot:
    def __init__(self,nazwa):
        self.nazwa = nazwa
        self.przedmioty = []
        typy_przedmiotow = ['stone', 'paper', 'scissors']
        for przedmiot in typy_przedmiotow:
            self.image = pygame.image.load(f'img/{przedmiot}.png')
            self.przedmioty.append(self.image)
        napis1 = napis.render("WYBIERZ KAMIEN(nacisnij k), Papier(nacisnij p)  lub NOZYCZKI(nacisnij n)  ", True,
                              (255, 255, 255))
        self.wynik = 0
        self.przedmioty.append(napis1)
        self.losowa = 0

    def draw(self, x, y, index):            # rysuje ruch gracza
        screen.blit(self.przedmioty[index], (x, y))

    def wylosuj(self):                  # Losuje ruch komputera
        self.losowa = np.random.randint(0, 3)

    def draw_wynik(self, x, y):              # Rysuje wynik
        wynik1 = wynik_og.render("Wynik: " + str(self.wynik), True, (255, 255, 255))
        return screen.blit(wynik1, (x, y))
    def draw_nazwa(self, x, y):                   # Rysuje nazwe uzytkownika
        nazwa = wynik_og.render(f'{self.nazwa}', True, (255, 255, 255))
        return screen.blit(nazwa, (x, y))


def wynik(index, losowa):          # Oblicza wynik
    if index == losowa:
        gracz.wynik += 1
        komputer.wynik += 1
    elif index == 0 and losowa == 2:
        gracz.wynik += 1
    elif index == 1 and losowa == 0:
        gracz.wynik += 1
    elif index == 2 and losowa == 1:
        gracz.wynik += 1
    else:
        komputer.wynik += 1


def winner(x, y):         # Podaje zwyciezce
    if gracz.wynik >= 3 and gracz.wynik - komputer.wynik >= 2:
        game_over = False
        winner = wynik_og.render("Wygrał gracz!", True, (255, 255, 255))
        spacja = napis.render("Nacisnij spacje aby zagrac jeszcze raz", True, (255, 255,255))
        screen.blit(winner, (x, y))
        screen.blit(spacja, (250, 500))
        return game_over

    elif komputer.wynik >= 3 and komputer.wynik - gracz.wynik >= 2:
        game_over = False
        winner = wynik_og.render("Wygrał komputer!", True, (255, 255, 255))
        spacja = napis.render("Nacisnij spacje aby zagrac jeszcze raz", True, (255, 255, 255))
        screen.blit(winner, (x, y))
        screen.blit(spacja, (250, 500))

        return game_over
    else:
        return True





gracz = Przedmiot("GRACZ")
komputer = Przedmiot("KOMPUTER")

run = True
while run:
    screen.fill((60, 179, 113))
    # FPS
    clock.tick(FPS)
    # Wybor wygranego
    game_over = winner(300, 300)
    if game_over:


        # Rysuj przedmiot
        gracz.draw(100, 200, index)
        if index in (0, 1, 2):
            komputer.draw(550, 200, komputer.losowa)
    # Nazwy graczy:
    komputer.draw_nazwa(550, 100)
    gracz.draw_nazwa(100, 100)
    # Rysuj wynik
    gracz.draw_wynik(20, 500)
    komputer.draw_wynik(700, 500)
    # Restart
    if restart is True and game_over is False:
        gracz.wynik = 0
        komputer.wynik = 0
        index = 3
        restart = False



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_k:
                    index = 0
                if event.key == pygame.K_n:
                    index = 2
                if event.key == pygame.K_p:
                    index = 1
            if event.key == pygame.K_SPACE:
                restart = True
            if event.key == pygame.K_k or event.key == pygame.K_n or event.key == pygame.K_p:
                komputer.wylosuj()          # Wylosuj przedmiot komputera
                wynik(index, komputer.losowa)        # Oblicz wynik

    pygame.display.update()
