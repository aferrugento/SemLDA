import pickle
import sys
def main(file_name):
	dict_ambi = pickle.load(open('dict_ambi_ap_aa.p'))

	string = ''
	f = open(string + file_name + '_eta.txt')
	g = f.read()
	f.close()

	g = g.split("\n")
	for i in range(len(g)):
		g[i] = g[i].split(" ")

	h = open(string +  file_name + '_freq.txt')
	m = h.read()
	h.close()

	m = m.split("\n")

	for i in range(len(m)):
		m[i] = m[i].split(" ")

	new_g = revert_dicio(g)
	dic_g = create_dicio(g)
	
	#agr_probs = agregate_probabilities(m)

	g = [var for var in g if var != ['']]
	print g[len(g)-1]
	j = open(string +  file_name + '_newformat.txt', 'w')
	j.write(str(len(g))+"\n")
	for i in range(len(m)):
		j.write(m[i][0] + ' ')
		for k in range(1, len(m[i])-1):
			#print m[i][k]
			#print new_g.get(int(m[i][k].split(':')[0]))

			#if dict_ambi.has_key(m[i][k].split(":")[0]):
			#	synset = dic_g.get(dict_ambi.get(m[i][k].split(":")[0]).split("_")[0])
			#	for l in range(len(synset)):
			#		if synset[l].split(":")[0] == dict_ambi.get(m[i][k].split(":")[0]).split("_")[1]:
			#			#updating the original word, must change to other
			#			j.write(m[i][k] + ":1[" + synset[l] +"] ")
						
			#else:
			j.write(m[i][k] +':'+ str(len(new_g.get(m[i][k].split(':')[0]))) + '[')
			for n in range(len(new_g.get(m[i][k].split(':')[0]))):
				if n == len(new_g.get(m[i][k].split(':')[0])) - 1:
					j.write(new_g.get(m[i][k].split(':')[0])[n] + '] ')
				else:
					j.write(new_g.get(m[i][k].split(':')[0])[n] + ' ')

		j.write('\n')

	j.close()
	#pickle.dump(new_g, open('cenas.p','w'))

def agregate_probabilities(m):
	dictio = {}

	words_id = pickle.load(open('words_ids_ap_pos.p'))

	for i in range(len(m)):
		for j in range(1, len(m[i])):
			word = words_id.get(m[i][j].split(":")[0])
			if word.split("_")[1] == 'VB':
				post = penn_to_wn(word.split("_")[1])
				word_p = word.split("_")[0]

				synsets = wn.synsets(word_p, pos=post)

				for n in range(len(synsets)):
					print synsets[n].lemmas
					lemmas = []
					for m in range(len(synsets[n].lemmas)):
						if synsets[n].lemmas[m].name == word_p:
							print synsets[n].lemmas[m].count()
							if synsets[n].lemmas[m].count() != 0:
								lemmas.append(synsets[n].lemmas[m])


def create_dicio(eta):
	dictio = {}

	for i in range(len(eta)-1):
		for j in range(2, len(eta[i])):
			if dictio.has_key(eta[i][0]):
				aux = dictio.get(eta[i][0])
				aux.append(eta[i][j])
				dictio[eta[i][0]] = aux
			else:
				aux = []
				aux.append(eta[i][j])
				dictio[eta[i][0]] = aux
	return dictio

def revert_dicio(eta):
	dictio = {}

	for i in range(len(eta)-1):
		for j in range(2, 2+int(eta[i][1])):
			if dictio.has_key(eta[i][j].split(":")[0]):
				aux = dictio.get(eta[i][j].split(":")[0])
				aux.append(str(i) + ":" + eta[i][j].split(":")[1])
				dictio[eta[i][j].split(":")[0]] = aux
			else:
				aux = []
				aux.append(str(i) + ":" + eta[i][j].split(":")[1])
				dictio[eta[i][j].split(":")[0]] = aux
	return dictio


if __name__ == "__main__":
	main(sys.argv[1])
