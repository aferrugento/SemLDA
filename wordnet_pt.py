file1 = "fuzzy_synsets_pt/fuzzy_synsets_pt_N.txt"
file2 = "fuzzy_synsets_pt/fuzzy_synsets_pt_V.txt"
file3 = "fuzzy_synsets_pt/fuzzy_synsets_pt_ADJ.txt"
file4 = "fuzzy_synsets_pt/fuzzy_synsets_pt_ADV.txt"

synsets_N = {}
words_N = {}
synsets_V = {}
words_V = {}
synsets_J = {}
words_J = {}
synsets_R = {}
words_R = {}
a = 1
syn_number = 0

def init():
	global synsets_N, words_N, synsets_V, words_V, synsets_J, words_J, synsets_R, words_R
	synsets_N = create_dict(file1)
	synsets_V = create_dict(file2)
	synsets_J = create_dict(file3)
	synsets_R = create_dict(file4)
	words_N = revert_dicio(synsets_N)
	words_V = revert_dicio(synsets_V)
	words_J = revert_dicio(synsets_J)
	words_R = revert_dicio(synsets_R)

def create_dict(file1):
	global syn_number
	dict_aux = {}
	f = open(file1)
	g = f.read()
	f.close()

	g = g.strip()
	g = g.split("\n")

	for i in range(len(g)):
		g[i] = g[i].strip()
		g[i] = g[i].split(";")
		aux = {}
		for j in range(len(g[i])):
			if g[i][j] == "":
				continue
			aux[g[i][j].split("(")[0]] = g[i][j].split("(")[1].split(")")[0]
		dict_aux[syn_number] = aux
		syn_number += 1
	return dict_aux

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

def get_synset(synset_id):
	global synsets_N, words_N, synsets_V, words_V, synsets_J, words_J, synsets_R, words_R
	if synsets_N.get(synset_id) != None:
		return (synsets_N[synset_id],'N')
	elif synsets_V.get(synset_id) != None:
		return (synsets_V[synset_id], 'V')
	elif synsets_J.get(synset_id) != None:
		return (synsets_J[synset_id], 'A')
	elif synsets_R.get(synset_id) != None:
		return (synsets_R[synset_id], 'R')

def synsets(lemma, pos):
	global synsets_N, words_N, synsets_V, words_V, synsets_J, words_J, synsets_R, words_R
	if pos == 'N':
		return words_N.get(lemma)
	elif pos == 'V':
		return words_V.get(lemma)
	elif pos == 'A':
		return words_J.get(lemma)
	elif pos == 'R':
		return words_R.get(lemma)
	else:
		return None