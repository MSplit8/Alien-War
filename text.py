import pygame

class Text():

    def __init__(self, ai_game):

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.game = ai_game.game

        self.font_name = pygame.font.match_font('arial')
        self.font = pygame.font.SysFont(self.font_name, 24)
        self.text_count = self.settings.bullets_allowed
        self.img = self.font.render('Ammo: ' + str(self.text_count), True, self.settings.color_text)
        self.rect = self.img.get_rect()

    def blitme(self, img):
        self.screen.blit(img, self.settings.size_text)