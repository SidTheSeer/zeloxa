import pygame
import os
from . import base


# /===================================/
#  Drawable game object class
# /===================================/


class DrawableGameObject(base.GameObject):
    def __init__(self, scene=None, x=0, y=0, width=100, height=100):
        super().__init__(scene, x, y)

        self.width = width
        self.height = height

        self.surface = pygame.Surface((self.width, self.height))

        self.rect = self.surface.get_rect()

        self.rect.x = x
        self.rect.y = y

        self._update()

    def _update(self):
        raise NotImplementedError('_update not defined in subclass')

    def draw(self, screen, optional_rect=None):
        if type(optional_rect) is None:
            screen.blit(self.surface, self.rect)
        else:
            screen.blit(self.surface, optional_rect)


# /===================================/
#  Menu scene class
# /===================================/


class MenuScene(base.Scene):
    def __init__(self, director=None, name=None, buttons=None, background=None, music=None):
        super().__init__(director, name)

        if buttons is not None:
            if type(buttons) is list:
                self.buttons = buttons
            else:
                raise Exception('Buttons is not a list')

        if background is not None:
            if type(background) is BackgroundImage:
                self.background = background
            else:
                raise Exception('Image is not BackgroundImage')

        if music is not None:
            if type(music) is list:
                self.music = pygame.mixer.Sound(os.path.join(*music))
            else:
                raise Exception('Music is not list')

        if music is not None:
            self.music.play()

    def on_update(self):
        pass

    def on_event(self, events):
        for event in events:
            # If event is mouse related
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                # Send the mouse event to every button
                for button in self.buttons:
                    button.handle_event(event)

    def on_draw(self, screen):
        # Draw the background first
        self.background.draw(screen)

        # Draw buttons over background
        for button in self.buttons:
            button.draw(screen)

    def handle_command(self):
        pass


# /===================================/
#  Background image class
# /===================================/


class BackgroundImage(base.Image):
    def __init__(self, rect=None, image=None, image_type=None):
        if image_type is None:
            self._image_type = 'static'
        elif type(image_type) is str:
            self._image_type = image_type
        else:
            self._image_type = 'static'

        super().__init__(rect, image)

    def _update(self):
        dest_width = self.rect.width
        dest_height = self.rect.height
        source_width = self._source_image.get_rect().width
        source_height = self._source_image.get_rect().height

        image_ratio = source_width / source_height
        dest_ratio = dest_width / dest_height

        new_width = 0
        new_height = 0

        if self._image_type == 'contain':
            if image_ratio <= dest_ratio:
                new_width = dest_height * image_ratio
                new_height = dest_height
            elif image_ratio >= dest_ratio:
                new_width = dest_width
                new_height = dest_width / image_ratio
        elif self._image_type == 'cover':
            if image_ratio <= dest_ratio:
                new_width = dest_width
                new_height = dest_width / image_ratio
            elif image_ratio >= dest_ratio:
                new_width = dest_height * image_ratio
                new_height = dest_height
        elif self._image_type == 'static' or self._image_type is None:
            new_width = dest_width
            new_height = dest_height

        scaled_image = pygame.transform.smoothscale(self._source_image, (int(new_width), int(new_height)))

        scaled_rect = scaled_image.get_rect()
        scaled_rect.center = int(self.rect.width / 2), int(self.rect.height / 2)

        self.surface.blit(scaled_image, scaled_rect)


# /===================================/
#  Main menu button class
# /===================================/


