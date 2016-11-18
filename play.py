# =======================================================================
# SEHR WICHTIG
# SPIELRICHTUNGEN SIND SO DEFINIERT
#
#		OBEN
#		 0
# LINKS			RECHTS
#  2			  3
#		UNTEN
#		 1
#		
# SO DASS BEI GERADEN BEWEGUNGEN DIE ARRAYS ZUM COLLAPSEN IN AUFSTEIGEN-
# DER REIHENFOLGE DURCHLAUFEN WERDEN, BEI UNGERADEN IN ABSTEIGENDER REI-
# HENFOLGE.
# =======================================================================


import json
import copy
import re
import random

def prnfield(prnfield__field, prnfield__score):
	for r in prnfield__field:
		for c in r:
			print "%4d" % (c),
		print
	print "Score:", prnfield__score, "\n"

def place(place__field, place__nn):
	nempty = 0
	empties = []
	for ir, r in enumerate(place__field):
		for ic, c in enumerate(r):
			if c == 0:
				empties.append([ir, ic])
				nempty = nempty + 1
	if nempty == 0: return field
	p = int(random.random()*nempty)
	v = place__nn[int(random.random()*len(place__nn))]
	place__field[empties[p][0]][empties[p][1]] = v
	return place__field

def move(move__field, move__dir):
	h = len(move__field)
	hasmoved = False

	if move__dir == 0:
		for c in range(h):
			for r in range(h):
				i = 1
				while move__field[r][c] == 0 and (r+i)<h:
					if move__field[r+i][c]>0:
						move__field[r][c] = move__field[r+i][c]
						move__field[r+i][c] = 0
						hasmoved = True
					i = i + 1

	elif move__dir == 1:
		for c in range(h):
			for r in range(h):
				i = 1
				while move__field[h-r-1][c] == 0 and (h-r-1-i)>=0:
					if move__field[h-r-1-i][c]>0:
						move__field[h-r-1][c] = move__field[h-r-1-i][c]
						move__field[h-r-1-i][c] = 0
						hasmoved = True
					i = i + 1

	elif move__dir == 2:
		for r in range(h):
			for c in range(h):
				i = 1
				while move__field[r][c] == 0 and (c+i)<h:
					if move__field[r][c+i]>0:
						move__field[r][c] = move__field[r][c+i]
						move__field[r][c+i] = 0
						hasmoved = True
					i = i + 1
	
	elif move__dir == 3:
		for r in range(h):
			for c in range(h):
				i = 1
				while move__field[r][h-c-1] == 0 and (h-c-1-i)>=0:
					if move__field[r][h-c-1-i]>0:
						move__field[r][h-c-1] = move__field[r][h-c-1-i]
						move__field[r][h-c-1-i] = 0
						hasmoved = True
					i = i + 1

	return move__field, hasmoved

