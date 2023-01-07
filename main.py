import sys
from random import randint
from tools import *
from time import sleep

clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Rapid Roll")
WINDOW_SIZE = (600, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)
FPS = 100
pygame.mouse.set_visible(False)

# load sound and music
collide_button_sound = pygame.mixer.Sound("sounds/button.mp3")
collide_button_sound.set_volume(0.3)

# load_images_start_________________________________________________________#
ball_image = load_image("sprites/red_ball")
tile_image = load_image("sprites/tile_1")
thorn_tile_image = load_image("sprites/thorn_tile")

new_game_image = load_image("buttons/new_game_image")
new_game_pressed_image = load_image("buttons/new_game_pressed_image")

continue_image = load_image("buttons/continue_image")
continue_pressed_image = load_image("buttons/continue_pressed_image")

level_image = load_image("buttons/level_image")
level_pressed_image = load_image("buttons/level_pressed_image")

back_image = load_image("buttons/back_image")
back_pressed_image = load_image("buttons/back_pressed_image")

back_1_image = load_image("buttons/back_1_image", scale=(1, 1))
back_1_pressed_image = load_image("buttons/back_1_pressed_image", scale=(1, 1))

yes_image = load_image("buttons/yes_image")
yes_pressed_image = load_image("buttons/yes_pressed_image")

no_image = load_image("buttons/no_image")
no_pressed_image = load_image("buttons/no_pressed_image")

records_image = load_image("buttons/records_image")
records_presed_image = load_image("buttons/records_pressed_image")

one_image = load_image("buttons/one_image")
one_pressed_image = load_image("buttons/one_pressed_image")
two_image = load_image("buttons/two_image")
two_pressed_image = load_image("buttons/two_pressed_image")
three_image = load_image("buttons/three_image")
three_pressed_image = load_image("buttons/three_pressed_image")

# background_image = load_image("background_image", scale=(20, 20))

top_spikes = load_image("sprites/spikes")
top_bar = load_image("sprites/top_bar")
life_bar = load_image("sprites/life_bar")

cursor_img = load_image("sprites/orange_cursor")

your_name_label = load_image("labels/your_name_label", scale=(1, 1))
your_score_label = load_image("labels/your_score_label", scale=(5, 5))
save_label = load_image("labels/save_label", scale=(5, 5))

one_level_label = load_image("labels/one_level_label", scale=(2, 2))
two_level_label = load_image("labels/two_level_label", scale=(2, 2))
three_level_label = load_image("labels/three_level_label", scale=(2, 2))
# load_images_end___________________________________________________________#


font = pygame.font.SysFont("consolas", 35)
font1 = pygame.font.SysFont("consolas", 70)


