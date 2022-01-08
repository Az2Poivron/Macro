from converter import csv2tab, image2csv
import numpy as np

from marche import is_connect

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
    
    

def trouver_coin(tab):
    L_point = []
    indice = np.where(tab == -1) #ou sont les murs
    for i in range(len(indice[0])):#pour chaque mur
        x,y = indice[0][i] , indice[1][i]
        for k in [ [0,0], [1,0], [0,1], [1,1]]:#pour chaque coin du mur
            a,b = x + k[0] , y + k[1]
            if 0<a<tab.shape[0] and 0<b<tab.shape[1]: #fuc les bords.
                if len(np.where(tab[a-1:a+1 , b-1:b+1] == -1)[0]) == 1: #si 3 truc vide autour 
                    L_point.append(trouver_oppose(a,b,tab))
    return(L_point)

def distance2(a,b):
    return(((b[0]-a[0])**2 + (b[1]-a[1])**2)**0.5 )

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
    graphe = [[] for _ in range(ns + nc )]
    for a in range(ns +nc):
        for b in range(a+1,ns +nc):
            if is_connect(noeuds[a],noeuds[b],tab):
                d = distance2(noeuds[a] ,  noeuds[b])
                graphe[a].append([b,d])
                graphe[b].append([a,d])
    #Plus court chemin en O(n²) , une vrai honte mais passons, il est 2 heures du mat
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
def plus_proche(graph,A,tab):
    N,D = graph
    n = [0,0]
    d = float("inf")
    for i in range(len(N)):        
        if D[i] + distance2(A,N[i]) < d and is_connect(A,N[i],tab):
            
            d = D[i] + distance2(A,N[i])
            n = N[i]
    return(n)




