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

        # Initialize
        background = extended.BackgroundImage((0, 0, director.screen_width, director.screen_height), ['assets', 'images', 'clouds.pcx'], 'cover')
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

        if self.director.scene_elapsed_time >= 6000:
            self.director.handle_command(['load_scene', 'MainMenu'])

    def on_draw(self, screen):
        screen.fill(base.Colors.BLACK)
        self.developer_name.draw(screen)
        screen.blit(self.fade_in_stuff, self.fade_in_stuff.get_rect())


class FirstGameScene(extended.AdvancedPlatformScene):
    def __init__(self, director=None):
        level_assets = extended.LoadedImages(
            ['assets', 'images', 'bricks.pcx']
        )

        green_surface = base.ColorSurface((100, 100), base.Colors.GREEN)

        self.test_animation_thing = extended.Animation([
            (level_assets['bricks.pcx'], 0.4),
            (green_surface, 0.4),
            (level_assets['bricks.pcx'], 0.4),
            (green_surface, 0.4),
            (level_assets['bricks.pcx'], 0.4),
            (green_surface, 0.4)
        ])

        self.test_animation_thing.play()
        self.test_animation_thing.loop = True

        level_config = {
            'file': ['data', 'levels', 'level_1.txt'],
            'object_dict': {
                'W': [extended.ImageObject(self, 0, 0, 32, 32, level_assets['bricks.pcx']), 1],
                'L': [extended.Wall(self, 0, 0, 32, 32), 1],
                'E': [extended.PhysicsObject(self, 0, 0, 32, 32), 2]
            },
            'width_constant': 32,
            'background': ['assets', 'images', 'clouds.pcx'],
            'name': 'FirstScene',
            'player': [extended.Player(self, 500, 100, 32, 32, 500, self.test_animation_thing), 3]
        }

        self.player_variables = {
            'invulnerable_time': 3000,
            'lives': 3
        }

        self.player_runtime = {
            'player_reborn_time': 0,
            'current_lives': 3
        }

        super().__init__(director, level_config)

        self.lives_text = extended.DynamicText((0, 0, 500, 100), 'Lives', base.DEFAULT_FONT, base.Colors.WHITE)

    def on_event(self, events):
        # Call the superclass on_event
        super().on_event(events)

    def on_update(self):
        # Call the superclass on_update
        super().on_update()

        # For each enemy
        for enemy in self.level[2]:
            # Is it colliding with the player?
            if enemy.rect.colliderect(self.player.rect) and self.director.scene_elapsed_time > self.player_runtime['player_reborn_time']:
                if self.player_runtime['current_lives'] <= 0:
                    pass
                elif self.player_runtime['current_lives'] > 0:
                    self.player_runtime['player_reborn_time'] = self.director.scene_elapsed_time + self.player_variables['invulnerable_time']
                    self.player_runtime['current_lives'] -= 1
            else:
                pass

        if self.director.scene_elapsed_time < self.player_runtime['player_reborn_time']:
            self.player.set_dead()
        else:
            self.player.set_alive()

        self.lives_text.update_text(self.player_runtime['current_lives'])

    def on_draw(self, screen):
        # Call the superclass on_draw
        super().on_draw(screen)

        self.lives_text.draw(screen)
