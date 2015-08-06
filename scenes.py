import pygame
import gamelib.gamelib as gamelib


class MainMenu(gamelib.MenuScene):
    def __init__(self, director=None):
        # Get button width and height positions
        button_width = 300
        button_height = 100
        w = director.screen.get_rect().width
        h = director.screen.get_rect().height
        w_center = int((w - button_width) / 2)
        h_center = int((h - button_height) / 2)

        # Initialise
        background = gamelib.BackgroundImage((0, 0, w, h), ['assets', 'images', 'test.jpg'], 'cover')
        play_button = gamelib.MainMenuButton(self, {'click': ['load_scene', 'FirstScene']}, (w_center, h_center - 150, 300, 100), 'Play')
        options_button = gamelib.MainMenuButton(self, None, (w_center, h_center, 300, 100), 'Options')
        quit_button = gamelib.MainMenuButton(self, {'click': ['quit']}, (w_center, h_center + 150, 300, 100), 'Quit')

        buttons = [play_button, options_button, quit_button]

        music = None

        name = 'MainMenu'

        super().__init__(director, name, buttons, background, music)


class MainMenu2(gamelib.MenuScene):
    def __init__(self, director=None):
        background = gamelib.BackgroundImage((0, 0, director.screen.get_rect().width, director.screen.get_rect().height), ['assets', 'images', 'test.jpg'], 'cover')

        buttons = [gamelib.MainMenuButton(self, {'click': ['load_scene', 'MainMenu']}, (0, 0, 500, 100), 'SCENE2'), gamelib.MainMenuButton(self, None, (0, 300, 500, 100), 'DERP')]

        music = None

        name = 'MainMenu2'

        super().__init__(director, name, buttons, background, music)


class SplashScreen(gamelib.Scene):
    def __init__(self, director=None):
        text_width = 500
        text_height = 150
        w = director.screen.get_rect().width
        h = director.screen.get_rect().height
        w_center = int((w - text_width) / 2)
        h_center = int((h - text_height) / 2)
        name = 'Splash'

        super().__init__(director, name)

        self.developer_name = gamelib.Text((w_center, h_center, text_width, text_height), 'Zeloxa', gamelib.NEW_FONT, gamelib.WHITE)

        self.fade_in_stuff = pygame.Surface((director.screen.get_rect().width, director.screen.get_rect().height))
        self.fade_in_stuff.fill(gamelib.BLACK)
        self.alpha = 255

    def on_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.director.handle_command(['load_scene', 'MainMenu'])

    def on_update(self):
        self.alpha -= 50 * self.director.delta_time
        self.fade_in_stuff.set_alpha(max(self.alpha, 0))

        if self.director.elapsed_time >= 6000:
            self.director.handle_command(['load_scene', 'MainMenu'])

    def on_draw(self, screen):
        screen.fill(gamelib.BLACK)
        self.developer_name.draw(screen)
        screen.blit(self.fade_in_stuff, self.fade_in_stuff.get_rect())


class FirstGameScene(gamelib.PlatformScene):
    def __init__(self, director=None):
        player = gamelib.Player(self, 0, 0, 100, 100, 250)

        name = 'FirstScene'

        walls = [gamelib.Wall(self, 300, 300, 100, 100)]

        background = None

        super().__init__(director, name, background, walls, player)
