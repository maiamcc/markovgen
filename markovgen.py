class Markov(object):
	def __init__(self, corpus_file):
		self.corpus = open(corpus_file)
		self.text = self.corpus.read()
		self.words = self.text.split()
		self.dictionary = self.make_dictionary()

	def triples():
		"""Prepare to make word triplets to feed the dictionary function."""
		#for x in range(0, 40):
            #print words[x], words[x+1], words[x+2]

        #for x in range(0, len(words), -3):
			#yield words[x], words[x+1], words[x+2]


	def make_dictionary(self):
		"""Take every two words as key and third one as value."""

	def generate(length=100):
		"""Make random text out given length for number of words."""

pp = Markov("test_data/pride_and_prejudice.txt")

