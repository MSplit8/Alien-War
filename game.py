import pygame

class Game():

    def __init__(self, ai_game):
        self.setting = ai_game.settings
        self.game_active = False
        pygame.mouse.set_visible(True)

