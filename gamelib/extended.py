import pygame
import os
import time
from . import base


# /===================================/
#  Drawable game object class
# /===================================/


class DrawableGameObject(base.GameObject):
    def __init__(self, scene=None, x=0, y=0, width=100, height=100):
        super().__init__(scene, x, y)

        self.width = width
        self.height = height

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.rect = self.surface.get_rect()

        self.rect.x = x
        self.rect.y = y

        self._update()

    def _update(self):
        raise NotImplementedError('_update not defined in subclass')

    def draw(self, screen, optional_rect=None):
        if optional_rect is None:
            screen.blit(self.surface, self.rect)
        else:
            screen.blit(self.surface, optional_rect)

    def duplicate(self):
        raise NotImplementedError('duplicate not defined in subclass!')

    def on_update(self, *args, **kwargs):
        pass


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
        destination_width = self.rect.width
        destination_height = self.rect.height
        source_width = self._source_image.get_rect().width
        source_height = self._source_image.get_rect().height

        image_ratio = source_width / source_height
        destination_ratio = destination_width / destination_height

        new_width = 0
        new_height = 0

        if self._image_type == 'contain':
            if image_ratio <= destination_ratio:
                new_width = destination_height * image_ratio
                new_height = destination_height
            elif image_ratio >= destination_ratio:
                new_width = destination_width
                new_height = destination_width / image_ratio
        elif self._image_type == 'cover':
            if image_ratio <= destination_ratio:
                new_width = destination_width
                new_height = destination_width / image_ratio
            elif image_ratio >= destination_ratio:
                new_width = destination_height * image_ratio
                new_height = destination_height
        elif self._image_type == 'static' or self._image_type is None:
            new_width = destination_width
            new_height = destination_height

        scaled_image = pygame.transform.scale(self._source_image, (int(new_width), int(new_height))).convert()

        scaled_rect = scaled_image.get_rect()
        scaled_rect.center = int(self.rect.width / 2), int(self.rect.height / 2)

        self.surface.blit(scaled_image, scaled_rect)

    def draw(self, screen, optional_rect=None):
        if optional_rect is None:
            screen.blit(self.surface, self.rect, (0, 0, self.rect.width, self.rect.height))
        else:
            screen.blit(self.surface, optional_rect, (0, 0, self.rect.width, self.rect.height))


# /===================================/
#  Main menu button class
# /===================================/


class MainMenuButton(base.Button):
    def __init__(self, scene, commands, rect, caption):
        border_config = {'normal': {'color': base.Colors.WHITE, 'width': 10}, 'toggle': {'color': base.Colors.BLACK, 'width': 10}, 'highlight': {'color': base.Colors.RED, 'width': 10}}
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

    def duplicate(self):
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


# /===================================/
#  Basic wall class
# /===================================/


class Wall(DrawableGameObject):
    def _update(self):
        self.surface.fill(base.Colors.BLUE)

    def duplicate(self):
        return Wall(self.scene, self.rect.x, self.rect.y, self.width, self.height)


# /===================================/
#  Player class
# /===================================/


