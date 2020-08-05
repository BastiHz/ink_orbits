
# TODO:
# - better distribution of positions and velocities for prettier results
# - more or different colors?
# - better ink loss rate, maybe bigger loose more or less than small sizes?

# The equations of motion are imprecise over time because of the timesteps
# and because I'm not using runge-kutta integration. But that's not important
# in this project.


import random
import math

import pygame


DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
FPS = 60
N_BLOBS = 50
RADIUS_MIN = 5
RADIUS_MAX = 20
BACKGROUND_COLOR = (230, 230, 230)
BLOB_COLOR = (60, 220, 60)
GM = 1e6  # attractor mass times gravitational constant
CENTER_X = DISPLAY_WIDTH / 2
CENTER_Y = DISPLAY_HEIGHT / 2
RADIUS_LOSS_RATE = 3  # pixel per second
PAINT_ORBIT = True


pygame.init()
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Ink Orbits")
clock = pygame.time.Clock()


def restart():
    display.fill(BACKGROUND_COLOR)
    return [InkBlob() for _ in range(N_BLOBS)]


class InkBlob:
    def __init__(self):
        self.radius = random.randint(RADIUS_MIN, RADIUS_MAX)
        self.color = BLOB_COLOR
        self.pos_x = random.uniform(0, DISPLAY_WIDTH)
        self.pos_y = random.uniform(0, DISPLAY_HEIGHT)
        self.vel_x = random.uniform(-100, 100)
        self.vel_y = random.uniform(-100, 100)

    def update(self, dt):
        dist_x = self.pos_x - CENTER_X
        dist_y = self.pos_y - CENTER_Y
        dist = math.hypot(dist_x, dist_y)
        acceleraton = - GM / dist**2
        acc_x = dist_x / dist * acceleraton
        acc_y = dist_y / dist * acceleraton
        self.vel_x += acc_x * dt
        self.vel_y += acc_y * dt
        self.pos_x += self.vel_x * dt * 0.5
        self.pos_y += self.vel_y * dt * 0.5

        self.radius -= RADIUS_LOSS_RATE * dt

    def draw(self):
        pygame.draw.circle(display, self.color, (self.pos_x, self.pos_y), self.radius)


inkblobs = restart()
running = True
while running:
    dt = clock.tick(FPS) / 1000  # seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                inkblobs = restart()

    if not PAINT_ORBIT:
        display.fill(BACKGROUND_COLOR)

    inkblobs[:] = [blob for blob in inkblobs if blob.radius >= 1]

    for blob in inkblobs:
        blob.update(dt)
        blob.draw()
    pygame.display.flip()
