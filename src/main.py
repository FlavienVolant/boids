import pygame
import random

from fish import Fish
from simulation import Simulation

pygame.init()

SCREEN_WIDTH = 620
SCREEN_HEIGHT = 620

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

simulation = Simulation([
    Fish(position=(random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT))
    for _ in range(120)
])

while running:

    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("lightblue")

    simulation.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
    simulation.draw(screen)

    pygame.display.flip()

pygame.quit()