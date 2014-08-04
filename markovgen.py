class Markov(object):
	def __init__(self, corpus_file):
		self.corpus = open(corpus_file)
		self.text = self.corpus.read()
		self.words = self.text.split()