import numpy as np
import pickle
from nltk.corpus import wordnet as wn
import sys
def main(filename):
	f = open(filename + '_eta.txt')
	g = f.read()
	f.close()
	g = g.strip()
	g = g.split("\n")

	for i in range(len(g)):
		g[i] = g[i].strip()
		g[i] = g[i].split(" ")

	probs_max = {}

	for j in range(len(g)):
		aux_id = []
		aux_prob = []
		for i in range(2,len(g[j])):
			aux_prob.append(g[j][i].split(":")[1])
			aux_id.append(g[j][i].split(":")[0])

		maxi = 0
		index = -1
		for i in range(len(aux_prob)):
			if aux_prob[i] > maxi:
				maxi = aux_prob[i]
				index = i
		probs_max[g[j][0]] = aux_id[index]
	print len(probs_max)


	f = open(filename + '_topics.txt')
	g = f.read()
	f.close()
	g = g.strip()
	g = g.split("\n")

	for i in range(len(g)):
		g[i] = g[i].strip()
		g[i] = g[i].split(" ")

	aux = []
	for i in range(len(g)):
		if g[i] != ['']:
			aux.append(g[i][0])

	g = aux 
	words = pickle.load(open(filename + "_vocab.p"))

	f = open(filename + '_topicswords.txt','w')
	n = 0
	for i in range(len(g)):
		if i % 11 == 0:
			f.write("\n")
			f.write("Topic " + str(n) + "\n")
			n += 1
		else:
			f.write(str(words.get(int(probs_max.get(g[i]))))+"#"+str(getSenseNumber(words.get(int(probs_max.get(g[i]))), g[i])) + "\n")
	f.close()

def getSenseNumber(lemma, ids):
	post = penn_to_wn(lemma.split("_")[1])
 	synsets = wn.synsets(lemma.split("_")[0], pos=post)
 	for i in range(len(synsets)):
 		if int(synsets[i].offset) == int(ids):
 			return (i+1)


def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']


def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return None

if __name__ == "__main__":
	main(sys.argv[1])

