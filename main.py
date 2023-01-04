from tools import *


clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WSIZE = WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode(WSIZE)
FPS = 100

collide_button_sound = pygame.mixer.Sound("data/sounds/button.mp3")
collide_button_sound.set_volume(0.3)

font2 = Font("data/font/letters.png", 2)
font3 = Font("data/font/letters.png", 3)

play_button = TextButton(
    "play",
    (WIDTH // 2, HEIGHT // 2),
    screen,
    collide_button_sound
)
exit_button = TextButton(
    "exit",
    (WIDTH // 2, HEIGHT // 2),
    screen,
    collide_button_sound
)


def game():
    running = True
    while running:
        screen.fill((40, 40, 100))
        mx, my = pygame.mouse.get_pos()

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        if exit_button.collided(mx, my):
            if clicked:
                return

        exit_button.update()

        pygame.display.update()
        clock.tick(FPS)


def main_menu():
    running = True
    while running:
        screen.fill((40, 40, 40))
        mx, my = pygame.mouse.get_pos()

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
        
        if play_button.collided(mx, my):
            if clicked:
                game()

        play_button.update()
        
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()
