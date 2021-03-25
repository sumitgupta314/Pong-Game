import pygame
import os
import random

# Initialize pygame
pygame.init()

# Creating and setting the screen size
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Icon and caption
icon = pygame.image.load(os.path.join("pong_icon.png"))
pygame.display.set_icon(icon)
pygame.display.set_caption("Pong - Python Game")

# Game Clock and FPS
# This is to keep runtime speed of the game consistent across different computers
clock = pygame.time.Clock()
FPS = 60


class paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.score = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

    def render_score(self, font, dest):
        score = font.render(f"{self.score}", True, (255, 255, 255))
        screen.blit(score, dest)


class ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # self.width = 25
        # self.height = 25
        self.radius = 12
        self.x_change = 0
        self.y_change = 0

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)


# Initialize paddle and pong ball positions
right_paddle = paddle(WIDTH - 40, HEIGHT / 2 - 50)
left_paddle = paddle(20, HEIGHT / 2 - 50)
pong_ball = ball(WIDTH / 2, HEIGHT / 2)
ball_speed = 5

# Randomly chooses if the ball will begin in the left or right direction
def random_x_direction():
    x_directions = ["left", "right"]
    return random.choice(x_directions)


# Randomly chooses if the ball with begin in up or down direction
def random_y_direction():
    y_directions = ["up", "down"]
    return random.choice(y_directions)


start_x_direction = random_x_direction()
start_y_direction = random_y_direction()


# ball's start direction
def random_x_change():
    if start_x_direction == "left":
        return -ball_speed
    elif start_x_direction == "right":
        return ball_speed


def random_y_change():
    if start_y_direction == "up":
        return -5
    elif start_y_direction == "down":
        return 5


pong_ball.x_change = random_x_change()
pong_ball.y_change = random_y_change()

# font type for rendering score
score_font_size = 64
font = pygame.font.Font("freesansbold.ttf", score_font_size)

running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255, 255, 255), (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.type == pygame.K_UP:
        #         right_paddle.y += -10
        #     if event.type == pygame.K_DOWN:
        #         right_paddle.y += 10

    # paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and right_paddle.y >= 0:
        right_paddle.y += -10
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height <= HEIGHT:
        right_paddle.y += 10
    if keys[pygame.K_w] and left_paddle.y >= 0:
        left_paddle.y += -10
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height <= HEIGHT:
        left_paddle.y += 10

    # Checking if pong ball touches upper or lower screen boundary and changing y-direction
    if pong_ball.y - pong_ball.radius <= 0:
        pong_ball.y_change = random.randint(4, 6)
    elif pong_ball.y + pong_ball.radius >= HEIGHT:
        pong_ball.y_change = random.randint(-6, -4)

    # checking if pong ball touches left or right screen boundary and restarting pong ball play from middle
    if pong_ball.x + pong_ball.radius >= WIDTH:
        left_paddle.score += 1
        # pong_ball.x_change = -5
        pong_ball.x = WIDTH / 2
        pong_ball.y = HEIGHT / 2
        start_x_direction = random_x_direction()
        start_y_direction = random_y_direction()
        pong_ball.x_change = random_x_change()
        pong_ball.y_change = random_y_change()
    elif pong_ball.x - pong_ball.radius <= 0:
        right_paddle.score += 1
        # pong_ball.x_change = 5
        pong_ball.x = WIDTH / 2
        pong_ball.y = HEIGHT / 2
        start_x_direction = random_x_direction()
        start_y_direction = random_y_direction()
        pong_ball.x_change = random_x_change()
        pong_ball.y_change = random_y_change()

    # Updating pong ball's position on screen
    pong_ball.x += pong_ball.x_change
    pong_ball.y += pong_ball.y_change

    # Checking if pong ball hits paddle, then changing x-direction
    if pong_ball.x + pong_ball.radius >= right_paddle.x and pong_ball.y >= right_paddle.y and pong_ball.y <= right_paddle.y + right_paddle.height:
        pong_ball.x_change = -ball_speed
    if pong_ball.x - pong_ball.radius <= left_paddle.x + left_paddle.width and pong_ball.y >= left_paddle.y and pong_ball.y <= left_paddle.y + left_paddle.height:
        pong_ball.x_change = ball_speed

    # Drawing game objects on screen and updating display
    pong_ball.draw(screen)
    left_paddle.draw(screen)
    right_paddle.draw(screen)
    left_paddle.render_score(font, (WIDTH / 2 - score_font_size, 10))
    right_paddle.render_score(font, (WIDTH / 2 + score_font_size / 2, 10))
    pygame.display.update()
