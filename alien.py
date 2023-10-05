import pygame
from pygame.sprite import Sprite
import random
import pygame.font

class Alien(Sprite):

    def __init__(self, ai_game):

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.game = ai_game.game

        self.image = pygame.image.load('images/alien_red.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(80, 1200)
        self.rect.y = self.rect.height - 180

        self.y = float(self.rect.y)

        self.font_name = pygame.font.match_font('arial')
        self.font = pygame.font.SysFont(self.font_name, 24)

        self.prep_alien()

    def check_edges(self):
        if self.rect.y == self.settings.screen_height:
            return True

    def prep_alien(self):
        alien_str = str(self.settings.alien_number)
        self.alien_image = self.font.render('Aliens: ' + alien_str, True, self.settings.color_text, self.settings.bg_color)

        self.alien_rect = self.alien_image.get_rect()

    def show_alien(self):
        self.screen.blit(self.alien_image, self.settings.size_text1)

    def update(self):
        self.y += self.settings.alien_speed
        self.rect.y = self.y