import pygame
import os
import time
import math
from . import base


# /===================================/
#  Drawable game object class
# /===================================/


class DrawableGameObject(base.GameObject):
    def __init__(self, scene=None, x=0, y=0, width=100, height=100):
        super().__init__(scene, x, y)

        # Width and height
        self.width = width
        self.height = height

        # The surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # The rect
        self.rect = self.surface.get_rect()

        # Set the x and y
        self.rect.x = x
        self.rect.y = y

        # Call the update method

        self._update()

    def _update(self):
        raise NotImplementedError('_update not defined in subclass')

    def draw(self, screen, optional_rect=None):
        if optional_rect is None:
            screen.blit(self.surface, self.rect)
        else:
            screen.blit(self.surface, optional_rect)

    def duplicate(self):
        # Necessary for level interpretation
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
        # Synatic sugar
        destination_width = self.rect.width
        destination_height = self.rect.height
        source_width = self._source_image.get_rect().width
        source_height = self._source_image.get_rect().height

        image_ratio = source_width / source_height
        destination_ratio = destination_width / destination_height

        new_width = 0
        new_height = 0

        # Algorithm for containing and covering images based on ratios
        # Semi-inspired by a blog post I found somewhere
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

        # Transform the image based off the ratio
        scaled_image = pygame.transform.scale(self._source_image, (int(new_width), int(new_height))).convert()

        # Get the rect
        scaled_rect = scaled_image.get_rect()
        scaled_rect.center = int(self.rect.width / 2), int(self.rect.height / 2)

        # Blit it
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
        # The border config
        border_config = {'normal': {'color': base.Colors.WHITE, 'width': 10}, 'toggle': {'color': base.Colors.BLACK, 'width': 10}, 'highlight': {'color': base.Colors.RED, 'width': 10}}
        super().__init__(rect, caption, base.DEFAULT_FONT, base.Colors.WHITE, base.Colors.BLACK, border_config)

        self.scene = scene

        # If we have some click commands
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


    # This stuff was never used because I didn't need it
    # However it does function as it should
    def mouse_enter(self, event):
        pass

    def mouse_exit(self, event):
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
#  Was the first basic wall I used
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
        # Movement rate
        self.movement_rate = movement_rate

        # Change on each axis
        self.delta_x = 0
        self.delta_y = 0

        # Whether we're groudned
        self.grounded = False

        # Whether we're dead
        self.dead = False

        # Our dead animation
        self.dead_animation = dead_animation

        super().__init__(scene, x, y, width, height)

    def _update(self):
        # If dead, play the animation
        if self.dead:
            self.dead_animation.play()
            self.surface.blit(self.dead_animation.get_surface(), (0, 0))
        # Else do normal stuff
        else:
            self.dead_animation.stop()
            self.surface.fill(base.Colors.BLUE)

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
        self.delta_y = min(15, self.delta_y)

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
#  Pretty useless
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
        # If image file then load it
        if type(image_surface) is list:
            self._source = pygame.image.load(os.path.join(*image_surface)).convert()
        # If surface then copy it
        else:
            self._source = image_surface.copy()

        super().__init__(scene, x, y, width, height)

    def _update(self):
        # Transform the image to fit dimensions
        self.surface = pygame.transform.scale(self._source, (int(self.width), int(self.height))).convert()

    def duplicate(self):
        return ImageObject(self.scene, self.rect.x, self.rect.y, self.width, self.height, self.surface)


# /===================================/
#  Loaded images class
# /===================================/


class LoadedImages:
    def __init__(self, *args):
        self.assets = {}
        # For each file reference sent
        # Load it in and make a surface for it
        for asset in args:
            self.assets[asset[-1]] = base.ImageSurface(asset)

    def __getitem__(self, item):
        # Make this class an iterable object
        return self.assets[item]


# /===================================/
#  Platform scene class
# /===================================/


