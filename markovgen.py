from collections import defaultdict
import cPickle
from random import choice
from random import randint
from random import shuffle



class Markov(object):
    """A class that analyzes the word occurance patterns of a given
    text file (the corpus) and can generate random text in the style
    of that corpus."""

    def __init__(self, corpus_file):
        self.corpus = open(corpus_file)
        self.text = self.corpus.read()
        self.words = self.text.split()

    def make_ngrams(self, n, inputlist):
        """Make ngrams of every n consecutive
        words to feed the dictionary function, AS LIST."""
        for x in range(0, len(inputlist)-n):
            yield [inputlist[x+i] for i in range(n)]

    def make_dictionary(self, n, inputlist=None):
        """For every ngram, takes first n-1 words as key, and last as value."""

        # TODO: make case/punct-insensitive?
        if inputlist is None:
            inputlist = self.words

        temp_dict = defaultdict(list)
        for wordlist in self.make_ngrams(n, inputlist):
            final_word = wordlist.pop()
            temp_dict[tuple(wordlist)].append(final_word)

        return temp_dict

    def generate(self, length=100, n=3):
        """Make random text of given length (using ngrams of the given n)."""
        word_dict = self.make_dictionary(n)
        seed_no = randint(0,len(self.words)-n) # choose random seed
        output = [self.words[seed_no+x] for x in range(n-1)]
        for x in range(n-1, length):
            next_key = tuple(output[-(n-1):])
            output.append(choice(word_dict[next_key]))

        return " ".join(output)

class POS_Markov(Markov):
    """A class that analyzes both word occurance patterns and
    part-of-speech patterns of a given text file (the corpus) and can
    generate random text in the style of that corpus.

    This class expects a text file of a corpus POS-tagged by nltk--a list
    of ("word", "POS") tuples--serialized by cPickle."""

    def __init__(self, corpus_file, word_n=3, pos_n=3):
        # maybe make a tagged_word named tuple?
        self.corpus_file = corpus_file
        self.tagged_words = self.open_serialized(corpus_file)
        self.words = [t[0] for t in self.tagged_words]
        self.pos = [t[1] for t in self.tagged_words]
        self.word_dictionary = self.make_dictionary(word_n, self.tagged_words)
        self.pos_dictionary = self.make_dictionary(pos_n, self.pos)
        self.pos_n = pos_n
        self.word_n = word_n

    def open_serialized(self, filename):
        """Unpickle a given file. Returns contents.
        Expected file contents: a list of ("word", "POS") tuples."""

        with open(filename, 'r') as infile:
            data = cPickle.load(infile)
        return data

    def get_word_by_pos(self, wordlist, pos):
        """Returns a list of items in a given wordlist that are of the
        given part of speech."""

        return [item for item in wordlist if item[1] == pos]

    def generate(self, length=100):
        """Generates random text of given length. First selects next POS;
        if there exists a matching next word of that POS, selects it; and if not,
        selects a different next POS.

        Unsure whether this works any better than non-POS generation. At a guess,
        will work best where pos_n > word_n."""

        seed_no = randint(0,len(self.tagged_words)-self.pos_n) # choose random seed
        output = [self.tagged_words[seed_no+x] for x in range(self.pos_n-1)]
        for x in range(self.pos_n-1, length):
            next_pos_key = tuple([t[1] for t in output[-(self.pos_n-1):]])
            next_pos_choices = self.pos_dictionary[next_pos_key]
            next_word_key = tuple(output[-(self.word_n-1):])
            next_picked = False
            while not next_picked:
                shuffle(next_pos_choices)
                next_pos = next_pos_choices.pop()
                choices = self.get_word_by_pos(self.word_dictionary[next_word_key], next_pos)
                if choices:
                    output.append(choice(choices))
                    next_picked = True
                else:
                    pass

        return " ".join([t[0] for t in output])

# This is a test Markov gen
m = POS_Markov("texts/tagged/pride_prejudice_tagged")

# TODO/notes
# weighting dict list manually??
# ab -> c, and also know that next key will start with b >> but is
# this even a necessary operation, given that getting a key from a dict is O(1)?
# is there info you're not using?
# garbage collection