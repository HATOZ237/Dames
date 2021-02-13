import pickle
import damier
fichiersave = open("donnees.txt", "wb")
Damier = damier.Damier("noir", 100)
test = str(Damier.ListeDamier)
pickle.dump(test, fichiersave)