class AdvancedPlatformScene(base.Scene):
    def __init__(self, director=None, level_config=None):
        super().__init__(director, level_config['name'])

        # Level config
        self.level_config = level_config

        # Define the player
        self.player = self.level_config['player'][0].duplicate()

        # Define the player movement dictionary
        self.player_movement = {'left': False, 'right': False, 'jump': False}

        # Define the level object
        self.level = Level(self.level_config['file'], self.level_config['width_constant'], self.level_config['object_dict'])

        # Define the camera offset object
        self.camera = base.Camera(self, self.level.level_width, self.level.level_height)

        # Set the background music
        self.music = self.level_config['music']

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
        # If game over the player can't move
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
        # Draw the background first
        self.background.draw(screen, self.camera.apply(self.background))

        # For each object in the physical level layer
        # Call its draw function
        for layer_number, level_layer in self.level.layers.items():
            for level_object in level_layer:
                level_object.draw(screen, self.camera.apply(level_object))

        # Draw the player last
        self.player.draw(screen, self.camera.apply(self.player))

    def end_game(self):
        # Game over
        self.game_over = True

        # Reset the game time
        self.game_over_time = self.director.scene_elapsed_time + 5000

    def on_load(self):
        # Play music on scene load
        self.music.play_and_loop()

    def on_exit(self):
        # Reset all the variables on the scene exiting

        self.player_movement = {'left': False, 'right': False, 'jump': False}

        self.level = Level(self.level_config['file'], self.level_config['width_constant'], self.level_config['object_dict'])

        self.player = self.level_config['player'][0].duplicate()

        self.player.rect.x, self.player.rect.y = self.level_config['player'][0].rect.x, self.level_config['player'][0].rect.y

        self.game_over = False

        self.music.stop()


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
#  Physics object class (actually enemy but too many references to change)
#  Was originally going to be a physics classes for other objects to inherit
#  But because I'm lazy it's just an enemy class
# /===================================/


class PhysicsObject(DrawableGameObject):
    def __init__(self, scene=None, x=0, y=0, width=32, height=32):
        super().__init__(scene, x, y, width, height)
        self.grounded = False
        self.delta_x = 0
        self.delta_y = 0

    def _update(self):
        # Make enemies green for no reason
        self.surface.fill(base.Colors.GREEN)

    def duplicate(self):
        return PhysicsObject(self.scene, self.x, self.y, self.width, self.height)

    def on_update(self, collision_objects):
        self.delta_x = 0

        # Synatic sugar
        player_x = self.scene.player.rect.x
        self_x = self.rect.x
        diff = abs(player_x - self_x)

        # If player is less than 350 units away but more than 2
        # If it was less than 2 I had errors with infinite juggling
        if player_x < self_x and 350 > diff > 2:
            self.delta_x = -200 * self.scene.director.delta_time
        elif player_x > self_x and 350 > diff > 2:
            self.delta_x = 200 * self.scene.director.delta_time

        # If not grounded then apply gravity
        if not self.grounded:
            self.delta_y += 25 * self.scene.director.delta_time

        self.grounded = False

        # Standard movement stuff from player

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


# /===================================/
#  Dynamic text class
# /===================================/


class DynamicText(base.Text):
    def update_text(self, text):
        self._caption = str(text)
        self._update()


# /===================================/
#  Animation class
#  I love this class, inspired from a blog post
#  But I understand everything it's doing
#  Some more exceptions could be added but it's just me coding so who cares
# /===================================/


