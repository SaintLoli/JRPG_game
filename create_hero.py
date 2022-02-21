import os
import sys
import pygame
import pygame_gui
from DBWorker import DBWork

all_sprites = pygame.sprite.Group()


class AnimatedHero(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super(AnimatedHero, self).__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.sprites = self.frames[0:3]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.update()

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
        self.image = pygame.transform.scale(self.sprites[self.cur_frame], (200, 300))


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def open_hero_creation_window(n, delete=None):
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Times New Roman', 15)
    heroList = [i[:-4] for i in os.listdir('data/sprites')]
    if delete:
        heroList.remove(delete)
    classList = ['Воин', 'Разбойник', 'Маг', 'Клирик']

    size = width, height = 660, 660
    screen = pygame.display.set_mode(size)
    background = load_image('data/menu.png')

    manager = pygame_gui.UIManager((660, 660), 'theme.json')
    set_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 110), (250, 35)), manager=manager)
    classInfo = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((30, 440), (600, 120)), manager=manager, html_text='')
    classInfo.hide()
    beginGame = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 590), (130, 40)), text='Начать игру', manager=manager)

    go_to_create_second_hero = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 590), (300, 40)), text='Перейти ко второму герою', manager=manager)
    go_to_create_second_hero.disable()
    if n == 2:
        go_to_create_second_hero.hide()

    if n == 1:
        beginGame.hide()

    change_hero = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(relative_rect=pygame.Rect((350, 175), (250, 35)), manager=manager, options_list=heroList, starting_option='Выберите героя')
    change_class = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(relative_rect=pygame.Rect((350, 250), (250, 35)), manager=manager, options_list=classList, starting_option='Выберите класс')

    label1 = font.render("Имя персонажа:", True, (19, 46, 98))
    font = pygame.font.SysFont('Times New Roman', 48, bold=True)
    label2 = font.render(f'Герой №{n}', True, (19, 46, 98))

    hero_image = ''
    show_hero = ''

    running = True
    HERO_ANIM = pygame.USEREVENT + 2
    pygame.time.set_timer(HERO_ANIM, 140)
    clock = pygame.time.Clock()
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            manager.process_events(event)

            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == change_hero:
                    if show_hero:
                        show_hero.remove(show_hero.groups()[0])
                    hero_image = AnimatedHero(load_image(f'data/sprites/{change_hero.selected_option}.png'), 3, 4)
                    show_hero = pygame_gui.elements.ui_image.UIImage(relative_rect=pygame.Rect((70, 90), (200, 300)), manager=manager, image_surface=hero_image.image)
                    set_name.set_text(change_hero.selected_option)

                if event.ui_element == change_class:
                    classInfo.show()
                    classInfo.set_text(DBWork().get_info_about_class(change_class.selected_option))

                if change_hero.selected_option != 'Выберите героя' and change_class.selected_option != 'Выберите класс':
                    go_to_create_second_hero.enable()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == beginGame or event.ui_element == go_to_create_second_hero:
                    return change_hero.selected_option

            if event.type == HERO_ANIM:
                if hero_image:
                    hero_image.update()
                    show_hero.image = hero_image.image

        set_name.redraw()

        screen.blit(background, (0, 0))
        screen.blit(label1, (355, 90))
        screen.blit(label2, (200, 0))
        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    open_hero_creation_window(1)
    open_hero_creation_window(2)