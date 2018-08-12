import pygame
import time
from pygame.sprite import Sprite, Group


class Bullet(Sprite):
    """A class to manage all bullets fired from the ship"""
    def __init__(self, game_set, screen, ship):
        """Create a bullet object at the ship's current position."""
        super(Bullet, self).__init__()
        self.screen = screen
        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, game_set.bullet_width,
                                game_set.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        # Store the bullet's position as decimal value.
        self.y = float(self.rect.y)
        self.time = time.time()

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Bullet_Norm(Bullet):
    """Class to manage Normal bullets"""
    bullets = Group()

    def __init__(self, game_set, screen, ship):
        super(Bullet_Norm, self).__init__(game_set, screen, ship)
        self.color = 100, 100, 100
        self.speed_factor = 0.021


class Bullet_Wait(Bullet):
    """Class to manage 5 second wait bullets"""
    bullets = Group()

    def __init__(self, game_set, screen, ship):
        super(Bullet_Wait, self).__init__(game_set, screen, ship)
        self.color = 0, 0, 100
        self.speed_factor = 0.042