class Player(DrawableGameObject):
    def __init__(self, scene=None, x=0, y=0, width=32, height=32, movement_rate=3, dead_animation=None):
        self.movement_rate = movement_rate

        self.delta_x = 0
        self.delta_y = 0

        self.grounded = False

        self.dead = False

        self.dead_animation = dead_animation

        super().__init__(scene, x, y, width, height)

    def _update(self):
        if self.dead:
            self.dead_animation.play()
            self.surface.blit(self.dead_animation.get_surface(), (0, 0))
        else:
            self.dead_animation.stop()
            self.surface.fill(base.Colors.GREEN)

    def handle_movement(self, collision_objects, movement):
        # Reset the x velocity each frame
        self.delta_x = 0

        # Check if grounded
        self.grounded = self.check_grounded(collision_objects)

        # If player pressed the jump key
        if movement['jump']:
            # If we're grounded
            if self.grounded:
                # Give ourselves upward velocity
                self.delta_y -= 12

        # If player pressed the move left key
        if movement['left']:
            self.delta_x = -self.movement_rate * self.scene.director.delta_time

        # If player pressed the move right key
        if movement['right']:
            self.delta_x = self.movement_rate * self.scene.director.delta_time

        # If player pressed both keys at the same time
        if movement['right'] and movement['left']:
            self.delta_x = 0

        # Gravity
        self.delta_y += 25 * self.scene.director.delta_time

        # Move ourselves on the x axis
        self.rect.x += int(self.delta_x)

        for wall in collision_objects:
            # If we actually changed positions
            if self.delta_x != 0:
                # If we collide with something and its not ourselves
                if self.rect.colliderect(wall.rect) and wall.id != self.id:
                    # If we're going right, then reset our right edge
                    if self.delta_x > 0:
                        self.rect.right = wall.rect.left
                    # If we're going left, reset our left edge
                    elif self.delta_x < 0:
                        self.rect.left = wall.rect.right

        # Move ourselves on the y axis
        self.rect.y += int(self.delta_y)

        for wall in collision_objects:
            # If we actually changed positions
            if self.delta_y != 0:
                # If we collide with something and its not ourselves
                if self.rect.colliderect(wall.rect) and wall.id != self.id:
                    # If we're going up, then reset our top edge
                    if self.delta_y > 0:
                        self.rect.bottom = wall.rect.top
                        # Not needed anymore but I'll keep it here anyway
                        self.grounded = True
                    # If we're going down, then reset our bottom edge
                    elif self.delta_y < 0:
                        self.rect.top = wall.rect.bottom
                        self.grounded = False

                    self.delta_y = 0

    def duplicate(self):
        return Player(self.scene, self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.movement_rate, self.dead_animation)

    def check_grounded(self, collision_objects):
        # Reset variable
        colliding = False

        # Get the rect to check our grounded condition
        # The rect has a width of the original, a height of one and sits
        # one unit below the original rect
        checking_rect = pygame.Rect(int(self.rect.x), int(self.rect.y + self.rect.height), int(self.rect.width), 1)

        # For each object that we can be grounded on
        for wall in collision_objects:
            # Check if the rect collides with it
            if checking_rect.colliderect(wall.rect):
                colliding = True

        # Return the value
        return colliding

    def set_dead(self):
        self.dead = True
        self._update()

    def set_alive(self):
        if self.dead:
            self.dead = False
            self._update()

# /===================================/
#  Utility functions class
# /===================================/


class Utility:
    def __init__(self):
        pass

    @staticmethod
    def center_rect(w, h, c_w, c_h):
        w_center = int((c_w - w) / 2)
        h_center = int((c_h - h) / 2)

        return w_center, h_center


# /===================================/
#  Level interpreting class
# /===================================/


class Level:
    def __init__(self, file_name, width_constant, object_dict):
        # Initialise the dictionary of all the objects in the layers
        self.layers = {}

        # Set the object dictionary
        self.object_dict = object_dict

        # For each key within the object dictionary
        for key in self.object_dict.keys():
            # Get its layer number
            layer_number = self.object_dict[key][1]

            # Initialise the layer it will be in
            self.layers[layer_number] = []

        # If the level file sent is a list
        if type(file_name) is list:
            # Join the array values into a file name
            filename = os.path.join(*file_name)

            # Initialise x and y for the spawning process
            x = 0
            y = 0

            # With the level file
            with open(filename) as fn:
                # Get the lines/level data
                level_data = fn.readlines()

            # Initialise the interpreted data
            new_level_data = []

            # Strip the empty lines
            for line in level_data:
                new_level_data.append(line.rstrip())

            # Strip empty stuff
            level_data = list(filter(None, new_level_data))

            # For each line in the level data file
            for row in level_data:
                # For each character on the line
                for col in row:
                    # For each key within the object dictionary
                    for key in self.object_dict.keys():
                        # If the character is equal the to the key
                        if col == key:
                            # Get its intended layer
                            layer = self.object_dict[key][1]

                            # Duplicate the object
                            level_prop = self.object_dict[key][0].duplicate()

                            # Set the x and y coordinates for this object
                            level_prop.rect.x = x
                            level_prop.rect.y = y

                            # Add it to the layer its intended to be in
                            self.layers[layer].append(level_prop)
                    x += width_constant
                y += width_constant

                # Reset the x position at the beginning of each new line
                x = 0

            # Set the display value for the level width and height
            # At the moment this is only used in the camera
            self.level_width = len(level_data[0]) * width_constant
            self.level_height = len(level_data) * width_constant

    # Have the layers accessible without calling level.layers[i]
    # But rather level[i]
    def __getitem__(self, item):
        return self.layers[item]


# /===================================/
#  Image object class
# /===================================/


