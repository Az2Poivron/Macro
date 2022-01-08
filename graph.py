from converter import csv2tab, image2csv
import numpy as np

from marche import is_connect

# Trouve les coordonnées du coin opposé à une coordonnées
def trouver_oppose(a,b,tab):
    dic = {
        (a-1,b) : [a,b-1],
        (a,b-1) : [a-1,b],
        (a-1,b-1) : [a,b],
        (a,b):[a-1,b-1] }
    for key in dic:
        i,j = key
        if tab[i,j] == -1:
            return(dic[key])
    
    
#Trouve la position des coins en cherchant parmis tout les coin de "mur" lequel sont entouré d'exactement 1 case "mur"
def trouver_coin(tab):
    L_point = []
    indice = np.where(tab == -1) #ou sont les murs
    for i in range(len(indice[0])):#pour chaque mur
        x,y = indice[0][i] , indice[1][i]
        for k in [ [0,0], [1,0], [0,1], [1,1]]:#pour chaque coin du mur
            a,b = x + k[0] , y + k[1]
            if 0<a<tab.shape[0] and 0<b<tab.shape[1]: #aucune utilité de regarder les bords , sans compter les pb que ça peut causer.
                if len(np.where(tab[a-1:a+1 , b-1:b+1] == -1)[0]) == 1: #si 3 truc vide autour 
                    L_point.append(trouver_oppose(a,b,tab))
    return(L_point)

#distance euclidienne, rien de bien choquant
def distance2(a,b):
    return(((b[0]-a[0])**2 + (b[1]-a[1])**2)**0.5 )

#génére pour un tableau données , le graph visible , son graph après réduction par plus court chemin, pour finalement renvoyer la liste des noeuds et leur plus courte distance à une sortie
def gen_graph(tab):
    #sortie
    wr = np.where(tab == -2)
    sortie = [[wr[0][i],wr[1][i]] for i in range(len(wr[0]))]
    ns = len(sortie)

    #coin
    coin = trouver_coin(tab)
    nc = len(coin)

    #total noeuds
    noeuds = sortie + coin
    graphe = [[] for _ in range(ns + nc )] #graphe sous forme de liste d'adjacence
    for a in range(ns +nc):
        for b in range(a+1,ns +nc):
            if is_connect(noeuds[a],noeuds[b],tab):
                d = distance2(noeuds[a] ,  noeuds[b])
                graphe[a].append([b,d])
                graphe[b].append([a,d])

    #Plus court chemin en O(n²) , (Dikstra sans mémorisation des longueurs calculés et sans queue)
    D = [0 for _ in range(ns)] + [float("inf") for _ in range(nc)]
    for _ in range(nc): #Pour chaque tour
        mini = float("inf")
        i = -1
        for j in range(ns + nc): # pour chaque pas deja calculé
            if D[j]== float("inf"):
                for k,d in graphe[j]:#pour chaque voisin de j 
                    c = D[k] + d
                    if c < mini:
                        mini = c 
                        i = j
        D[i] = mini

    return(noeuds,D)


#Renvoye la case accessible rendant le chemin de A le plus court
#Calcul de D_P
def plus_proche(graph,A,tab):
    N,D = graph
    n = [0,0]
    d = float("inf")
    for i in range(len(N)):        
        if D[i] + distance2(A,N[i]) < d and is_connect(A,N[i],tab):
            
            d = D[i] + distance2(A,N[i])
            n = N[i]
    return(n)




