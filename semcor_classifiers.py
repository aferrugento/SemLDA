import pickle
from sklearn import datasets
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from nltk.corpus import wordnet as wn 
import sys
#cria-se um dummy synset sempre que uma palavra nao esta no semcor


def main():
	probs = pickle.load(open("/home/adriana/Dropbox/mine/Tese/preprocessing/data_output/classifier/words_synsets.p"))
	probs_l = pickle.load(open("/home/adriana/Dropbox/mine/Tese/preprocessing/data_output/classifier/lemmas_synsets.p"))
	words = pickle.load(open("/home/adriana/Dropbox/mine/Tese/preprocessing/data_output/classifier/semcor_onix_wordnetlemma_vocab.p"))
	f = open("/home/adriana/Dropbox/mine/Tese/preprocessing/data_output/classifier/lda_semcor/final.gamma")
	m = f.read()
	f.close()

	h = open("/home/adriana/Dropbox/mine/Tese/preprocessing/data_output/classifier/semcor_onix_wordnetlemma_freq.txt")
	g = h.read()
	h.close()
	#resultados do lda
	data = {}
	#palavras do corpus
	labels = {}
	classifiers = {}

	m = m.strip()
	m = m.split("\n")
	docs = []
	
	for i in range(len(m)):
		m[i] = m[i].strip()
		m[i] = m[i].split(" ")
		aux = []
		for j in range(len(m[i])):
			aux.append(float(m[i][j]))
		docs.append(aux)

	g = g.strip()
	g = g.split("\n")
	#inver_probs = revert_dicio(probs)

	for i in range(len(g)):
		g[i] = g[i].strip()
		g[i] = g[i].split(" ")
		for j in range(1,len(g[i])):
			word = words[int(g[i][j].split(":")[0])]
			#if word == 'else' or word == 'ups' or word == 'pas' or word == 'michael' or word == 'francis' or word == 'morgan' or word == 'wallace' or word == 'refresh' or word == 'samuel' or word == 'christopher' or word == 'rhode' or word == 'warwick' or word == 'multi' or word == 'edwin' or word == 'cherry' or word == 'stuart' or word == 'stag' or word == 'marcus' or word == 'francisco' or word == 'salyer' or word == 'perplex' or word == 'pel' or word == 'juan' or word == 'edward' or word == 'richard' or word == 'i.e' or word == 'gene' or word == 'crosby' or word == 'sutherland' or word == 'garry' :
			#	continue
			try:
				synsets = probs[word]
			except Exception, e:
				try:
					synsets = probs_l[word]
				except Exception, e:
					continue

			for synset in synsets:
				if data.has_key(synset):
					aux1 = data[synset]
					aux2 = labels[synset]

					aux1.append(docs[i])
					aux2.append(int(g[i][j].split(":")[0]))

					data[synset] = aux1
					labels[synset] = aux2

				else:
					data[synset] = [docs[i]]
					labels[synset] = [int(g[i][j].split(":")[0])]
	for synset in data:
		model = LogisticRegression()
		try:
			model.fit(data[synset], labels[synset])
		except ValueError:
			continue
		classifiers[synset] = model
	print len(classifiers), len(data)
	pickle.dump(classifiers, open("/home/adriana/Dropbox/mine/Tese/preprocessing/data_output/classifier/synset_classifiers.p", "w"))

def check_probs(word):

	probs = pickle.load(open('prob_dictio_pos2.p'))

	not_here = 0
	for i in probs.keys():
		for k in probs.get(i).keys():
			if k == word:
				not_here = 1
				break
		if not_here == 1:
			break

	return not_here

