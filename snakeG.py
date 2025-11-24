import pygame
import random
import sys
import math
import os
import array

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Rainbow Snake - Realistic")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 15
GRID = 10

snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_speed = GRID
direction = 'RIGHT'
change_to = direction

food_pos = [random.randrange(1, WIDTH//GRID) * GRID, random.randrange(1, HEIGHT//GRID) * GRID]
food_spawn = True

score = 0
high_score = 0
particles = []

ASSET_HEAD = 'snake_head.png'
ASSET_BODY = 'snake_body.png'
ASSET_OOF = 'oof.wav'

head_img = None
body_img = None
death_sound = None
eat_sound = None

def load_image(path):
    if os.path.exists(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            return None
    return None

head_img = load_image(ASSET_HEAD)
body_img = load_image(ASSET_BODY)

def make_oof():
    buf = array.array('h')
    vol = 3000
    for i in range(2000):
        t = i / 2000.0
        sample = int(vol * math.sin(50 * (t**2)))
        buf.append(sample)
    try:
        return pygame.mixer.Sound(buffer=buf)
    except:
        return None

def make_eat():
    buf = array.array('h')
    vol = 3000
    length = 800
    for i in range(length):
        t = i / length
        sample = int(vol * (1 - t) * math.sin(2 * math.pi * 900 * t))
        buf.append(sample)
    try:
        return pygame.mixer.Sound(buffer=buf)
    except:
        return None

if os.path.exists(ASSET_OOF):
    try:
        death_sound = pygame.mixer.Sound(ASSET_OOF)
    except:
        death_sound = make_oof()
else:
    death_sound = make_oof()

eat_sound = make_eat()

def add_particles(pos):
    for _ in range(14):
        particles.append({
            'x': pos[0] + GRID//2,
            'y': pos[1] + GRID//2,
            'dx': random.uniform(-3, 3),
            'dy': random.uniform(-3, 3),
            'life': random.randint(10, 26),
            'color': [random.randint(100,255), random.randint(100,255), random.randint(100,255)],
            'r': random.randint(2,5)
        })

def update_particles():
    global particles
    new_particles = []
    for p in particles:
        p['x'] += p['dx']
        p['y'] += p['dy']
        p['dy'] += 0.12
        p['life'] -= 1
        if p['life'] > 0:
            new_particles.append(p)
            pygame.draw.circle(win, p['color'], (int(p['x']), int(p['y'])), p['r'])
    particles = new_particles

def rainbow_color(index):
    r = int(127 * (1 + math.sin(index * 0.25)))
    g = int(127 * (1 + math.sin(index * 0.25 + 2)))
    b = int(127 * (1 + math.sin(index * 0.25 + 4)))
    return (r, g, b)

def make_head_surface(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    w = size
    pygame.draw.ellipse(surf, (80,120,60), (0, 0, w, int(w*0.7)))
    for i in range(6):
        for j in range(6):
            cx = int(j * (w/6) + (i%2)*5)
            cy = int(i * (w/12) + 5)
            pygame.draw.circle(surf, (60,100,50), (cx, cy), 6, 1)
    eye_x = int(w*0.65)
    eye_y = int(w*0.25)
    pygame.draw.circle(surf, (20,20,20), (eye_x, eye_y), max(2, w//15))
    pygame.draw.circle(surf, (255,255,255), (eye_x+2, eye_y-1), max(1, w//40))
    pygame.draw.ellipse(surf, (100,170,90,60), (int(w*0.1), int(w*0.05), int(w*0.7), int(w*0.3)))
    return surf

def make_body_surface(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    for i in range(3):
        pygame.draw.ellipse(surf, (70,110,60), (i*2, 0, size- i*4, size- i*6))
    return surf

SEGMENT_SIZE = GRID
head_surface_base = pygame.transform.smoothscale(head_img, (SEGMENT_SIZE*2, SEGMENT_SIZE*2)) if head_img else make_head_surface(SEGMENT_SIZE*2)
body_surface = pygame.transform.smoothscale(body_img, (SEGMENT_SIZE, SEGMENT_SIZE)) if body_img else make_body_surface(SEGMENT_SIZE)

ANGLE = {'RIGHT': 0, 'LEFT': 180, 'UP': 90, 'DOWN': -90}

def game_over():
    global score, snake_body, snake_pos, direction, FPS, high_score
    if death_sound:
        try:
            death_sound.play()
        except:
            pass
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
        if eat_sound:
            try:
                eat_sound.play()
            except:
                pass
        FPS += 0.5
        add_particles(food_pos)
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, WIDTH//GRID) * GRID, random.randrange(1, HEIGHT//GRID) * GRID]
        food_spawn = True

    win.fill(BLACK)
    update_particles()

    for idx, block in enumerate(snake_body[1:]):
        color = rainbow_color(idx)
        rect = pygame.Rect(block[0], block[1], SEGMENT_SIZE, SEGMENT_SIZE)
        pygame.draw.ellipse(win, color, rect)
        win.blit(body_surface, (block[0], block[1]))

    head_angle = ANGLE.get(direction, 0)
    head_surf = pygame.transform.rotate(head_surface_base, head_angle)
    head_rect = head_surf.get_rect(center=(snake_body[0][0] + SEGMENT_SIZE//2, snake_body[0][1] + SEGMENT_SIZE//2))
    win.blit(head_surf, head_rect.topleft)

    pygame.draw.rect(win, RED, pygame.Rect(food_pos[0], food_pos[1], GRID, GRID))

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