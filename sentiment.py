import sys
import glob
sys.path.append('/Users/quentin/COMP479-P3/afinn/')
from afinn import Afinn
from nltk.corpus import gutenberg
try:
	import json
except ImportError:
	import simplejson as json



def calculateSentimentForEachDepartment():
	categories = ['biology', 'chemistry', 'exercise-science', 'geography-planning-environment', 'math-stats', 'physics','psychology','science-college', 'mystery']
	dictionary = dict()
	counter = dict()
	afinn = Afinn()
	for category in categories:
		dictionary[category] = 0
		counter[category] = 0
		for filename in glob.glob('project3/project3/corpus/' + category + '/*.json'):
			with open(filename, 'r') as theFile:
				docs = json.load(theFile)
				for key, value in docs.iteritems():
					for arr in value:
						for sentences in arr:
							clean = sentences.replace('\n', ' ').replace('\n\r', ' ').replace('\r', ' ')
							clean = clean.strip()
							if clean == '':
								continue
							else:
								counter[category] += 1
								dictionary[category] += afinn.score(clean)

	dictionary = sorted(dictionary.items(), key=lambda x:x[1])
	for key, value in dictionary:
		print str(key) + " with afinn score: " + str(value)
		print str(key) + " with average afinn score: " + str(value/counter[key])



# afinn = Afinn()

# print afinn.score('support')