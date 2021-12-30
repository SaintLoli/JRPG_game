import pygame
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('left.png')

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    def moving(self, key):
        if key == 'w':
            self.image = load_image('back.png')
            self.rect.y -= 10
        if key == 's':
            self.image = load_image('fore.png')
            self.rect.y += 10
        if key == 'a':
            self.image = load_image('left.png')
            self.rect.x -= 10
        if key == 'd':
            self.image = load_image('right.png')
            self.rect.x += 10



if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    screen.fill('orange')
    running = True

    fps = 60
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    hero_sprites = pygame.sprite.Group()

    hero = Hero()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == 771:
                hero.moving(event.text)

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
        screen.fill('orange')

    pygame.quit()