import pygame
from gamelib import base
from gamelib import extended

utility = extended.Utility()


class MainMenu(extended.MenuScene):
    def __init__(self, director=None):
        # Get button width and height positions
        button_width = 300
        button_height = 100
        w_center, h_center = utility.center_rect(button_width, button_height, director.screen_width, director.screen_height)

        # Initialise
        background = extended.BackgroundImage((0, 0, director.screen_width, director.screen_height), ['assets', 'images', 'test.jpg'], 'cover')
        play_button = extended.MainMenuButton(self, {'click': ['load_scene', 'FirstScene']}, (w_center, h_center - 150, button_width, button_height), 'Play')
        options_button = extended.MainMenuButton(self, None, (w_center, h_center, button_width, button_height), 'Options')
        quit_button = extended.MainMenuButton(self, {'click': ['quit']}, (w_center, h_center + 150, button_width, button_height), 'Quit')

        buttons = [play_button, options_button, quit_button]

        music = None

        name = 'MainMenu'

        super().__init__(director, name, buttons, background, music)


class SplashScreen(base.Scene):
    def __init__(self, director=None):
        text_width = 500
        text_height = 150
        w_center, h_center = utility.center_rect(text_width, text_height, director.screen_width, director.screen_height)
        name = 'Splash'

        super().__init__(director, name)

        self.developer_name = base.Text((w_center, h_center, text_width, text_height), 'Zeloxa', base.NEW_FONT, base.Colors.WHITE)

        self.fade_in_stuff = pygame.Surface((director.screen.get_rect().width, director.screen.get_rect().height))
        self.fade_in_stuff.fill(base.Colors.BLACK)
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
        screen.fill(base.Colors.BLACK)
        self.developer_name.draw(screen)
        screen.blit(self.fade_in_stuff, self.fade_in_stuff.get_rect())


class FirstGameScene(extended.AdvancedPlatformScene):
    def __init__(self, director=None):
        level_assets = extended.LoadedImages(
            ['assets', 'images', 'bricks.png'],
            ['assets', 'images', 'SMOrc.jpg']
        )

        level_config = {
            'file': ['data', 'levels', 'level_1.txt'],
            'object_dict': {
                'W': extended.ImageObject(self, 0, 0, 32, 32, level_assets['bricks.png']),
                'L': extended.Wall(self, 0, 0, 32, 32)
            },
            'width_constant': 32,
            'background': ['assets', 'images', 'test.jpg'],
            'name': 'FirstScene',
            'player': extended.Player(self, 500, -1000, 32, 32, 500),
        }

        super().__init__(director, level_config)
