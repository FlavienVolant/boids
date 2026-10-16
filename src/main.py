import pygame
import random

from fish import Fish

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MAX_SPEED = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

fishs = [
    Fish((random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT), (random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED)))
    for _ in range(1_000)
]


while running:

    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("lightblue")

    for fish in fishs:
        pygame.draw.circle(screen, "yellow", fish.position, 10)
        fish.update(dt)

    pygame.display.flip()




pygame.quit()