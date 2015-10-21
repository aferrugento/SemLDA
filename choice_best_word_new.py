import numpy as np
import pickle
from nltk.corpus import wordnet as wn
import sys
def main(filename):
	string = ''
	f = open(filename + '_synsetVoc.txt')
	g = f.read()
	f.close()
	g = g.strip()
	g = g.split("\n")

	senseIdToSynset = {s.offset:s for s in wn.all_synsets()}

	# for i in range(len(g)):
	# 	g[i] = g[i].strip()
	# 	g[i] = g[i].split(" ")

	# probs_max = {}

	# for j in range(len(g)):
	# 	aux_id = []
	# 	aux_prob = []
	# 	for i in range(2,len(g[j])):
	# 		aux_prob.append(g[j][i].split(":")[1])
	# 		aux_id.append(g[j][i].split(":")[0])

	# 	maxi = 0
	# 	index = -1
	# 	for i in range(len(aux_prob)):
	# 		if aux_prob[i] > maxi:
	# 			maxi = aux_prob[i]
	# 			index = i
	# 	probs_max[g[j][0]] = aux_id[index]
	# print len(probs_max)


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
	print g
	words = pickle.load(open(filename + "_vocab.p"))
	words_new = revert_dicio(words)
	f = open(filename + '_topicswords.txt','w')
	n = 0
	for i in range(len(g)):
		if i % 11 == 0:
			f.write("\n")
			f.write("Topic " + str(n) + "\n")
			n += 1
		else:
			if int(g[i]) < 0:
				f.write(g[i] + "\n")
				continue
			else:
				aux = 0
				#print senseIdToSynset[int(g[i])].lemmas
				max_lemma = maxCount(senseIdToSynset[int(g[i])], aux)
				aux += 1
				pos = lemma_pos(str(max_lemma))
				#print max_lemma.name.lower() + '_' + pos
				a = words_new.get(str(max_lemma.name.lower()) + '_' + str(pos))
				#print senseIdToSynset[int(g[i])]
				while a == None:
					max_lemma = maxCount(senseIdToSynset[int(g[i])], aux)
					aux += 1
					pos = lemma_pos(str(max_lemma))
					a = words_new.get(str(max_lemma.name.lower()) + '_' + str(pos))
					#print max_lemma.name + '_' + pos, words_new.get(max_lemma.name + '_' + pos)
				#print 'FICHEIRO ' + str(words_new.get(max_lemma.name.lower() + '_' + pos))
				f.write(max_lemma.name.lower() + '_' + pos + "\n")
	f.close()

def revert_dicio(words_ids):
	new_dictio = {}
	for key in words_ids:
		new_dictio[words_ids[key]] = key

	return new_dictio

def lemma_pos(lemma):
	if '.n.' in lemma:
		return 'NN'
	elif '.v.' in lemma:
		return 'VB'
	elif '.a.' or '.s.' in lemma:
		return 'JJ'
	elif '.r.' in lemma:
		return 'RB'

def getKey(item):
	return item[1]
def maxCount(synsets, pos):
	max_i = 0
	max_lemma = 0
	lista = []
	for i in range(len(synsets.lemmas)):
		aux = [synsets.lemmas[i], synsets.lemmas[i].count()]
		lista.append(aux)

	sorted(lista, key=getKey)
	#print lista
	return lista[pos][0]

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

