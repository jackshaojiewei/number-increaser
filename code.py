import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 400, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Counting Up")

# Set up fonts
font = pygame.font.SysFont(None, 72)

# Set up clock
clock = pygame.time.Clock()

# Set up counting variables
number = 0
counter_event = pygame.USEREVENT + 1
pygame.time.set_timer(counter_event, 1000)  # 1000 milliseconds = 1 second

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == counter_event:
            number += 1

    # Clear screen
    screen.fill((30, 30, 30))  # Dark gray background

    # Render number
    text = font.render(str(number), True, (255, 255, 255))  # White text
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
