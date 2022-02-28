from create_hero import load_image, Animate
import pygame
import pygame_gui
import sys
from DBWorker import DBWork


class LocalMenu:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.size = width, height = 660, 660
        self.screen = pygame.display.set_mode(self.size)
        self.background = load_image('data/menu.png')
        self.BASE = DBWork()
        self.manager = pygame_gui.UIManager((660, 660), 'theme.json')
        self.set_manager_gui()
        self.open_local_menu()

    def set_manager_gui(self):
        self.box_with_options = pygame_gui.elements.UIPanel(pygame.Rect((10, 10), (150, 260)), 0, manager=self.manager)
        self.items = pygame_gui.elements.UIButton(pygame.Rect((self.box_with_options.rect.x + 10, self.box_with_options.rect.y + 10),
                                                              (self.box_with_options.rect.w - 20, 30)), manager=self.manager, text='Предметы')
        self.equipment = pygame_gui.elements.UIButton(pygame.Rect((self.box_with_options.rect.x + 10, self.items.rect.y + 40),
                                                                  (self.box_with_options.rect.w - 20, 30)), manager=self.manager, text='Снаряжение')
        self.exit_game = pygame_gui.elements.UIButton(pygame.Rect((self.box_with_options.rect.x + 10, self.box_with_options.rect.h - 40),
                                                                  (self.box_with_options.rect.w - 20, 30)), manager=self.manager, text='Выйти из игры')
        self.back = pygame_gui.elements.UIButton(pygame.Rect((self.box_with_options.rect.x + 10, self.exit_game.rect.y - 40),
                                                             (self.box_with_options.rect.w - 20, 30)), manager=self.manager, text='Назад')

        self.box_with_information = pygame_gui.elements.UIPanel(pygame.Rect((200, 10), (450, 470)), 0, manager=self.manager)
        self.heroes = [pygame_gui.elements.UIPanel(pygame.Rect((210, (10 * i + 30) + i * 100), (430, 100)), 1, manager=self.manager) for i in range(4)]
        self.labels = {'class': [], 'names': [], 'HP': [], 'MP': []}

        for i, hero in enumerate(self.heroes):
            hero_img = Animate(load_image(f'data/sprites/{self.BASE.get_heroes()[i]}.png'), 3, 4)
            preview_image = pygame_gui.elements.UIImage(pygame.Rect((hero.rect.x + 10, hero.rect.y + 10), (60, 80)), manager=self.manager,
                                                        image_surface=pygame.transform.scale(hero_img.frames[4], (60, 80)))
            self.font = pygame.font.SysFont('Calibri', 15)
            self.labels['class'].append(self.font.render(f"{self.BASE.get_all_info_about_characters(self.BASE.get_heroes()[i])[3]}", True, (255, 255, 255)))
            self.font = pygame.font.SysFont('Calibri', 20)
            self.font.set_bold(True)
            self.labels['names'].append(self.font.render(f"{self.BASE.get_all_info_about_characters(self.BASE.get_heroes()[i])[2]}", True, (255, 255, 255)))
            self.font.set_bold(False)
            self.labels['HP'].append(self.font.render(f"{self.BASE.get_all_info_about_characters(self.BASE.get_heroes()[i])[4]}  /  {self.BASE.get_info_about_class(self.BASE.get_all_info_about_characters(self.BASE.get_heroes()[i])[3])[2]}", True, (255, 255, 255)))
            self.labels['MP'].append(self.font.render(f"{self.BASE.get_all_info_about_characters(self.BASE.get_heroes()[i])[5]}  /  {self.BASE.get_info_about_class(self.BASE.get_all_info_about_characters(self.BASE.get_heroes()[i])[3])[3]}", True, (255, 255, 255)))

    def open_local_menu(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                self.manager.process_events(event)

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED and 'ui_element' in dir(event):
                    if event.ui_element == self.exit_game:
                        sys.exit()
                    if event.ui_element == self.back:
                        running = False
                    if event.ui_element == self.items:
                        print('items')
                    if event.ui_element == self.equipment:
                        print('equipment')

            self.screen.blit(self.background, (0, 0))

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            for key in self.labels.keys():
                for i, label in enumerate(self.labels[key]):
                    if key == 'class':
                        self.screen.blit(label, (self.heroes[i].rect.x + 80, self.heroes[i].rect.y + 10))
                    elif key == 'names':
                        self.screen.blit(label, (self.heroes[i].rect.x + 80, self.heroes[i].rect.y + 35))
                    elif key == 'HP':
                        self.screen.blit(self.font.render("ОЗ: ", True, (255, 255, 255)), (self.heroes[i].rect.x + 260, self.heroes[i].rect.y + 10))
                        self.screen.blit(label, (self.heroes[i].rect.x + 320, self.heroes[i].rect.y + 10))
                    elif key == 'MP':
                        self.screen.blit(self.font.render("MP: ", True, (255, 255, 255)), (self.heroes[i].rect.x + 255, self.heroes[i].rect.y + 35))
                        self.screen.blit(label, (self.heroes[i].rect.x + 320, self.heroes[i].rect.y + 35))

            pygame.display.flip()
            clock.tick(60)


if __name__ == '__main__':
    LocalMenu()