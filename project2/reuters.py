import re
# Provides operations on Reuters corpus
class ReutersCorpus:
	
	FILENAMES = ["reut2-000.sgm", "reut2-001.sgm", "reut2-002.sgm", "reut2-003.sgm", "reut2-004.sgm", "reut2-005.sgm", 
	"reut2-006.sgm", "reut2-007.sgm", "reut2-008.sgm", "reut2-009.sgm", "reut2-010.sgm", "reut2-011.sgm", "reut2-012.sgm",
	"reut2-013.sgm", "reut2-014.sgm", "reut2-015.sgm", "reut2-016.sgm", "reut2-017.sgm", "reut2-018.sgm", "reut2-019.sgm",
	"reut2-020.sgm", "reut2-021.sgm"]
	#FILENAMES = ["reut2-000.sgm"]

	REUTERS_START_TAG = "<REUTERS"
	BODY_START_TAG = "<BODY>"
	BODY_END_TAG = "</BODY>"
	
	def getDocuments(self):
		documents = {}
		body = ""
		for filename in self.FILENAMES:			
			file = open("reuters_corpus/" + filename);	
			count = 0
			body = ""
			
			bodyIsOpen = False
			currentReutersId = -1
			
			#Iterate through the lines in this document
			for line in file:
				count += 1
				#if count > 200: break #just for quick testing
				
				if bodyIsOpen:
					# Look for BODY CLOSE
					bodyEnd = line.find(self.BODY_END_TAG)
					if bodyEnd != -1: # close tag found
						body += line[:bodyEnd]
						documents[currentReutersId] = body
						#documents.append(body)
						body = ""
						bodyIsOpen = False
						currentReutersId = -1
					else:
						body += line	
						
						
				else:
					# Look for REUTERS OPEN
					reutersStart = line.find(self.REUTERS_START_TAG)
					if reutersStart != -1:
						# Get NEWID attribute
						currentReutersId = int(re.search("NEWID=\"(\d*)", line).group(1))
					# Look for BODY OPEN
					bodyStart = line.find(self.BODY_START_TAG)
					if bodyStart != -1:
						bodyIsOpen = True;	
						# start recording into body
						#special case: check if body ends on this string too
						firstline = line[bodyStart+len(self.BODY_START_TAG):]
						bodyEnd = firstline.find(self.BODY_END_TAG)
						if bodyEnd != -1:
							body = firstline[:bodyEnd]
							bodyIsOpen = False;
							body = ""	
						else:
							body += firstline

		return documents