class Ball(pygame.sprite.Sprite):
    def __init__(self, coords=(WINDOW_SIZE[0] // 2, 100), health=3):
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

        if collisions["top"]:
            self.gravity = -self.gravity - 2
        if collisions["bottom"]:
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

        display.blit(self.image, self.rect)


class Tile(pygame.sprite.Sprite):
    tile_speed = 1

    def __init__(self, coords, image=tile_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft=coords)

    def update(self):
        self.rect.y -= self.tile_speed
        display.blit(self.image, self.rect)


class Life_heart(pygame.sprite.Sprite):
    life_heart_speed = 1

    def __init__(self, coords):
        pygame.sprite.Sprite.__init__(self)
        self.animation_frames = {}
        self.animation_database = {}
        self.animation_database["life_heart"] = load_animation("life_heart", [40, 10, 10, 10], self.animation_frames)
        self.player_frame = 0
        self.player_action = None
        self.player_image_id = None

        self.image = self.animation_database["life_heart"][0]
        self.rect = pygame.Rect(*coords, 19, 17)

    def update(self):
        self.player_action, self.player_frame = change_action(self.player_action, self.player_frame, "life_heart")
        self.player_frame += 1
        if self.player_frame >= len(self.animation_database[self.player_action]):
            self.player_frame = 0
        self.player_image_id = self.animation_database[self.player_action][self.player_frame]
        self.image = self.animation_frames[self.player_image_id]

        self.rect.y -= self.life_heart_speed
        display.blit(self.image, self.rect)


def delete_tiles(tiles_for_ball):
    i = 0
    while i < len(tiles_for_ball):
        if tiles_for_ball[i].rect.y < -100:
            tiles_for_ball[i].kill()
            del tiles_for_ball[i]
        else:
            i += 1


def delete_life_hearts(life_hearts):
    i = 0
    while i < len(life_hearts):
        if life_hearts[i].rect.y < -100:
            life_hearts[i].kill()
            del life_hearts[i]
        else:
            i += 1


def generate_tiles(tiles_for_ball, thorn_tiles_for_ball, life_hearts):
    generate_or_no = False
    if tiles_for_ball[-1].rect.y < 800 and (thorn_tiles_for_ball[-1].rect.y < 800 if thorn_tiles_for_ball else True):
        generate_or_no = True

    if generate_or_no:
        if randint(0, 5) == 0:
            thorn_tiles_for_ball.append(Tile((randint(0, 454), 900), thorn_tile_image))
        else:
            coord_y = randint(0, 454)
            tiles_for_ball.append(Tile((coord_y, 900)))
            if randint(0, 8) == 0:
                life_hearts.append(Life_heart((coord_y + 60, 875)))


def draw_life_bar(ball):
    for i in range(ball.health):
        display.blit(life_bar, (i * 32 + 54, 10))


def draw_score(score):
    text = font.render(str(score), 1, (10, 10, 10))
    x = 600 - text.get_width() - 12
    display.blit(text, (x, 10))


def draw_cursor(mx, my):
    display.blit(cursor_img, (mx - 1, my - 1))


continue_button = Button(continue_image, continue_pressed_image, (WINDOW_SIZE[0] // 2 - continue_image.get_width() // 2,
                                                                  150), display, collide_button_sound)

new_game_button = Button(new_game_image, new_game_pressed_image, (WINDOW_SIZE[0] // 2 - new_game_image.get_width() // 2,
                                                                  230), display, collide_button_sound)

level_button = Button(level_image, level_pressed_image, (WINDOW_SIZE[0] // 2 - level_image.get_width() // 2, 310),
                      display, collide_button_sound)

back_button = Button(back_image, back_pressed_image, (10, 10), display, collide_button_sound)

back_1_button = Button(back_1_image, back_1_pressed_image, (10, 10), display, collide_button_sound)

no_button = Button(no_image, no_pressed_image, (WINDOW_SIZE[0] // 2 - no_image.get_width() // 2 + 70, 500), display, collide_button_sound)

yes_button = Button(yes_image, yes_pressed_image, (WINDOW_SIZE[0] // 2 - yes_image.get_width() // 2 - 70, 500), display, collide_button_sound)

records_button = Button(records_image, records_presed_image,
                        (WINDOW_SIZE[0] // 2 - records_image.get_width() // 2, 390), display, collide_button_sound)

one_button = Button(one_image, one_pressed_image, (WINDOW_SIZE[0] // 2 - one_image.get_width() // 2 - 100, 390), display, collide_button_sound)
two_button = Button(two_image, two_pressed_image, (WINDOW_SIZE[0] // 2 - two_image.get_width() // 2, 390), display, collide_button_sound)
three_button = Button(three_image, three_pressed_image, (WINDOW_SIZE[0] // 2 - three_image.get_width() // 2 + 100, 390), display, collide_button_sound)


def save_game(score, tiles_for_ball, thorn_tiles_for_ball, life_hearts, ball):
    with open("SAV/last_game.txt", "w", encoding="utf-8") as file:
        if ball[2] > 0:
            file.write(f"{score}\n")

            if tiles_for_ball:
                for tile in tiles_for_ball:
                    file.write(f"\n{tile.rect.x} {tile.rect.y}")
            else:
                file.write("\n-")
            file.write("\n")

            if thorn_tiles_for_ball:
                for tile in thorn_tiles_for_ball:
                    file.write(f"\n{tile.rect.x} {tile.rect.y}")
            else:
                file.write("\n-")
            file.write("\n")

            if life_hearts:
                for heart in life_hearts:
                    file.write(f"\n{heart.rect.x} {heart.rect.y}")
            else:
                file.write("\n-")

            file.write("\n\n{}\n{}\n{}".format(*ball))
        else:
            file.write("---")


def update_game():
    with open("SAV/last_game.txt", "w", encoding="utf-8") as file:
        file.write("---")


def load_game():
    with open("SAV/last_game.txt", "r", encoding="utf-8") as file:
        data = file.read()
    if data == "---":
        return []
    data = data.split("\n\n")
    score = int(data.pop(0))
    tiles_for_ball = data.pop(0)
    if tiles_for_ball == "-":
        tiles_for_ball = []
    else:
        tiles_for_ball = list(map(lambda x: list(map(int, x.split())), tiles_for_ball.split("\n")))

    thorn_tiles_for_ball = data.pop(0)
    if thorn_tiles_for_ball == "-":
        thorn_tiles_for_ball = []
    else:
        thorn_tiles_for_ball = list(map(lambda x: list(map(int, x.split())), thorn_tiles_for_ball.split("\n")))

    life_hearts = data.pop(0)
    if life_hearts == "-":
        life_hearts = []
    else:
        life_hearts = list(map(lambda x: list(map(int, x.split())), life_hearts.split("\n")))
    ball_coords_and_health = list(map(int, data.pop(0).split("\n")))
    return (
        score,
        tiles_for_ball,
        thorn_tiles_for_ball,
        life_hearts,
        (ball_coords_and_health[:2], ball_coords_and_health[2]),
    )

def save_record(name, result):
    with open("SAV/records.txt", "a", encoding="utf-8") as file:
        file.write(f"\n{result}:{name}")
    sorted_keys, data = load_records()
    if len(sorted_keys) > 15:
        sorted_keys = sorted_keys[:15]
        with open("SAV/records.txt", "w", encoding="utf-8") as file:
            for i in range(len(sorted_keys)):
                file.write("\n".join(sorted_keys[i] + ":" + data[sorted_keys[i]]))


def load_records():
    with open("SAV/records.txt", "r", encoding="utf-8") as file:
        data = file.read().strip().split("\n")
    if data == [""]:
        return []
    slovar = {}
    for i in range(len(data)):
        spisok = data[i].split(":")
        slovar[int(spisok[0])] = spisok[1]
    sorted_keys = sorted(slovar, reverse=True)
    return (sorted_keys, slovar)


def save_level(level):
    with open("SAV/current_level.txt", "r", encoding="utf-8") as file:
        level_from_file = int(file.read().strip())
    if level != level_from_file:
        update_game()
        with open("SAV/current_level.txt", "w", encoding="utf-8") as file:
            file.write(str(level))


def load_level():
    with open("SAV/current_level.txt", "r", encoding="utf-8") as file:
        level = int(file.read())
    return level


# menu functions
def records_menu():
    click = False
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        display.fill((40, 40, 40))

        if back_1_button.collided(mx, my):
            if click:
                sleep(0.1)
                break

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        sorted_keys, data = load_records()
        for ind in range(len(sorted_keys)):
            text = font.render(f"{ind + 1}) {sorted_keys[ind]}: {data[sorted_keys[ind]]}", 1, (0, 162, 232))
            display.blit(text, (100, ind * 50 + 30))

        back_1_button.update()
        draw_cursor(mx, my)

        screen.blit(display, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


def death_menu(score):
    click = False
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        display.fill((40, 40, 40))

        if no_button.collided(mx, my):
            if click:
                sleep(0.1)
                running = False

        if yes_button.collided(mx, my):
            if click:
                sleep(0.1)
                name_of_player = registration_menu()
                save_record(name_of_player, score)
                running = False

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        display.blit(your_score_label, (WINDOW_SIZE[0] // 2 - your_score_label.get_width() // 2, 100))
        text = font1.render(str(score), 1, (0, 162, 232))
        display.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, 200))
        display.blit(save_label, (WINDOW_SIZE[0] // 2 - save_label.get_width() // 2, 400))

        no_button.update()
        yes_button.update()
        draw_cursor(mx, my)

        screen.blit(display, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


def registration_menu():
    click = False
    running = True
    user_text = ''
    base_font = pygame.font.Font(None, 40)

    # set left, top, width, height in
    # Pygame.Rect()
    input_rect = pygame.Rect(200, 200, 100, 100)
    color_active = pygame.Color("red")

    while running:
        mx, my = pygame.mouse.get_pos()
        display.fill((40, 40, 40))

        if yes_button.collided(mx, my):
            if click:
                sleep(0.1)
                running = False
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_BACKSPACE:

                    # stores text except last letter
                    user_text = user_text[0:-1]
                else:
                    user_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.draw.rect(screen, color_active, input_rect)
        display.blit(your_name_label, (WINDOW_SIZE[0] // 2 - your_name_label.get_width() // 2, 100))

        # TODO: to draw ok_button image
        yes_button.update()
        draw_cursor(mx, my)

        screen.blit(display, (0, 0))
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.update()
        clock.tick(FPS)
    return user_text


def choose_level_menu():
    click = False
    running = True
    current_level_label = load_level()
    while running:
        mx, my = pygame.mouse.get_pos()
        display.fill((40, 40, 40))

        if back_1_button.collided(mx, my):
            if click:
                sleep(0.1)
                break

        if one_button.collided(mx, my):
            if click:
                sleep(0.1)
                save_level(1)
                current_level_label = 1

        if two_button.collided(mx, my):
            if click:
                sleep(0.1)
                save_level(2)
                current_level_label = 2

        if three_button.collided(mx, my):
            if click:
                sleep(0.1)
                save_level(3)
                current_level_label = 3

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if current_level_label == 1:
            display.blit(one_level_label, (300 - one_level_label.get_width() // 2, 170))
        elif current_level_label == 2:
            display.blit(two_level_label, (300 - two_level_label.get_width() // 2, 170))
        else:
            display.blit(three_level_label, (300 - three_level_label.get_width() // 2, 170))
        back_1_button.update()
        one_button.update()
        two_button.update()
        three_button.update()
        draw_cursor(mx, my)

        screen.blit(display, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


def game(score=0, tiles_for_ball_from_file=None, thorn_tiles_for_ball_from_file=None, life_hearts_from_file=None,
         ball_coords_and_health=None):
    tiles_for_ball = [Tile((300, 500)), Tile((100, 800))]
    thorn_tiles_for_ball = []
    life_hearts = []

    score = score
    background_counter = 0

    ball = Ball()
    ball_speed_adder = 1
    tile_speed_adder = 0.2

    level = load_level()
    if level == 1:
        ball.speed = 3
        Tile.tile_speed = 0.3
        Life_heart.life_heart_speed = 0.3
        ball_speed_adder = 0.5
        tile_speed_adder = 0.1
    elif level == 3:
        ball.y_momentum = 0.4
        ball.speed = 6
        Tile.tile_speed = 2
        Life_heart.life_heart_speed = 2
        ball_speed_adder = 1.5
        tile_speed_adder = 0.4

    if score != 0 and ball_coords_and_health[1] > 0:
        tiles_for_ball.clear()
        for tile in tiles_for_ball_from_file:
            tiles_for_ball.append(Tile(tile))

        for tile in thorn_tiles_for_ball_from_file:
            thorn_tiles_for_ball.append(Tile(tile, thorn_tile_image))

        for heart in life_hearts_from_file:
            life_hearts.append(Life_heart(heart))

        ball = Ball(*ball_coords_and_health)

        level = score // 1000
        ball.gravity_limit += level
        ball.jump_force -= level
        Tile.tile_speed += 0.2 * level
        Life_heart.life_heart_speed += 0.2 * level

    running = True
    click = False
    while running:
        mx, my = pygame.mouse.get_pos()
        if back_button.collided(mx, my):
            if click:
                save_game(score, tiles_for_ball, thorn_tiles_for_ball, life_hearts, ball.get_coords())
                sleep(0.1)
                break

        display.fill((0, 132, 202))

        # make game faster
        score += 1
        score = int(score)
        if score % 1000 < 1:
            ball.gravity_limit += ball_speed_adder
            ball.jump_force -= ball_speed_adder
            Tile.tile_speed += tile_speed_adder
            Life_heart.life_heart_speed += tile_speed_adder

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(score, tiles_for_ball, thorn_tiles_for_ball, life_hearts, ball.get_coords())
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    ball.moving_left = True

                if event.button == 3:
                    ball.moving_right = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    ball.moving_left = False

                if event.button == 3:
                    ball.moving_right = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_game(score, tiles_for_ball, thorn_tiles_for_ball, life_hearts, ball.get_coords())
                    running = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    ball.moving_right = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    ball.moving_left = True
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    ball.y_momentum -= 0.1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    ball.y_momentum += 0.1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    ball.moving_right = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    ball.moving_left = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    ball.y_momentum += 0.1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    ball.y_momentum -= 0.1

        for i in tiles_for_ball + thorn_tiles_for_ball + life_hearts:
            i.update()
        ball.update(tiles_for_ball, thorn_tiles_for_ball, life_hearts)

        delete_tiles(tiles_for_ball)
        delete_life_hearts(life_hearts)
        generate_tiles(tiles_for_ball, thorn_tiles_for_ball, life_hearts)

        display.blit(top_spikes, (0, 50))
        display.blit(top_bar, (0, 0))
        back_button.update()
        draw_life_bar(ball)
        draw_score(score)
        draw_cursor(mx, my)

        if ball.health <= 0:
            update_game()
            death_menu(score)
            running = False

        screen.blit(display, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

    Tile.tile_speed = 1
    Life_heart.life_heart_speed = 1


def main_menu():
    click = False
    while True:

        display.fill((40, 40, 40))

        # checking button presses
        mx, my = pygame.mouse.get_pos()
        if new_game_button.collided(mx, my):
            if click:
                sleep(0.1)
                game()

        if continue_button.collided(mx, my):
            if click:
                sleep(0.1)
                game(*load_game())

        if level_button.collided(mx, my):
            if click:
                sleep(0.1)
                choose_level_menu()

        if records_button.collided(mx, my):
            if click:
                sleep(0.1)
                records_menu()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        continue_button.update()
        new_game_button.update()
        level_button.update()
        records_button.update()
        draw_cursor(mx, my)
        screen.blit(display, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()
