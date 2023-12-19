import sys
#from BitVector import *

#might need to change b if its a different type ppm is binary
def compare(File1,File2,File3):
    with open(File1, 'rb') as f1:
        d = set(f1.readlines())
    
    with open(File2, 'rb') as f2:
        e = set(f2.readlines())

    open(File3, 'wb').close()

    with open(File3, 'ab') as f3:
        for line in list(d-e):
            f3.write(line)


if __name__ == '__main__':
    if(len(sys.argv) != 4):
        sys.exit("Need 3 file inputs\n\n")
    File1 = sys.argv[1]
    File2 = sys.argv[2]
    File3 = sys.argv[3]

    compare(File1, File2, File3)

    print("Finished!\n")