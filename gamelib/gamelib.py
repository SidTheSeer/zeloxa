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
    def __init__(self, gameName=None):
        # Get screen dimensions
        self.screenWidth = 800  # int(pygame.display.Info().current_w)
        self.screenHeight = 600  # int(pygame.display.Info().current_h)

        # Initialise screen surface
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))  # pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

        # Set game name
        pygame.display.set_caption(gameName)

        # Initialise director variables
        self.scene = None
        self.quitFlag = False
        self.clock = pygame.time.Clock()
        self.scenes = {}
        self.startTime = pygame.time.get_ticks()

    def loop(self):
        # Main game loop
        while not self.quitFlag:
            # Get a 'global' delta time variable for scenes to access
            self.deltaTime = self.clock.tick(60) / 1000
            self.elapsedTime = pygame.time.get_ticks() - self.startTime

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
            self.activeScene.onEvent(events)

            # Update scene
            self.activeScene.onUpdate()

            # Draw the screen
            self.activeScene.onDraw(self.screen)

            # Redraw display
            pygame.display.flip()

        # If we break the loop exit the game
        pygame.quit()
        sys.exit()

    def addScenes(self, scenes):
        # If scenes is a list
        if type(scenes) is list:
            for scene in scenes:
                # For each scene pass a director reference
                scene.director = self

                # Make scenes accessible by name
                self.scenes[str(scene.name)] = scene

    def loadScene(self, sceneName):
        # Fill screen with black to clear all previous outputs
        self.screen.fill(BLACK)

        # Set the active scene for the main game loop
        self.activeScene = self.scenes[sceneName]

        # Pass a director reference to the scene
        self.activeScene.director = self

    def quit(self):
        # Break the loop so the game ends
        self.quitFlag = True

    def handleCommand(self, command):
        # Command has to be list
        if type(command) is list:
            if command[0] == 'loadScene':
                self.loadScene(command[1])
            elif command[0] == 'quit':
                self.quit()


# /===================================/
#  Base scene class
# /===================================/


class Scene():
    def __init__(self, director=None, name=None):
        # Set director reference
        if director is not None:
            self.director = director

        if name is not None and type(name) is str:
            self.name = name

    def onEvent(self, event):
        # Pass events to scene for processing
        raise NotImplementedError("onEvent not defined in subclass")

    def onUpdate(self):
        # Calculate game logic every frame
        raise NotImplementedError("onUpdate not defined in subclass")

    def onDraw(self, screen):
        # Draw surfaces within scene
        raise NotImplementedError("onDraw not defined in subclass")


# /===================================/
#  Base GUI Class
# /===================================/


class GUIElement:
    def __init__(self, rect=None):
        # Default to a 100x100 rect
        if rect is None:
            self._rect = pygame.rect.Rect(0, 0, 100, 100)
        else:
            self._rect = pygame.rect.Rect(rect)

    def draw(self, screen):
        raise NotImplementedError('draw not defined in subclass')

    def _update(self):
        raise NotImplementedError('_update not defined in subclass')

    def handleEvent(self, event):
        raise NotImplementedError('handleEvent not defined in subclass')

# /===================================/
#  General text class
# /===================================/


class Text(GUIElement):
    def __init__(self, rect=None, caption=None, font=None, fontColor=WHITE, centered=True):
        super().__init__(rect)

        if caption is None:
            self._caption = None
        else:
            self._caption = caption

        if font is None:
            self._font = DEFAULT_FONT
        else:
            self._font = font

        self._fontColor = fontColor

        self._visible = True

        # Initalise surface
        self.surface = pygame.Surface(self._rect.size, pygame.SRCALPHA)

        self._centered = centered

        # Update to fill surfaces for first time
        self._update()

    def _update(self):
        # Make it easier to code
        w = self._rect.width
        h = self._rect.height

        # Render font
        renderedText = self._font.render(self._caption, True, self._fontColor)
        captionRect = renderedText.get_rect()

        # Center text
        if self._centered:
            captionRect.center = int(w / 2), int(h / 2)

        # Blit text to surface
        self.surface.blit(renderedText, captionRect)

    def draw(self, screen):
        # Blit text to screen
        if self._visible:
            screen.blit(self.surface, self._rect)

    def handleEvent(self, event):
        pass


# /===================================/
#  General button class
# /===================================/


