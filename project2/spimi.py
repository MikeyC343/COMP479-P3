from os import listdir
from collections import OrderedDict
import ast
import re

def spimi():
	# Open all the block files
	blockFiles = [open('blocks/'+i) for i in listdir('blocks/')]
	#create final block file
	indexFile = open('blocks/index.txt', 'a+')
	# Initialize Holder
	firstLines = OrderedDict() # blockId:{term:[postings]}
	
	# Populate firstLines
	for blockFile in blockFiles:
		blockFileId = getBlockFileId(blockFile)
		term = {}
		line = blockFile.readline()
		if not line == '':
			split = line.split(':')
			term = split[0]
			postings = ast.literal_eval(split[1])
			firstLines[blockFileId] = {term : postings}
	#print min([firstLines[i] for i in firstLines])
	
	blocksEmpty = False #set to true when nothing is left in blocks
	while not blocksEmpty:
		# Find the minimum in firstLine
		lowestWordBlockIdTuple = min([[firstLines[i], i] for i in firstLines]) # get lowest term alphabetically, format [{term: [postings list]}, blockId]
		# look if any other firstLine items are same... 
		currentTerm = lowestWordBlockIdTuple[0].keys()[0]
		blocksWithThisTerm = [blockId for blockId in firstLines if currentTerm in [termKey for termKey in firstLines[blockId]]] # returns the blockIds of the blocks that have the same term at the top of their file
		# combine into single line (sum collapses all the PLs in the list of PL lists)
		combinedPostings = sorted(sum([pl[currentTerm] for pl in (firstLines[i] for i in blocksWithThisTerm)], []))
		#combinedPostings = sorted(sum([pl for pl in (firstLines[i] for i in blocksWithThisTerm)], []))
		# write to main index
		indexFile.write(str(currentTerm) + ":" + str(combinedPostings) + "\n")
		# replace the lines read in
		for blockFileId in blocksWithThisTerm:
			blockFile = getBlockFileById(blockFileId, blockFiles)
			if blockFile: # if blockFile was found
				term = {}
				line = blockFile.readline()
				if not line == '':
					split = line.split(':')
					term = split[0]
					postings = ast.literal_eval(split[1])
					firstLines[blockFileId] = {term:postings}
				#else, remove blockFile from blockFiles list
				else:
					del firstLines[blockFileId]
					blockFiles.remove(getBlockFileById(blockFileId, blockFiles))
			else:
				print "remove"
				blockFiles.remove(getBlockFileById(blockFileId, blockFiles))
		if not blockFiles: #if blockFiles is completely empty
			blocksEmpty = True
	return 0
		
def getBlockFileId(blockFile):
	fileName = blockFile.name
	idMatch = re.search('block-(\d*)', fileName)
	if id: # if block-# found and not some other accidental file
		return int(idMatch.group(1))

def getBlockFileById(usedBlockId, blockFiles):
	matchingFiles = [file for file in blockFiles if re.search('block-'+str(usedBlockId), file.name)] # should be only one that matches
	if matchingFiles: # if not empty
		return matchingFiles[0]
	else:
		return False

		
class NoSuchBlockFileException(Exception):
	pass