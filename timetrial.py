import time
import nltk

hpwords = open("chamber_secrets.txt").read().split()

t0 = time.clock()
nltk.pos_tag(hpwords)
tend = time.clock()
print tend - t0