import pygame
import gamelib as gamelib
import scenes as zeloxa
import argparse

pygame.init()

# XXX: get debug stuff done

# XXX: level design crap - collision and draw levels, same collision level they collide, render from 0 - *, make some constants i.e BASE, BACKGROUND, ENEMIES, PLAYER

# XXX: More stuff to do - make a level config class i.e level, background etc.

# XXX: Comment your code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="turn on debugging", action="store_true")
    args = parser.parse_args()

    # Initialise director
    director = gamelib.base.Director('Zeloxa')

    # Initialise scenes
    splash_screen = zeloxa.SplashScreen(director)
    main_menu = zeloxa.MainMenu(director)
    level_1 = zeloxa.FirstGameScene(director)

    # Collect into list
    game_scenes = [splash_screen, main_menu, level_1]

    # Add levels to director
    director.add_scenes(game_scenes)

    if args.debug:
        # Implement debug stuff at some point
        pass
    else:
        pass

    # Load starting scene
    director.load_scene('Splash')

    # Start the main loop
    director.loop()

if __name__ == '__main__':
    main()
