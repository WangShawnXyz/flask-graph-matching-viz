import shutil as su
import os
import time
CWD = os.getcwd()
EXE_PATH = './file'
CMD = "dir"# > 'tested.txt'"

def copy_exec(src, target, command):
    su.copy(src, target)
    res = os.popen(command)
    print(res.readlines())

def is_matching_done(path):
    init_size = os.path.getsize(path)
    while os.path.getsize(path) == init_size:
        time.sleep(5)
    return True
if __name__ == '__main__':
    # copy_exec("1.txt", EXE_PATH+'copy_exec.txt', CMD)
    is_matching_done("1.txt")
    