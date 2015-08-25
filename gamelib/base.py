import pygame
import sys
import os

pygame.font.init()
pygame.mixer.init()

DEFAULT_FONT = pygame.font.Font('Arial.ttf', 35)
NEW_FONT = pygame.font.Font('Arial.ttf', 90)


class Colors:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (125, 125, 125)


# /===================================/
#  Director
# /===================================/


class Director:
    def __init__(self, game_name=None):
        # Get screen dimensions
        self.screen_width = 800
        self.screen_height = 600

        icon = pygame.image.load('zeloxa.icns')
        pygame.display.set_icon(icon)
        # Initialise screen surface
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Set game name
        pygame.display.set_caption(game_name)

        # Initialise director variables
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()
        self.scenes = {}
        self.start_time = pygame.time.get_ticks()

        # Initialise active scene
        self.active_scene = None

        # Initialise delta time variables
        self.delta_time = 0
        self.elapsed_time = 0

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
        self.screen.fill(Colors.BLACK)

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
            self.rect = pygame.Rect(0, 0, 100, 100)
        else:
            self.rect = pygame.Rect(rect)

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
    def __init__(self, rect=None, caption=None, font=DEFAULT_FONT, font_color=Colors.WHITE, centered=True):
        super().__init__(rect)

        # Set caption
        self._caption = caption

        # Set font
        self._font = font

        # Set font color
        self.font_color = font_color

        # Default to is variable
        self._visible = True

        # Initialise surface
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # Set centered text
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
    def __init__(self, rect=None, caption=None, font=None, font_color=Colors.WHITE, background_color=Colors.BLACK, border=None):

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

        # Create blank surfaces for the button
        self.normal_surface = pygame.Surface(self.rect.size)
        self.toggle_surface = pygame.Surface(self.rect.size)
        self.highlight_surface = pygame.Surface(self.rect.size)

        # Call the initial update to draw the button
        self._update()

    def draw(self, screen):
        if self._visible:
            if self.button_toggled:
                screen.blit(self.toggle_surface, self.rect)
            elif self.mouse_over_button:
                screen.blit(self.highlight_surface, self.rect)
            else:
                screen.blit(self.normal_surface, self.rect)

    def _update(self):
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
            self._source_image = pygame.Surface((100, 100))
        else:
            self._source_image = pygame.image.load(os.path.join(*image)).convert()

        self.surface = pygame.Surface(self.rect.size)
        self._update()

    def draw(self, screen):
        screen.blit(self.surface, self.rect, (0, 0, self.rect.width, self.rect.height))

    def _update(self):
        pass

    def handle_event(self, event):
        pass


# /===================================/
#  Base game object class
# /===================================/


class GameObject:
    def __init__(self, scene=None, x=0, y=0):
        self.scene = scene
        self.x = x
        self.y = y


# /===================================/
#  Camera class
# /===================================/


class Camera:
    def __init__(self, scene, width=100, height=100):
        self.state = pygame.Rect(0, 0, width, height)
        self.scene = scene

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.complex_camera(self.state, target.rect)

    def simple_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        return pygame.Rect(-l + int(self.scene.director.screen_width / 2), -t + int(self.scene.director.screen_height / 2), w, h)

    def complex_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l + int(self.scene.director.screen_width / 2), -t + int(self.scene.director.screen_height / 2), w, h
        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width - int(self.scene.director.screen_width)), l)   # stop scrolling at the right edge
        t = max(-(camera.height - int(self.scene.director.screen_height)), t)  # stop scrolling at the bottom
        #t = min(0, t)

        return pygame.Rect(l, t, w, h)


class ImageSurface(pygame.Surface):
    def __init__(self, file_location):
        source_image = pygame.image.load(os.path.join(*file_location)).convert().copy()
        super().__init__((source_image.get_rect().width, source_image.get_rect().height))

        self.blit(source_image, (0, 0, source_image.get_rect().width, source_image.get_rect().height))

