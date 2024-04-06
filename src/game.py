import pygame
import player
import utils
import settings

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, 
                                               settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = player.Player(400, 300, self.screen)
        self.asteroids = []
        self.bullets = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.rotate_left()
        if keys[pygame.K_RIGHT]:
            self.player.rotate_right()
        if keys[pygame.K_UP]:
            self.player.accelerate()
        if keys[pygame.K_SPACE]:
            self.player.shoot(self.bullets)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(120)

    def update(self):
        self.player.update()
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_alive():
                self.bullets.remove(bullet)
            else:
                for asteroid in self.asteroids[:]:  
                    if utils.check_collision(bullet, asteroid):
                        self.asteroids.remove(asteroid)
                        bullet.alive = False
                        break

        for asteroid in self.asteroids:
            asteroid.update()
            if utils.check_collision(self.player, asteroid):
                pass


    def draw(self):
        self.screen.fill(settings.BLACK)
        self.player.draw()
        for bullet in self.bullets:
            bullet.draw()
        for asteroid in self.asteroids:
            asteroid.draw()
        self.draw_ui()
        pygame.display.flip()


    def draw_ui(self):
        ammo_count = 20 - len([b for b in self.bullets if b.is_alive()])
        ammo_text = f"Ammo: {ammo_count}"
        font = pygame.font.SysFont(None, 36)
        text_surf = font.render(ammo_text, True, settings.WHITE)
        self.screen.blit(text_surf, (10, self.screen.get_height() - 40))