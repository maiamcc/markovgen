import time
import yaml
import cPickle

def open_serialized(filename):
        with open(filename, 'r') as infile:
            data = cPickle.load(infile)
        return data

print "Opening pride_prejudice_cPickle.txt"
t0 = time.clock()
open_serialized("texts/pride_prejudice_cPickle.txt")
tend = time.clock()
print tend - t0