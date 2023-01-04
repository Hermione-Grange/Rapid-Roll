import sys
from tools import *


clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WSIZE = WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode(WSIZE)
FPS = 100


def game():
    running = True
    while running:
        screen.fill((40, 40, 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)


def main_menu():
    running = True
    while running:
        screen.fill((40, 40, 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()
