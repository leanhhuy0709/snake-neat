# Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from classes.cube import Cube
from classes.snake import Snake


def draw_grid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redraw_window(surface, snake: Snake, snack: Cube):
    global rows, width
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def random_snack_2(index=0):

    raw_pos = [(4, 0), (7, 1), (19, 12), (14, 12), (10, 6), (19, 13), (9, 9), (16, 10), (7, 2), (0, 16), (9, 15), (9, 12), (19, 14), (13, 19), (7, 2), (10, 6), (15, 10), (6, 12), (1, 19), (9, 19), (1, 5), (2, 3), (17, 4), (17, 7), (18, 0), (2, 19), (18, 2), (17, 19), (2, 4), (7, 11), (18, 13), (4, 3), (3, 10), (15, 13), (14, 7), (13, 5), (4, 10), (0, 8), (8, 7), (5, 0), (7, 3), (15, 17), (3, 7), (16, 4), (10, 9), (6, 12), (10, 1), (6, 3), (13, 5), (16, 18),
               (5, 19), (7, 15), (14, 9), (5, 2), (2, 4), (0, 6), (9, 14), (18, 4), (0, 19), (5, 1), (13, 10), (6, 6), (18, 14), (4, 14), (12, 15), (13, 16), (2, 1), (10, 3), (18, 3), (15, 14), (12, 8), (12, 10), (5, 9), (16, 19), (5, 15), (7, 9), (11, 16), (7, 4), (7, 18), (14, 18), (14, 17), (0, 1), (4, 1), (12, 16), (11, 0), (4, 0), (3, 4), (10, 1), (15, 19), (17, 10), (16, 16), (14, 18), (15, 15), (19, 18), (3, 2), (6, 0), (19, 18), (17, 17), (0, 5), (0, 1), (7, 4), (5, 6)]

    return raw_pos[index % len(raw_pos)]


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    snake = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack_2(len(snake.body)), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.body[0].pos == snack.pos:
            snake.addCube()
            snack = Cube(random_snack_2(len(snake.body)), color=(0, 255, 0))

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x+1:])):
                print('Score: ', len(snake.body))
                message_box('You Lost!', 'Play again...')
                snake.reset((10, 10))
                break

        redraw_window(win, snake, snack)


main()
