# Snake Tutorial Python

import math
import pickle
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from classes.cube import Cube
from classes.snake import Snake, Color
import matplotlib.pyplot as plt

import neat
import os

from config import Args


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


gen = 0
best_fitness_all_gens = 0
data = []


def eval_genomes(genomes: list[(int, neat.DefaultGenome)], config, show=False):
    global width, rows, gen, best_fitness_all_gens
    width = 500
    rows = 20
    if show:
        win = pygame.display.set_mode((width, width))
    else:
        win = None
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
        snack = Cube(random_snack_2(len(snake.body)), color=(0, 255, 0))
        snacks.append(snack)
        ges.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    clock = pygame.time.Clock()
    lives = 100

    while flag:
        lives -= 1
        # pygame.time.delay(50)
        if show:
            clock.tick(10)

        if len(snakes) == 0:
            break

        for i, snake in enumerate(snakes):
            snack = snacks[i]
            ge = ges[i]

            l = 1
            r = 1
            u = 1
            d = 1
            head = snake.body[0]
            for x in range(len(snake.body)):
                pos = snake.body[x].pos
                if head.pos[0] == pos[0] and head.pos[1] + 1 == pos[1]:
                    d = 0
                if head.pos[0] == pos[0] and head.pos[1] - 1 == pos[1]:
                    u = 0
                if head.pos[0] + 1 == pos[0] and head.pos[1] == pos[1]:
                    r = 0
                if head.pos[0] - 1 == pos[0] and head.pos[1] == pos[1]:
                    l = 0
            l1 = 0
            r1 = 0
            u1 = 0
            d1 = 0

            if snack.pos[0] - snake.body[0].pos[0] > 0:
                r1 = 1
            elif snack.pos[0] - snake.body[0].pos[0] < 0:
                l1 = 1

            if snack.pos[1] - snake.body[0].pos[1] > 0:
                d1 = 1
            elif snack.pos[1] - snake.body[0].pos[1] < 0:
                u1 = 1

            output = nets[i].activate(
                (l1, u1, r1, d1, l, u, r, d))

            max_value = max(output)
            max_indexes = [i for i, j in enumerate(output) if j == max_value]

            max_index = random.choice(max_indexes)

            snake.move_with_direction(max_index)
            if snake.body[0].pos == snack.pos:
                snake.addCube()
                snacks[i] = Cube(random_snack_2(
                    len(snake.body)), color=(0, 255, 0))
                ge.fitness += 10

            # if head.pos[0] < 0 or head.pos[0] > 19 or head.pos[1] < 0 or head.pos[1] > 19:
            #     ge.fitness -= 5
            #     snakes.pop(i)
            #     snacks.pop(i)
            #     ges.pop(i)
            #     best_fitness = max(best_fitness, ge.fitness)
            #     continue

            if lives + len(snake.body) * 50 <= 0:
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
        if show:
            redraw_window(win, snake, snack)
            for i in range(len(snakes)):
                snake = snakes[i]
                snack = snacks[i]
                draw_snake_snack(win, snake, snack)
            pygame.display.update()

    best_fitness_all_gens = max(best_fitness_all_gens, best_fitness)
    print(
        f"Generation:{gen}-------Fitness:{best_fitness}-------BestFitness:{best_fitness_all_gens}-------", end='\r')

    data.append(best_fitness)
    gen += 1


def get_next_filename(prefix):
    directory = os.path.dirname(prefix)
    base_prefix = os.path.basename(prefix)
    highest_num = 0
    for filename in os.listdir(directory):
        if filename.startswith(base_prefix) and filename.endswith('.pkl'):
            num = int(filename[len(base_prefix):-4])
            highest_num = max(highest_num, num)
    return prefix + str(highest_num + 1) + '.pkl'


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
    if Args.is_retrain:
        p = neat.Checkpointer.restore_checkpoint(Args.retrain_checkpoint)
    else:
        p = neat.Population(config)

    if Args.generation_interval != -1:
        checkpoint = neat.Checkpointer(
            Args.generation_interval, filename_prefix=Args.checkpoint_prefix)
        p.add_reporter(checkpoint)

    winner = p.run(eval_genomes, Args.number_runs)

    # Save checkpoint when a winner is found
    checkpoint.save_checkpoint(config, p.population, p.species, p.generation)

    # show final stats
    print('\nBest genome:')
    print(f"Key: {winner.key}")
    print(f"Fitness: {winner.fitness}")

    winner_file = get_next_filename(Args.winner_prefix)

    with open(winner_file, 'wb') as f:
        pickle.dump(winner, f)

    # data/winner-x.txt
    data_folder = Args.data_prefix.split('/')[0]
    data_of_winner_file = data_folder + '/' + winner_file.split('/')[-1]
    data_of_winner_file = data_of_winner_file[:-4] + '.txt'

    # save data to data_of_winner_file
    with open(data_of_winner_file, 'w') as f:
        for item in data:
            f.write("%s\n" % item)

    # draw plot with data
    plt.plot(data)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.show()


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, Args.config_neat_filename)
    run(config_path)
