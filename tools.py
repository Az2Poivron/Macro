import numpy as np
from graph import gen_graph, plus_proche
from marche import is_connect


def gen_mur(tab):
    tab = tab.copy()
    tab[np.where(tab != -1)] = 0
    return(tab)

def get_angle(tab,file_name=None, auto_caching= False):

    if auto_caching :
        try: #si deja en stock
            tab =np.genfromtxt(f"cache_angle/{file_name}.csv")
            return(tab)
        except:
            pass
    
    angle_deg = angle(tab)
    angle_rad = angle_to_radian(angle_deg) 
    
    if file_name != None and auto_caching:
        np.savetxt(f"cache_angle/{file_name}.csv" , angle_rad)


    return(angle_rad)

def angle_to_radian(tab):
    return(tab*np.pi/180)


##Affiche un tableau en 3D
def afficher3D(tab):
    a,b,c = tab.shape
    new = np.zeros(a*b*c).reshape(b,a,c)
    for i in range(a):
        for j in range(b):
            new[b-1-j,i] = tab[i,j]
    for l in new:
        for c in l:
            print(c , end=" ")
        print("")

#affiche un tableau 2D
def afficher(tab):
    a,b = tab.shape
    new = np.zeros(a*b).reshape(b,a)
    for i in range(a):
        for j in range(b):
            new[b-1-j,i] = tab[i,j]
    for x in new:
        for y in x:
            print(" "*(y>=0) + f"{y:0.2f}",end=" ")
        print("")
#tableau 3D , sortie => tableau d'angle en deg , sortie est en 3D
def angle(tableau):

    graph = gen_graph(tableau)
    tab=np.zeros((len(tableau),len(tableau[0])))
    for i in range(len(tableau)):
        print(i , "/" , len(tableau) , "colonnes calculées")
        for j in range(len(tableau[0])):
            if tableau[i,j]!=-1:
                s = plus_proche(graph,[i,j],tableau)
                tab[i,j]=droite_to_angle([i,j],s)
            else:
                tab[i,j] = 0

    return(tab)


#Donne l'angle d'un point vers la sortie
def droite_to_angle(point,sortie): #Convertisseur angle
    dx=sortie[0]-point[0]
    dy=sortie[1]-point[1]

    if dx!=0 : #Pas la même colonne
        sy = 1 if dy>=0 else -1
        alpha=(dx/np.abs(dx))*sy*np.arctan(np.abs(dy/dx))
        teta=alpha*180/np.pi
        if dx<0:
            teta += 180

    elif dx==0 and dy!=0: #Même colonne pas la même ligne
        signe=(dy/np.abs(dy))
        teta = signe * 90
    
    else: #sortie Arbitrairement 720 mais aucune importance
        teta=30 #Sur la sortie
    return(teta)

#projette une vitesse en 2D en fonction de son orientation
def angle_to_vitesse(v,teta_ij , epsilon = 10**-15):
    s=np.sin(teta_ij)
    c=np.cos(teta_ij)
    s[np.where(np.abs(s) < epsilon)] = 0
    c[np.where(np.abs(c) < epsilon)] = 0
    return(np.array([v*c,v*s]))
    
#renvoye un tableau
def signe(tab): 
    n = tab.copy()
    n[np.where(tab<0)] = -1
    n[np.where(tab>=0)] = 1
    return(np.array(n , dtype=np.int8))