from pygame import gfxdraw
import random
import pygame
import os
import time as t
from math import sqrt

# Game presets
start_time = t.time()
fps = 120
width, height = 1000, 770

# Centers window
x, y = 1360 - width, 40
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (x, y)
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing balls")
clock = pygame.time.Clock()

background = pygame.image.load("img/start_img.png")

# initialize pygame mixer and load audio file
pygame.mixer.init()

white = (255, 255, 255)
black = (0, 0, 0)

g = -9.81
bigr = 400 // 2  # rad of big cirlce
centx, centy = width // 2, height // 2  # center of cirlce
frames = 0

class Balls:
    
    # Voice settings
    soundIndex = 1
    soundName = "part_" + str(soundIndex) + ".mp3"
    # radius increasing per bounce
    radiusForBounce = 10
    # ball speed settings
    speedForBounce = 0.001
    speed = 1
    # random rgb values of ring (white for start)
    i = 255
    j = 255
    k = 255
    # random rgb values of ball (white for start)
    a = 255
    b = 255
    c = 255

    trail = True
    balls = list()

    def __init__(self, name, radius, thicc, posx, posy):
        Balls.balls.append(self)

        self.name = name
        self.color = (self.i, self.j, self.k)
        self.radius = radius
        self.thicc = thicc
        self.posx = posx
        self.posy = posy
        self.velx = 0
        self.vely = 0
        self.acc = g / fps
        self.track = list()

    def drawball(self):
        pygame.draw.circle(
            screen,
            (self.i, self.j, self.k),
            (self.posx, self.posy),
            self.radius,
            self.thicc,
        )

    def collision_handling(self):
        temp = 0
        vel = sqrt(self.velx**2 + self.vely**2)

        x, y = centx, centy  # center of circle
        ballx, bally = self.posx, self.posy
        velx, vely = self.velx, self.vely
        # center to ball is the distance between ball's center and the ring's center
        center_to_ball = sqrt((x - ballx) ** 2 + (y - bally) ** 2)

        if center_to_ball >= (bigr - self.radius):
            self.soundName = "part_" + str(self.soundIndex) + ".mp3"
            self.sound = "sounds/" + self.soundName
            pygame.mixer.Sound.play(pygame.mixer.Sound(self.sound))
            if self.soundIndex >= 88:
                self.soundIndex = 1
            else:
                self.soundIndex += 1

            self.radius += self.radiusForBounce
            self.speed += self.speedForBounce

            # ball random colors
            self.i = random.randint(0, 255)
            self.j = random.randint(0, 255)
            self.k = random.randint(0, 255)
            # circle random colors
            self.a = random.randint(0, 255)
            self.b = random.randint(0, 255)
            self.c = random.randint(0, 255)

            while sqrt((x - self.posx) ** 2 + (y - self.posy) ** 2) > (
                bigr - self.radius
            ):
                step = 0.3
                # moving the ball backwawrds in dir of velocity by small steps
                self.posx += -self.velx * step / vel
                self.posy -= -self.vely * step / vel
                if(temp > 100000):
                    t.sleep(3)
                    quit()
                else:
                    temp+=1
                
            normal = ballx - x, bally - y
            normal_mag = center_to_ball  # sqrt(normal[0]**2 + normal[1]**2)
            n = normal[0] / normal_mag, normal[1] / normal_mag
            nx, ny = n[0], n[1]

            d = velx, -vely  # incident
            dx, dy = d[0], d[1]

            reflected = dx - 2 * dot(n, d) * nx, dy - 2 * dot(n, d) * ny

            self.velx = reflected[0]
            self.vely = -reflected[1]

    def motion(self):

        self.velx += 0
        self.vely += self.acc

        self.posx += self.velx * self.speed
        self.posy -= self.vely * self.speed

        every = 2
        period = 5
        if frames % every == 0 and Balls.trail:
            self.track.append((self.posx, self.posy))
        if Balls.trail is False:
            self.track.clear()
        elif len(self.track) > fps * period / every:
            self.track.pop(0)


def aacirlce(rad, x, y, color, thickness):
    layers = thickness
    increment = 0.3
    for i in range(int(layers / increment) + 3):
        gfxdraw.aacircle(screen, int(x), int(y), int(rad - (i * increment)), color)


def draw_cricle(color, radius, thicc, posx, posy):
    pygame.draw.circle(screen, color, (posx, posy), radius, thicc)


def dot(v, u):
    """v and u are vectors. v and u -> list"""
    vx, vy = v[0], v[1]
    ux, uy = u[0], u[1]
    dotproduct = vx * ux + vy * uy
    return dotproduct


ball = Balls(
    "green ball",
    12,
    0,
    width // 2.5,
    height // 3,
)
pause = False
start_sim = False


while start_sim is False:

    screen.fill(black)
    screen.blit(background, [0, 0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                start_sim = True

    pygame.display.update()
    clock.tick(fps)

while True:

    screen.fill(black)
    for ball in Balls.balls:
        if len(ball.track) > 2 and Balls.trail:
            aacirlce(bigr, width // 2, height // 2, (ball.a, ball.b, ball.c), 10)
            pygame.draw.aalines(screen, white, False, ball.track, ball.radius)

    for ball in Balls.balls:

        ball.drawball()
        if not pause:
            ball.collision_handling()
            ball.motion()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_t:
                Balls.trail = not Balls.trail

    pygame.display.update()
    clock.tick(fps)
    frames += 1
