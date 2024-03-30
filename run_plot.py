import matplotlib.pyplot as plt
from config import Args
import os

data_file = Args.data_of_winner_path

if data_file == '':
    # get newest file in directory
    directory = Args.data_prefix.split('/')[0]
    files = os.listdir(directory)
    files = [f for f in files if f.startswith(
        'winner-') and f.endswith('.txt')]
    files.sort()
    data_file = directory + '/' + files[-1]

print(data_file)


# load data from file
data = []
with open('output.txt', 'r') as f:
    for line in f:
        data.append(float(line))


plt.plot(data)
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.show()
