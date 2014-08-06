from sys import argv
import cPickle
import nltk

script, source = argv

with open(source, "r") as infile:
    source_text = infile.read()

print "Text loaded. First 100 charcters:", source_text[:100]

word_list = source_text.split()

print "Word list created. First 20 words:", word_list[:20]

tagged_words = nltk.pos_tag(word_list)

print "Word list tagged. First 20 words:", tagged_words[:20]

output_file = source[:-4] + "_cPickle.txt"

with open(output_file, 'w') as outfile:
    cPickle.dump(tagged_words, outfile)

print "File written. Program over."