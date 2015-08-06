import pygame
import sys
import os

pygame.font.init()
pygame.display.init()
pygame.mixer.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)

DEFAULT_FONT = pygame.font.SysFont('Menlo', 35)
NEW_FONT = pygame.font.SysFont('Helvetica', 90)

# /===================================/
#  Director
# /===================================/


class Director():
    def __init__(self, game_name=None):
        # Get screen dimensions
        self.screen_width = 800  # int(pygame.display.Info().current_w)
        self.screen_height = 600  # int(pygame.display.Info().current_h)

        # Initialise screen surface
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

        # Set game name
        pygame.display.set_caption(game_name)

        # Initialise director variables
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()
        self.scenes = {}
        self.start_time = pygame.time.get_ticks()

        self.active_scene = None

    def loop(self):
        # Main game loop
        while not self.quit_flag:
            # Get a 'global' delta time variable for scenes to access
            self.delta_time = self.clock.tick(60) / 1000
            self.elapsed_time = pygame.time.get_ticks() - self.start_time

            # Get all pygame events in current frame
            events = pygame.event.get()

            for event in events:
                # If system quit signal
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()

            # Detect events
            self.active_scene.on_event(events)

            # Update scene
            self.active_scene.on_update()

            # Draw the screen
            self.active_scene.on_draw(self.screen)

            # Redraw display
            pygame.display.flip()

        # If we break the loop exit the game
        pygame.quit()
        sys.exit()

    def add_scenes(self, scenes):
        # If scenes is a list
        if type(scenes) is list:
            for scene in scenes:
                # For each scene pass a director reference
                scene.director = self

                # Make scenes accessible by name
                self.scenes[str(scene.name)] = scene

    def load_scene(self, scene_name):
        # Fill screen with black to clear all previous outputs
        self.screen.fill(BLACK)

        # Set the active scene for the main game loop
        self.active_scene = self.scenes[scene_name]

        # Pass a director reference to the scene
        self.active_scene.director = self

    def quit(self):
        # Break the loop so the game ends
        self.quit_flag = True

    def handle_command(self, command):
        # Command has to be list
        if type(command) is list:
            if command[0] == 'load_scene':
                self.load_scene(command[1])
            elif command[0] == 'quit':
                self.quit()


# /===================================/
#  Base scene class
# /===================================/


class Scene:
    def __init__(self, director=None, name=None):
        # Set director reference
        if director is not None:
            self.director = director

        if name is not None and type(name) is str:
            self.name = name

    def on_event(self, event):
        # Pass events to scene for processing
        raise NotImplementedError("on_event not defined in subclass")

    def on_update(self):
        # Calculate game logic every frame
        raise NotImplementedError("on_update not defined in subclass")

    def on_draw(self, screen):
        # Draw surfaces within scene
        raise NotImplementedError("on_draw not defined in subclass")


# /===================================/
#  Base GUI Class
# /===================================/


class GUIElement:
    def __init__(self, rect=None):
        # Default to a 100x100 rect
        if rect is None:
            self.rect = pygame.rect.Rect(0, 0, 100, 100)
        else:
            self.rect = pygame.rect.Rect(rect)

    def draw(self, screen):
        raise NotImplementedError('draw not defined in subclass')

    def _update(self):
        raise NotImplementedError('_update not defined in subclass')

    def handle_event(self, event):
        raise NotImplementedError('handle_event not defined in subclass')

# /===================================/
#  General text class
# /===================================/


class Text(GUIElement):
    def __init__(self, rect=None, caption=None, font=None, font_color=WHITE, centered=True):
        super().__init__(rect)

        if caption is None:
            self._caption = None
        else:
            self._caption = caption

        if font is None:
            self._font = DEFAULT_FONT
        else:
            self._font = font

        self.font_color = font_color

        self._visible = True

        # Initalise surface
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self._centered = centered

        # Update to fill surfaces for first time
        self._update()

    def _update(self):
        # Make it easier to code
        w = self.rect.width
        h = self.rect.height

        # Render font
        rendered_text = self._font.render(self._caption, True, self.font_color)
        caption_rect = rendered_text.get_rect()

        # Center text
        if self._centered:
            caption_rect.center = int(w / 2), int(h / 2)

        # Blit text to surface
        self.surface.blit(rendered_text, caption_rect)

    def draw(self, screen):
        # Blit text to screen
        if self._visible:
            screen.blit(self.surface, self.rect)

    def handle_event(self, event):
        pass


# /===================================/
#  General button class
# /===================================/


