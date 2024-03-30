import random
result = []

for i in range(100):
    x = random.randint(0, 19)
    y = random.randint(0, 19)

    while i > 0 and result[i - 1] == (x, y):
        x = random.randint(0, 19)
        y = random.randint(0, 19)

    result.append((x, y))

print(result)
