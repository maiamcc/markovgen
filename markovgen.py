from random import randint
from random import choice
import yaml

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
class POS_Markov(object):
    def __init__(self, corpus_file):
        self.corpus_file = corpus_file
        self.tagged_words = self.tagged_words_from_yaml()
        self.word_dictionary = {}
        self.pos_dictionary = {}
        self.tag_dictionary = {}
        self.make_all_dicts()

# if call only once then leave as funct.--otherwise, store in the object

    def tagged_words_from_yaml(self):
        with open(self.corpus_file, 'r') as infile:
            data = yaml.load(infile)
        return data

    def triple_to_dict(self, triple, dict, ident):
        """Assumes a word/pos pair as input. Ident = 0 --> word, ident = 1 --> pos."""

        if dict.get((triple[0][ident], triple[1][ident])):
            dict[triple[0][ident], triple[1][ident]].append(triple[2][ident])
        else:
            dict[triple[0][ident], triple[1][ident]]=[triple[2][ident]]

    def make_all_dicts(self):
        # add first two to tag dict.
        temp_triple = 0, self.tagged_words[0], self.tagged_words[1]

        for pair in self.tagged_words[:-2]: # dont' do all of them, tho!
            temp_triple = temp_triple[1], temp_triple[2], pair

            # word dict
            self.triple_to_dict(temp_triple, self.word_dictionary, 0)

            # pos dict
            self.triple_to_dict(temp_triple, self.pos_dictionary, 1)

            # add to tag dict
            if self.tag_dictionary.get(pair[1]):
                self.tag_dictionary[pair[1]].append(pair[0])
            else:
                self.tag_dictionary[pair[1]] = [pair[0]]

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

    def random_pos(self, length=100):
        """Make random text (in parts-of-speech) out given length for number of words."""

        # pick a random key from pos dictionary
        seed_pair = choice(self.pos_dictionary.keys())
        output = [seed_pair[0], seed_pair[1]]

        for x in range(2, length):
            output.append(choice(self.pos_dictionary[output[x-2], output[x-1]]))

        return output

    def generate(self, length=100):
        output = []

        pos_only = self.random_pos(length)
        for item in pos_only:
            output.append(choice(self.tag_dictionary[item]))

        return " ".join(output)

hp = POS_Markov("texts/short_corpus_tagged.yml")

# print "Classes loaded."
# pp = POS_Markov("pride_prejudice.txt")

# weighting dict list manually??
# timing functions/loadtime (end-start)
# ab -> c, and also know that next key will start with b
# is there info you're not using?
# garbage collection