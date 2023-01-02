import pygame


def load_image(file_name, *, ext='png', color_key=True, scale=()):
    image = pygame.image.load(f'{file_name}.{ext}').convert()
    if color_key:
        image.set_colorkey((255, 255, 255))
    if scale:
        image = pygame.transform.scale(image, (image.get_width() * scale[0], image.get_height() * scale[1]))
    return image


# animation_functions_start_________________________________________________#
def load_animation(path, frame_durations, animation_frames) -> list:
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image = pygame.transform.scale(animation_image,
                                                 (animation_image.get_width(), animation_image.get_height()))
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
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    return rect, collision_types

# collide_functions_end_____________________________________________________#


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pressed_image, coords, display):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.pressed = pressed_image
        self.rect = self.image.get_rect(topleft=coords)
        self.mouse_on = False
        self.display = display

    def update(self):
        if self.mouse_on:
            self.display.blit(self.pressed, self.rect)
        else:
            self.display.blit(self.image, self.rect)

    def collided(self, mx, my):
        if self.rect.collidepoint((mx, my)):
            self.mouse_on = True
        else:
            self.mouse_on = False
        return self.mouse_on
