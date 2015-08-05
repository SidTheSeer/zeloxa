import pygame
import gamelib.gamelib as gamelib


class MainMenu(gamelib.MenuScene):
    def __init__(self, director=None, name=None, buttons=None, background=None, music=None):
        buttonWidth = 300
        buttonHeight = 100
        w = director.screen.get_rect().width
        h = director.screen.get_rect().height
        wCenter = int((w - buttonWidth) / 2)
        hCenter = int((h - buttonHeight) / 2)

        background = gamelib.BackgroundImage((0, 0, w, h), ['assets', 'images', 'test.jpg'], 'cover')
        playButton = gamelib.MainMenuButton(self, {'click': ['loadScene', 'FirstScene']}, (wCenter, hCenter - 150, 300, 100), 'Play')
        optionsButton = gamelib.MainMenuButton(self, None, (wCenter, hCenter, 300, 100), 'Options')
        quitButton = gamelib.MainMenuButton(self, {'click': ['quit']}, (wCenter, hCenter + 150, 300, 100), 'Quit')

        buttons = [playButton, optionsButton, quitButton]

        music = None

        name = 'MainMenu'

        super().__init__(director, name, buttons, background, music)

        # self.text = gamelib.Text((820, 450, 500, 100), 'I like POTATO', DEFAULT_FONT, gamelib.BLACK)

    def handleCommand(self, command):
        pass


class MainMenu2(gamelib.MenuScene):
    def __init__(self, director=None, name=None, buttons=None, background=None, music=None):
        background = gamelib.BackgroundImage((0, 0, director.screen.get_rect().width, director.screen.get_rect().height), ['assets', 'images', 'test.jpg'], 'cover')

        buttons = [gamelib.MainMenuButton(self, {'click': ['loadScene', 'MainMenu']}, (0, 0, 500, 100), 'SCENE2'), gamelib.MainMenuButton(self, None, (0, 300, 500, 100), 'DERP')]

        music = None

        name = 'MainMenu2'

        super().__init__(director, name, buttons, background, music)

        # self.text = gamelib.Text((820, 450, 500, 100), 'I like POTATO', DEFAULT_FONT, gamelib.BLACK)

    def handleCommand(self, command):
        pass


class SplashScreen(gamelib.Scene):
    def __init__(self, director=None, name=None):
        textWidth = 500
        textHeight = 150
        w = director.screen.get_rect().width
        h = director.screen.get_rect().height
        wCenter = int((w - textWidth) / 2)
        hCenter = int((h - textHeight) / 2)
        name = 'Splash'

        super().__init__(director, name)

        self.developerName = gamelib.Text((wCenter, hCenter, textWidth, textHeight), 'Zeloxa', gamelib.NEW_FONT, gamelib.WHITE)

        self.fadeInStuff = pygame.Surface((director.screen.get_rect().width, director.screen.get_rect().height))
        self.fadeInStuff.fill((0, 0, 0))
        self.alpha = 255

    def onEvent(self, event):
        pass

    def onUpdate(self):
        self.alpha -= 50 * self.director.deltaTime
        self.fadeInStuff.set_alpha(max(self.alpha, 0))

        if self.director.elapsedTime >= 6000:
            self.director.handleCommand(['loadScene', 'MainMenu'])

    def onDraw(self, screen):
        screen.fill(gamelib.BLACK)
        self.developerName.draw(screen)
        screen.blit(self.fadeInStuff, self.fadeInStuff.get_rect())


class FirstGameScene(gamelib.PlatformerScene):
    def __init__(self, director=None, name=None, background=None, walls=None, player=None):
        player = gamelib.Player(self, 0, 0, 100, 100, 250)

        name = 'FirstScene'

        walls = [gamelib.Wall(self, 300, 300, 100, 100)]

        super().__init__(director, name, background, walls, player)
