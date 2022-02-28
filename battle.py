import pygame
import pygame_gui
import sys
from create_hero import load_image, Animate
from DBWorker import DBWork
import random
BASE = DBWork()
all_sprites = pygame.sprite.Group()


class Enemy:
    def __init__(self):
        self.enemies = BASE.get_enemies_imgname()
        self.enemies_count = random.randint(3, 3)

        self.enemies = [[self.enemies[0][0], BASE.get_all_about_enemy(self.enemies[0][0])[2]] for _ in range(self.enemies_count)]

    def enemy_strike(self, i, k_heroes):
        attack = random.randint(BASE.get_all_about_enemy(self.enemies[i][0])[3], BASE.get_all_about_enemy(self.enemies[i][0])[4])
        hero_who_attacked = random.choice([i for i in k_heroes if i.visible == 1])
        return k_heroes.index(hero_who_attacked), attack


class BattleWindow:
    def __init__(self):
        self.move = 0
        self.iter_count = 0
        self.step = 'HEROES'
        self.ef = None
        self.attack_effect = Animate(load_image('data/attack.png'), 5, 1, (140, 140))
        self.attack_effect.sprites = self.attack_effect.frames
        self.is_attack = False
        self.enemies = Enemy()
        self.set_gui()
        self.open_battle()

    def set_gui(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Calibri', 17)
        self.size = width, height = 660, 660
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.transform.scale(load_image('battlemap.png'), (660, 660))
        self.manager = pygame_gui.UIManager((660, 660), 'theme.json')

        self.panels = [pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-2, 518), (164, 144)), starting_layer_height=0, manager=self.manager),
                       pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((159, 518), (164, 144)), starting_layer_height=0, manager=self.manager),
                       pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((321, 518), (341, 144)), starting_layer_height=0, manager=self.manager)]

        self.attack = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.panels[0].rect.x + 5, self.panels[0].rect.y + 5), (self.panels[0].rect.w - 10, 30)),
                                                   text='Атака', manager=self.manager)
        self.special = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.panels[0].rect.x + 5, self.panels[0].rect.y + 40), (self.panels[0].rect.w - 10, 30)),
                                                    text='Способности', manager=self.manager)
        self.special.disable()
        self.items = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.panels[0].rect.x + 5, self.panels[0].rect.y + 75), (self.panels[0].rect.w - 10, 30)),
                                                  text='Предметы', manager=self.manager)
        self.items.disable()
        self.labels = [self.font.render(f'{BASE.get_all_info_about_characters(i)[2]}{" " * (15 - len(i))}'
                                        f'ОЗ:  {BASE.get_all_info_about_characters(i)[4]} / {BASE.get_info_about_class(BASE.get_all_info_about_characters(i)[3])[2]}{" " * 7}'
                                        f'ОМ:  {BASE.get_all_info_about_characters(i)[5]} / {BASE.get_info_about_class(BASE.get_all_info_about_characters(i)[3])[3]}',
                                        True, (255, 255, 255)) for i in BASE.get_heroes()]

        self.images_heroes = []
        for i in range(4):
            if BASE.get_all_info_about_characters(BASE.get_heroes()[i])[4] > 0:
                hero_img = Animate(load_image(f'data/sprites/{BASE.get_heroes()[i]}.png'), 3, 4)
                self.images_heroes.append(pygame_gui.elements.UIImage(pygame.Rect((125 + i * 120, 385), (70, 90)), manager=self.manager,
                                                                      image_surface=pygame.transform.scale(hero_img.frames[10], (70, 90))))

        if not BASE.get_info_about_class(BASE.get_all_info_about_characters(BASE.get_heroes()[0])[3])[6]:
            self.special.disable()

        self.images_enemies = []
        for i in range(self.enemies.enemies_count):
            enemy_img = load_image(f'data/enemies/{self.enemies.enemies[i][0]}.png')
            self.images_enemies.append(pygame_gui.elements.UIImage(pygame.Rect(((490 - 130 * (self.enemies.enemies_count - i)) // 2 + 110 + 55 * i, 120), (130, 130)),
                                                                   manager=self.manager, image_surface=pygame.transform.scale(enemy_img, (130, 130))))

        print(self.images_enemies[0].rect, self.images_enemies[-1].rect)

    def set_move(self):
        self.images_heroes[self.move].rect.y -= 60

    def end_move(self):
        self.images_heroes[self.move].rect.y += 60
        self.move = self.move + 1

        if self.move == len(self.images_heroes):
            self.step = 'ENEMIES'
        self.move %= len(self.images_heroes)

        if not BASE.get_info_about_class(BASE.get_all_info_about_characters(BASE.get_heroes()[self.move])[3])[6]:
            self.special.disable()
        else:
            self.special.enable()

        self.arrow_coord = ()
        self.is_attack = False

    def strike(self, attack, enemy_id):
        self.enemies.enemies[enemy_id][1] -= attack
        self.ef = (self.attack_effect.image, (self.images_enemies[enemy_id].rect.x, self.images_enemies[enemy_id].rect.y))
        self.iter_count = 0
        if self.enemies.enemies[enemy_id][1] <= 0:
            self.images_enemies[enemy_id].hide()
            del self.images_enemies[enemy_id], self.enemies.enemies[enemy_id]
            self.enemies.enemies_count -= 1
            if len(self.images_enemies) == 0:
                print('win')

    def take_damage(self, hero, damage):
        BASE.set_HP(BASE.get_heroes()[hero], BASE.get_all_info_about_characters(BASE.get_heroes()[hero])[4] - damage if BASE.get_all_info_about_characters(BASE.get_heroes()[hero])[4] - damage > 0 else 0)
        self.ef = (self.attack_effect.image, (self.images_heroes[hero].rect.x - 10, self.images_heroes[hero].rect.y))
        if BASE.get_all_info_about_characters(BASE.get_heroes()[hero])[4] <= 0:
            self.images_heroes[hero].visible = 0
        self.images_heroes = [i for i in self.images_heroes if i.visible == 1]

    def death(self):
        print('you lose')
        sys.exit()

    def open_special(self):
        self.special_events = [pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.panels[1].rect.x + 5, self.panels[1].rect.y + 5 + i * 35), (self.panels[1].rect.w - 10, 30)),
                                                            manager=self.manager, text=text) for i, text in
                               enumerate(eval(BASE.get_info_about_class(BASE.get_all_info_about_characters(BASE.get_heroes()[self.move])[3])[6]))]

    def use_special(self, special):
        info = BASE.get_special_info(special)


    def open_battle(self):
        eme = 0
        running = True
        arrow = pygame.transform.scale(load_image('data/arrow.png'), (25, 25))
        self.arrow_coord = ()

        clock = pygame.time.Clock()
        while running:
            try:
                self.screen.blit(self.background, (0, 0))
                time_delta = clock.tick(60) / 1000.0

                if self.images_heroes[self.move].rect.y == 385:
                    self.set_move()

                for event in pygame.event.get():
                    self.manager.process_events(event)

                    if event.type == pygame.QUIT:
                        sys.exit()
                    if 'ui_element' in dir(event) and event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element in [self.attack, self.special, self.items]:
                            if event.ui_element == self.attack:
                                self.arrow_coord = (self.images_enemies[[i.visible for i in self.images_enemies].index(1)].rect.x + 55, 80)
                                self.is_attack = True
                            if event.ui_element == self.special:
                                self.open_special()
                            if event.ui_element == self.items:
                                self.end_move()
                        else:
                            '''self.use_special(event.ui_element.text)'''

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                    if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN) and self.is_attack:
                        for i, sprite in enumerate(self.images_enemies):
                            if sprite.rect.collidepoint(event.pos):
                                self.arrow_coord = (sprite.rect.x + 55, sprite.rect.y - 40)
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    self.strike(random.randint(*BASE.get_attack_power(BASE.get_all_info_about_characters(BASE.get_heroes()[self.move])[3])), i)
                                    self.end_move()

                if self.step == 'ENEMIES':
                    if self.iter_count % 20 == 0:
                        if eme == 0:
                            self.images_enemies[eme].rect.y += 40
                        elif eme <= self.enemies.enemies_count - 1:
                            self.images_enemies[eme].rect.y += 40
                            self.images_enemies[eme - 1].rect.y -= 40
                        if eme < self.enemies.enemies_count - 1 and self.images_enemies[eme].visible:
                            self.iter_count = 0
                            self.take_damage(*self.enemies.enemy_strike(eme, self.images_heroes))
                            eme += 1
                        elif eme == self.enemies.enemies_count - 1:
                            self.take_damage(*self.enemies.enemy_strike(eme, self.images_heroes))
                            eme += 1

                        self.labels = [self.font.render(f'{BASE.get_all_info_about_characters(i)[2]}{" " * (15 - len(i))}'
                                                        f'ОЗ:  {BASE.get_all_info_about_characters(i)[4]} / {BASE.get_info_about_class(BASE.get_all_info_about_characters(i)[3])[2]}{" " * 7}'
                                                        f'ОМ:  {BASE.get_all_info_about_characters(i)[5]} / {BASE.get_info_about_class(BASE.get_all_info_about_characters(i)[3])[3]}',
                                                        True, (255, 255, 255)) for i in BASE.get_heroes()]
                        if eme == self.enemies.enemies_count and self.iter_count == 40:
                            self.iter_count = 0
                            self.images_enemies[eme - 1].rect.y -= 40
                            self.step = 'HEROES'
                            eme = 0

                self.manager.update(time_delta)
                self.manager.draw_ui(self.screen)

                if self.arrow_coord:
                    self.screen.blit(arrow, self.arrow_coord)

                if self.ef:
                    self.screen.blit(*self.ef)
                    if self.iter_count % 2 == 0:
                        self.ef = (self.attack_effect.image, (self.ef[1][0], self.ef[1][1]))
                        self.attack_effect.update((140, 140))

                    if self.iter_count == 10 or self.iter_count == 30:
                        self.ef = None

                for i, name_hero in enumerate(self.labels):
                    self.screen.blit(name_hero, (self.panels[2].rect.x + 5, self.panels[2].rect.y + 30 * i + 15))

                self.iter_count += 1
                pygame.display.flip()
                clock.tick(60)
            except IndexError as error:
                print(error)


if __name__ == '__main__':
    BattleWindow()