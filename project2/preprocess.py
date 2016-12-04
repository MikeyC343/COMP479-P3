import string
#import nltk
from collections import OrderedDict


#from nltk.tokenize import word_tokenize
import nltk_functions.word_tokenize
#from nltk.corpus import stopwords
#from nltk.stem.porter import PorterStemmer
from nltk_functions.stemmer import PorterStemmer
import sys

def preprocess(documents, memorysize):

	tokenizer = nltk_functions.word_tokenize.Word_Tokenize()
	
	terms = []
	termPostingsList = {}
	filenameincrementer = 0
	
	for index, documentId in enumerate(documents):
		#if documentId > 300: break; # for testing on small sample
		
		# Step 1: Tokenize
		tokens = tokenizer.word_tokenize(documents[documentId])		

		# Step 1B: Stem
		#tokens = [PorterStemmer().stem(i) for i in tokens] 

		# Step 2: Normalize
		normalized = tokens
		
		normalized = [i.lower() for i in normalized] # lowercase
		#print "normalizing 1..."
		#normalized = [i for i in normalized if not i in stopwords.words('english')] #remove stopwords (commented out because teacher instructed to keep stopwords)
		#print "normalizing 2..."
		normalized = [i for i in normalized if not any(c.isdigit() for c in i)] # remove numbers
		#print "normalizing 3..."
		normalized = [i for i in normalized if not i in string.punctuation] # remove punctuation
		#print "normalizing 4..."
		#normalized = [i for i in normalized if not any(c in string.punctuation for c in i)] # remove any term containing a punctuation mark
		normalized = [i for i in normalized if not i == '``' and not i == "''"] # remove blank words
		#print "normalizing 5..."
		# Step 3: Stemmer
		
		#print "normalizing ", documentId, " ... done"
		
		#terms = terms + [(i, documentId) for i in normalized]
		terms = normalized
		
		# Create postings list for each term 
		for term in terms:
			if term in termPostingsList:
				# term is already in and has posting list. Append to existing PL
				if documentId not in termPostingsList[term]:
					termPostingsList[term].append(documentId)
			else:
				termPostingsList[term] = [documentId]
		# Before saving to block file, sort.
		
		# Write every 100 documents (and last document) to files
		# if ((index + 1) % 100 == 0) or (len(documents) == index-1):
		# write to file when the list gets too big for memory
		if ((sys.getsizeof(termPostingsList) > memorysize) or 
			(index == len(documents)-1)): #or if we're up to the last document
			# sort termPostingsList
			sortedTerms = sorted(termPostingsList)
			termPostingsListSorted = OrderedDict()
			for item in sortedTerms:
				termPostingsListSorted[item] = termPostingsList[item]	
			termPostingsList = termPostingsListSorted
			termPostingsListSorted = {}
		
			# write to file every one hundred docs
			#file = open('blocks/block-' + str(index/100) + ".txt", 'a+')
			file = open('blocks/block-' + str(filenameincrementer) + ".txt", 'a+')
			filenameincrementer += 1
			for plIndex, term in enumerate(termPostingsList):
				#if plIndex > 20: break # TESTING			
				file.write(str(term) + ":" + str(termPostingsList[term]) + "\n")
				#file.write(str(term[0]) + "::" + str(term[1]) + "\n")
			file.close()
			terms = []
			termPostingsList = {}
