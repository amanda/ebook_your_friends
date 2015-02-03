from nltk import word_tokenize
from collections import defaultdict, Counter
from sys import argv
import random, operator, bisect, string

def default_tokenize(text):
	# hacky, maybe fix
	return [w for w in word_tokenize(text) \
		if w not in string.punctuation \
		and w != "''" and w != "``"]


def twitter_tokenize(text):
	prefixes = set(['@', '#'])
	garbage = set(["''", "``", "http"])
	tokens = word_tokenize(text)
	result = []
	for tok in tokens:
		if result and result[-1] in prefixes:
			result[-1] = '{}{}'.format(result[-1], tok)
		elif (tok in string.punctuation or tok in garbage) and tok not in prefixes:
			pass
		else:
			result.append(tok)
	return result

class MarkovGenerator(object):
	'''version of a markov text generator for
	making bots from people's twitter timelines'''
	def __init__(self, text, length, ngram=2, tokenize_fun=default_tokenize):
		self.text = text
		self.length = length
		self.ngram = ngram
		self.tokenize_fun = tokenize_fun
		self.markov_dict = self.make_markov_dict()
		self.generated_text = self.generate_words()

	def make_markov_dict(self):
		'''populates a dict of word: ngram
		based on source text'''
		text = self.text
		ngram = self.ngram
		words = self.tokenize_fun(text)
		zippy_words = zip(*[words[i:] for i in xrange(ngram)])
		markov_dict = defaultdict(Counter)
		for t in zippy_words:
			a, b = t[:-1], t[-1]
			markov_dict[a][b] += 1
		return markov_dict

	def choose_word(self, start_key):
		'''chooses a next word based on cumulative distribution
		likelihood that it follows the start_key'''
		def accumulate(iterable, func=operator.add):
			it = iter(iterable)
			total = next(it)
			yield total
			for el in it:
				total = func(total, el)
				yield total
		choices, weights = zip(*self.markov_dict[start_key].iteritems())
		cumulative_distribution = list(accumulate(weights))
		rando = random.random() * cumulative_distribution[-1]
		return choices[bisect.bisect(cumulative_distribution, rando)]

	def generate_words(self):
		'''generates the new text'''
		def tup_to_words(tuple_list):
			'''(list of tuples) -> string
			helper function'''
			word_list = [x[0] for x in tuple_list[1:-1]] + list(tuple_list[-1])
			words = ''
			for i in word_list:
				if i not in string.punctuation:
					words += i + ' '
				else:
					words = words.strip() + i + ' '
			return words.strip()
		start_tup = random.choice(self.markov_dict.keys()) # let me tell you about my startup
		words_length = 0
		words_tuples = [start_tup]
		while words_length < self.length:
			next_word = self.choose_word(words_tuples[-1])
			next_tup = words_tuples[-1][1:] + (next_word,)
			words_length += len(next_word) + 1
			words_tuples.append(next_tup)
		words_tuples.append(('.',))
		self.generated_text = tup_to_words(words_tuples)
		return self.generated_text
