# Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from classes.cube import Cube
from classes.snake import Snake, Color

import neat
import os


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
    draw_grid(width, rows, surface)


def draw_snake_snack(surface, snake: Snake, snack: Cube):
    snake.draw(surface)
    snack.draw(surface)


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


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


gen = 0
best_fitness_all_gens = 0


def eval_genomes(genomes: list[(int, neat.DefaultGenome)], config):
    global width, rows, gen, best_fitness_all_gens
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    snakes: list[Snake] = []
    snacks: list[Cube] = []
    ges: list[neat.DefaultGenome] = []
    nets = []

    flag = True
    best_fitness = 0

    for genome_id, genome in genomes:
        snake = Snake(Color.get_color(len(snakes)), (10, 10))
        snakes.append(snake)
        snake.addCube()
        snake.addCube()
        snack = Cube(random_snack(rows, snake), color=(0, 255, 0))
        snacks.append(snack)
        ges.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    clock = pygame.time.Clock()
    lives = 2000

    while flag:
        lives -= 1
        # pygame.time.delay(50)
        if True:
            clock.tick(10)

        if len(snakes) == 0:
            break

        for i, snake in enumerate(snakes):
            snack = snacks[i]
            ge = ges[i]

            l = 0
            r = 0
            u = 0
            d = 0
            head = snake.body[0]
            for x in range(len(snake.body)):
                pos = snake.body[x].pos
                if pos[0] == head.pos[0] and pos[1] + 1 == head.pos[1]:
                    d = 1
                if pos[0] == head.pos[0] and pos[1] - 1 == head.pos[1]:
                    u = 1
                if pos[0] + 1 == head.pos[0] and pos[1] == head.pos[1]:
                    r = 1
                if pos[0] - 1 == head.pos[0] and pos[1] == head.pos[1]:
                    l = 1

            output = nets[i].activate(
                (snack.pos[0] - snake.body[0].pos[0], snack.pos[1] - snake.body[0].pos[1], l, r, u, d))

            max_index = output.index(max(output))

            snake.move_with_direction(max_index)
            if snake.body[0].pos == snack.pos:
                snake.addCube()
                snacks[i] = Cube(random_snack(rows, snake), color=(0, 255, 0))
                ge.fitness += 10

            if head.pos[0] < 0 or head.pos[0] > 19 or head.pos[1] < 0 or head.pos[1] > 19:
                ge.fitness -= 5
                snakes.pop(i)
                snacks.pop(i)
                ges.pop(i)
                best_fitness = max(best_fitness, ge.fitness)
                continue

            if lives + len(snake.body) * 400 <= 0:
                snakes.pop(i)
                snacks.pop(i)
                ges.pop(i)
                best_fitness = max(best_fitness, ge.fitness)
                continue

            for x in range(len(snake.body)):
                if x == 0:
                    continue
                if snake.body[x].pos == head.pos:
                    ge.fitness -= 5
                    snakes.pop(i)
                    snacks.pop(i)
                    ges.pop(i)
                    best_fitness = max(best_fitness, ge.fitness)
                    break
        if True:
            redraw_window(win, snake, snack)
            for i in range(len(snakes)):
                snake = snakes[i]
                snack = snacks[i]
                draw_snake_snack(win, snake, snack)
            pygame.display.update()

    best_fitness_all_gens = max(best_fitness_all_gens, best_fitness)
    print(
        f"Generation:{gen}-------Fitness:{best_fitness}-------BestFitness:{best_fitness_all_gens}-------", end='\r')

    gen += 1


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play snake.
    :param config_file: location of config file
    :return: None
    """
    global gen
    gen = 0
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    # p = neat.Population(config)
    p = neat.Checkpointer.restore_checkpoint(
        'checkpoints/neat-checkpoint-280098')
    # p.load_checkpoint('checkpoints/neat-checkpoint-5000')

    # Add a stdout reporter to show progress in the terminal.
    # p.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(
        100000, filename_prefix='checkpoints/neat-checkpoint-'))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 1000)

    # show final stats
    # print('\nBest genome:\n{!s}'.format(winner))
    print('\nBest genome:')
    print(f"Key: {winner.key}")
    print(f"Fitness: {winner.fitness}")


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
