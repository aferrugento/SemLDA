import collections as c
import pickle
from nltk.corpus import wordnet as wn
import nltk
import random
import sys
extra = -1
extra_dict = {}
another_extra = {}
dict_ambi = {}
string = ''

def contains_digits(word):
	digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

	for digit in digits:
		if digit in word:
			return True

	return False

def create_eta_with_extra(file_name, probs, rever_words_ids):
	global string
	h = open(string + file_name +'_eta.txt','w')
	extra_dict = pickle.load(open(file_name + '_extra.p'))

	#add imaginary synsets to the ones from semcor
	for key in extra_dict.keys():
		probs[key] = extra_dict.get(key)

	print "probs " + str(len(probs))

	#get all synsets and for each retrieve the respective lemmas 
	for id_synset in probs.keys():
		lemmas = probs.get(id_synset)
		count = 0
		size = 0
		string = ""
		#for each lemma of a certain synset get its id given by gensim
		for lemma in lemmas.keys():
			word_id = rever_words_ids.get(lemma)
			#if that lemma doesnt exist in the text then it wont be added
			if word_id != None:
				size += 1
				if count == len(lemmas) - 1:
					string += str(word_id) + ":" + str(lemmas.get(lemma))
				else:
					string += str(word_id) + ":" + str(lemmas.get(lemma)) + " "
			count += 1
		if size != 0:
			doc = str(id_synset) + " " + str(size) + " " + string 
			h.write(doc + "\n")
	h.close()

def create_extra(file_name, g, probs, rever):
	global extra_dict, dict_ambi
	for j in range(len(g)):
		g[j] = g[j].split(" ")
		print "Doc " + str(j)
		doc = ""
		cnt = c.Counter()
		for word in g[j]:
			cnt[word] += 1

		for i in range(len(cnt.items())):
			if cnt.items()[i][0] == '':
				continue
			synset = synsets(cnt.items()[i][0], probs, rever)

	pickle.dump(extra_dict, open(file_name +'_extra.p','w'))
	pickle.dump(dict_ambi, open('dict_ambi_ap_aa.p','w'))

def count_average(probs):
	total = 0
	som = 0.0
	for synset in probs.keys():
		for lemma in probs.get(synset).keys():
			som += probs.get(synset).get(lemma)
			total += 1
	print som, total
	print som/total

def main(file_name):
	global extra_dict, string
	f = open(string + file_name + '_proc.txt')
	g = f.read()
	f.close()
	g = g.split("\n")

	
	words_ids = pickle.load(open(string + file_name +'_vocab.p'))
	probs = pickle.load(open('prob_dictio_pos2.p'))
	
	#average = count_average(probs)

	rever_words_ids = revert_dicio(words_ids)
	#print probs
	#always first
	create_extra(file_name,g, probs, rever_words_ids)
	#always second
	create_eta_with_extra(file_name,probs, rever_words_ids)



		# doc += str(len(cnt)) + " "

		# for i in range(len(cnt.items())):
		# 	synset = synsets(cnt.items()[i][0], probs)

		# 	synset_str = ""
		# 	count = 0
		# 	for key in synset.keys():
		# 		aux_id = 0

		# 		if dictio.has_key(key):
		# 			aux_id =  dictio.get(key)
		# 		else:
		# 			dictio[key] = ids
		# 			aux_id = ids
		# 			ids += 1
		# 		if count == len(synset) - 1:	
		# 			synset_str += str(aux_id) +":"+str(synset.get(key))
		# 		else:
		# 			synset_str += str(aux_id) +":"+str(synset.get(key))+","
		# 		count += 1

		# 	if i == len(cnt.items()) - 1:
		# 		doc += "<"+synset_str+">" + ":" + str(cnt.items()[i][1])
		# 	else:
		# 		doc += "<"+synset_str+">" + ":" + str(cnt.items()[i][1]) + " "
		# h.write(doc + "\n")
		#	doc += "\n"
		#print doc
	
	

def revert_dicio(words_ids):
	new_dictio = {}
	for key in words_ids:
		new_dictio[words_ids[key]] = key

	return new_dictio

def synsets(word, probs, rever):
	global extra
	global extra_dict, dict_ambi, another_extra

	synset = {}
	not_here = 0
	for i in probs.keys():
		for k in probs.get(i).keys():
			if k == word:
				not_here = 1
				break
		if not_here == 1:
			break
	# qd palavra n existe na lista de synsets atribuir lhe uma prob
	
	# not_unique = 0
	# post = penn_to_wn(word.split("_")[1])
	# word_p = word.split("_")[0]

	# synsets = wn.synsets(word_p, pos=post)

	# if len(synsets) == 1:
	# 	max_l = 0
	# 	lemma_x = synsets[0].lemmas[0]
	# 	for lemma in synsets[0].lemmas:
	# 		if lemma.count() > max_l:
	# 			max_l = lemma.count()
	# 			lemma_x = lemma
	# 	#print word, lemma_x
	# 	not_unique = 1
	# 	aux = rever.get(lemma_x.name+"_"+str(word.split("_")[1]))
	# 	if aux == None:
	# 		aux = rever.get(word)
		
	# 	if probs.has_key(str(synsets[0].offset)):
	# 		dict_ambi[rever.get(word)] = str(synsets[0].offset) + "_" + str(aux)
	# 	elif another_extra.has_key(str(synsets[0].offset)):
			
	# 	else:
	# 		aux = {}
	# 		aux[]
	# 		another_extra[str(synsets[0].offset)] = aux


		#print str(lemma) +" " + str(lemma.count())

	if not_here == 0:
		flag = 0
		for key in extra_dict.keys():
			for key2 in extra_dict.get(key).keys():
				if key2 == word:
					flag = 1
					break
			if flag == 1:
				break
		if flag == 0:
			aux = {}
			aux[word] = 1
			#aux[word] = random.uniform(0,1)
			#aux[word] = 0.77686148679
			extra_dict[extra] = aux
			extra -= 1 

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
