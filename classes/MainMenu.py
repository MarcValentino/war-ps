from classes.Button import MenuButton
from classes.Game import *

PLAY_BUTTON = "Jogar"
OPTIONS_BUTTON = "Opções"
QUIT_BUTTON = "Fechar"

class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.buttons = [
            MenuButton(PLAY_BUTTON, 200),
            MenuButton(OPTIONS_BUTTON, 300),
            MenuButton(QUIT_BUTTON, 400)
        ]
        self.background_image = pygame.image.load('classes/assets/images/bg/main-menu-bg.png')

    def show_options_menu(self):
        print("Abrindo menu de opções...")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            self.screen.fill(WHITE)
            pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for button in self.buttons:
                    if button.is_clicked(event):
                        if button.text == PLAY_BUTTON:
                            game = Game()
                            game.onExecute()
                        elif button.text == OPTIONS_BUTTON:
                            self.show_options_menu()
                        elif button.text == QUIT_BUTTON:
                            running = False

            self.screen.blit(self.background_image, (0, 0))
            for button in self.buttons:
                button.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.run()
