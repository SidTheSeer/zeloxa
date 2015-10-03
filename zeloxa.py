import pygame
import gamelib as gamelib
import scenes as zeloxa
import argparse

pygame.init()

# XXX: get debug stuff done

# XXX: TRY OUT POSSIBLE RENDER STUFF LAYERZ

# XXX: Comment your code

# XXX: Add different tile types, triggering blocks (i.e exit blocks), get
# the other stuff above done I.E COLLISION LEVELS

# XXX: add self deleting stuff

# XXX: ADD MARGIN FOR ERROR TO ENEMY AI THING
# XXX: LIKE 10 UNITS OR SOMETHING

# XXX: GROUND DETECTION ON PLAYER REGISTER ON THE ENEMY AND STACKS BECAUSE IT DOESNT COLLIDE AND YOU GO SHOOTING UP


def main():
    # Debug flag
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", help="turn on debugging", action="store_true")
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