class Button(GUIElement):
    def __init__(self, rect=None, caption=None, font=None, fontColor=WHITE, backgroundColor=BLACK, border=None, normal=None, toggle=None, highlight=None):

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
        self._fontColor = fontColor

        # Assign the background color
        self._bgcolor = backgroundColor

        # Default value for button visibility
        self._visible = True

        # Default values for hover and toggle
        self.buttonToggled = False
        self.mouseOverButton = False
        self.lastButtonToggled = False

        # Button defaults as normal text button when no custom surfaces are passed
        self.customSurfaces = False

        if normal is None:
            # Create blank surfaces for the button
            self.normalSurface = pygame.Surface(self._rect.size)
            self.toggleSurface = pygame.Surface(self._rect.size)
            self.highlightSurface = pygame.Surface(self._rect.size)

            # Call the initial update to draw the button
            self._update()
        else:
            self.assignSurfaces(normal, toggle, highlight)

    def draw(self, screen):
        if self._visible:
            if self.buttonToggled:
                screen.blit(self.toggleSurface, self._rect)
            elif self.mouseOverButton:
                screen.blit(self.highlightSurface, self._rect)
            else:
                screen.blit(self.normalSurface, self._rect)

    def _update(self):

        # If using custom surfaces
        if self.customSurfaces:
            self.normalSurface = pygame.transform.smoothscale(self.origNormalSurface, self._rect.size)
            self.toggleSurface = pygame.transform.smoothscale(self.origToggleSurface, self._rect.size)
            self.highlightSurface = pygame.transform.smoothscale(self.origHighlightSurface, self._rect.size)
            return

        w = self._rect.width
        h = self._rect.height

        # Fill the background color for all states
        self.normalSurface.fill(self._bgcolor)
        self.toggleSurface.fill(self._bgcolor)
        self.highlightSurface.fill(self._bgcolor)

        # Draw the caption text
        renderedText = self._font.render(self._caption, True, self._fontColor, self._bgcolor)
        captionRect = renderedText.get_rect()
        captionRect.center = int(w / 2), int(h / 2)
        self.normalSurface.blit(renderedText, captionRect)
        self.toggleSurface.blit(renderedText, captionRect)
        self.highlightSurface.blit(renderedText, captionRect)

        if self._border is not None:
            pygame.draw.rect(self.normalSurface, self._border['normal']['color'], pygame.Rect((0, 0, w, h)), self._border['normal']['width'])
            pygame.draw.rect(self.toggleSurface, self._border['toggle']['color'], pygame.Rect((0, 0, w, h)), self._border['toggle']['width'])
            pygame.draw.rect(self.highlightSurface, self._border['highlight']['color'], pygame.Rect((0, 0, w, h)), self._border['highlight']['width'])

    def handleEvent(self, eventObject):

        # If event is not relevant or button not visible
        if eventObject.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP) or not self._visible:
            return

        hasExited = False

        # If mouse not over button previously but over button now
        if not self.mouseOverButton and self._rect.collidepoint(eventObject.pos):
            # Mouse has entered the button
            self.mouseOverButton = True
            self.mouseEnter(eventObject)
        # If mouse over button previously but no over button now
        elif self.mouseOverButton and not self._rect.collidepoint(eventObject.pos):
            self.mouseOverButton = False
            hasExited = True

        if self._rect.collidepoint(eventObject.pos):
            if eventObject.type == pygame.MOUSEMOTION:
                self.mouseMove(eventObject)
            elif eventObject.type == pygame.MOUSEBUTTONDOWN:
                self.buttonToggled = True
                self.lastButtonToggled = True
                self.mouseDown(eventObject)
        else:
            if eventObject.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                self.lastButtonToggled = False

        doMouseClick = False
        if eventObject.type == pygame.MOUSEBUTTONUP:
            if self.lastButtonToggled:
                doMouseClick = True
            self.lastButtonToggled = False

            if self.buttonToggled:
                self.buttonToggled = False
                self.mouseUp(eventObject)

            if doMouseClick:
                self.buttonToggled = False
                self.mouseClick(eventObject)

        if hasExited:
            self.mouseExit(eventObject)

    def assignSurfaces(self, normal, toggle=None, highlight=None):

        # If toggle or highlight surface or reference not sent
        if toggle is None:
            toggle = normal
        if highlight is None:
            highlight = normal

        if type(normal) == str:
            self.origNormalSurface = pygame.image.load(normal)
        if type(toggle) == str:
            self.origToggleSurface = pygame.image.load(toggle)
        if type(highlight) == str:
            self.origHighlightSurface = pygame.image.load(highlight)

        if normal.get_size() != toggle.get_size() != highlight.get_size():
            raise Exception('Surfaces not same size!')

        self.normalSurface = self.origNormalSurface
        self.toggleSurface = self.origToggleSurface
        self.highlightSurface = self.origHighlightSurface
        self.customSurfaces = True

    def mouseClick(self, event):
        raise NotImplementedError("mouseClick not defined in subclass")

    def mouseEnter(self, event):
        raise NotImplementedError("mouseEnter not defined in subclass")

    def mouseExit(self, event):
        raise NotImplementedError("mouseExit not defined in subclass")

    def mouseMove(self, event):
        raise NotImplementedError("mouseMove not defined in subclass")

    def mouseDown(self, event):
        raise NotImplementedError("mouseDown not defined in subclass")

    def mouseUp(self, event):
        raise NotImplementedError("mouseUp not defined in subclass")


# /===================================/
#  General image class
# /===================================/