def classify_data(filename):
	probs = pickle.load(open('prob_dictio_pos2.p'))
	classifiers = pickle.load(open("synset_classifiers.p"))
	words = pickle.load(open(filename + "_vocab.p"))
	f = open("infer-gamma.dat")
	m = f.read()
	f.close()
	
	h = open(filename + "_freq.txt")
	g = h.read()
	h.close()
	g = g.strip()
	g = g.split("\n")

	m = m.strip()
	m = m.split("\n")
	docs = []
	for i in range(len(m)):
		m[i] = m[i].strip()
		m[i] = m[i].split(" ")
		aux = []
		for j in range(len(m[i])):
			aux.append(float(m[i][j]))
		docs.append(aux)
	aux_probs = revert_dicio(probs)
	p = open(filename + "_newformat.txt", 'w')
	#p.write(str(len(g))+"\n")
	synset_number = 0
	synset_dic =  {}
	synset_file = open(filename + "_synsetVoc.txt","w")
	imag_synset_number = -1
	imag_synset = {}
	to_write = []
	for i in range(len(g)):
		aux = ""
		print "DOC " + str(i)
		g[i] = g[i].strip()
		g[i] = g[i].split(" ")
		aux = g[i][0] + " "
		#p.write(g[i][0] + " ")
		for j in range(1, len(g[i])):
			word = words.get(int(g[i][j].split(":")[0]))
			#synsets = wn.synsets(word.split("_")[0], penn_to_wn(word.split("_")[1]))
			#not_here = check_probs(word)
			synsets = aux_probs.get(word)
			if synsets == None:
				aux += g[i][j] + ":1[" + str(synset_number) + ":" + str(1)+ "] "
				#p.write(g[i][j] + ":1[" + str(synset_number) + ":" + str(1)+ "] ")
				imag_synset[imag_synset_number] = word
				synset_dic[imag_synset_number] = synset_number
				#synset_file.write(str(imag_synset_number) + "\n")
				synset_number += 1
				imag_synset_number = imag_synset_number - 1
				continue
			
			aux += g[i][j] +':'+ str(len(synsets)) + '['
			#p.write(g[i][j] +':'+ str(len(synsets)) + '[')
			count = 0
			for k in synsets.keys():
				if classifiers.has_key(int(k)):
					probas = classifiers[int(k)].predict_proba(docs[i])
					classes = classifiers[int(k)].classes_
					ids = -1
					for c in range(len(classes)):
						if int(classes[c]) == int(g[i][j].split(":")[0]):
							ids = c
							break
					#print probas
					if ids == -1 and count == len(synsets) - 1:
						aux2 = 0
						if synset_dic.has_key(int(k)):
							aux2 = synset_dic[int(k)]
						else:
							synset_dic[int(k)] = synset_number
							aux2 = synset_number
							synset_number += 1

						aux += str(aux2)+":"+ str(1) + '] '
						count += 1
						#p.write(str(synset_number)+":"+ str(1) + '] ')
						
						#synset_file.write(str(int(k)) + "\n")
					elif ids == -1 and count != len(synsets) - 1:
						aux2 = 0
						if synset_dic.has_key(int(k)):
							aux2 = synset_dic[int(k)]
						else:
							synset_dic[int(k)] = synset_number
							aux2 = synset_number
							synset_number += 1
						aux += str(aux2)+":"+ str(1) + ' '
						count += 1
						#p.write(str(synset_number)+":"+ str(1) + ' ')
						#synset_file.write(str(int(k)) + "\n")
					elif ids != -1 and count == len(synsets) - 1:
						aux2 = 0
						if synset_dic.has_key(int(k)):
							aux2 = synset_dic[int(k)]
						else:
							synset_dic[int(k)] = synset_number
							aux2 = synset_number
							synset_number += 1
						aux += str(aux2)+":"+ str(probas[0][c]) + '] '
						count += 1
						#p.write(str(synset_number)+":"+ str(probas[c]) + '] ')
						#synset_file.write(str(int(k)) + "\n")
					elif ids != -1 and count != len(synsets) - 1:
						aux2 = 0
						if synset_dic.has_key(int(k)):
							aux2 = synset_dic[int(k)]
						else:
							synset_dic[int(k)] = synset_number
							aux2 = synset_number
							synset_number += 1
						aux += str(aux2)+":"+ str(probas[0][c]) + ' '
						count += 1
						#p.write(str(synset_number)+":"+ str(probas[0][c]) + ' ')
						#synset_file.write(str(int(k)) + "\n")
				else:
					if count == len(synsets) - 1:
						aux2 = 0
						if synset_dic.has_key(int(k)):
							aux2 = synset_dic[int(k)]
						else:
							synset_dic[int(k)] = synset_number
							aux2 = synset_number
							synset_number += 1
						aux += str(aux2)+":"+ str(1) + '] '
						count += 1
						#aux += str(aux2)+":"+ str(1/len(synsets))) + '] '
						#p.write(str(synset_number)+":"+ str(1) + '] ')
						#synset_file.write(str(int(k)) + "\n")
					else:
						aux2 = 0
						if synset_dic.has_key(int(k)):
							aux2 = synset_dic[int(k)]
						else:
							synset_dic[int(k)] = synset_number
							aux2 = synset_number
							synset_number += 1
						aux += str(aux2)+":"+ str(1) + ' '
						count += 1
						#aux += str(aux2)+":"+ str(1/len(synsets))) + ' '
						#p.write(str(synset_number)+":"+ str(1) + ' ')
						#synset_file.write(str(synsets[k].offset) + "\n")
		#p.write("\n")
		to_write.append(aux)
	

	ne = revert_dicio2(synset_dic)
	for i in range(len(ne)):
		synset_file.write(str(ne.get(i))+'\n')
	synset_file.close()

	p.write(str(len(ne))+"\n")
	for i in range(len(to_write)):
		p.write(to_write[i] + "\n")
	p.close()
	pickle.dump(imag_synset, open(filename + "_imag.txt", "w"))
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

def revert_dicio2(words_ids):
	new_dictio = {}
	for key in words_ids:
		new_dictio[words_ids[key]] = key

	return new_dictio

def revert_dicio(words_ids):
	new_dictio = {}
	for key in words_ids:
		for words in words_ids[key]:
			if new_dictio.has_key(words):
				aux = new_dictio[words]
				aux[key] = words_ids[key][words]
				new_dictio[words] = aux
			else:
				aux = {}
				aux[key] = words_ids[key][words]
				new_dictio[words] = aux

	return new_dictio

if __name__ == "__main__":
	#main()
	classify_data(sys.argv[1])
