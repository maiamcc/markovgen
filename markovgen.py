from random import randint
from random import choice
import cPickle

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
        self.corpus_file = corpus_file
        self.tagged_words = self.open_serialized(corpus_file)
        self.word_dictionary = {}
        self.pos_dictionary = {}
        self.make_dicts()
        self.seed_pair = None

    def open_serialized(self, filename):
        with open(filename, 'r') as infile:
            data = cPickle.load(infile)
        return data

    def triple_to_dict(self, triple, dict, ident):
        """Assumes a word/pos pair as input. Ident = 0 --> word, ident = 1 --> pos."""

        if dict.get((triple[0][ident], triple[1][ident])):
            dict[triple[0][ident], triple[1][ident]].append(triple[2][ident])
        else:
            dict[triple[0][ident], triple[1][ident]]=[triple[2][ident]]

    def make_dicts(self):
        """Populates two dictionaries, one of words, one of parts of speech.
        For every three words in the text, (w1, w2) --> w3"""

        # adds first two words of corpus to temp triple
        temp_triple = 0, self.tagged_words[0], self.tagged_words[1]

        for pair in self.tagged_words[2:]:
            temp_triple = temp_triple[1], temp_triple[2], pair
            #Word(pair[0], pair[1])

            # word dict
            self.triple_to_dict(temp_triple, self.word_dictionary, 0)

            # pos dict
            self.triple_to_dict(temp_triple, self.pos_dictionary, 1)

    def get_word_by_pos(self, wordlist, pos):
        return [item[0] for item in wordlist if item[1] == pos]

    def random_pos(self, length=100):
        """Make random text (in parts-of-speech) out given length for number of words."""

        # pick a random key from word dictionary
        seed_no = randint(0,len(self.tagged_words)-3) # choose random seed
        self.seed_pair = [self.tagged_words[seed_no], self.tagged_words[seed_no + 1]]
        output = [self.seed_pair[0][1], self.seed_pair[1][1]]

        for x in range(2, length):
            output.append(choice(self.pos_dictionary[output[x-2], output[x-1]]))
        return output

    def generate(self, length=100):
        pos_only = self.random_pos(length) #crappy var name
        print pos_only

        output = [self.seed_pair[0][0], self.seed_pair[1][0]]
        print "Starting output:", output

        for x in range(2, length):
            print "Index:", x
            options = self.word_dictionary[output[x-2], output[x-1]]
            print "POS needed:", pos_only[x]
            output.append(choice(options))
                #self.get_word_by_pos(options, pos_only[x])))
            print "Output so far:", output
            print "----------"

        return " ".join(output)

# test = POS_Markov("multifox_cPickle.txt")
pp = POS_Markov("texts/pride_prejudice_cPickle.txt")

# weighting dict list manually??
# ab -> c, and also know that next key will start with b
# is there info you're not using?
# garbage collection