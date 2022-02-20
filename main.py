import pytmx
from global_map import *
from menu import *

pygame.init()
size = width, height = 660, 660
screen = pygame.display.set_mode(size)


class Map:
    def __init__(self, loc_name):
        self.location = loc_name
        self.map = pytmx.load_pygame(f'data/maps/{self.location}.tmx')
        self.width = self.map.width
        self.walk_block = GLOBAL_MAP[self.location]['tiles']
        self.height = self.map.height
        self.tile_size = 60

    def render(self, args=()):
        j, i = 0, 0
        args = list(args)
        if args[0] + 5 > 29:
            args[0] = 24
        if args[1] + 5 > 29:
            args[1] = 24
        if args[0] - 5 < 0:
            args[0] = 5
        if args[1] - 5 < 0:
            args[1] = 5

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
    def __init__(self, coord, sheet, columns, rows, xs, ys):
        super().__init__(all_sprites)
        self.coord = coord
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
        if key == 119:
            self.sprites = self.frames[9:]
            if self.get_next_tile((self.coord[0], self.coord[1] - 1)):
                '''self.rect.y -= now_map.tile_size'''
                if not self.check_camera_y() and self.coord[1] <= 5:
                    self.rect.y -= 60
                self.coord = (self.coord[0], self.coord[1] - 1)
                if not self.check_camera_y() and self.coord[1] >= 24:
                    self.rect.y -= 60
        if key == 115:
            self.sprites = self.frames[0:3]
            if self.get_next_tile((self.coord[0], self.coord[1] + 1)):
                '''self.rect.y += now_map.tile_size'''
                if not self.check_camera_y() and self.coord[1] >= 24:
                    self.rect.y += 60
                self.coord = (self.coord[0], self.coord[1] + 1)
                if not self.check_camera_y() and self.coord[1] <= 5:
                    self.rect.y += 60
        if key == 97:
            self.sprites = self.frames[3:6]
            if self.get_next_tile((self.coord[0] - 1, self.coord[1])):
                '''self.rect.x -= now_map.tile_size'''
                if not self.check_camera_x() and self.coord[0] <= 5:
                    self.rect.x -= 60
                self.coord = (self.coord[0] - 1, self.coord[1])
                if not self.check_camera_x() and self.coord[0] >= 24:
                    self.rect.x -= 60
        if key == 100:
            self.sprites = self.frames[6:9]
            if self.get_next_tile((self.coord[0] + 1, self.coord[1])):
                '''self.rect.x += now_map.tile_size'''
                if not self.check_camera_x() and self.coord[0] >= 24:
                    self.rect.x += 60
                self.coord = (self.coord[0] + 1, self.coord[1])
                if not self.check_camera_x() and self.coord[0] <= 5:
                    self.rect.x += 60

        self.get_prop(self.coord[0], self.coord[1])

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
            if (x, y) == (ob.x // 32, ob.y // 32):
                if 'text' in ob.properties:
                    return ob.properties['text']
                if 'enter' in ob.properties:
                    self.load_new_location(location_name=ob.properties['enter'])

    def get_next_tile(self, position):
        try:
            for i in list(location.map.visible_tile_layers):
                gid = location.map.get_tile_gid(position[0], position[1], i)
                if gid != 0 and location.map.tiledgidmap[gid] not in location.walk_block:
                    return False
            return True
        except Exception:
            self.load_new_location(position=position)

    def load_new_location(self, position=(0, 0), location_name=None):
        global location
        if not location_name:
            if position[1] == 30:
                self.coord = GLOBAL_MAP[location.location]['S'][1]
                if len(GLOBAL_MAP[location.location]['S']) == 2:
                    self.rect.x, self.rect.y = 60 * 5, -40
                else:
                    self.rect.x, self.rect.y = GLOBAL_MAP[location.location]['S'][2]
                location = Map(GLOBAL_MAP[location.location]['S'][0])
            elif position[1] == -1:
                self.coord = GLOBAL_MAP[location.location]['N'][1]
                self.rect.x, self.rect.y = 60 * 5, height - 20
                location = Map(GLOBAL_MAP[location.location]['N'][0])
            elif position[0] == -1:
                self.coord = GLOBAL_MAP[location.location]['W'][1]
                self.rect.x, self.rect.y = width - 60, 60 * 5 - 20
                location = Map(GLOBAL_MAP[location.location]['W'][0])
            elif position[0] == 30:
                self.coord = GLOBAL_MAP[location.location]['E'][1]
                self.rect.x, self.rect.y = 0, 60 * 5 - 20
                location = Map(GLOBAL_MAP[location.location]['E'][0])
        else:
            self.coord = GLOBAL_MAP[location_name]['coord']
            self.rect.x, self.rect.y = 60 * 5, height - 100
            location = Map(location_name)

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
    menu_call()

    running = True
    HERO_WALK = pygame.USEREVENT + 1
    pygame.time.set_timer(HERO_WALK, 95)

    manager = pygame_gui.UIManager((660, 660))
    box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0, 0), (660, 100)), manager=manager,
                                        html_text='', visible=0)

    fps = 60
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    hero = Hero(InfoAboutHero.get_coord(), load_image("data/sprites/hero8.png", True), 3, 4, 32, 48)
    location = Map(InfoAboutHero.get_location())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == 101:
                    hero.interact()

                if event.key == pygame.K_F5:
                    InfoAboutHero.save_game(location.location, hero.coord)
                if event.key == pygame.K_F9:
                    location = Map(InfoAboutHero.get_location())
                    hero.coord = InfoAboutHero.get_coord()

            if event.type == HERO_WALK:
                if pygame.key.get_pressed()[pygame.K_d]:
                    hero.moving(pygame.K_d)
                if pygame.key.get_pressed()[pygame.K_a]:
                    hero.moving(pygame.K_a)
                if pygame.key.get_pressed()[pygame.K_w]:
                    hero.moving(pygame.K_w)
                if pygame.key.get_pressed()[pygame.K_s]:
                    hero.moving(pygame.K_s)

        location.render(hero.coord)

        manager.update(fps)
        manager.draw_ui(screen)

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()