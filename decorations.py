from tools import *


class Cube(pygame.sprite.Sprite):
    def __init__(self, display, coords, size, width, round_value, speed, color=30):
        self.display = display
        self.image = pygame.Surface((size, size))
        self.coords = coords
        pygame.draw.rect(self.image, (color,) * 3, (0, 0, size, size), width, round_value)

        self.image.set_colorkey((0, 0, 0))

        self.origin_image = self.image.copy()

        self.angle = 0
        self.rotation_speed = random.randrange(-20, 20) / 10

        self.vx = random.randrange(-2, 3) / 10
        self.vy = speed

    def update(self):
        self.coords[0] += self.vx
        self.coords[1] += self.vy
        self.angle += self.rotation_speed

        self.image = pygame.transform.rotate(self.origin_image, self.angle)
        self.display.blit(self.image, self.image.get_rect(center=self.coords))


class Cubes:
    def __init__(self, display, window_size):
        self.display = display
        self.cubes_list = list()
        self.w_width, self.w_height = window_size

        self.counter = 39
        self.counter_limit = 40

    def update(self):
        self.counter += 1
        if self.counter > self.counter_limit:
            self.counter = 0
            num = randint(30, 90)
            speed = random.randrange(7, 20) / 10
            color = 35 - speed * 8
            self.cubes_list.append(
                Cube(
                    self.display,
                    [randint(50, self.w_width - 50), -100],
                    num,
                    0,
                    num // 10,
                    speed,
                    color,
                )
            )

        i = 0
        while i < len(self.cubes_list):
            self.cubes_list[i].update()
            if self.cubes_list[i].coords[1] > (self.w_height + 100):
                del self.cubes_list[i]
            else:
                i += 1
