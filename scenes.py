import gamelib.gamelib as gamelib

class MainMenu(gamelib.MenuScene):
	def __init__(self, director = None, buttons = None, background = None, music = None):
		background = gamelib.BackgroundImage((0, 0, director.screen.get_rect().width, director.screen.get_rect().height), ['assets', 'images', 'test.jpg'], 'contain')
		buttons = [gamelib.MainMenuButton(self, {'click': ['loadScene', 1]}, (0, 0, 500, 100), 'YARRR'), gamelib.MainMenuButton(self, None, (0, 300, 500, 100), 'DERP')]
		music = None

		#self.fadeInStuff = pygame.Surface((director.screen.get_rect().width, director.screen.get_rect().height))
		#self.fadeInStuff.fill((0, 0, 0))
		#self.alpha = 255
		super().__init__(director, buttons, background, music)

		#self.text = gamelib.Text((820, 450, 500, 100), 'I like POTATO', DEFAULT_FONT, gamelib.BLACK)


	def handleCommand(self, command):
		pass

class MainMenu2(gamelib.MenuScene):
	def __init__(self, director = None, buttons = None, background = None, music = None):
		background = gamelib.BackgroundImage((0, 0, director.screen.get_rect().width, director.screen.get_rect().height), ['assets', 'images', 'test.jpg'], 'cover')
		buttons = [gamelib.MainMenuButton(self, {'click': ['loadScene', 0]}, (0, 0, 500, 100), 'SCENE2'), gamelib.MainMenuButton(self, None, (0, 300, 500, 100), 'DERP')]
		music = None
		super().__init__(director, buttons, background, music)

		#self.text = gamelib.Text((820, 450, 500, 100), 'I like POTATO', DEFAULT_FONT, gamelib.BLACK)

	def handleCommand(self, command):
		pass