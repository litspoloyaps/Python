import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Factory Clicker")

# Colors
WHITE = (255, 255, 255)
PINK = (255, 182, 193)
BLUE = (173, 216, 230)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 36)

# Game variables
candies = 0
click_power = 1
auto_candies = 0
auto_upgrade_cost = 50
click_upgrade_cost = 20
clock = pygame.time.Clock()

# Buttons
click_button = pygame.Rect(200, 150, 200, 100)
click_upgrade_button = pygame.Rect(50, 300, 200, 50)
auto_upgrade_button = pygame.Rect(350, 300, 200, 50)

# Auto candy event
AUTO_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(AUTO_EVENT, 1000)  # Every 1 second

def draw():
    screen.fill(WHITE)
    # Draw click button
    pygame.draw.rect(screen, PINK, click_button)
    screen.blit(font.render("Click Me!", True, BLACK), (click_button.x + 40, click_button.y + 30))

    # Draw upgrades
    pygame.draw.rect(screen, BLUE, click_upgrade_button)
    screen.blit(font.render(f"Upgrade Click ({click_upgrade_cost})", True, BLACK), (click_upgrade_button.x + 5, click_upgrade_button.y + 10))
    
    pygame.draw.rect(screen, BLUE, auto_upgrade_button)
    screen.blit(font.render(f"Hire Worker ({auto_upgrade_cost})", True, BLACK), (auto_upgrade_button.x + 10, auto_upgrade_button.y + 10))

    # Draw candy count
    screen.blit(font.render(f"Candies: {candies}", True, BLACK), (10, 10))
    screen.blit(font.render(f"Click Power: {click_power}", True, BLACK), (10, 50))
    screen.blit(font.render(f"Auto Candies/sec: {auto_candies}", True, BLACK), (10, 90))
    
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if click_button.collidepoint(event.pos):
                candies += click_power
            if click_upgrade_button.collidepoint(event.pos) and candies >= click_upgrade_cost:
                candies -= click_upgrade_cost
                click_power += 1
                click_upgrade_cost = int(click_upgrade_cost * 1.5)
            if auto_upgrade_button.collidepoint(event.pos) and candies >= auto_upgrade_cost:
                candies -= auto_upgrade_cost
                auto_candies += 1
                auto_upgrade_cost = int(auto_upgrade_cost * 1.5)
        if event.type == AUTO_EVENT:
            candies += auto_candies

    draw()
    clock.tick(60)
