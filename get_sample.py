import os  
import os.path  
import gzip  
import sys

def read_gz_file(path):  
    if os.path.exists(path):  
        with gzip.open(path, 'r') as pf:  
            for line in pf:  
                yield line  
    else:  
        print('the path [{}] is not exist!'.format(path))  

def sampling(filename):
    con = read_gz_file(filename)  
    counter = 200
    out = open(sys.argv[1]+'_sample.txt', 'w')
    if getattr(con, '__iter__', None):
        for line in con:
            counter -= 1
            out.write(line.decode() + "\n")
            if counter <= 0:
                out.close()
                break
	      
if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit(1)
    if sys.argv[1]:
        sampling(sys.argv[1])
        print("Done")
    else:
        print("Missing argv[1]!")
