import time
import yaml

def tagged_words_from_yaml(filename):
        with open(filename, 'r') as infile:
            data = yaml.load(infile)
        return data

t0 = time.clock()
tagged_words_from_yaml("texts/pride_prejudice_tagged.yml")
tend = time.clock()
print tend - t0