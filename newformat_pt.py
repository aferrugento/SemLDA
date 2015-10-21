import wordnet_pt as wn_pt 
import pickle
import sys
def main(filename):
	words = pickle.load(open(filename + "_vocab.p"))
	h = open(filename + "_freq.txt")
	g = h.read()
	h.close()
	g = g.strip()
	g = g.split("\n")

	p = open(filename + "_newformat.txt", 'w')
	#p.write(str(len(g))+"\n")
	synset_number = 0
	synset_dic =  {}
	synset_file = open(filename + "_synsetVoc.txt","w")
	imag_synset_number = -1
	imag_synset = {}
	to_write = []
	wn_pt.init()
	for i in range(len(g)):
		aux = ""
		print "DOC " + str(i)
		g[i] = g[i].strip()
		g[i] = g[i].split(" ")
		aux = g[i][0] + " "
		#p.write(g[i][0] + " ")
		for j in range(1, len(g[i])):
			#get the lemma from vocab for that word id
			word = words.get(int(g[i][j].split(":")[0]))
			#retrieve synset for that word
			#print word
			pos = word[len(word)-1]
			word = word[:len(word)-2]
			s = word.split("_")
			z = ""
			for x in range(len(s)):
				if x == len(s) - 1:
					z = s[x].encode('utf-8')
				else:
					z = s[x].encode('utf-8') + "_"
			word = z
			synsets = wn_pt.synsets(word, pos)
			#if that word has no synsets
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
			for k in synsets:
				if count == len(synsets) - 1:
					aux2 = 0
					if synset_dic.has_key(k):
						aux2 = synset_dic[k]
					else:
						synset_dic[k] = synset_number
						aux2 = synset_number
						synset_number += 1
					aux += str(aux2) + ":" + str(synsets.get(k)) + '] '
					#aux += str(aux2)+":"+ str(pc) + '] '
					#p.write(str(synset_number)+":"+ str(1) + '] ')
					#synset_file.write(str(synsets[k].offset) + "\n")
				else:
					aux2 = 0
					if synset_dic.has_key(k):
						aux2 = synset_dic[k]
					else:
						synset_dic[k] = synset_number
						aux2 = synset_number
						synset_number += 1
					aux += str(aux2) + ":" + str(synsets.get(k)) + ' '
					count += 1
					#aux += str(aux2)+":"+ str(pc) + ' '
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

def revert_dicio2(words_ids):
	new_dictio = {}
	for key in words_ids:
		new_dictio[words_ids[key]] = key

	return new_dictio

if __name__ == '__main__':
	main(sys.argv[1])