class ImageObject(DrawableGameObject):
    def __init__(self, scene=None, x=0, y=0, width=100, height=100, image_surface=None):
        if type(image_surface) is list:
            self._source = pygame.image.load(os.path.join(*image_surface)).convert()
        else:
            self._source = image_surface.copy()

        super().__init__(scene, x, y, width, height)

    def _update(self):
        self.surface = pygame.transform.scale(self._source, (int(self.width), int(self.height))).convert()

    def duplicate(self):
        return ImageObject(self.scene, self.rect.x, self.rect.y, self.width, self.height, self.surface)


# /===================================/
#  Loaded images class
# /===================================/


class LoadedImages:
    def __init__(self, *args):
        self.assets = {}
        for asset in args:
            self.assets[asset[-1]] = base.ImageSurface(asset)

    def __getitem__(self, item):
        return self.assets[item]


# /===================================/
#  Platform scene class
# /===================================/


class AdvancedPlatformScene(base.Scene):
    def __init__(self, director=None, level_config=None):
        super().__init__(director, level_config['name'])

        self.level_config = level_config

        # Define the player
        self.player = self.level_config['player'][0].duplicate()

        # Define the player movement dictionary
        self.player_movement = {'left': False, 'right': False, 'jump': False}

        # Define the level object
        self.level = Level(self.level_config['file'], self.level_config['width_constant'], self.level_config['object_dict'])

        # Define the camera offset object
        self.camera = base.Camera(self, self.level.level_width, self.level.level_height)

        # Set the level background
        if type(self.level_config['background']) is not None:
            self.background = BackgroundImage((0, 0, self.level.level_width, self.level.level_height), self.level_config['background'], 'cover')

        self.game_over = False

    def on_event(self, events):
        for event in events:
            # For player movement keys being pressed down
            if event.type == pygame.KEYDOWN and not self.game_over:
                self.player_movement['left'] = True if event.key == pygame.K_a else self.player_movement['left']
                self.player_movement['right'] = True if event.key == pygame.K_d else self.player_movement['right']
                self.player_movement['jump'] = True if event.key == pygame.K_w else self.player_movement['jump']
            # For player movement keys being let up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player_movement['jump'] = False
                elif event.key == pygame.K_a:
                    self.player_movement['left'] = False
                elif event.key == pygame.K_d:
                    self.player_movement['right'] = False

    def on_update(self):
        if self.game_over:
            self.player_movement['jump'] = False
            self.player_movement['left'] = False
            self.player_movement['right'] = False

        # Handle player movement first
        self.player.handle_movement(self.level[1], self.player_movement)

        # For each object in the physical layer level
        # Call its on_update function
        for layer_number, level_layer in self.level.layers.items():
            for level_object in level_layer:
                level_object.on_update(self.level[1])

        # Update the camera offset to the position
        # of the player before drawing the objects
        self.camera.update(self.player)

    def on_draw(self, screen):
        # Fill the background with black first
        # This gets rid of any object streaking effects
        screen.fill(base.Colors.BLACK)

        # Draw the background first
        self.background.draw(screen, self.camera.apply(self.background))

        # For each object in the physical level layer
        # Call its draw function
        for layer_number, level_layer in self.level.layers.items():
            for level_object in level_layer:
                level_object.draw(screen, self.camera.apply(level_object))

        # Draw the player last
        self.player.draw(screen, self.camera.apply(self.player))

    def on_exit(self):
        self.player_movement = {'left': False, 'right': False, 'jump': False}

        self.level = Level(self.level_config['file'], self.level_config['width_constant'], self.level_config['object_dict'])

        self.player = self.level_config['player'][0].duplicate()

        self.player.rect.x, self.player.rect.y = self.level_config['player'][0].rect.x, self.level_config['player'][0].rect.y

        self.game_over = False


# /===================================/
#  Level config class
# /===================================/
# !!! NOT EVEN SURE IF USED !!!


class LevelConfig:
    def __init__(self, level_file, background, width_constant, config):
        self.level_file = level_file
        self.width_constant = width_constant
        self.background = background
        self.objects = {}
        for key, value in config.iteritems():
            self.objects[key] = value

    def __getitem__(self, item):
        return self.objects[item]


# /===================================/
#  Physics object class
# /===================================/


