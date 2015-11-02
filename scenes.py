import pygame
import math
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
        play_button = extended.MainMenuButton(self, {'click': ['load_scene', 'LevelSelect']}, (w_center, h_center - 150, button_width, button_height), 'Play')
        help_button = extended.MainMenuButton(self, {'click': ['load_scene', 'HelpScene']}, (w_center, h_center, button_width, button_height), 'Help')
        quit_button = extended.MainMenuButton(self, {'click': ['quit']}, (w_center, h_center + 150, button_width, button_height), 'Quit')

        buttons = [play_button, help_button, quit_button]

        music = None

        name = 'MainMenu'

        super().__init__(director, name, buttons, background, music)


class SplashScreen(base.Scene):
    def __init__(self, director=None):
        # Ease
        text_width = 500
        text_height = 150
        w_center, h_center = utility.center_rect(text_width, text_height, director.screen_width, director.screen_height)

        # Scene name
        name = 'Splash'

        super().__init__(director, name)

        # The text on the splash screen
        self.developer_name = base.Text((w_center, h_center, text_width, text_height), 'Zeloxa', base.NEW_FONT, base.Colors.WHITE)

        # My weird way of fading stuff in
        self.fade_in_stuff = base.ColorSurface((director.screen.get_rect().width, director.screen.get_rect().height), base.Colors.BLACK)
        self.alpha = 255

    def on_event(self, events):
        for event in events:
            # Who wants splash screens? :(
            if event.type == pygame.KEYDOWN:
                self.director.handle_command(['load_scene', 'MainMenu'])

    def on_update(self):
        # Have a little black
        if self.director.scene_elapsed_time >= 300:
            self.alpha -= 60 * self.director.delta_time
            self.fade_in_stuff.set_alpha(max(self.alpha, 0))

        # Can't have an infinite splash screen
        if self.director.scene_elapsed_time >= 6000:
            self.director.handle_command(['load_scene', 'MainMenu'])

    def on_draw(self, screen):
        screen.fill(base.Colors.BLACK)
        self.developer_name.draw(screen)
        screen.blit(self.fade_in_stuff, self.fade_in_stuff.get_rect())


class GameScene(extended.AdvancedPlatformScene):
    def __init__(self, director=None, level=None, name=None):
        text_width = 700
        text_height = 150
        w_center, h_center = utility.center_rect(text_width, text_height, director.screen_width, director.screen_height)

        # Preload the image assets and get around file errors inside gamelib
        level_assets = extended.LoadedImages(
            ['assets', 'images', 'bricks.pcx'],
            ['assets', 'images', 'heart.pcx']
        )

        # Color surfaces for animation
        red_surface = base.ColorSurface((100, 100), base.Colors.RED)
        green_surface = base.ColorSurface((100, 100), base.Colors.BLUE)

        # Lazy right
        self.test_animation_thing = extended.Animation([
            (red_surface, 0.2),
            (green_surface, 0.2),
            (red_surface, 0.2),
            (green_surface, 0.2),
            (red_surface, 0.2),
            (green_surface, 0.2),
            (red_surface, 0.2),
            (green_surface, 0.2),
            (red_surface, 0.2),
            (green_surface, 0.2),
        ])

        self.test_animation_thing.loop = False

        # Da level config
        level_config = {
            'file': level,
            'object_dict': {
                'W': [extended.ImageObject(self, 0, 0, 32, 32, level_assets['bricks.pcx']), 1],
                'L': [extended.Wall(self, 0, 0, 32, 32), 1],
                'E': [extended.PhysicsObject(self, 0, 0, 32, 32), 2],
                'A': [extended.EndBlock(self, 0, 0, 32, 32), 0]
            },
            'width_constant': 32,
            'background': ['assets', 'images', 'clouds.pcx'],
            'name': name,
            'music': extended.BackgroundMusic(['assets', 'sounds', 'background.wav']),
            'player': [extended.Player(self, 500, 100, 32, 32, 400, self.test_animation_thing), 3]
        }

        # Da player variables
        # They do actually work
        self.player_variables = {
            'invulnerable_time': 2000,
            'lives': 3
        }

        # Da player runtime variables
        self.player_runtime = {
            'player_reborn_time': 0,
            'current_lives': 3
        }

        super().__init__(director, level_config)

        # Da lives text
        self.lives_text = extended.DynamicText((director.screen_width - 88, 33, 50, 50), 'Lives', base.DEFAULT_FONT, base.Colors.WHITE)

        # Da timer text
        self.timer = extended.DynamicText((20, 20, 50, 50), '0', base.DEFAULT_FONT, base.Colors.WHITE)

        # Da lives text love heart background
        self.life_counter = base.ImageSurface(['assets', 'images', 'heart.pcx'], (85, 85))
        self.life_counter.set_colorkey((255, 255, 255), pygame.RLEACCEL)

        # Da lazy fade in copy paste
        self.fade_in_stuff = base.ColorSurface((director.screen.get_rect().width, director.screen.get_rect().height), base.Colors.BLACK)
        self.game_over_text = base.Text((w_center, h_center, text_width, text_height), 'Game over!', base.NEW_FONT, base.Colors.WHITE)
        self.fade_in_stuff.blit(self.game_over_text.surface, self.game_over_text.rect)
        self.fade_in_stuff.set_alpha(0)
        self.alpha = 0

    def on_event(self, events):
        # Call the superclass on_event
        super().on_event(events)

        for event in events:
            # Kill the enemies if we mouse over them
            if event.type == pygame.MOUSEMOTION:
                for enemy in self.level[2]:
                    # Weird stuff with calling on_event before on_draw with the offsets and stuff
                    if self.camera.apply(enemy).collidepoint(event.pos):
                        # Rip enemy
                        self.level[2].remove(enemy)
            # Skip 6 second end game screen
            elif self.game_over and event.type == pygame.KEYDOWN:
                self.director.handle_command(['load_scene', 'LevelSelect'])

    def on_update(self):
        # Call the superclass on_update
        super().on_update()

        # For each enemy
        for enemy in self.level[2]:
            # Is it colliding with the player and not invulnerable?
            if enemy.rect.colliderect(self.player.rect) and self.director.scene_elapsed_time > self.player_runtime['player_reborn_time']:
                # If we ded den end da game
                if 0 < self.player_runtime['current_lives'] <= 1:
                    self.end_game()
                    self.player_runtime['player_reborn_time'] = self.director.scene_elapsed_time + self.player_variables['invulnerable_time']
                    self.player_runtime['current_lives'] -= 1
                # If we still alive den YAY
                elif self.player_runtime['current_lives'] > 0:
                    self.player_runtime['player_reborn_time'] = self.director.scene_elapsed_time + self.player_variables['invulnerable_time']
                    self.player_runtime['current_lives'] -= 1
            else:
                # What is this here for
                pass

        # If we hit da end of da level end da game
        for end_block in self.level[0]:
            if end_block.rect.colliderect(self.player.rect) and not self.game_over:
                self.end_game()

        # Set da dead and alive animations on da player
        if self.director.scene_elapsed_time < self.player_runtime['player_reborn_time']:
            self.player.set_dead()
        else:
            self.player.set_alive()

        # Update da lives text
        self.lives_text.update_text(self.player_runtime['current_lives'])
        self.timer.update_text(str(math.floor(self.director.scene_elapsed_time / 1000)))

        # If we over den alert da player
        if self.game_over:
            self.alpha += 70 * self.director.delta_time
            self.fade_in_stuff.set_alpha(min(self.alpha, 255))

            if self.director.scene_elapsed_time >= self.game_over_time:
                self.director.handle_command(['load_scene', 'LevelSelect'])

    def on_draw(self, screen):
        # Call the superclass on_draw
        super().on_draw(screen)

        # Draw ALL the things
        screen.blit(self.life_counter, (self.director.screen_width - 105, 20, 85, 85))

        self.lives_text.draw(screen)
        self.timer.draw(screen)

        screen.blit(self.fade_in_stuff, (0, 0))

    def on_exit(self):
        super().on_exit()

        # Reset stuff because otherwise it stuffs up
        self.alpha = 0
        self.fade_in_stuff.set_alpha(0)

        self.player_runtime = {
            'player_reborn_time': 0,
            'current_lives': 3
        }


