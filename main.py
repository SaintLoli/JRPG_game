import pygame
import pytmx
import pygame_gui
import sys
import os
from global_map import *

pygame.init()
size = width, height = 660, 660
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Map:
    def __init__(self, loc_name):
        self.location = loc_name
        self.map = pytmx.load_pygame(f'data/maps/{self.location}')
        self.width = self.map.width
        self.walk_block = GLOBAL_MAP[self.location]['tiles']
        self.height = self.map.height
        self.tile_size = 60

    def render(self, args=()):
        j, i = 0, 0
        for y in range(args[1] - 5, args[1] + 6):
            for x in range(args[0] - 5, args[0] + 6):
                for k in self.map.layers[:-1]:
                    image = self.map.get_tile_image(x, y, k.id - 1)
                    if image:
                        image = pygame.transform.scale(image, (60, 60))
                        screen.blit(image, (i * self.tile_size, j * self.tile_size))
                i += 1
            j += 1
            i = 0


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, columns, rows, xs, ys):
        super().__init__(all_sprites)
        self.coord = (x, y)
        self.key = ''

        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.sprites = self.frames[0:3]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.update()
        self.rect = self.rect.move(xs, ys)

        self.rect = self.image.get_rect()
        self.rect.x = 60 * 5
        self.rect.y = 60 * 5 - 20

    def moving(self, key):
        if key.key == 119:
            self.sprites = self.frames[9:]
            if self.get_next_tile((self.coord[0], self.coord[1] - 1)):
                '''self.rect.y -= now_map.tile_size'''
                if not self.check_camera_y() and self.coord[1] <= 5:
                    self.rect.y -= 60
                self.coord = (self.coord[0], self.coord[1] - 1)
                if not self.check_camera_y() and self.coord[1] >= 24:
                    self.rect.y -= 60
        if key.key == 115:
            self.sprites = self.frames[0:3]
            if self.get_next_tile((self.coord[0], self.coord[1] + 1)):
                '''self.rect.y += now_map.tile_size'''
                if not self.check_camera_y() and self.coord[1] >= 24:
                    self.rect.y += 60
                self.coord = (self.coord[0], self.coord[1] + 1)
                if not self.check_camera_y() and self.coord[1] <= 5:
                    self.rect.y += 60
        if key.key == 97:
            self.sprites = self.frames[3:6]
            if self.get_next_tile((self.coord[0] - 1, self.coord[1])):
                '''self.rect.x -= now_map.tile_size'''
                if not self.check_camera_x() and self.coord[0] <= 5:
                    self.rect.x -= 60
                self.coord = (self.coord[0] - 1, self.coord[1])
                if not self.check_camera_x() and self.coord[0] >= 24:
                    self.rect.x -= 60
        if key.key == 100:
            self.sprites = self.frames[6:9]
            if self.get_next_tile((self.coord[0] + 1, self.coord[1])):
                '''self.rect.x += now_map.tile_size'''
                if not self.check_camera_x() and self.coord[0] >= 24:
                    self.rect.x += 60
                self.coord = (self.coord[0] + 1, self.coord[1])
                if not self.check_camera_x() and self.coord[0] <= 5:
                    self.rect.x += 60

        self.update()

    def interact(self):
        if box.visible == 0:
            for x in range(self.coord[0] - 1, self.coord[0] + 2, 2):
                text = self.get_prop(x, self.coord[1])
                if text:
                    try:
                        box.set_text(text)
                    finally:
                        box.set_text(text)
                    box.visible = 1

            for y in range(self.coord[1] - 1, self.coord[1] + 2, 2):
                text = self.get_prop(self.coord[0], y)
                if text:
                    try:
                        box.set_text(text)
                    finally:
                        box.set_text(text)
                    box.visible = 1
        else:
            box.visible = 0

    def get_prop(self, x, y):
        for ob in location.map.layers[-1]:
            if (x, y) == (ob.x // 32, ob.y // 32) and 'text' in ob.properties:
                return ob.properties['text']

    def get_next_tile(self, position):
        global location
        try:
            for i in list(location.map.visible_tile_layers):
                gid = location.map.get_tile_gid(position[0], position[1], i)
                if gid != 0 and location.map.tiledgidmap[gid] not in location.walk_block:
                    return False
            return True
        except Exception:
            if position[1] == 30:
                self.coord = GLOBAL_MAP[location.location]['S'][1]
                self.rect.x, self.rect.y = 60 * 5, -40
                location = Map(GLOBAL_MAP[location.location]['S'][0])
            elif position[1] == -1:
                self.coord = GLOBAL_MAP[location.location]['N'][1]
                self.rect.x, self.rect.y = 60 * 5, height - 20
                location = Map(GLOBAL_MAP[location.location]['N'][0])

    def check_camera_x(self):
        return 0 < self.coord[0] - 5 and self.coord[0] + 6 < 30

    def check_camera_y(self):
        return 0 < self.coord[1] - 5 and self.coord[1] + 6 < 30

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.sprites)
        self.image = pygame.transform.scale(self.sprites[self.cur_frame], (64, 92))


if __name__ == '__main__':
    running = True

    manager = pygame_gui.UIManager((660, 660))
    box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0, 0), (660, 100)), manager=manager,
                                        html_text='', visible=0)

    fps = 60
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    hero = Hero(6, 7, load_image("data/sprites/hero1.png", True), 3, 4, 32, 48)
    location = Map(LOCATION)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [115, 100, 97, 119]:
                    hero.moving(event)

                if event.key == 101:
                    hero.interact()

                if event.key == pygame.K_F5:
                    ...
        if not hero.check_camera_x():
            render = (5 if hero.coord[0] <= 5 else 24, hero.coord[1])
        elif not hero.check_camera_y():
            render = (hero.coord[0], 5 if hero.coord[1] <= 5 else 24)
        else:
            render = hero.coord
        location.render(render)

        manager.update(fps)
        manager.draw_ui(screen)

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)



    pygame.quit()