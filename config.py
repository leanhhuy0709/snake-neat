class Args:
    # run_neat.py
    config_neat_filename = 'config_neat.txt'
    number_runs = 1000000
    generation_interval = 10000  # -1 if not used
    checkpoint_prefix = 'checkpoints/neat-checkpoint-'
    is_retrain = False
    retrain_checkpoint = 'checkpoints/neat-checkpoint-1'  # use if is_retrain is True
    winner_prefix = 'winners/winner-'
    data_prefix = 'data/winner-'
    show_training = False

    # Note: if '' is used, the path will be the newest file in the directory
    # run_winner.py
    winner_path = ''  # 'winners/winner-2.pkl'
    # run_plot.py
    data_of_winner_path = 'data/winner-2.txt'  # 'data/winner-2.txt'
