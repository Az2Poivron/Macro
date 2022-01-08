import random

#Somme trié de 2 liste trié O(N+M)
def fusion2D(L1,L2,i = 2):
    if L1==[] or L2==[]:
        return(L1+L2)
    if L1[0][i]<L2[0][i]:
        return([L1[0]]+fusion2D(L2,L1[1:]))
    return([L2[0]]+fusion2D(L1,L2[1:]))

#Génère la liste des entier entre 2 bornes (prenant l'ordre)
def gen_x(A,B,i=0):
    ax = A[i]
    bx = B[i]
    if ax > bx:
        ax,bx = bx,ax
        reverse = True
    else:
        reverse = False

    b_inf = int(ax) + 1 #(ax != int(ax))
    b_sup = int(bx) + (bx != int(bx))

    L = [i for i in range(b_inf,b_sup)]
    if reverse:
        L.reverse()
    return(L)

#Génère un y associé à un x
def gen_y(A,B,x,i=0):#i = indice de x
    ax = A[i]
    bx = B[i]
    ay = A[1-i]
    by = B[1-i]

    p = gen_p(ax,bx,x)
    y = ay + (by-ay)*p
    return(y)

#Renvoye le pourcentage de segment parcouru
def gen_p(ax,bx,x):
    l = bx-ax #longueur
    if l == 0: #histoire d'éviter de diviser par 0 :)
        return(1)
    return((x-ax)/l)

#Génère la liste des points d'intersection à la grille
def gen_intersection(A,B):
    X = gen_x(A,B,0)
    Y = gen_x(A,B,1)
    LX = []
    for x in X:
        y = gen_y(A,B,x,0)
        if y ==int(y):
            marker = 'xy'
        else:
            marker = 'x'
        LX.append([x , y , gen_p(A[0],B[0],x) , marker])
    LY = []
    for y in Y:
        x = gen_y(A,B,y,1)
        if x == int(x):
            marker = 'xy'
        else:
            marker = 'y'

        LY.append([x , y , gen_p(A[1],B[1],y) , marker])

    L = fusion2D(LX,LY)
    return(L)

#Redondance de code mais pas trouvé mieux
#Cas particulier traité, ne pas regarder
def ligne_droite(A,B):
    L=[]
    L_inter = gen_intersection(A,B)
    if A[0] == B[0]:
        sy =[-1,1][ A[1] < B[1] ] #direction en y 
        x1 = A[0]-1
        x2 = A[0]
        y = int(A[1])
        if y == A[1] and A[1] > B[1]:
            y -= 1
        L = [ [[x1,y]],[[x2,y]]]
        for _ in L_inter:
            y+=sy
            L[0].append([x1,y])
            L[1].append([x2,y])

    if A[1] == B[1]:
        sy =[-1,1][ A[0] < B[0] ] #direction en y 
        x1 = A[1]-1
        x2 = A[1]
        y = int(A[0])
        if y == A[0] and A[0] > B[0]:
            y -= 1
        L = [ [[y,x1]],[[y,x2]]]
        for _ in L_inter:
            y+=sy
            L[0].append([y,x1])
            L[1].append([y,x2])

    return(L)
        
#Dit si 2 Point sont connecté entre eux , gère le cas des doubles chemin pour les lignes droites
def is_connect(A,B,tab, wall =-1):
    trajets = gen_trajet(A,B)
    R = []
    for trajet in trajets:
        statut = True
        for x,y in trajet:
            if tab[x,y] == wall:
                statut = False
        R.append(statut)
    return(statut)

#génère la liste des cases rencontrée de A à B, mixte étrange entre hardcodage et astuce, ne pas chercher à comprendre
def gen_trajet(A,B):
    if (A[0] == B[0] == int(A[0])) or (A[1] == B[1] == int(A[1])):
        return(ligne_droite(A,B))

    sx = [-1,1][ A[0] < B[0] ] #direction en x
    sy = [-1,1][ A[1] < B[1] ] #direction en y 
    
    x = int(A[0])
    if x == A[0] and A[0] > B[0]:
        x -= 1

    y = int(A[1])
    if y == A[1] and A[1] > B[1]:
        y -= 1
    L = [[x,y]]
    L_inter = gen_intersection(A,B)
    skip = False
    for p in L_inter:
        marker = p[3]
        if skip == True:
            skip = False
        else:
            if marker == 'x':
                x += sx
            elif marker =='y':
                y += sy
            elif marker == 'xy': #gestion des diagonales ou le trajet passe exactement entre 4 case de tableau d'un coup
                add = [[x+sx,y] , [x,y+sy]]
                random.shuffle(add) #pas de jaloux
                L += add
                x += sx
                y += sy
                skip = True
            L.append([x,y])
    return([L])