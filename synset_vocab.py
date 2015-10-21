import sys
filename = sys.argv[1]
f = open(filename+"_eta.txt")
g = f.read()
f.close()
g = g.split("\n")

h = open(filename + '_synsetvocab.txt','w')

for i in range(len(g)):
	g[i] = g[i].split(" ")
	h.write(str(g[i][0])+"\n")

h.close()
