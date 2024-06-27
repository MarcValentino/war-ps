import pygame
from classes.Button import MenuButton
from classes.Game import *
from classes.Jukebox import Jukebox
from classes.OptionsMenu import OptionsMenu

PLAY_BUTTON = "Jogar"
OPTIONS_BUTTON = "Opções"
QUIT_BUTTON = "Fechar"


class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.buttons = [
            MenuButton(PLAY_BUTTON, 200),
            MenuButton(OPTIONS_BUTTON, 300),
            MenuButton(QUIT_BUTTON, 400)
        ]
        self.background_image = pygame.image.load('classes/assets/images/bg/main-menu-bg.png')
        self.in_options_menu = False
        self.options_menu = OptionsMenu(self.exit_options_menu)

    def exit_options_menu(self):
        self.in_options_menu = False

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                jukebox = Jukebox()
                jukebox.check_event()

                if event.type == pygame.QUIT:
                    running = False
                elif self.in_options_menu:
                    self.options_menu.handle_event(event)
                else:
                    for button in self.buttons:
                        if button.is_clicked(event):
                            if button.text == PLAY_BUTTON:
                                game = Game()
                                game.onExecute()
                            elif button.text == OPTIONS_BUTTON:
                                self.in_options_menu = True
                            elif button.text == QUIT_BUTTON:
                                running = False

            if self.in_options_menu:
                self.options_menu.draw()
            else:
                self.screen.blit(self.background_image, (0, 0))
                for button in self.buttons:
                    button.draw(self.screen)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.run()
