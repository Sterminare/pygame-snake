import pygame
from random import randint
from pygame.math import Vector2
from sys import exit


class Display:
    def __init__(self):
        self.size = Vector2(cell_number_horizontal * cell_size, display_height)

    def draw(self):
        display_rect = pygame.Rect((0, cell_number_vertical * cell_size), (self.size.x, self.size.y))
        pygame.draw.rect(screen, display_color, display_rect)


class Snake:
    def __init__(self):
        self.previous_direction = Vector2(1, 0)
        self.body = [Vector2(16, 10), Vector2(15, 10), Vector2(14, 10)]
        self.direction = Vector2(1, 0)

    def reset(self):
        self.body = [Vector2(16, 10), Vector2(15, 10), Vector2(14, 10)]
        self.direction = Vector2(1, 0)

    def draw(self):
        for segment in self.body:
            segment_rect = pygame.Rect(int(segment.x) * cell_size, int(segment.y) * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, snake_color, segment_rect)

    def move(self):
        next_body = self.body[:-1]
        next_body.insert(0, next_body[0] + self.direction)
        if next_body[0] == self.body[1]:
            self.direction = self.previous_direction
        else:
            self.body = next_body[:]

    def grow(self):
        next_body = self.body[:]
        next_body.insert(-0, next_body[0] + self.direction)
        self.body = next_body[:]


class Fruit:
    def __init__(self):
        self.x = randint(0, cell_number_horizontal - 1)
        self.y = randint(0, cell_number_vertical - 1)
        self.pos = Vector2(self.x, self.y)

    def draw(self):
        fruit_rect = pygame.Rect(int(self.pos.x) * cell_size, int(self.pos.y) * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, fruit_color, fruit_rect)

    def reposition(self):
        self.x = randint(0, cell_number_horizontal - 1)
        self.y = randint(0, cell_number_vertical - 1)
        self.pos = Vector2(self.x, self.y)
        if self.pos.x in [0, cell_number_horizontal - 1] and self.pos.y in [0, cell_number_vertical - 1]:
            self.reposition()


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.display = Display()

    def update(self):
        self.snake.move()
        self.check_fruit_collision()
        self.check_gameover()

        for segment in self.snake.body:
            if self.fruit.pos == segment:
                self.fruit.reposition()
                break

    def draw(self):
        self.snake.draw()
        self.fruit.draw()
        self.display.draw()

    def reset(self):
        self.snake.reset()
        self.fruit.reposition()

    def check_fruit_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.reposition()
            self.snake.grow()

    def check_gameover(self):
        for segment in self.snake.body[1:]:
            if self.snake.body[0] == segment:
                self.reset()
        if not 0 <= self.snake.body[0].x < cell_number_horizontal or not 0 <= self.snake.body[0].y < cell_number_vertical:
            self.reset()


pygame.init()

cell_size = 30
cell_number_horizontal = 30
cell_number_vertical = 15

display_height = 200

background_color = pygame.Color('#689689')
display_color = pygame.Color('#36413e')
display_accent_color = pygame.Color('#de8f6e')
snake_color = pygame.Color('#b2e6d4')
fruit_color = pygame.Color('#83e8ba')

screen = pygame.display.set_mode((cell_size * cell_number_horizontal, cell_size * cell_number_vertical + display_height))
clock = pygame.time.Clock()

screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 100)

main = Main()
pause = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == screen_update and not pause:
            main.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main.snake.previous_direction = main.snake.direction
                main.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                main.snake.previous_direction = main.snake.direction
                main.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                main.snake.previous_direction = main.snake.direction
                main.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                main.snake.previous_direction = main.snake.direction
                main.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_ESCAPE:
                if pause:
                    pause = False
                else:
                    pause = True

    screen.fill(background_color)
    main.draw()
    pygame.display.update()
    clock.tick(60)
