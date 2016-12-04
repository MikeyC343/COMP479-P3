import shutil
from collections import OrderedDict
import ast
import os

def wipeblocks():
	for root, dirs, files in os.walk('./blocks'):
		for f in files:
			os.unlink(os.path.join(root, f))
		for d in dirs:
			shutil.rmtree(os.path.join(root, d))
			
def readIndexIntoMemory():
	index = OrderedDict()
	# Open Index File
	indexFile = open("./blocks/index.txt")
	for line in indexFile:
		if not line == '':
			split = line.split(':')
			term = split[0]
			postings = ast.literal_eval(split[1]) # convert a string list to a list
			index.update({term: postings})
			
	# Generate some stats about imported index
	postingsCount = 0
	print "Size of index: ", len(index)
	for i in index:
		postingsCount += len(index[i])
	print "Number of total postings: ", postingsCount
	
	return index