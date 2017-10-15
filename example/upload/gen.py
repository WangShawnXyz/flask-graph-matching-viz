import random

for x in range(1,10):
    f = open(str(x) + ".txt", "w")
    string = ""
    for x in range(1,10):
        string += str(random.randint(-100, 100))
    f.write(string)
    f.close()

