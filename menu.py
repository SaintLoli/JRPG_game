import pygame
import pygame_gui
import os
import sys
from DBWorker import *


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def menu_call():
    pygame.init()
    size = width, height = 660, 660
    screen = pygame.display.set_mode(size)
    MAIN_MENU = load_image('data/menu.png')

    running = True
    manager = pygame_gui.UIManager((660, 660))

    begin = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 330), (220, 40)), text='Начать новую игру',
                                         manager=manager)
    load_game = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 390), (220, 40)), text='Продолжить',
                                             manager=manager)
    if not InfoAboutHero.is_save():
        load_game.disable()

    options = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 450), (220, 40)), text='Опции',
                                           manager=manager)
    exit_game = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 510), (220, 40)), text='Выйти из игры',
                                             manager=manager)

    clock = pygame.time.Clock()

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_game:
                    sys.exit()

                if event.ui_element == begin:
                    InfoAboutHero.reset_game()
                    running = False

                if event.ui_element == load_game:
                    running = False

                if event.ui_element == options:
                    print('В скором времени здесь будут опции')

            manager.process_events(event)

        screen.blit(MAIN_MENU, (0, 0))
        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()


InfoAboutHero = DBWork()