from random import randint
from random import choice
import nltk

class Markov(object):
    def __init__(self, corpus_file):
        self.corpus = open(corpus_file)
        self.text = self.corpus.read()
        self.words = self.text.split()
        self.dictionary = self.make_dictionary()

    def triples(self):
        """Prepare to make word triplets to feed the dictionary function."""
        for x in range(0, len(self.words)-3):
            yield self.words[x], self.words[x+1], self.words[x+2]

    def make_dictionary(self):
        """Take every two words as key and third one as value."""

        temp_dict = {}
        for w1, w2, w3 in self.triples():
            if temp_dict.get((w1, w2)):
                temp_dict[w1, w2].append(w3)
            else:
                temp_dict[w1, w2]=[w3]

        return temp_dict

    def generate(self, length=100):
        """Make random text out given length for number of words."""

        seed_no = randint(0,len(self.words)-3) # choose random seed
        output = [self.words[seed_no], self.words[seed_no + 1]]
        for x in range(2, length):
            output.append(choice(self.dictionary[output[x-2], output[x-1]]))

        return " ".join(output)

class POS_Markov(object):
    def __init__(self, corpus_file):
        self.corpus = open(corpus_file)
        self.text = self.corpus.read()
        self.words = self.text.split()
        self.dictionary = self.make_dictionary(self.words)
        self.tagged_words = nltk.pos_tag(self.words)
        self.pos_words = map(self.tag_from_tuple, self.tagged_words)
        self.pos_dictionary = self.make_dictionary(self.pos_words)
        self.tag_dictionary = self.make_tag_dictionary()

        # pos text == text that's entirely parts of speech tags
    def tag_from_tuple(self, tuple):
        return tuple[1]

    def triples(self, my_list):
        """Prepare to make word triplets to feed the dictionary function."""
        for x in range(0, len(my_list)-3):
            yield my_list[x], my_list[x+1], my_list[x+2]

    def make_dictionary(self, my_list):
        """Take every two words as key and third one as value."""

        temp_dict = {}
        for w1, w2, w3 in self.triples(my_list):
            if temp_dict.get((w1, w2)):
                temp_dict[w1, w2].append(w3)
            else:
                temp_dict[w1, w2]=[w3]

        return temp_dict

    def make_tag_dictionary(self):
        """Make a dictionary indexing every word in the corpus by part of speech."""

        temp_dict = {}
        for tagged_word, tag in self.tagged_words:
            if temp_dict.get(tag):
                temp_dict[tag].append(tagged_word)
            else:
                temp_dict[tag] = [tagged_word]

        return temp_dict

    def pos_generate(self, length=100):
        """Make random text out given length for number of words."""

        seed_no = randint(0,len(self.pos_words)-3) # choose random seed
        output = [self.pos_words[seed_no], self.pos_words[seed_no + 1]]
        for x in range(2, length):
            output.append(choice(self.pos_dictionary[output[x-2], output[x-1]]))

        return output

    def populate_pos_random(self, length=100):
        output = []
        pos_only = pos_generate(length)
        print "POS only:", pos_only

        for item in pos_only

hp = POS_Markov("short_corpus.txt")


