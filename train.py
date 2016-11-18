import json
import numpy
import keras

#	Feldgroesse
fs = 5
#	Multiplikator fuer Zahlen und Vielfache
mp = 3
#	Anzahl Vielfache-Stufen (0, 1, 3, 9, ...)
np = 8

#	Neuronales Netz
#	Eingangsknoten
input_nodes = fs**2 * np
#	Verdeckte Knoten
hidden_nodes = 30
#	Ausgangsknoten
output_nodes = 4

model = keras.models.Sequential([
	keras.layers.Dense(hidden_nodes, input_dim=input_nodes),
	keras.layers.Activation("elu"),
	keras.layers.Dense(output_nodes), 
	keras.layers.Activation("linear")])
model.compile(optimizer="rmsprop", loss="mse", metrics=["accuracy"])

fh = open("spielstaende_NN_"+str(fs)+"_"+str(mp)+".dat", "r")
ssA = json.load(fh)
print "Spielstaende geladen."
fh.close()
ssM = numpy.array(ssA)
print "Spielstaende konvertiert."

X_train = ssM[0:5000, 0:200]
Y_train = (ssM[0:5000, 200:204].T*ssM[0:5000,205]).T
print "Trainingsdaten erzeugt."

model.fit(X_train, Y_train, nb_epoch=50)
