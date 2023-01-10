import pygame

from random import randint
import random
import sys
import math
from time import sleep


def load_image(file_name, *, ext="png", color_key=True, scale=()):
    image = pygame.image.load(f"{file_name}.{ext}").convert()
    if color_key:
        image.set_colorkey((255, 255, 255))
    if scale:
        image = pygame.transform.scale(
            image, (image.get_width() * scale[0], image.get_height() * scale[1])
        )
    return image


# animation_functions_start_________________________________________________#
def load_animation(path, frame_durations, animation_frames) -> list:
    animation_name = path.split("/")[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + "_" + str(n)
        img_loc = path + "/" + animation_frame_id + ".png"
        animation_image = pygame.image.load(img_loc).convert()
        animation_image = pygame.transform.scale(
            animation_image, (animation_image.get_width(), animation_image.get_height())
        )
        animation_image.set_colorkey((255, 255, 255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value) -> tuple:
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


# animation_functions_end___________________________________________________#


# collide_functions_start___________________________________________________#
def collision_test(rect, tiles) -> list:
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles) -> tuple:
    collision_types = {"top": False, "bottom": False, "right": False, "left": False}
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True
    return rect, collision_types


# collide_functions_end_____________________________________________________#


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pressed_image, coords, display, sound):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.pressed = pressed_image
        self.rect = self.image.get_rect(topleft=coords)
        self.mouse_on = False
        self.display = display
        self.sound = sound

    def update(self):
        if self.mouse_on:
            self.display.blit(self.pressed, self.rect)
        else:
            self.display.blit(self.image, self.rect)

    def collided(self, mx, my):
        previous_mouse = self.mouse_on
        if self.rect.collidepoint((mx, my)):
            self.mouse_on = True
        else:
            self.mouse_on = False
        if (not previous_mouse) and self.mouse_on:
            self.sound.play()
        return self.mouse_on

    def set_coords(self, coords):
        self.rect.topleft = coords

    def copy(self):
        return Button(
            self.image.copy(),
            self.pressed.copy(),
            self.rect.topleft,
            self.display,
            self.sound,
        )


class Slider(pygame.sprite.Sprite):
    def __init__(self, display, coords, size=(200, 20)):
        self.offset = size[1] // 8
        self.radius = size[1] // 2
        self.display = display
        self.size = size

        self.image = pygame.Surface(size)
        pygame.draw.rect(
            self.image,
            (70, 106, 155),
            (
                self.offset,
                self.offset,
                size[0] - self.offset * 2,
                size[1] - self.offset * 2,
            ),
            2,
            self.radius,
        )
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect(center=coords)

        self.point_image = pygame.Surface((size[1], size[1] * 1.5))
        pygame.draw.rect(
            self.point_image,
            (112, 146, 190),
            (0, 0, *self.point_image.get_size()),
            0,
            self.radius,
        )
        pygame.draw.rect(
            self.point_image,
            (70, 106, 155),
            (0, 0, *self.point_image.get_size()),
            2,
            self.radius,
        )
        self.point_image.set_colorkey((0, 0, 0))

        self.point_rect = self.point_image.get_rect(
            center=(coords[0] - size[0] // 2 + self.offset * 2, coords[1])
        )

        self.start, self.end = (
            self.point_rect.centerx,
            self.point_rect.centerx + size[0] - size[1] // 2,
        )
        self.length = self.end - self.start
        self.dragged = False

    def release(self):
        self.dragged = False

    def set_value(self, num):
        self.point_rect.centerx = self.start + self.length * (num)

    def get_value(self) -> int:
        return round((self.point_rect.centerx - self.start) / self.length * 100) / 100

    def update(self, clicked, mouse_pos):
        if clicked and self.rect.collidepoint(mouse_pos):
            self.dragged = True
        if self.dragged:
            if mouse_pos[0] <= self.start:
                self.point_rect.centerx = self.start
            elif mouse_pos[0] >= self.end:
                self.point_rect.centerx = self.end
            else:
                self.point_rect.centerx = mouse_pos[0]

        image = self.image.copy()
        pygame.draw.rect(
            image,
            (112, 146, 190),
            (
                self.offset,
                self.offset,
                self.point_rect.centerx - self.start,
                self.size[1] - self.offset * 2,
            ),
            0,
            self.radius,
        )

        self.display.blit(image, self.rect)
        self.display.blit(self.point_image, self.point_rect)


def chance(num: float = 1.00) -> int:
    return random.randrange(0, 101) <= (round(num, 2) * 100)