class MainMenuButton(base.Button):
    def __init__(self, scene, commands, rect, caption):
        border_config = {'normal': {'color': base.Colors.WHITE, 'width': 10}, 'toggle': {'color': base.Colors.BLUE, 'width': 10}, 'highlight': {'color': base.Colors.RED, 'width': 10}}
        super().__init__(rect, caption, base.DEFAULT_FONT, base.Colors.WHITE, base.Colors.BLACK, border_config)

        self.scene = scene

        if type(commands) is dict:
            self.click_command = commands['click'] if 'click' in commands else None
            self.enter_command = commands['enter'] if 'enter' in commands else None
            self.exit_command = commands['exit'] if 'exit' in commands else None
            self.move_command = commands['move'] if 'move' in commands else None
            self.down_command = commands['down'] if 'down' in commands else None
            self.up_command = commands['up'] if 'up' in commands else None
        else:
            self.click_command = None
            self.enter_command = None
            self.exit_command = None
            self.move_command = None
            self.down_command = None
            self.up_command = None

    def mouse_click(self, event):
        if self.click_command is not None:
            self.scene.director.handle_command(self.click_command)

    def mouse_enter(self, event):
        # pygame.mouse.set_cursor(*cursors.hover)
        pass

    def mouse_exit(self, event):
        # pygame.mouse.set_cursor(*cursors.normal)
        pass

    def mouse_move(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass


# /===================================/
#  Basic game scene class
# /===================================/


class GameScene(base.Scene):
    def __init__(self, director=None, name=None, entities_list=None):
        super().__init__(director, name)

        if type(entities_list) is list and entities_list is not None:
            self.entities = entities_list

        self.level = []

    def on_event(self, events):
        for event in events:
            pass

    def on_update(self):
        pass

    def on_draw(self, screen):
        for entity in self.entities:
            entity.draw(screen)

    def handle_command(self, command):
        pass


class PlatformScene(base.Scene):
    def __init__(self, director=None, name=None, background=None, walls=None, player=None):
        super().__init__(director, name)

        self.background = background
        self.walls = []
        self.player = player

        self.player_movement = {'left': False, 'right': False, 'jump': False}

        x, y = 0, 0

        for row in walls:
            for col in row:
                if col == "P":
                    p = Wall(self, x, y, 32, 32)
                    self.walls.append(p)
                x += 32
            y += 32
            x = 0

        total_level_width = len(walls[0]) * 32
        total_level_height = len(walls) * 32

        self.camera = base.Camera(self, total_level_width, total_level_height)

    def on_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.player_movement['left'] = True if event.key == pygame.K_a else self.player_movement['left']
                self.player_movement['right'] = True if event.key == pygame.K_d else self.player_movement['right']
                self.player_movement['jump'] = True if event.key == pygame.K_w else self.player_movement['jump']

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player_movement['jump'] = False
                elif event.key == pygame.K_a:
                    self.player_movement['left'] = False
                elif event.key == pygame.K_d:
                    self.player_movement['right'] = False

    def on_update(self):
        self.player.handle_movement(self.walls, self.player_movement)
        self.camera.update(self.player)

    def on_draw(self, screen):
        screen.fill(base.Colors.BLACK)

        for wall in self.walls:
            wall.draw(screen, self.camera.apply(wall))

        self.player.draw(screen, self.camera.apply(self.player))

    def shift_world(self, offset):
        for wall in self.walls:
            wall.rect.x += offset


# /===================================/
#  Basic wall class
# /===================================/


class Wall(DrawableGameObject):
    def _update(self):
        self.surface.fill(base.Colors.RED)


# /===================================/
#  Player class
# /===================================/


class Player(DrawableGameObject):
    def __init__(self, scene=None, x=0, y=0, width=32, height=32, movement_rate=3):
        self.movement_rate = movement_rate

        self.delta_x = 0
        self.delta_y = 0

        self.grounded = False

        super().__init__(scene, x, y, width, height)

    def _update(self):
        self.surface.fill(base.Colors.BLUE)

    def handle_movement(self, collision_objects, movement):
        self.delta_x = 0

        if movement['jump']:
            if self.grounded:
                self.delta_y -= 10

        if movement['left']:
            self.delta_x = -self.movement_rate * self.scene.director.delta_time

        if movement['right']:
            self.delta_x = self.movement_rate * self.scene.director.delta_time

        if movement['right'] and movement['left']:
            self.delta_x = 0

        if not self.grounded:
            self.delta_y += 25 * self.scene.director.delta_time

        self.grounded = False

        self.rect.x += self.delta_x

        for wall in collision_objects:
            if self.rect.colliderect(wall.rect):
                if self.delta_x > 0:
                    self.rect.right = wall.rect.left
                elif self.delta_x < 0:
                    self.rect.left = wall.rect.right

        self.rect.y += self.delta_y

        for wall in collision_objects:
            if self.rect.colliderect(wall.rect):
                if self.delta_y > 0:
                    self.rect.bottom = wall.rect.top
                    self.grounded = True
                elif self.delta_y < 0:
                    self.rect.top = wall.rect.bottom

                self.delta_y = 0

    def calculate_gravity(self):
        self.delta_y += 3 * self.scene.director.delta_time