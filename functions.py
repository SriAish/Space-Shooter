import sys
import pygame
import random
import time
from threading import Timer
from pygame.locals import *
from bullet import Bullet, Bullet_Norm, Bullet_Wait
from alien import Alien


def get_number_aliens_x(game_set, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = game_set.screen_width
    number_aliens_x = int(available_space_x / alien_width)
    return number_aliens_x-1


def create_alien(game_set, screen):
    """Create an alien and place it in the row."""
    t_create = Timer(10.0, create_alien, [game_set, screen])
    t_create.start()
    alien = Alien(game_set, screen)
    number_aliens_x = get_number_aliens_x(game_set, alien.rect.width)
    row_number = random.randint(1, 2)
    alien_number = random.randint(0, number_aliens_x)
    alien_width = alien.rect.width
    alien.x = alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height * row_number
    Alien.aliens.add(alien)


def delete_alien(game_set, screen, ship):
    """Delete an alien"""
    t_del = Timer(10.0, delete_alien, [game_set, screen, ship])
    t_del.start()
    for alien in Alien.aliens:
        if alien.flag == 1:
            Alien.aliens.remove(alien)


def update_bullets(game_set, screen, stats, sb, ship):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    Bullet_Norm.bullets.update()
    Bullet_Wait.bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in Bullet_Norm.bullets.copy():
        if bullet.rect.bottom <= 0:
            Bullet_Norm.bullets.remove(bullet)
    for bullet in Bullet_Wait.bullets.copy():
        if bullet.rect.bottom <= 0:
            Bullet_Wait.bullets.remove(bullet)
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    check_bullet_alien_collisions(game_set, screen, stats, sb,
                                  ship, Bullet_Norm.bullets)
    check_bullet_alien_collisions2(game_set, screen, stats, sb,
                                   ship, Bullet_Wait.bullets)


def check_bullet_alien_collisions(game_set, screen, stats, sb,
                                  ship, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, Alien.aliens, True, True)

    if collisions:
        for aliens in collisions.values():
                    stats.score += game_set.alien_points
    sb.prep_score()


def check_bullet_alien_collisions2(game_set, screen, stats, sb,
                                   ship, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, Alien.aliens, True, False)
    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                alien.update()


def check_keydown(event, game_set, screen, ship, stats, flag):
    """Respond to keypresses."""
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_set, screen, ship,
                    Bullet_Norm.bullets, Bullet_Norm)
    elif event.key == pygame.K_s:
        fire_bullet(game_set, screen, ship, Bullet_Wait.bullets, Bullet_Wait)
    elif event.key == pygame.K_q:
        pygame.quit()
        return 1
    return flag


def check_keyup(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False


def fire_bullet(game_set, screen, ship, bullets, typ):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < game_set.bullets_allowed:
        new_bullet = typ(game_set, screen, ship)
        bullets.add(new_bullet)


def check_events(game_set, screen, ship, stats, flag):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return 1
        elif event.type == pygame.KEYDOWN:
            flag = check_keydown(event, game_set, screen, ship, stats, flag)
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)
    return flag


def update_screen(game_set, screen, stats, sb, ship):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(game_set.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in Bullet_Norm.bullets.sprites():
        bullet.draw_bullet()
    for bullet in Bullet_Wait.bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    Alien.aliens.draw(screen)
    # Draw the score information.
    sb.show_score()
    # Make the most recently drawn screen visible.
    pygame.display.flip()
