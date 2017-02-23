import os

dir = '../../res/naturepack_extended/Models'
for filename in os.listdir(dir):
    if filename.endswith('.obj'):
        file = open(dir + '/' + filename)
        for line in file.readlines():
            if line.startswith('g'):
                print(filename, '-', line[2:-2])
