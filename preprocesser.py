import sys
import glob
import nltk
import re
try:
	import json
except ImportError:
	import simplejson as json
from collections import OrderedDict
reload(sys)
sys.setdefaultencoding('utf-8')


def preProcess(memorysize):
	dictionary = dict()
	
	postingsList = {}
	
	finalDictionnary = dict()

	indexNumber = 00
	categories = ['biology', 'chemistry', 'exercise-science', 'geography-planning-environment', 'math-stats', 'mystery', 'physics', 'psychology', 'science-college']
	for category in categories:
		for filename in glob.glob('project3/project3/corpus/' + category + '/*.json'):
			with open(filename,'r') as theFile:
				intermediate = json.load(theFile)
				for key, value in intermediate.iteritems():
					dictionary[key] = value

<<<<<<< HEAD
	for key, value in dictionary.iteritems():
		if key in finalDictionnary:
			continue
		else:
			finalDictionnary[key] = value
=======
	finalDictionnary = dict()
>>>>>>> d678f813a7d84f965262091d276c74c99d75bf05

	categories = ['biology', 'chemistry', 'exercise-science', 'geography-planning-environment', 'math-stats', 'physics','psychology','science-college', 'mystery']
	for category in categories:
		for filename in glob.glob('project3/project3/corpus/' + category + '/*.json'):
			with open(filename,'r') as theFile:
				intermediate = json.load(theFile)
				for key, value in intermediate.iteritems():
					dictionary[key] = value

<<<<<<< HEAD
=======
	for key, value in dictionary.iteritems():
		if key in finalDictionnary:
			continue
		else:
			finalDictionnary[key] = value

	nonWordsRegex = re.compile('[^a-zA-Z0-9]+')

>>>>>>> d678f813a7d84f965262091d276c74c99d75bf05
	for key, value in finalDictionnary.iteritems():
		for values in value:
			for sentences in values:
				clean = sentences.strip()

				tokens = []

				allWords = nltk.word_tokenize(clean)

				for words in allWords:
					if nonWordsRegex.match(words):
						continue
					else:
						tokens.append(words)

				for term in tokens:
					# term = unicode(term, errors="ignore")

					if term in postingsList:
						#getting the double array of postings List
						split = postingsList[str(term)]

						#initialize index to none for check later
						index = None
						#looping over all arrays in double array split and searching for key (index of doc)
						for i in range(len(split)):
							if key in split[i]:
								index = i

						#if a key already exist => get the number of occurences as of now, add 1 to it and then put this number back into the array
						if index is not None:
							splitAtIndex = split[index]
							occurencesOfTermInADoc = splitAtIndex[1] + 1
							postingsList[str(term)][index] = [key,occurencesOfTermInADoc]
						#otherwise just add the key and the occurence 1
						else:
							postingsList[str(term)].append([key,1])
					else:
						#if term not in postings list, initiate an empty array of document ids
						postingsList[str(term)] = [[key,1]]
				if ((sys.getsizeof(postingsList)) > memorysize):

					sortedPostings = sorted(postingsList)
					sortedPostingsListTerms = OrderedDict()
					#sorting process for postingsList
					for item in sortedPostings:
						sortedPostingsListTerms[item] = postingsList[item]
					postingsList = sortedPostingsListTerms
					sortedPostingsListTerms = {}

					if indexNumber < 100:
						formatedIndexNumber = '%03d' % indexNumber
					else:
						formatedIndexNumber = str(indexNumber)

					with open('index/blocks-' + formatedIndexNumber + '.json', 'w') as theFile:
						indexNumber += 1
						json.dump(postingsList, theFile)
					postingsList = {}