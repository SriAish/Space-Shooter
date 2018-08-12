import os
import pygame
from threading import Timer
from pygame.locals import *
from pygame.sprite import Group
import functions as gf
from bullet import Bullet_Norm, Bullet_Wait
from ship import Ship
from stats import GameStats
from scoreboard import Scoreboard
from settings import Settings


def run_game():
    """Engine of the game"""
    # Initialize game and create a screen object.
    pygame.init()
    game_set = Settings()
    screen = pygame.display.set_mode((game_set.screen_width,
                                      game_set.screen_height))
    # Setting caption
    pygame.display.set_caption("Alien Invasion")
    # An instance to store game statistics and create a scoreboard.
    stats = GameStats(game_set)
    sb = Scoreboard(game_set, screen, stats)
    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(game_set, screen)
    flag = 0
    # Create the fleet of aliens.
    Timer(0.0, gf.create_alien,
          [game_set, screen]).start()
    Timer(8.0, gf.delete_alien,
          [game_set, screen, ship]).start()
    # Start the main loop for the game.
    while True:
        # Watch for keyboard events.
        flag = gf.check_events(game_set, screen, ship, stats, flag)
        # End game check
        if flag == 1:
            break
        # Update condition of bullets and ship
        ship.update()
        Bullet_Norm.bullets.update()
        Bullet_Wait.bullets.update()
        # Get rid of bullets that have disappeared.
        gf.update_bullets(game_set, screen, stats, sb, ship)
        gf.update_screen(game_set, screen, stats, sb, ship)
    print("Counter : " + (str)(stats.score))
    os._exit(0)

if __name__ == "__main__":
    run_game()