def collapse(collapse__field, collapse__dir, collapse__n, collapse__score):
	h = len(collapse__field)
	hascollapsed = False
	
	if collapse__dir == 0:
		for c in range(h):
			for r in range(h):
				if collapse__field[r][c] == 0: continue
				i = 1
				while (r+i)<h and (i<collapse__n):
					if collapse__field[r+i][c] == collapse__field[r][c]:
						i = i + 1
					else: break
				if i == collapse__n:
					collapse__field[r][c] = collapse__n * collapse__field[r][c]
					collapse__score = collapse__score + collapse__field[r][c]
					for j in range(collapse__n-1):
						collapse__field[r+j+1][c]=0
					hascollapsed = True
	
	elif collapse__dir == 1:
		for c in range(h):
			for r in range(h):
				if collapse__field[h-r-1][c] == 0: continue
				i = 1
				while (h-r-1-i)<h and (i<collapse__n):
					if collapse__field[h-r-1-i][c] == collapse__field[h-r-1][c]:
						i = i + 1
					else: break
				if i == collapse__n:
					collapse__field[h-r-1][c] = collapse__n * collapse__field[h-r-1][c]
					collapse__score = collapse__score + collapse__field[h-r-1][c]
					for j in range(collapse__n-1):
						collapse__field[h-r-1-j-1][c]=0
					hascollapsed = True
	
	elif collapse__dir == 2:
		for r in range(h):
			for c in range(h):
				if collapse__field[r][c] == 0: continue
				i = 1
				while (c+i)<h and (i<collapse__n):
					if collapse__field[r][c+i] == collapse__field[r][c]:
						i = i + 1
					else: break
				if i == collapse__n:
					collapse__field[r][c] = collapse__n * collapse__field[r][c]
					collapse__score = collapse__score + collapse__field[r][c]
					for j in range(collapse__n-1):
						collapse__field[r][c+j+1]=0
					hascollapsed = True
						
	elif collapse__dir == 3:
		for r in range(h):
			for c in range(h):
				if collapse__field[r][h-c-1] == 0: continue
				i = 1
				while (h-c-1-i)<h and (i<collapse__n):
					if collapse__field[r][h-c-1-i] == collapse__field[r][h-c-1]:
						i = i + 1
					else: break
				if i == collapse__n:
					collapse__field[r][h-c-1] = collapse__n * collapse__field[r][h-c-1]
					collapse__score = collapse__score + collapse__field[r][h-c-1]
					for j in range(collapse__n-1):
						collapse__field[r][h-c-1-j-1]=0
					hascollapsed = True
						
	return collapse__field, hascollapsed, collapse__score

def checklost(checklost__field, checklost__n):
	temp_field = copy.deepcopy(checklost__field)
	for checklost__d in range(4):
		temp__field1, checklost__hm = move(temp_field, checklost__d)
		if checklost__hm: return False
		temp__field2, checklost__hc, checklost__s = collapse(temp_field, checklost__d, checklost__n, 0)
		if checklost__hc: return False
	return True

spielstaende = []

# Feldgroesse
fs = 5
# Multiplikator fuer Zahlen und Vielfache
mp = 3
# Moegliche neu erscheinende Zahlen
nn = [1,mp]

try:
	fh = open("verbotene_zuege_"+str(fs)+"_"+str(mp)+".dat", "r")
	verbotene_zuege = json.load(fh)
	fh.close()
except:
	verbotene_zuege = []

for i in range(1000):
	
	spielstand = []

	lost = False
	score = 0
	hm = True
	hc = False

	field = []
	for j in xrange(fs):
		field.append(fs*[0])

	while lost is False:
		#	print "Vor place():"
		#	prnfield(field, score)
		if hm or hc:
			field = place(field, nn)
			#	print "Nach place():"
			#	prnfield(field, score)
		field0 = copy.deepcopy(field)
		dir = int(random.random()*4)
		#	dir = int(raw_input("Zugrichtung (o:0, u:1, l:2, r:3): "))
		field, hm = move(field, dir)
		#	if hm: print "move(): ja, Richtung", dir
		#	else: print "move(): nein, Richtung", dir
		#	prnfield(field, score)
		field, hc, score = collapse(field, dir, mp, score)
		#	if hc: print "collapse(): ja, Richtung", dir
		#	else: print "collapse(): nein, Richtung", dir
		#	prnfield(field, score)
		if hc:
			field, hm = move(field, dir)
			#	print "Nach move() wegen collapse():"
			#	prnfield(field, score)
		if hm or hc:
			spielstand.append([copy.deepcopy(field0), dir, score, 0])
		if not hm and not hc:
			if not ([copy.deepcopy(field0), dir] in verbotene_zuege):
				verbotene_zuege.append([copy.deepcopy(field0), dir])
		#	print spielstand
		lost = checklost(field[:], mp)
		#	print "Nach checklost():"
		#	prnfield(field, score)
	# 	break
		
	for s in spielstand:
		s[3] = score

	spielstaende.append(copy.deepcopy(spielstand))

	print i
		
fh = open("spielstaende_"+str(fs)+"_"+str(mp)+".dat", "w")
json.dump(spielstaende, fh)
fh.close()

fh = open("verbotene_zuege_"+str(fs)+"_"+str(mp)+".dat", "w")
json.dump(verbotene_zuege, fh)
fh.close()
