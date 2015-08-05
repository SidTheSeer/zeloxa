import pygame
import gamelib.gamelib as gamelib
import scenes as zeloxa
import argparse

pygame.init()

# XXX: get debug stuff done

# XXX: level design crap - collison and draw levels, same collision level they collide, render from 0 - *, make some constants i.e BASE, BACKGROUND, ENEMIES, PLAYER


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="turn on debugging", action="store_true")
    args = parser.parse_args()

    # Initalise director
    director = gamelib.Director('Zeloxa')

    # Initalise scenes
    splashScreen = zeloxa.SplashScreen(director)
    mainMenu1 = zeloxa.MainMenu(director)
    mainMenu2 = zeloxa.MainMenu2(director)
    firstGameScene = zeloxa.FirstGameScene(director)

    # Collect into list
    gameScenes = [mainMenu1, mainMenu2, splashScreen, firstGameScene]

    # Add levels to director
    director.addScenes(gameScenes)

    if args.debug:
        print('yay')
    else:
        print('Nay!')

    # Load starting scene
    director.loadScene('MainMenu')

    # Start the main loop
    director.loop()

if __name__ == '__main__':
    main()
