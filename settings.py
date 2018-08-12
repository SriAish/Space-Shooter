import sys
import pygame


class Settings():
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 400
        self.screen_height = 450
        self.bg_color = (0, 0, 0)
        # Ship settings
        self.ship_speed_factor = 0.2
        # Bullet settings
        self.bullet_height = 25
        self.bullet_width = 10
        self.bullets_allowed = 10
        # Scoring
        self.alien_points = 1
