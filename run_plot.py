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
with open(data_file, 'r') as f:
    for line in f:
        data.append(float(line))

# convert size
size_convert = 200

new_data = []
max_value = 0
for i in range(0, len(data)):
    max_value = max(max_value, data[i])
    if (i % size_convert == 0):
        new_data.append(max_value)
        max_value = 0
new_data.append(max_value)

x_values = [i * size_convert for i in range(len(new_data))]


plt.plot(x_values, new_data)
plt.xlabel('Generation')
plt.ylabel('Best Fitness')


plt.show()
