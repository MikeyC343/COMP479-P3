import os
import fileops
import reuters
from bm25 import okapi_score
from collections import defaultdict

class SPIMIQuery:
	
	def __init__(self):
		self.index = fileops.readIndexIntoMemory()

	def runQuery(self, queryInput):
		# Parse queryInput
		terms = self.parseQuery(queryInput)

		#for calculating the score
		reutersFunctions = reuters.ReutersCorpus();
		documents = reutersFunctions.getDocuments();
		
		print "Your Terms Are:"
		for term in terms:
			print term, "  ",
		print "" #blank line to skip to next line

		# Collect Postings Lists
		listOfPostingsList = [[]]
		for term in terms:
			if term in self.index:
				listOfPostingsList.append(self.index[term])

		del listOfPostingsList[0] # delete the blank array initializer so as not to mess up intersection calc
		# find intersections
		if listOfPostingsList: # not empty
			results = list(set.intersection(*map(set, listOfPostingsList)))
		else: 
			results = []
		
		print "----------------------------------------------------"
		print "Document Results: ", sorted(results)
		print "----------------------------------------------------"
		print "Calculating Okapi/BM25 Scores"
		scores = defaultdict(list)
		for term in terms:
			for docId in results:
				scores[docId].append(okapi_score(term, self.index[term], docId, len(documents)))
		
		finalScores = {}
		for key in scores.keys():
			finalScores[key] = sum(scores[key])
		print "DocId		Score"
		print "----------------------------------------------------"
		for i in sorted(finalScores, key=finalScores.get, reverse=True):
			print str(i) + "		" + str(finalScores[i])
		
		print "----------------------------------------------------"


		
		
		#print [i for i in self.index[term] for term in terms]
		
	# Currently, words must be separated by single AND to be parse correctly
	def parseQuery(self, queryInput):
		lower = queryInput.lower()
		return lower.split(' ')