from collections import defaultdict
import cPickle
from random import randint
from random import choice

class Markov(object):
    """A class that analyzes the word occurance patterns of a given
    text file (the corpus) and can generate random text in the style
    of that corpus."""

    def __init__(self, corpus_file):
        self.corpus = open(corpus_file)
        self.text = self.corpus.read()
        self.words = self.text.split()

    def ngrams(self, n):
        """Make ngrams of every n consecutive
        words to feed the dictionary function, AS LIST."""
        for x in range(0, len(self.words)-n):
            yield [self.words[x+i] for i in range(n)]

    def make_word_dictionary(self, n):
        """For every ngram, takes first n-1 words as key, and last as value."""

        # TODO: make case/punct-insensitive?

        temp_dict = defaultdict(list)
        for wordlist in self.ngrams(n):
            final_word = wordlist.pop()
            temp_dict[tuple(wordlist)].append(final_word)

        return temp_dict

    def generate(self, length=100, n=3):
        """Make random text of given length (using ngrams of the given n)."""
        word_dict = self.make_ngram_dictionary(n)
        seed_no = randint(0,len(self.words)-n) # choose random seed
        output = [self.words[seed_no+x] for x in range(n-1)]
        for x in range(n-1, length):
            next_key = tuple(output[-(n-1):])
            output.append(choice(word_dict[next_key]))

        return " ".join(output)

class POS_Markov(object):
    """A class that analyzes both word occurance patterns and
    part-of-speech patterns of a given text file (the corpus) and can
    generate random text in the style of that corpus.

    This class expects a text file of a corpus POS-tagged by nltk--a list
    of ("word", "POS") tuples--serialized by cPickle."""

    def __init__(self, corpus_file):
        self.corpus_file = corpus_file
        self.tagged_words = self.open_serialized(corpus_file)
        self.word_dictionary = {}
        self.pos_dictionary = {}
        self.tag_dictionary = {}
        self.make_dicts()
        self.seed_pair = None

    def open_serialized(self, filename):
        """Unpickle a given file. Returns contents.
        Expected file contents: a list of ("word", "POS") tuples."""

        with open(filename, 'r') as infile:
            data = cPickle.load(infile)
        return data

    #TODO: this could totally be more efficient
    def triple_to_dict(self, triple, dict, ident):
        """Given a triple, adds it to the appropriate dictionary
        with the first two elements as the key, the third as the value.

        Assumes a ("word", "POS") tuple as input. Ident = 0 --> word,
        ident = 1 --> POS."""

        if ident == 0:
            if dict.get((triple[0], triple[1])):
                dict[triple[0], triple[1]].append(triple[2])
            else:
                dict[triple[0], triple[1]]=[triple[2]]
        elif ident == 1:
            if dict.get((triple[0][1], triple[1][1])):
                dict[triple[0][1], triple[1][1]].append(triple[2][1])
            else:
                dict[triple[0][1], triple[1][1]]=[triple[2][1]]
        else:
            return

    def make_dicts(self):
        """Populates three dictionaries, one of word occurance patterns,
        one of POS-occurance-patterns, and one of all of the words in the
        text indexed by POS.

        For the word and POS dictionaries, for every three words in the
        text, (w1, w2) --> w3"""

        # adds first two words of corpus to temp triple
        temp_triple = 0, self.tagged_words[0], self.tagged_words[1]

        for pair in self.tagged_words[2:]:
            # update triple
            temp_triple = temp_triple[1], temp_triple[2], pair

            # add to word dict
            self.triple_to_dict(temp_triple, self.word_dictionary, 0)

            # add to pos dict
            self.triple_to_dict(temp_triple, self.pos_dictionary, 1)

            # add to tag dict
            if self.tag_dictionary.get(pair[1]):
                self.tag_dictionary[pair[1]].append(pair)
            else:
                self.tag_dictionary[pair[1]] = [pair]

    def get_word_by_pos(self, wordlist, pos):
        """Returns a list of items in a given wordlist that are of the
        given part of speech."""

        return [item for item in wordlist if item[1] == pos]

    def random_pos(self, length=100):
        """Make random text (abstracted to parts-of-speech) of given
        length."""

        # pick a random key from word dictionary
        seed_no = randint(0,len(self.tagged_words)-3) # choose random seed
        self.seed_pair = [self.tagged_words[seed_no], self.tagged_words[seed_no + 1]]
        output = [self.seed_pair[0][1], self.seed_pair[1][1]]

        for x in range(2, length):
            output.append(choice(self.pos_dictionary[output[x-2], output[x-1]]))
        return output

    def generate(self, length=100):
        """Generates random text of given length. First generates abstracted
        text (POS only), then fills in with words.

        Given w1 and w2 and next part-of-speech POS[x], if there exists a
        word in the word dictionary that follows w1 and w2 and is
        part-of-speech POS[x], append that. Otherwise, append a random word
        of POS[x] (from the tag dictionary)."""

        # TODO: this is a silly order to do this in. Rather than a whole
        # paragraph's worth of POS's to fill in, should pick POS and words
        # nearly concurrently.

        pos_only = self.random_pos(length) # pick a better var name
        print pos_only

        result = [self.seed_pair[0], self.seed_pair[1]]
        print "Starting output:", result
        next = None

        for x in range(2, length):
            all_options = self.word_dictionary.get((result[x-2], result[x-1]))
            if all_options:
                pos_options = self.get_word_by_pos(all_options, pos_only[x])
                if len(pos_options) > 0:
                    result.append(choice(pos_options))
                    print x, "appended from wordlist"
                else: # if no words of appropriate POS follow w1 & w2, use random
                    result.append(choice(self.tag_dictionary[pos_only[x]]))
            else: # if no words follow w1 & w2, use random POS
                result.append(choice(self.tag_dictionary[pos_only[x]]))

        output = []
        for pair in result:
            output.append(pair[0])
        return " ".join(output)

# This is a test Markov gen
testgen = Markov("texts/plain/pride_prejudice.txt")

# TODO/notes
# weighting dict list manually??
# ab -> c, and also know that next key will start with b >> but is
# this even a necessary operation, given that getting a key from a dict
# is O(1)?
# is there info you're not using?
# garbage collection