class Button(GUIElement):
    def __init__(self, rect=None, caption=None, font=None, font_color=WHITE, background_color=BLACK, border=None, normal=None, toggle=None, highlight=None):

        super().__init__(rect)

        # Assign the caption
        if caption is None:
            self._caption = None
        else:
            self._caption = caption

        # Assign the font
        if font is None:
            self._font = DEFAULT_FONT
        else:
            self._font = font

        if border is None:
            self._border = None  # {'normal': [0, None], 'highlight': [0, None], 'toggle': [0, None]}
        else:
            self._border = border

        # Assign the font color
        self.font_color = font_color

        # Assign the background color
        self._bgcolor = background_color

        # Default value for button visibility
        self._visible = True

        # Default values for hover and toggle
        self.button_toggled = False
        self.mouse_over_button = False
        self.last_button_toggled = False

        # Button defaults as normal text button when no custom surfaces are passed
        self.custom_surfaces = False

        if normal is None:
            # Create blank surfaces for the button
            self.normal_surface = pygame.Surface(self.rect.size)
            self.toggle_surface = pygame.Surface(self.rect.size)
            self.highlight_surface = pygame.Surface(self.rect.size)

            # Call the initial update to draw the button
            self._update()
        else:
            self.assign_surfaces(normal, toggle, highlight)

        self.orig_normal_surface = None
        self.orig_highlight_surface = None
        self.orig_toggle_surface = None

    def draw(self, screen):
        if self._visible:
            if self.button_toggled:
                screen.blit(self.toggle_surface, self.rect)
            elif self.mouse_over_button:
                screen.blit(self.highlight_surface, self.rect)
            else:
                screen.blit(self.normal_surface, self.rect)

    def _update(self):

        # If using custom surfaces
        if self.custom_surfaces:
            self.normal_surface = pygame.transform.smoothscale(self.orig_normal_surface, self.rect.size)
            self.toggle_surface = pygame.transform.smoothscale(self.orig_toggle_surface, self.rect.size)
            self.highlight_surface = pygame.transform.smoothscale(self.orig_highlight_surface, self.rect.size)
            return

        w = self.rect.width
        h = self.rect.height

        # Fill the background color for all states
        self.normal_surface.fill(self._bgcolor)
        self.toggle_surface.fill(self._bgcolor)
        self.highlight_surface.fill(self._bgcolor)

        # Draw the caption text
        rendered_text = self._font.render(self._caption, True, self.font_color, self._bgcolor)
        caption_rect = rendered_text.get_rect()
        caption_rect.center = int(w / 2), int(h / 2)
        self.normal_surface.blit(rendered_text, caption_rect)
        self.toggle_surface.blit(rendered_text, caption_rect)
        self.highlight_surface.blit(rendered_text, caption_rect)

        if self._border is not None:
            pygame.draw.rect(self.normal_surface, self._border['normal']['color'], pygame.Rect((0, 0, w, h)), self._border['normal']['width'])
            pygame.draw.rect(self.toggle_surface, self._border['toggle']['color'], pygame.Rect((0, 0, w, h)), self._border['toggle']['width'])
            pygame.draw.rect(self.highlight_surface, self._border['highlight']['color'], pygame.Rect((0, 0, w, h)), self._border['highlight']['width'])

    def handle_event(self, event_object):

        # If event is not relevant or button not visible
        if event_object.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP) or not self._visible:
            return

        has_exited = False

        # If mouse not over button previously but over button now
        if not self.mouse_over_button and self.rect.collidepoint(event_object.pos):
            # Mouse has entered the button
            self.mouse_over_button = True
            self.mouse_enter(event_object)
        # If mouse over button previously but no over button now
        elif self.mouse_over_button and not self.rect.collidepoint(event_object.pos):
            self.mouse_over_button = False
            has_exited = True

        if self.rect.collidepoint(event_object.pos):
            if event_object.type == pygame.MOUSEMOTION:
                self.mouse_move(event_object)
            elif event_object.type == pygame.MOUSEBUTTONDOWN:
                self.button_toggled = True
                self.last_button_toggled = True
                self.mouse_down(event_object)
        else:
            if event_object.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                self.last_button_toggled = False

        do_mouse_click = False
        if event_object.type == pygame.MOUSEBUTTONUP:
            if self.last_button_toggled:
                do_mouse_click = True
            self.last_button_toggled = False

            if self.button_toggled:
                self.button_toggled = False
                self.mouse_up(event_object)

            if do_mouse_click:
                self.button_toggled = False
                self.mouse_click(event_object)

        if has_exited:
            self.mouse_exit(event_object)

    def assign_surfaces(self, normal, toggle=None, highlight=None):

        # If toggle or highlight surface or reference not sent
        if toggle is None:
            toggle = normal
        if highlight is None:
            highlight = normal

        if type(normal) == str:
            self.orig_normal_surface = pygame.image.load(normal)
        if type(toggle) == str:
            self.orig_toggle_surface = pygame.image.load(toggle)
        if type(highlight) == str:
            self.orig_highlight_surface = pygame.image.load(highlight)

        if normal.get_size() != toggle.get_size() != highlight.get_size():
            raise Exception('Surfaces not same size!')

        self.normal_surface = self.orig_normal_surface
        self.toggle_surface = self.orig_toggle_surface
        self.highlight_surface = self.orig_highlight_surface
        self.custom_surfaces = True

    def mouse_click(self, event):
        raise NotImplementedError("mouse_click not defined in subclass")

    def mouse_enter(self, event):
        raise NotImplementedError("mouse_enter not defined in subclass")

    def mouse_exit(self, event):
        raise NotImplementedError("mouse_exit not defined in subclass")

    def mouse_move(self, event):
        raise NotImplementedError("mouse_move not defined in subclass")

    def mouse_down(self, event):
        raise NotImplementedError("mouse_down not defined in subclass")

    def mouse_up(self, event):
        raise NotImplementedError("mouse_up not defined in subclass")