class PhysicsObject(DrawableGameObject):
    def __init__(self, scene=None, x=0, y=0, width=32, height=32):
        super().__init__(scene, x, y, width, height)
        self.grounded = False
        self.delta_x = 0
        self.delta_y = 0

    def _update(self):
        self.surface.fill(base.Colors.GREEN)

    def duplicate(self):
        return PhysicsObject(self.scene, self.x, self.y, self.width, self.height)

    def on_update(self, collision_objects):
        self.delta_x = 0

        player_x = self.scene.player.rect.x
        self_x = self.rect.x
        diff = abs(player_x - self_x)

        if player_x < self_x and 250 > diff > 2:
            self.delta_x = -200 * self.scene.director.delta_time
        elif player_x > self_x and 250 > diff > 2:
            self.delta_x = 200 * self.scene.director.delta_time

        if not self.grounded:
            self.delta_y += 25 * self.scene.director.delta_time

        self.grounded = False

        self.rect.x += int(self.delta_x)

        for wall in collision_objects:
            if self.delta_x != 0:
                if self.rect.colliderect(wall.rect) and wall.id != self.id:
                    if self.delta_x > 0:
                        self.rect.right = wall.rect.left
                    elif self.delta_x < 0:
                        self.rect.left = wall.rect.right

        self.rect.y += int(self.delta_y)

        for wall in collision_objects:
            if self.rect.colliderect(wall.rect) and wall.id != self.id:
                if self.delta_y > 0:
                    self.rect.bottom = wall.rect.top
                    self.grounded = True
                elif self.delta_y < 0:
                    self.rect.top = wall.rect.bottom

                self.delta_y = 0


class DynamicText(base.Text):
    def update_text(self, text):
        self._caption = str(text)
        self._update()


class Animation:
    def __init__(self, frames):
        self.images = []
        self.durations = []
        self.start_times = []

        self._state = 2
        self.loop = False
        self.rate = 1

        self.play_start_time = 0
        self.pause_start_time = 0

        self.num_frames = len(frames)
        # Add exception for length

        for i in range(self.num_frames):
            frame = frames[i]

            # Add exceptions here

            if type(frame[0]) == list:
                frame = (pygame.image.load(os.path.join(*frame[0])).convert_alpha(), frame[1])
            elif frame[0] is None:
                frame = (pygame.Surface((0, 0)), frame[1])

            self.images.append(frame[0])
            self.durations.append(frame[1])

        self.start_times = self.get_start_times()

    def get_start_times(self):
        start_times = [0]

        for i in range(self.num_frames):
            start_times.append(start_times[-1] + self.durations[i])

        return start_times

    def get_elapsed(self):
        if self._state == 2:
            return 0

        if self._state == 1:
            elapsed = (time.time() - self.play_start_time) * self.rate
        elif self._state == 0:
            elapsed = (self.pause_start_time - self.play_start_time) * self.rate

        if self.loop:
            elapsed = elapsed % self.start_times[-1]
        else:
            elapsed = base.middle_value(0, elapsed, self.start_times[-1])

        elapsed += 0.00001

        return elapsed

    def set_elapsed(self, elapsed):
        elapsed += 0.00001

        if self.loop:
            elapsed = elapsed % self.start_times[-1]
        else:
            elapsed = base.middle_value(0, elapsed, self.start_times[-1])

        right_now = time.time()
        self.play_start_time = right_now - (elapsed * self.rate)

        if self.state in (0, 2):
            self.state = 0
            self.pause_start_time = right_now

    elapsed = property(get_elapsed, set_elapsed)

    def get_state(self):
        if self.is_finished():
            self._state = 2

        return self._state

    def set_state(self, state):
        if state not in (0, 1, 2):
            raise Exception('WRONG STATE')
        if state == 1:
            self.play()
        elif state == 0:
            self.pause()
        elif state == 2:
            self.stop()

    state = property(get_state, set_state)

    def get_surface(self):
        frame_number = base.find_start_times(self.start_times, self.get_elapsed())
        return self.images[frame_number]

    def is_finished(self):
        return not self.loop and self.elapsed >= self.start_times[-1]

    def play(self):
        start_time = time.time()

        if self._state == 1:
            if self.is_finished():
                self.play_start_time = start_time
        elif self._state == 0:
            self.play_start_time = start_time - (self.pause_start_time - self.play_start_time)
        elif self._state == 2:
            self.play_start_time = start_time

        self._state = 1

    def pause(self):
        start_time = time.time()

        if self._state == 0:
            return
        elif self._state == 1:
            self.pause_start_time = start_time
        elif self._state == 2:
            right_now = time.time()
            self.play_start_time = right_now
            self.pause_start_time = right_now

        self._state = 0

    def stop(self):
        if self._state == 2:
            return

        self._state = 2