# Woohoo for classes


class FirstLevel(GameScene):
    def __init__(self, director=None):
        super().__init__(director, ['data', 'levels', 'level_1.txt'], 'FirstLevel')


class SecondLevel(GameScene):
    def __init__(self, director=None):
        super().__init__(director, ['data', 'levels', 'level_2.txt'], 'SecondLevel')


class ThirdLevel(GameScene):
    def __init__(self, director=None):
        super().__init__(director, ['data', 'levels', 'level_3.txt'], 'ThirdLevel')


class LevelSelect(extended.MenuScene):
    # Main meny copy because I was lazy
    def __init__(self, director=None):
        # Get button width and height positions
        button_width = 300
        button_height = 100
        w_center, h_center = utility.center_rect(button_width, button_height, director.screen_width, director.screen_height)

        # Initialize
        background = extended.BackgroundImage((0, 0, director.screen_width, director.screen_height), ['assets', 'images', 'clouds.pcx'], 'cover')
        play_button = extended.MainMenuButton(self, {'click': ['load_scene', 'FirstLevel']}, (w_center, h_center - 150, button_width, button_height), 'Level 1')
        options_button = extended.MainMenuButton(self, {'click': ['load_scene', 'SecondLevel']}, (w_center, h_center, button_width, button_height), 'Level 2')
        quit_button = extended.MainMenuButton(self, {'click': ['load_scene', 'ThirdLevel']}, (w_center, h_center + 150, button_width, button_height), 'Level 3')
        back_button = extended.MainMenuButton(self, {'click': ['load_scene', 'MainMenu']}, (20, director.screen_height - 120, 120, button_height), 'Back')

        buttons = [play_button, options_button, quit_button, back_button]

        music = None

        name = 'LevelSelect'

        super().__init__(director, name, buttons, background, music)


class HelpScene(base.Scene):
    # Main meny copy because I was lazy again
    def __init__(self, director=None):
        button_width = director.screen_width
        button_height = 100
        w_center, h_center = utility.center_rect(button_width, button_height, director.screen_width, director.screen_height)

        captions = [
            'Mouse over enemies to delete them.',
            'Get to the right side to win.',
            'Have fun!',
            'WOH LOOK SOME TEXT THAT NO ONE WILL SEE',
            'HEY TEACHER!'
        ]

        self.help_text_1 = base.Text((w_center, h_center - 120, button_width, button_height), captions[0])
        self.help_text_2 = base.Text((w_center, h_center, button_width, button_height), captions[1])
        self.help_text_3 = base.Text((w_center, h_center + 120, button_width, button_height), captions[2])

        self.back_button = extended.MainMenuButton(self, {'click': ['load_scene', 'MainMenu']}, (20, director.screen_height - 120, 120, button_height), 'Back')

        name = 'HelpScene'

        super().__init__(director, name)

    def on_event(self, events):
        # You don't want to get stuck in this scene do you?
        for event in events:
            self.back_button.handle_event(event)

    def on_update(self):
        # Stuff raise exception I'm too lazy to delete it
        pass

    def on_draw(self, screen):
        self.help_text_1.draw(screen)
        self.help_text_2.draw(screen)
        self.help_text_3.draw(screen)

        self.back_button.draw(screen)