# /===================================/
#  General image class
# /===================================/


class Image(GUIElement):
    def __init__(self, rect=None, image=None):
        super().__init__(rect)

        if image is None:
            image = pygame.Surface((100, 100))
        else:
            self._source_image = pygame.image.load(os.path.join(*image)).convert()

        self.surface = pygame.Surface(self.rect.size)
        self._update()

    def draw(self, screen):
        screen.blit(self.surface, self.rect, (0, 0, self.rect.width, self.rect.height))

    def _update(self):
        pass

    def handle_event(self):
        pass


# /===================================/
#  Extended classes
# /===================================/
#
# From this point on, all classes will be classes to
# extended classes from the base classes above

# /===================================/
#  Menu scene class
# /===================================/


class MenuScene(Scene):
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


class BackgroundImage(Image):
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


class MainMenuButton(Button):
    def __init__(self, scene, commands, rect, caption):
        border_config = {'normal': {'color': WHITE, 'width': 10}, 'toggle': {'color': BLUE, 'width': 10}, 'highlight': {'color': RED, 'width': 10}}
        super().__init__(rect, caption, DEFAULT_FONT, WHITE, BLACK, border_config)

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


class GameScene(Scene):
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


class PlatformScene(Scene):
    def __init__(self, director=None, name=None, background=None, walls=None, player=None):
        super().__init__(director, name)

        self.background = background
        self.walls = walls
        self.player = player

        self.player_movement = {'moveUp': 0, 'moveDown': 0, 'moveLeft': 0, 'moveRight': 0}

    def on_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.player_movement['moveUp'] = self.player.movement_rate if event.key == pygame.K_w else self.player_movement['moveUp']
                self.player_movement['moveDown'] = self.player.movement_rate if event.key == pygame.K_s else self.player_movement['moveDown']
                self.player_movement['moveLeft'] = self.player.movement_rate if event.key == pygame.K_a else self.player_movement['moveLeft']
                self.player_movement['moveRight'] = self.player.movement_rate if event.key == pygame.K_d else self.player_movement['moveRight']

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player_movement['moveUp'] = 0
                elif event.key == pygame.K_s:
                    self.player_movement['moveDown'] = 0
                elif event.key == pygame.K_a:
                    self.player_movement['moveLeft'] = 0
                elif event.key == pygame.K_d:
                    self.player_movement['moveRight'] = 0

        self.player.delta_x = int((self.player_movement['moveRight'] - self.player_movement['moveLeft']) * self.director.delta_time)
        self.player.delta_y = int((self.player_movement['moveDown'] - self.player_movement['moveUp']) * self.director.delta_time)

    def on_update(self):
        self.player.handle_movement(self.walls)

        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500
            self.player.rect.right = 500
            self.shift_world(-diff)

        if self.player.rect.left <= 120:
            diff = 120 - self.player.rect.left
            self.player.rect.left = 120
            self.shift_world(diff)

    def on_draw(self, screen):
        screen.fill(BLACK)

        for wall in self.walls:
            wall.draw(screen)

        self.player.draw(screen)

    def shift_world(self, offset):
        for wall in self.walls:
            wall.rect.x += offset


# /===================================/
#  Base game object class
# /===================================/


class GameObject:
    def __init__(self, scene=None, x=0, y=0):
        self.scene = scene
        self.x = x
        self.y = y


# /===================================/
#  Basic wall class
# /===================================/


class Wall(GameObject):
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
        self.surface.fill(RED)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class Player(GameObject):
    def __init__(self, scene=None, x=0, y=0, width=100, height=100, movement_rate=3):
        super().__init__(scene, x, y)

        self.width = width
        self.height = height

        self.surface = pygame.Surface((self.width, self.height))

        self.rect = self.surface.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.movement_rate = movement_rate

        self.delta_x = 0
        self.delta_y = 0

        self._update()

    def _update(self):
        self.surface.fill(BLUE)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def handle_movement(self, collision_objects):
        self.x += self.delta_x
        self.y += self.delta_y

        self.rect.x += self.delta_x

        for thing in collision_objects:
            if self.rect.colliderect(thing.rect):
                if self.delta_x > 0:
                    self.rect.right = thing.rect.left
                else:
                    self.rect.left = thing.rect.right

        self.rect.y += self.delta_y

        for thing in collision_objects:
            if self.rect.colliderect(thing.rect):
                if self.delta_y > 0:
                    self.rect.bottom = thing.rect.top
                else:
                    self.rect.top = thing.rect.bottom

        self.rect.clamp_ip(self.scene.director.screen.get_rect())
