import pygame
from gamelib import base
from gamelib import extended


class MainMenu(extended.MenuScene):
    def __init__(self, director=None):
        # Get button width and height positions
        button_width = 300
        button_height = 100
        w = director.screen.get_rect().width
        h = director.screen.get_rect().height
        w_center = int((w - button_width) / 2)
        h_center = int((h - button_height) / 2)

        # Initialise
        background = extended.BackgroundImage((0, 0, w, h), ['assets', 'images', 'test.jpg'], 'cover')
        play_button = extended.MainMenuButton(self, {'click': ['load_scene', 'FirstScene']}, (w_center, h_center - 150, 300, 100), 'Play')
        options_button = extended.MainMenuButton(self, None, (w_center, h_center, 300, 100), 'Options')
        quit_button = extended.MainMenuButton(self, {'click': ['quit']}, (w_center, h_center + 150, 300, 100), 'Quit')

        buttons = [play_button, options_button, quit_button]

        music = None

        name = 'MainMenu'

        super().__init__(director, name, buttons, background, music)


class MainMenu2(extended.MenuScene):
    def __init__(self, director=None):
        background = extended.BackgroundImage((0, 0, director.screen.get_rect().width, director.screen.get_rect().height), ['assets', 'images', 'test.jpg'], 'cover')

        buttons = [extended.MainMenuButton(self, {'click': ['load_scene', 'MainMenu']}, (0, 0, 500, 100), 'SCENE2'), extended.MainMenuButton(self, None, (0, 300, 500, 100), 'DERP')]

        music = None

        name = 'MainMenu2'

        super().__init__(director, name, buttons, background, music)


class SplashScreen(base.Scene):
    def __init__(self, director=None):
        text_width = 500
        text_height = 150
        w = director.screen.get_rect().width
        h = director.screen.get_rect().height
        w_center = int((w - text_width) / 2)
        h_center = int((h - text_height) / 2)
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


class FirstGameScene(extended.PlatformScene):
    def __init__(self, director=None):
        player = extended.Player(self, 500, 0, 32, 32, 500)

        name = 'FirstScene'

        background = None

        walls = [
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P                                          P",
            "P       PPPPPPPPPPP                        P",
            "P                                          P",
            "P     PPPPPPPPPPPP                         P",
            "P                                          P",
            "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        ]

        super().__init__(director, name, background, walls, player)
