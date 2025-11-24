import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Player Snake Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

font = pygame.font.SysFont(None, 35)

def draw_snake(snake, color):
    for block in snake:
        pygame.draw.rect(screen, color, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))

def random_food():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return [x, y]

def show_message(message):
    text = font.render(message, True, WHITE)
    screen.blit(text, [WIDTH // 4, HEIGHT // 2])

def main():
    snake1 = [[100, 100]]
    snake2 = [[500, 300]]
    dir1 = [CELL_SIZE, 0]
    dir2 = [-CELL_SIZE, 0]
    food = random_food()
    score1 = 0
    score2 = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: dir1 = [0, -CELL_SIZE]
                if event.key == pygame.K_s: dir1 = [0, CELL_SIZE]
                if event.key == pygame.K_a: dir1 = [-CELL_SIZE, 0]
                if event.key == pygame.K_d: dir1 = [CELL_SIZE, 0]

                if event.key == pygame.K_UP: dir2 = [0, -CELL_SIZE]
                if event.key == pygame.K_DOWN: dir2 = [0, CELL_SIZE]
                if event.key == pygame.K_LEFT: dir2 = [-CELL_SIZE, 0]
                if event.key == pygame.K_RIGHT: dir2 = [CELL_SIZE, 0]

        snake1[0][0] += dir1[0]
        snake1[0][1] += dir1[1]
        snake2[0][0] += dir2[0]
        snake2[0][1] += dir2[1]

        snake1.insert(0, list(snake1[0]))
        snake2.insert(0, list(snake2[0]))

        if snake1[0] == food:
            score1 += 1
            food = random_food()
        else:
            snake1.pop()

        if snake2[0] == food:
            score2 += 1
            food = random_food()
        else:
            snake2.pop()

        if (snake1[0] in snake1[1:] or snake1[0] in snake2 or
            snake1[0][0] < 0 or snake1[0][0] >= WIDTH or
            snake1[0][1] < 0 or snake1[0][1] >= HEIGHT):
            screen.fill(BLACK)
            show_message("Player 2 Wins!")
            pygame.display.update()
            pygame.time.delay(2000)
            break

        if (snake2[0] in snake2[1:] or snake2[0] in snake1 or
            snake2[0][0] < 0 or snake2[0][0] >= WIDTH or
            snake2[0][1] < 0 or snake2[0][1] >= HEIGHT):
            screen.fill(BLACK)
            show_message("Player 1 Wins!")
            pygame.display.update()
            pygame.time.delay(2000)
            break

        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))
        draw_snake(snake1, RED)
        draw_snake(snake2, BLUE)

        score_text = font.render(f"P1: {score1}  P2: {score2}", True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()
