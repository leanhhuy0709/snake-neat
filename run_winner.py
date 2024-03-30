from run_neat import eval_genomes
from config import Args
import pickle
import neat
import os


# load winner from Args.winner_path
neatConfig = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                Args.config_neat_filename)


winner_path = Args.winner_path

if winner_path == '':
    # get newest file in directory
    directory = Args.winner_prefix.split('/')[0]
    files = os.listdir(directory)
    files = [f for f in files if f.startswith(
        'winner-') and f.endswith('.pkl')]
    files.sort()
    winner_path = directory + '/' + files[-1]

print(winner_path)

with open(winner_path, 'rb') as f:
    winner = pickle.load(f)
    eval_genomes([(0, winner)], neatConfig, True)
    print('\nBest genome:')
    print(f"Key: {winner.key}")
    print(f"Fitness: {winner.fitness}")
