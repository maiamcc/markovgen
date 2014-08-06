from random import randint
from random import choice
import cPickle

'''
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
'''

class Word(object):
    def __init__(self, the_word, pos):
        self.the_word = the_word
        self.pos = pos
    def __repr__(self):
        return "%s (%s)" % (self.the_word, self.pos)
    def __str__(self):
        return self.the_word

class POS_Markov(object):
    def __init__(self, corpus_file):
        self.corpus_file = corpus_file
        self.tagged_words = self.open_serialized(corpus_file)
        self.word_dictionary = {}
        self.pos_dictionary = {}
        self.tag_dictionary = {}
        self.make_all_dicts()

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

    def make_all_dicts(self):
        # add first two to tag dict.
        temp_triple = 0, Word(self.tagged_words[0][0], self.tagged_words[0][1]), \
            Word(self.tagged_words[1][0], self.tagged_words[1][1])

        for pair in self.tagged_words[:-2]: # dont' do all of them, tho!
            temp_triple = temp_triple[1], temp_triple[2], Word(pair[0], pair[1])

            # word dict
            if self.word_dictionary.get((temp_triple[0], temp_triple[1])):
                self.word_dictionary[temp_triple[0], temp_triple[1]].append(temp_triple[2])
            else:
                self.word_dictionary[temp_triple[0], temp_triple[1]]=[temp_triple[2]]


            # self.triple_to_dict(temp_triple, self.word_dictionary, 0)

            # pos dict

            if self.pos_dictionary.get((temp_triple[0].pos, temp_triple[1].pos)):
                self.pos_dictionary[temp_triple[0].pos, temp_triple[1].pos].append(temp_triple[2].pos)
            else:
                self.pos_dictionary[temp_triple[0].pos, temp_triple[1].pos]=[temp_triple[2].pos]
            # self.triple_to_dict(temp_triple, self.pos_dictionary, 1)

    '''
            # add to tag dict
            if self.tag_dictionary.get(pair[1]):
                self.tag_dictionary[pair[1]].append(pair[0])
            else:
                self.tag_dictionary[pair[1]] = [pair[0]]
    '''
    '''
    def make_tag_dictionary(self):
        """Make a dictionary indexing every word in the corpus by part of speech."""

        tagged_words = self.tagged_words()

        temp_dict = {}
        for tagged_word, tag in tagged_words:
            if temp_dict.get(tag):
                temp_dict[tag].append(tagged_word)
            else:
                temp_dict[tag] = [tagged_word]

        return temp_dict
    '''

    def get_word_by_pos(self, wordlist, pos):
        return [word for word in wordlist if word.pos == pos]

    def random_pos(self, length=100):
        """Make random text (in parts-of-speech) out given length for number of words."""

        # pick a random key from pos dictionary
        # seed_pair = choice(self.pos_dictionary.keys())
        # output = [seed_pair[0], seed_pair[1]]
        # TEMPORARILY FREEZING THE SEED

        output = ['NNP', 'NNP']

        for x in range(2, length):
            output.append(choice(self.pos_dictionary[output[x-2], output[x-1]]))

        return output

    def generate(self, length=100):
        # TEMPORARILY FREEZING THE SEED
        output = [Word('It', 'PRP'), Word('is', 'VBZ')]

        pos_only = self.random_pos(length) #crappy var name
        for x in range(2, length):
            options = self.word_dictionary[output[x-2], output[x-1]]
            output.append(get_word_by_pos(options, pos_only[x]))

        return " ".join(output)

hp = POS_Markov("texts/pride_prejudice_cPickle.txt")

# weighting dict list manually??
# ab -> c, and also know that next key will start with b
# is there info you're not using?
# garbage collection