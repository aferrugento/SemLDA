import logging
from gensim import corpora, models, similarities
import string
import operator
import pickle
#from stemming.porter2 import stem
import sys
def contains_digits(word):
	digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

	for digit in digits:
		if digit in word:
			return True

	return False

def main(file_name):
	string = ''
	#string = '/home/adriana/Documents/novos_topicos/info_toda_22_2/'
	with open(string+file_name) as d:
		documents = d.readlines()

	#labels = [document[0] for document in documents]
  # divide texto em palavras, e so palavras com mais de duas palavras e que nao contem digitos
# lista de listas, cada celula e uma lista das palavra do texto 

	texts = [[word for word in document.split() if (len(word.split('_')[0])>2 and not contains_digits(word))] for document in documents]
	#texts = [[word for word in document.split() if (len(word)>2 and not contains_digits(word))] for document in documents]
	
	#nao posso remover numeros porque o ficheiro e maior parte so numeros
	#texts = [[word for word in document.split() if (len(word)>2)] for document in documents]
	

#remove palavras raras, que aparecem menos de duas vezes
	all_tokens = sum(texts, [])
	tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) <= 2)
	texts = [[word for word in text if word not in tokens_once] for text in texts]

#cria dicionario, deve atribuir ids as palavras
	dictionary = corpora.Dictionary(texts)
	dictionary.save('LDA.dict')
#ver api do gensim
	corpus = [dictionary.doc2bow(text) for text in texts]
	corpora.MmCorpus.serialize('LDA.mm', corpus)
	#print corpus

	tfidf = models.TfidfModel(corpus)

	#for i in range(len(corpus)):
	
	#	corpus = tfidf[corpus]

	"""f = open('labels.txt', 'w')

	for i in range(len(labels)):
		if len(corpus[i])> 0:
			f.write(labels[i]+'\n')

	f.close()
"""
	#remove words with low tfidf
	# new_texts = []
	# limite = 0.01
	# for i in range(len(corpus)):
	# 	aux = tfidf[corpus[i]]
	# 	aux_text = []
	# 	for j in range(len(corpus[i])):
	# 		#g.write(str(corpus[i][j][0])+str(':')+str(corpus[i][j][1])+ ' ')
	# 		if aux[j][1] > limite:
	# 			aux_text.append(dictionary.get(corpus[i][j][0]))

	# 	new_texts.append(aux_text)

	# dictionary = corpora.Dictionary(new_texts)
	# dictionary.save('LDA.dict')

	# corpus = [dictionary.doc2bow(text) for text in new_texts]
	# corpora.MmCorpus.serialize('LDA.mm', corpus)

   	#write files
	g = open(string+ file_name.split(".")[0]+'_freq.txt', 'w')
	h = open(string+ file_name.split(".")[0]+'_proc.txt', 'w')
	for i in range(len(texts)):
		for word in texts[i]:
			h.write(str(word) + ' ')
		h.write('\n')
	h.close()
	
	for i in range(len(corpus)):
		aux = tfidf[corpus[i]]
		g.write(str(len(corpus[i]))+ ' ')
		for j in range(len(corpus[i])):
			g.write(str(corpus[i][j][0])+str(':')+str(corpus[i][j][1])+ ' ')
			#if aux[j][1] > limite:
			#	g.write(str(corpus[i][j][0])+str(':')+str(corpus[i][j][1])+ ' ')
			#g.write(str(dictionary.get(corpus[i][j][0]))+str(':')+str(corpus[i][j][1])+str(':')+str(aux[j][1])+ ' ')

		g.write('\n')

	g.close()
	
	#print len(dictionary)
	dictionary = corpora.Dictionary(texts)
	pickle.dump(dictionary, open(string+ file_name.split(".")[0]+'_vocab.p', 'w'))
	#print dictionary.items()

	#corpus = [dictionary.doc2bow(text) for text in texts]

	#tfidf = models.TfidfModel(corpus)

	




def makeSet(cat):

	categories = cat.replace('[','').replace(']','').replace('u\'','').replace('\'','').split(';')

	allCat=set()

	for category in categories:
		cat = category.replace('u\'','').replace('\'','').replace('&amp','')

		if len(cat)>1 and cat[0]==' ':
			cat = cat[1:len(cat)]

		if len(cat)>1 and cat[len(cat)-1]==' ':
			cat = cat[0:len(cat)-1]

		if cat.lower() not in allCat and len(cat)>1:
			allCat.add(cat.lower())

	return allCat


def removePunctuation(s):
	for c in string.punctuation:
		s=s.replace(c," ")

	return s

if __name__ == '__main__':
	main(sys.argv[1])
