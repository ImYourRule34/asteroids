import pygame
import settings

def draw_text(screen, text, position, size, color):
  font = pygame.font.Font(None, size)
  text_surface = font.render(text, True, color)
  rect = text_surface.get_rect(center=position)
  screen.blit(text_surface, rect)

def show_start_screen(screen, top_scores):
  screen.fill(settings.BLACK)
  draw_text(screen, "ASTEROIDS", (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 4), 64, settings.OFF_WHITE)
  draw_text(screen, "Press any key to start", (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2), 32, settings.OFF_WHITE)
  draw_text(screen, "Use arrow keys to move and space to shoot", (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * 3 // 4), 24, settings.OFF_WHITE)
  font = pygame.font.SysFont(None, 24)
  y_offset = 100
  for name, score in top_scores:
    score_text = f"{name}: {score}"
    text_surface = font.render(score_text, True, settings.WHITE)
    screen.blit(text_surface, (settings.SCREEN_WIDTH // 4, y_offset))
    y_offset += 30

  pygame.display.flip()
  waiting = True
  while waiting:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        waiting = False

def show_game_over_screen(screen, score):
  screen.fill(settings.BLACK)
  draw_text(screen, "GAME OVER", 
            (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3), 
            64, settings.RED)
  draw_text(screen, f"Score: {score}", 
            (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2), 
            32, settings.OFF_WHITE)
  draw_text(screen, "Press 'r' to restart", 
            (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * 2 // 3), 
            24, settings.OFF_WHITE)

  pygame.display.flip()
  waiting = True
  while waiting:
      for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
              waiting = False