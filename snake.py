import pygame
import random
import sys
import math


pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Rainbow Snake")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 15

snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_speed = 10
direction = 'RIGHT'
change_to = direction

food_pos = [random.randrange(1, WIDTH//10) * 10, random.randrange(1, HEIGHT//10) * 10]
food_spawn = True


score = 0
high_score = 0

particles = []

def add_particles(pos):
    for _ in range(10):
        particles.append({
            'x': pos[0] + 5,
            'y': pos[1] + 5,
            'dx': random.uniform(-2, 2),
            'dy': random.uniform(-2, 2),
            'life': random.randint(10, 20),
            'color': [random.randint(100,255), random.randint(100,255), random.randint(100,255)]
        })

def update_particles():
    global particles
    new_particles = []
    for p in particles:
        p['x'] += p['dx']
        p['y'] += p['dy']
        p['life'] -= 1
        if p['life'] > 0:
            new_particles.append(p)
            pygame.draw.circle(win, p['color'], (int(p['x']), int(p['y'])), 3)
    particles = new_particles

def rainbow_color(index):
    r = int(127 * (1 + math.sin(index * 0.3)))
    g = int(127 * (1 + math.sin(index * 0.3 + 2)))
    b = int(127 * (1 + math.sin(index * 0.3 + 4)))
    return (r, g, b)

def game_over():
    global score, snake_body, snake_pos, direction, FPS, high_score
    if score > high_score:
        high_score = score
    score = 0
    FPS = 15
    snake_body[:] = [[100, 50], [90, 50], [80, 50]]
    snake_pos[:] = [100, 50]
    direction = 'RIGHT'


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
  

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_pos[1] -= snake_speed
    if direction == 'DOWN':
        snake_pos[1] += snake_speed
    if direction == 'LEFT':
        snake_pos[0] -= snake_speed
    if direction == 'RIGHT':
        snake_pos[0] += snake_speed

    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10
        FPS += 0.5
        add_particles(food_pos)
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, WIDTH//10) * 10, random.randrange(1, HEIGHT//10) * 10]
        food_spawn = True

    win.fill(BLACK)

    update_particles()

    for idx, block in enumerate(snake_body):
        pygame.draw.rect(win, rainbow_color(idx), pygame.Rect(block[0], block[1], 10, 10))

    pygame.draw.rect(win, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        game_over()
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    font = pygame.font.SysFont('Arial', 20)
    score_surface = font.render(f'Score: {score}  High Score: {high_score}', True, WHITE)
    win.blit(score_surface, (10, 10))

    pygame.display.update()

    clock.tick(FPS)
