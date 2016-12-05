from __future__ import division
import re
from math import log
from collections import Counter
import glob
import os, os.path
import json


# reutersFunctions = reuters.ReutersCorpus(); #for testing
# documents = reutersFunctions.getDocuments(); #for testing



k = 1.5
b = 0.75

corpus = './project3/project3/corpus'
docCount = sum([len(files) for r, d, files in os.walk(corpus)])
#print docCount

#calculate tf-idf weights - dictionary = {key:[[doc, termfreq, tf-idf], tf-idf]}
def calculate():
    with open('./index/index.json', 'r') as theFile:
        dictionnary = json.load(theFile)
        for key, value in dictionnary.iteritems():
            postingsList = []
            tfidf = 0
            for v in value:
                postingsList.append(v[0])
                tfidf += v[1] * idf(postingsList, docCount)
            #value.append(tfidf)
            print "========"
            print key
            print tfidf
            

#return the bm25 score
#q = query term 
#p = postings list of querry term
#D = document id
#k,b = constants
#N = total documents in collection
#dl = document length in words
#avdl = average document length
def okapi_score(q, p, D, N):
    first = idf(p, N)
    second = termFreq(q, documents[D]) * (k+1)
    third = termFreq(q, documents[D]) + k * (1 - b + b * (float(format(dl(documents[D]), '.10f')) / float(avdl(documents[D], N))))
    return first * (second / third)


#return the frequency of term q in document D
def termFreq(q, D):
    doc = re.findall(r"[\w]+", D)
    count = 0
    for d in doc:
        if d.lower() == q:
            count += 1
    return count

#print (termFreq("simple", documents[1623])) #for testing should return 1

def idf(p, N):
    #p = length of postings list for querry term
    return log( (N - len(p) + 0.5) / (len(p) + 0.5) )

def dl(D):
    doc = D.split(' ')
    count = 0
    for d in doc:
        count += 1
    return count  

def avdl(D, t):
    return format((dl(D) / t), '.10f')

#print(documents[8500])
#print(dl(documents[8500])) #for testing
#print(termFreq("bush", documents[8500]))
