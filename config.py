class Args:
    config_neat_filename = 'config_neat.txt'
    number_runs = 10

    is_retrain = False
    retrain_checkpoint = 'checkpoints/neat-checkpoint-'  # use if is_retrain is True

    generation_interval = 1000
    checkpoint_prefix = 'checkpoints/neat-checkpoint-'
    winner_prefix = 'winners/winner-'
    data_prefix = 'data/winner-'

    # Note: if '' is used, the path will be the newest file in the directory
    winner_path = ''  # 'winners/winner-2.pkl'
    data_of_winner_path = ''  # 'data/winner-2.txt'
