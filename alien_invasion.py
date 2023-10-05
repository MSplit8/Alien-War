import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from text import Text
from alien import Alien
from game import Game
from button import Button
import random
import asyncio
from time import sleep

class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        self.game = Game(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.text = Text(self)
        self.alien = Alien(self)
        self.play_button = Button(self, "Play")

    async def run_game(self):
        while True:
            await self._check_events()
            if self.game.game_active:
                self.ship.update()
                await self._update_bullets()
                await self._update_aliens()
            await self._update_screen()
            await asyncio.sleep(0)

    async def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                await self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                await self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    async def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.game.game_active:
                await self._fire_bullet()
                self._update_text()

    async def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    async def _fire_bullet(self):
        self.settings.bullets_count += 1

        if self.settings.bullets_count <= self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    async def _create_fleet(self):
        for a in range(self.settings.alien_number + 1):
            alien = Alien(self)
            self.aliens.add(alien)
            await asyncio.sleep(random.uniform(0.5, 2))
        if self.settings.alien_number == 0:
            await self._game_over()

    async def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                await self._game_over()

    def _update_text(self):
        if self.settings.bullets_count <= self.settings.bullets_allowed:
            self.text.text_count = self.settings.bullets_allowed - self.settings.bullets_count
            self.text.img = self.text.font.render('Ammo: ' + str(self.text.text_count), True, self.settings.color_text)

    async def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            self.settings.alien_number -= 1
            self.alien.prep_alien()

    async def _update_aliens(self):
        await self._check_fleet_edges()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            await self._game_over()
        self.aliens.update()

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            self.settings.bullets_count = 0
            self.settings.alien_number = 30
            self.alien.prep_alien()
            self.game.game_active = True
            self._update_text()
            self.aliens.empty()
            self.bullets.empty()
            pygame.mouse.set_visible(False)

    async def _game_over(self):
        self.game.game_active = False
        self.settings.bullets_count = 0
        self.settings.alien_number = 30
        self.aliens.empty()
        self.bullets.empty()
        sleep(0.5)
        pygame.mouse.set_visible(True)

    async def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.text.blitme(self.text.img)
        self.aliens.draw(self.screen)
        if not self.game.game_active:
            self.play_button.draw_button()
        self.alien.show_alien()
        pygame.display.flip()

    async def asyncio_task(self):
        task1 = asyncio.create_task(self.run_game())
        task2 = asyncio.create_task(self._create_fleet())

        await asyncio.gather(task1, task2)

if __name__ == '__main__':
    ai = AlienInvasion()
    asyncio.run(ai.asyncio_task())

