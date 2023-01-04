from tools import *


def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image


class Font:
    def __init__(self, path, size):
        self.spacing = size
        self.ocharacters_order = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                  'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8',
                                  '9', '0', '?', '!', '<', '>', '[', ']', '%', '-', '/']
        font_img = pygame.image.load(path).convert()
        font_img.set_colorkey((0, 0, 0))
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 237:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                char_ = char_img.copy()
                self.characters[self.ocharacters_order[character_count]] = pygame.transform.scale(char_, (
                char_.get_width() * size, char_.get_height() * size))
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['a'].get_width()
        self.space_height = self.characters['a'].get_height()

    def render(self, text, color):
        length = 0
        for char in text:
            if char in "abcdefgjkmnopqsuvxyz234567890":
                length += 4
            elif char in "ilt1?%/":
                length += 3
            elif char in "<>[]-":
                length += 2
            elif char in "!":
                length += 1
            else:
                length += 4
        length *= self.spacing
        length += (self.spacing * (len(text) + 1))
        res_surf = pygame.Surface((length, self.space_height + 1))
        color_surf = pygame.Surface((length, self.space_height + 1))
        color_surf.fill(color)
        color_surf.set_alpha(254)
        # делаем шрифт цветным засчёт заливания всей поверхности полупрозрачной поверхностью
        x_offset = 0
        for char in text:
            if char != " ":
                res_surf.blit(self.characters[char], (x_offset, 0))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing
        res_surf.blit(color_surf, (0, 0))
        res_surf.set_colorkey(res_surf.get_at((0, self.space_height))[:3])

        # pygame.draw.rect(res_surf, (80, 120, 200), (0, 0, *res_surf.get_size()), 2)  # for debugging
        return res_surf


if __name__ == "__main__":
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
