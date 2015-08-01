import pygame
import gamelib.gamelib as gamelib
import scenes as zeloxa

def main():
    # Initalise director
    director = gamelib.Director('Zeloxa')

    # Initalise scenes
    mainMenu1 = zeloxa.MainMenu(director)
    mainMenu2 = zeloxa.MainMenu2(director)

    # Collect into list
    gameScenes = [mainMenu1, mainMenu2]

    # Add levels to director
    director.addScenes(gameScenes)

    # Load starting scene
    director.loadScene(0)

    # Start the main loop
    director.loop()

# Initalise pygames
pygame.init()

if __name__ == '__main__':
    main()