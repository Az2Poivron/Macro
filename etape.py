#Etape a t + dt avec v <= 1
def etape(tab_densite,tab_vitesse,tab_vide,where_sortie):
	tab = tab_vide.copy() #Nouveau tableau sans densite
	for ii in range(tab_densite.shape[0]): #Pour chaque i
		for jj in range(tab_densite.shape[1]): #Pour chaque j
			#Copy des coordonnees
			i = ii
			j = jj
			d = tab_densite[i,j] #recuperation de la densite de la case (i,j)
			if d > 0: #si il y a de la densite a deplacer
				dx = tab_vitesse[0,i,j] #vitesse en x
				dy = tab_vitesse[1,i,j] #vitesse en y 
				#SHIFT
				if dx < 0: #si deplaceemnt en x negatif
					i -= 1
					dx = 1 + dx
				if dy < 0: #si deplacement en y negatif
					j -= 1
					dy = 1 + dy
				coord = [[i,j] , [i+1,j] , [i,j+1] , [i+1,j+1]] #coordonnee generale
				pourcentage = [(1-dx)*(1-dy) , dx*(1-dy) , (1-dx)*dy , dx*dy] #pourcentage associe
				for k in range(4): #pour chaque endroit a distribuer
					a,b = coord[k]
					#distribuer
					tab = random_walk(tab ,a ,b ,pourcentage[k]*d) #faire marche aleatoire
	tab[where_sortie] = 0
	return(tab)