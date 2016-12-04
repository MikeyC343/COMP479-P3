# Project Modules
import sys
import reuters
from preprocess import preprocess
from spimi import spimi
import fileops
import query as q

def generateindex(memorysize):

	reutersFunctions = reuters.ReutersCorpus();

	# Step 0:
	fileops.wipeblocks()
	
	# Step 1: Get Documents
	print "Fetching Documents..."
	documents = reutersFunctions.getDocuments();
	print "   --> Total number of documents", len(documents)
	#documents = testDocuments
	#print documents
	
	# Step 2: Tokenize/Normalize/Remove Stopwords + Save Blocks
	print "Tokenizing and saving blocks..."
	preprocess(documents, memorysize)
	
	# Step 3: SPIMI 
	print "Performing SPIMI..."
	spimi()
	
	print "\nComplete."
	print "--------------------------------------------\n\n"

def query():
	query = q.SPIMIQuery()
	while True: # keep running the program 
		queryInput = raw_input("Please enter your query, using AND / OR for boolean queries  ")
		print "You entered " + queryInput
		result = query.runQuery(queryInput)
	

if __name__ == '__main__':
	#generateindex(int(sys.argv[1])) #comment if blocks are already created
	query()