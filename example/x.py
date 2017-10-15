import time
import hashlib


src = time.time()

md5 = hashlib.md5(str(src).encode('utf-8')).hexdigest()

print(src)
print(md5)

cookie = ""

def get_cookie(func):
    def wrapper(*args, **kargs):
        global cookie
        if not cookie:
            cookie = 123
        return func(*args, **kargs)
    return wrapper

@get_cookie
def index():
    return "index.html"

def gen_md5(path):
    content = open(path, "r", encoding="utf-8").read().encode("utf-8")
    md5 = hashlib.md5(content).hexdigest()
    return md5

if __name__ == '__main__':
    # print(index())
    # print(cookie)
    print(gen_md5('app.py'))