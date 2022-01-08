import matplotlib.image as mpimg
import numpy as np

#[Rouge, Vert, Bleu]
# Rouge = Mur
# Vert = Sortie
# #bleu = gros dodo
#
def image2csv(name):
    img = mpimg.imread(f"map/image/{name}.png")
    #densité
    tab = 1 - img[:,:,0]
    #Mur
    tab[np.where( (img[:,:,0] == 1) * (img[:,:,1] == 0) * (img[:,:,2] == 0) )] = -1
    #Sortie
    tab[np.where( (img[:,:,0] == 0) * (img[:,:,1] == 1) * (img[:,:,2] == 0) )] = -2
    np.savetxt(f"map/csv/{name}.csv" , tab ,fmt="%1.3f")

def csv2tab(name):
    #j,len(tab) - i-1

    tab =np.genfromtxt(f"map/csv/{name}.csv")
    a,b = tab.shape
    new = np.zeros(a*b).reshape(b,a)
    for i in range(b):
        for j in range(a):
            new[i,j] = tab[a-1-j,i]
    return(new)

image2csv("djikstra")