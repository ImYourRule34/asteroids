import pygame
import player
import asteroid
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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Handle other events (e.g., key presses)

    def update(self):
        # Update game entities
        self.player.update()
        # Update asteroids and bullets

    def draw(self):
        self.screen.fill(settings.BLACK)
        self.player.draw()
        # Draw asteroids and bullets
        pygame.display.flip()

    def draw_ui(self):
        ammo_count = 20 - len([b for b in self.bullets if b.is_alive()])
        ammo_text = f"Ammo: {ammo_count}"
        font = pygame.font.SysFont(None, 36)
        text_surf = font.render(ammo_text, True, settings.WHITE)
        self.screen.blit(text_surf, (10, self.scree.get_height() - 40))