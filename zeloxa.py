import pygame
import gamelib as gamelib
import scenes as zeloxa
import argparse

pygame.init()

def main():
    # Debug flag
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="turn on debugging", action="store_true")
    args = parser.parse_args()

    # Initialise director
    director = gamelib.base.Director('Zeloxa')

    # The director scene model was inspired by another blog post

    # Initialise scenes
    splash_screen = zeloxa.SplashScreen(director)
    main_menu = zeloxa.MainMenu(director)
    help_screen = zeloxa.HelpScene(director)
    level_select = zeloxa.LevelSelect(director)
    level_1 = zeloxa.FirstLevel(director)
    level_2 = zeloxa.SecondLevel(director)
    level_3 = zeloxa.ThirdLevel(director)

    # Collect into list
    game_scenes = [splash_screen, main_menu, help_screen, level_select, level_1, level_2, level_3]

    # Add levels to director
    director.add_scenes(game_scenes)

    if args.debug:
        # Implement debug stuff at some point
        # Welp that never happened
        pass
    else:
        pass

    # Load starting scene
    director.load_scene('Splash')

    # Start the main loop
    director.loop()

if __name__ == '__main__':
    # Make sure we're running the right file
    main()
