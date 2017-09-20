import random

def gen_random_string(num = 10):
    s = ""
    if num < 1:
        num = 10
    for x in range(1,num):
        s += str(random.randint(-100, 100))
    return s

def gen_txt(num):
    for x in range(1,num):
        with open(str(x)+".txt", "w") as f:
            f.write(gen_random_string())

if __name__ == '__main__':
    gen_txt(20)