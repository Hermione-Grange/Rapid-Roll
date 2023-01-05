from tools import *


clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WSIZE = WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode(WSIZE)
FPS = 100

collide_button_sound = pygame.mixer.Sound("data/sounds/button.mp3")
collide_button_sound.set_volume(0.3)

ball_image = load_image("data/sprites/red_ball")
tile_image = load_image("data/sprites/tile_1")

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
    (100, 50),
    screen,
    collide_button_sound
)


class Tile(pygame.sprite.Sprite):
    tile_speed = 1

    def __init__(self, coords, image=tile_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft=coords)

    def update(self):
        self.rect.y -= self.tile_speed
        screen.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self, coords=(WIDTH // 2, 100), health=3):
        pygame.sprite.Sprite.__init__(self)
        self.image = ball_image
        self.rect = self.image.get_rect(topleft=coords)

        self.speed = 4
        self.gravity = 0
        self.gravity_limit = 10
        self.air_timer = 0
        self.jump_force = -8
        self.moving_right = False
        self.moving_left = False
        self.health = health
        self.y_momentum = 0.2
        self.side_rects = [pygame.Rect(-2, 1, 1, 800), pygame.Rect(600, 1, 1, 800)]
        self.death_rects = [pygame.Rect(0, 800, 600, 2), pygame.Rect(0, 50, 600, 40)]

    def get_coords(self):
        return self.rect.x, self.rect.y, self.health

    def update(self, tiles_for_ball, thorn_tiles_for_ball, life_hearts):

        ball_movement = [0, 0]
        if self.moving_right:
            ball_movement[0] += self.speed

        if self.moving_left:
            ball_movement[0] -= self.speed

        ball_movement[1] += self.gravity

        self.gravity += self.y_momentum
        if self.gravity > self.gravity_limit:
            self.gravity = self.gravity_limit

        tiles_for_ball = [obj.rect for obj in tiles_for_ball]
        self.rect, collisions = move(self.rect, ball_movement, self.side_rects + tiles_for_ball)

        if collisions['top']:
            self.gravity = -self.gravity - 2
        if collisions['bottom']:
            self.gravity = 0.2
            self.air_timer = 0
        else:
            self.air_timer += 1

        # check to death
        if self.rect.collidelist(self.death_rects + thorn_tiles_for_ball) > -1:
            sleep(0.1)
            self.health -= 1
            self.moving_right = False
            self.moving_left = False
            self.gravity = 0
            if len(tiles_for_ball) > 1:
                spawn_point = tiles_for_ball[-2]
            else:
                spawn_point = tiles_for_ball[-1]
            self.rect.x = spawn_point.x + 60
            self.rect.y = spawn_point.y - 40

        i = 0
        while i < len(life_hearts):
            if self.rect.colliderect(life_hearts[i]):
                if self.health < 5:
                    self.health += 1
                life_hearts[i].kill()
                del life_hearts[i]
            else:
                i += 1

        screen.blit(self.image, self.rect)


def game():
    tiles_for_ball = [Tile((300, 500)), Tile((100, 800))]
    ball = Ball()

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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    ball.moving_right = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    ball.moving_left = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    ball.moving_right = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    ball.moving_left = False

        if exit_button.collided(mx, my):
            if clicked:
                return
        
        for obj in tiles_for_ball:
            obj.update()

        ball.update(tiles_for_ball, list(), list())
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