class Image(GUIElement):
    def __init__(self, rect=None, image=None):
        super().__init__(rect)

        if image is None:
            image = pygame.Surface((100, 100))
        else:
            self._sourceImage = pygame.image.load(os.path.join(*image)).convert()

        self.surface = pygame.Surface(self._rect.size)
        self._update()

    def draw(self, screen):
        screen.blit(self.surface, self._rect, (0, 0, self._rect.width, self._rect.height))

    def _update(self):
        pass

    def handleEvent(self):
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

    def onUpdate(self):
        pass

    def onEvent(self, events):
        for event in events:
            # If event is mouse related
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                # Send the mouse event to every button
                for button in self.buttons:
                    button.handleEvent(event)

    def onDraw(self, screen):
        # Draw the background first
        self.background.draw(screen)

        # Draw buttons over background
        for button in self.buttons:
            button.draw(screen)

    def handleCommand(self):
        pass


# /===================================/
#  Background image class
# /===================================/


class BackgroundImage(Image):
    def __init__(self, rect=None, image=None, imageType=None):
        if imageType is None:
            self._imageType = 'static'
        elif type(imageType) is str:
            self._imageType = imageType
        else:
            self._imageType = 'static'

        super().__init__(rect, image)

    def _update(self):
        destWidth = self._rect.width
        destHeight = self._rect.height
        sourceWidth = self._sourceImage.get_rect().width
        sourceHeight = self._sourceImage.get_rect().height

        imageRatio = sourceWidth / sourceHeight
        destRatio = destWidth / destHeight

        if self._imageType == 'contain':
            if imageRatio <= destRatio:
                newWidth = destHeight * imageRatio
                newHeight = destHeight
            elif imageRatio >= destRatio:
                newWidth = destWidth
                newHeight = destWidth / imageRatio
        elif self._imageType == 'cover':
            if imageRatio <= destRatio:
                newWidth = destWidth
                newHeight = destWidth / imageRatio
            elif imageRatio >= destRatio:
                newWidth = destHeight * imageRatio
                newHeight = destHeight
        elif self._imageType == 'static' or self._imageType is None:
            newWidth = destWidth
            newHeight = destHeight

        scaledImage = pygame.transform.smoothscale(self._sourceImage, (int(newWidth), int(newHeight)))

        scaledRect = scaledImage.get_rect()
        scaledRect.center = int(self._rect.width / 2), int(self._rect.height / 2)

        self.surface.blit(scaledImage, scaledRect)


# /===================================/
#  Main menu button class
# /===================================/


class MainMenuButton(Button):
    def __init__(self, scene, commands, rect, caption):
        borderConfig = {'normal': {'color': WHITE, 'width': 10}, 'toggle': {'color': BLUE, 'width': 10}, 'highlight': {'color': RED, 'width': 10}}
        super().__init__(rect, caption, DEFAULT_FONT, WHITE, BLACK, borderConfig)

        self.scene = scene

        if type(commands) is dict:
            self.clickCommand = commands['click'] if 'click' in commands else None
            self.enterCommand = commands['enter'] if 'enter' in commands else None
            self.exitCommand = commands['exit'] if 'exit' in commands else None
            self.moveCommand = commands['move'] if 'move' in commands else None
            self.downCommand = commands['down'] if 'down' in commands else None
            self.upCommand = commands['up'] if 'up' in commands else None
        else:
            self.clickCommand = None
            self.enterCommand = None
            self.exitCommand = None
            self.moveCommand = None
            self.downCommand = None
            self.upCommand = None

    def mouseClick(self, event):
        if self.clickCommand is not None:
            self.scene.director.handleCommand(self.clickCommand)

    def mouseEnter(self, event):
        # pygame.mouse.set_cursor(*cursors.hover)
        pass

    def mouseExit(self, event):
        # pygame.mouse.set_cursor(*cursors.normal)
        pass

    def mouseMove(self, event):
        pass

    def mouseDown(self, event):
        pass

    def mouseUp(self, event):
        pass


# /===================================/
#  Basic game scene class
# /===================================/


class GameScene(Scene):
    def __init__(self, director=None, name=None, entitiesList=None):
        super().__init__(director, name)

        if type(entitiesList) is list and entitiesList is not None:
            self.entities = entitiesList

        self.level = []

    def onEvent(self, events):
        for event in events:
            pass

    def onUpdate(self):
        pass

    def onDraw(self, screen):
        for entity in self.entities:
            entity.draw(screen)

    def handleCommand(self, command):
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
#  Basic wall class
# /===================================/


class Wall(GameObject):
    def __init__(self, scene=None, x=0, y=0, width=100, height=100):
        super().__init__(scene, x, y)

        self.width = width
        self.height = height

        self.surface = pygame.Surface((self.width, self.height))

        self._rect = self.surface.get_rect()

        self._rect.x = x
        self._rect.y = y

        self._update()

    def _update(self):
        self.surface.fill(BLUE)

    def draw(self, screen):
        screen.blit(self.surface, self._rect)