class Animation:
    def __init__(self, frames):
        self.images = []
        self.durations = []
        self.start_times = []

        # 2 is stopped
        # 1 is playing
        # 0 is paused
        self._state = 2
        self.loop = False
        self.rate = 1

        self.play_start_time = 0
        self.pause_start_time = 0

        self.num_frames = len(frames)

        for i in range(self.num_frames):
            frame = frames[i]

            # If the frame is a file reference load its image
            if type(frame[0]) == list:
                frame = (pygame.image.load(os.path.join(*frame[0])).convert_alpha(), frame[1])
            elif frame[0] is None:
                frame = (pygame.Surface((0, 0)), frame[1])

            # Append surface and duration to lists
            self.images.append(frame[0])
            self.durations.append(frame[1])

        # Get the start times once all frame loaded
        self.start_times = self.get_start_times()

    def get_start_times(self):
        start_times = [0]

        # Just get the last value and add the current value
        # It just kind of skips along
        # [x, x + y, (x + y) + z] etc
        for i in range(self.num_frames):
            start_times.append(start_times[-1] + self.durations[i])

        return start_times

    def get_elapsed(self):
        # If stopped we have no running time
        if self._state == 2:
            return 0

        # If playing we use a relative time reference
        if self._state == 1:
            elapsed = (time.time() - self.play_start_time) * self.rate
        # If paused we have to use a pause time because its a difference state
        elif self._state == 0:
            elapsed = (self.pause_start_time - self.play_start_time) * self.rate

        # If we loop then we reset the elapsed when rerun/loop the animation
        if self.loop:
            elapsed = elapsed % self.start_times[-1]
        else:
            # Basically a combined min/max
            elapsed = base.middle_value(0, elapsed, self.start_times[-1])

        # Again some rounding thing?
        elapsed += 0.00001

        return elapsed

    # Not sure if ever used
    def set_elapsed(self, elapsed):
        # From blog post, not sure what its for
        # Apparently rounding errors
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

    # Used as property because of some weird recursive errors
    elapsed = property(get_elapsed, set_elapsed)

    def get_state(self):
        # If done return stopped state
        if self.is_finished():
            self._state = 2

        return self._state

    def set_state(self, state):
        # If state not allowed
        # This method is also used to play and pause if need be
        if state not in (0, 1, 2):
            raise Exception('WRONG STATE')
        if state == 1:
            self.play()
        elif state == 0:
            self.pause()
        elif state == 2:
            self.stop()

    # Again a property because of some recursive stuff
    state = property(get_state, set_state)

    def get_surface(self):
        # Get the surface for the current time
        # Basically how you actually blit the animation
        # We don't keep an active running count of time
        # We only check from relative start times when we actually need the frame
        frame_number = base.find_start_times(self.start_times, self.get_elapsed())
        return self.images[frame_number]

    def is_finished(self):
        # If we don't loop and our elapsed is greater than our last frame time
        return not self.loop and self.elapsed >= self.start_times[-1]

    def play(self):
        # Relative time
        start_time = time.time()

        # If playing and finished, reset our start time and play again
        if self._state == 1:
            if self.is_finished():
                self.play_start_time = start_time
        # If paused, reset the play start time based on the pause start time and stuff whilst retaining relative times
        elif self._state == 0:
            self.play_start_time = start_time - (self.pause_start_time - self.play_start_time)
        # If stopped just reset time altogether
        elif self._state == 2:
            self.play_start_time = start_time

        # We are playing now
        self._state = 1

    def pause(self):
        # Relative time
        start_time = time.time()

        # If paused we need do nothing
        if self._state == 0:
            return
        # If playing reset paused time
        elif self._state == 1:
            self.pause_start_time = start_time
        # If stopped reset all the times
        elif self._state == 2:
            right_now = time.time()
            self.play_start_time = right_now
            self.pause_start_time = right_now

        # We paused now
        self._state = 0

    def stop(self):
        # If we're stopped we don't need to stop
        # (duh)
        if self._state == 2:
            return

        # ME STOP NOW
        self._state = 2


# /===================================/
#  End block class
#  Placeholder invisible block to use for collision detection
#  To end level
#  Could have been a better way but I'm too lazy
# /===================================/


class EndBlock(DrawableGameObject):
    def __init__(self, scene=None, x=0, y=0, width=100, height=100):
        super().__init__(scene, x, y, width, height)

    def _update(self):
        pass

    def duplicate(self):
        return EndBlock(self.scene, self.x, self.y, self.width, self.height)

    def draw(self, screen, optional_rect=None):
        pass


# /===================================/
#  Background music class
# /===================================/


class BackgroundMusic(pygame.mixer.Sound):
    def __init__(self, file):
        # Load file
        super().__init__(os.path.join(*file))

    def play_and_loop(self):
        # Play and loop
        super().play(-1)
