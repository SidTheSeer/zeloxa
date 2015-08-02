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
        playButton = gamelib.MainMenuButton(self, {'click': ['loadScene', 'MainMenu2']}, (wCenter, hCenter - 150, 300, 100), 'PLAY')
        optionsButton = gamelib.MainMenuButton(self, None, (wCenter, hCenter, 300, 100), 'OPTIONS')
        quitButton = gamelib.MainMenuButton(self, {'click': ['quit']}, (wCenter, hCenter + 150, 300, 100), 'QUIT')

        buttons = [playButton, optionsButton, quitButton]

        music = None

        name = 'MainMenu'

        # self.fadeInStuff = pygame.Surface((director.screen.get_rect().width, director.screen.get_rect().height))
        # self.fadeInStuff.fill((0, 0, 0))
        # self.alpha = 255
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
