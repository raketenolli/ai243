import json
from math import log

# Feldgroesse
fs = 5
# Multiplikator fuer Zahlen und Vielfache
mp = 3

fh = open("spielstaende_"+str(fs)+"_"+str(mp)+".dat", "r")
spielstaende = json.load(fh)
fh.close()

spielstaende_NN = []

for s in spielstaende:
	for z in s:
		spielstand_NN = (fs**2 * 8 + 4 + 1 + 1)*[0]
		field = z[0]
		dir = z[1]
		score_nach_zug = z[2]
		score_nach_spiel = z[3]
		for r in xrange(fs):
			for c in xrange(fs):
				if field[r][c] == 0:
					spielstand_NN[(fs*r+c)*8+0] = 1
				else:
					node = int(round(log(field[r][c])/log(mp)))
					spielstand_NN[(fs*r+c)*8+1+node] = 1
		spielstand_NN[fs**2 * 8 + dir] = 1
		spielstand_NN[fs**2 * 8 + 4] = score_nach_zug
		spielstand_NN[fs**2 * 8 + 4 + 1] = score_nach_spiel

		spielstaende_NN.append(spielstand_NN)

fh = open("spielstaende_NN_"+str(fs)+"_"+str(mp)+".dat", "w")
json.dump(spielstaende_NN, fh)
fh.close()
