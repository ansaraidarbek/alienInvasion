import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, screen, ship, bullets, stats, play_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats=stats, play_button= play_button, mouse_x= mouse_x, mouse_y = mouse_y, ai_settings=ai_settings)

def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.game_active = True
        ai_settings.initialize_dynamic_settings()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

    
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if (len(bullets)< ai_settings.bullets_allowed):
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()

def update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    check_bullets_collision(ai_settings, screen, ship, aliens, bullets, stats, sb)

def check_bullets_collision(ai_settings, screen, ship, aliens, bullets, stats, sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if(collisions):
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats=stats, sb=sb)
    if(len(aliens) == 0):
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats, sb):
    stats.high_score = max(stats.high_score, stats.score)
    sb.prep_high_score()

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows_y(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    availables_space_x = ai_settings.screen_width - (2*alien_width)
    number_aliens_x = int(availables_space_x/(2*alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + (2*alien.rect.height * row_number)
    aliens.add(alien)

def get_number_rows_y(ai_settings, ship_height, alien_height ):
    available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(ai_settings, aliens, ship, stats, screen, bullets, sb):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings=ai_settings, stats=stats, screen=screen, ship=ship, aliens=aliens, bullets=bullets, sb=sb)
    check_alliens_bottom(ai_settings=ai_settings, stats=stats, screen=screen, ship=ship, aliens=aliens, bullets=bullets, sb=sb)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    stats.ships_left -= 1
    sb.prep_ships()
    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens)
    ship.center_ship()
    if(stats.ships_left<=0):
        stats.reset_stats()
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()
        stats.game_active = False
        pygame.mouse.set_visible(True)

    sleep(0.5)

def check_alliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if(alien.rect.bottom >= screen_rect.bottom):
            ship_hit(ai_settings=ai_settings, stats=stats, screen=screen, aliens=aliens, bullets=bullets, ship=ship, sb=sb)
            break

