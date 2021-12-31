import pygame
import pytmx
import sys
import os


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode((768, 768))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Map:
    def __init__(self, walk_block):
        self.map = pytmx.load_pygame('test.tmx')
        self.width = self.map.width
        self.walk_block = walk_block
        print(self.walk_block)
        print(self.width)
        self.height = self.map.height
        self.tile_size = 70
        self.render()

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                image = pygame.transform.scale(image, (70, 70))
                screen.blit(image, (x * self.tile_size, y * self.tile_size))


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.coord = (x, y)
        self.image = load_image('fore.png')

        self.rect = self.image.get_rect()
        self.rect.x = 70 * x + 5
        self.rect.y = 70 * y + 1

    def moving(self, key):
        if key == 'w':
            if now_map.map.get_tile_properties_by_gid(now_map.map.get_tile_gid(self.coord[0],
                                                                               self.coord[1] - 1, 0))['id'] in now_map.walk_block:
                self.image = load_image('back.png')
                self.rect.y -= 70
                self.coord = (self.coord[0], self.coord[1] - 1)
        if key == 's':
            if now_map.map.get_tile_properties_by_gid(now_map.map.get_tile_gid(self.coord[0],
                                                                               self.coord[1] + 1, 0))['id'] in now_map.walk_block:
                self.image = load_image('fore.png')
                self.rect.y += 70
                self.coord = (self.coord[0], self.coord[1] + 1)
        if key == 'a':
            if now_map.map.get_tile_properties_by_gid(now_map.map.get_tile_gid(self.coord[0] - 1,
                                                                               self.coord[1], 0))['id'] in now_map.walk_block:
                self.image = load_image('left.png')
                self.rect.x -= 70
                self.coord = (self.coord[0] - 1, self.coord[1])
        if key == 'd':
            if now_map.map.get_tile_properties_by_gid(now_map.map.get_tile_gid(self.coord[0] + 1,
                                                                               self.coord[1], 0))['id'] in now_map.walk_block:
                self.image = load_image('right.png')
                self.rect.x += 70
                self.coord = (self.coord[0] + 1, self.coord[1])


if __name__ == '__main__':
    screen.fill('orange')
    running = True

    fps = 60
    clock = pygame.time.Clock()

    now_map = Map([2, 141, 406])
    all_sprites = pygame.sprite.Group()
    hero_sprites = pygame.sprite.Group()

    hero = Hero(6, 4)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == 771:
                hero.moving(event.text)

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
        now_map.render()


    pygame.quit()