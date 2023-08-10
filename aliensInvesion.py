
import pygame
from settings import Settings as st
from pygame.sprite import Group
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    pygame.init()
    ai_settings = st()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")

    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()
    gf.create_fleet(ai_settings, screen,ship, aliens)
    stats = GameStats(ai_settings=ai_settings)
    sb = Scoreboard(ai_settings=ai_settings, screen=screen, stats=stats)
    while True:
        gf.check_events(ai_settings=ai_settings, screen=screen, ship= ship, bullets=bullets, stats=stats, play_button=play_button)
        gf.update_screen(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens, bullets=bullets, play_button = play_button, stats = stats, sb=sb) 
        if(stats.game_active):
            ship.update()
            gf.update_bullets(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens, bullets=bullets, stats=stats, sb=sb)
            gf.update_aliens(ship = ship, ai_settings=ai_settings, aliens=aliens, stats=stats, bullets=bullets, screen=screen, sb=sb)   
  
run_game()