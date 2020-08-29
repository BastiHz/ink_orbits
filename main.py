
# TODO:
# - better distribution of positions and velocities for prettier results:
#   modify the parameters so the blobs don't start at the center and don't come
#   too close to the center to fling into infinity
# - more or different colors?
# - better ink loss rate, maybe bigger loose more or less than small sizes?

# The equations of motion are imprecise over time because of the timesteps
# and because I'm not using runge-kutta integration. But that's not important
# in this project.


import random

import pygame


pygame.init()

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
DISPLAY_CENTER = pygame.math.Vector2(DISPLAY_WIDTH, DISPLAY_HEIGHT) / 2
FPS = 60
N_BLOBS = 20
RADIUS_MIN = 5
RADIUS_MAX = 20
BACKGROUND_COLOR = pygame.Color(230, 230, 230)
BLOB_COLOR = pygame.Color(60, 220, 60)
GM = 1e6  # attractor mass times gravitational constant
RADIUS_LOSS_RATE = 3  # pixel per second
PAINT_ORBIT = True


class InkBlob:
    def __init__(self):
        self.radius = random.randint(RADIUS_MIN, RADIUS_MAX)
        self.color = BLOB_COLOR
        self.position = pygame.math.Vector2(
            random.uniform(0, DISPLAY_WIDTH),
            random.uniform(0, DISPLAY_HEIGHT)
        )
        self.velocity = pygame.math.Vector2(
            random.uniform(-100, 100),
            random.uniform(-100, 100)
        )

    def update(self, dt):
        distance = self.position - DISPLAY_CENTER
        acceleration = - GM / distance.length_squared() * distance.normalize()
        self.velocity += acceleration * dt
        self.position += self.velocity * dt * 0.5

        self.radius -= RADIUS_LOSS_RATE * dt

    def draw(self):
        pygame.draw.circle(display, self.color, self.position, self.radius)


def restart():
    display.fill(BACKGROUND_COLOR)
    return [InkBlob() for _ in range(N_BLOBS)]


display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Ink Orbits")
clock = pygame.time.Clock()
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

    for i, blob in sorted(enumerate(inkblobs), reverse=True):
        # reversed because the list is modified while iterating
        if blob.radius < 1:
            del inkblobs[i]
            continue
        blob.update(dt)
        blob.draw()
    pygame.display.flip()
