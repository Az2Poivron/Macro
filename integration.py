import pygame
import random
import sys
import numpy as np
import time
#Personnal fct
from tools import angle_to_vitesse, get_angle , signe, gen_mur
from converter import csv2tab

#vitesse entre 0 et 1 
v = 0.8

#vitesse de diminution de la couleur en fonction de la densité
coef_color = 1

#facteur de multiplicationd de la fenetre 
screen_size = 10

#nb d'image par seconde
FPS = 10

#file_name = "metro1"
file_name = "laby4"
file_name = "comparatif3"
#file_name = "monstrueux1"
#file_name = "dedale"
#file_name = "demo"
#file_name = "uniform2"

def random_walk(tab,a,b,d):
	L = [[-1,0] ,[1,0] ,[0,-1] ,[0,1]]
	while d > 0:
		p=0
		if 0 <= tab[a,b] < 1: #si y a de la place
			disponible = 1 - tab[a,b]
			if disponible >= d: #si + de place qu'on en a 
				p = d
				d = 0
			else: #si on peu en mettre qu'une partie
				p = disponible
				d = d - disponible
			tab[a,b] += p
		#si prochaine étape
		if d>0:
			possibilite = []
			for x,y in L: #pour chaque petits décallages possibles
				bonobo , nobono = a + x , b + y  
				if 0<= bonobo < tab.shape[0] and 0 <= nobono <tab.shape[1] and tab[bonobo,nobono] != -1 :
					
					possibilite.append( [bonobo, nobono])
					
			r = possibilite[random.randint(0,len(possibilite)-1)]
			a,b = r[0] , r[1]
	return(tab)
				

#Etape a t + dt avec v <= 1
def etape(tab_densite,tab_vitesse,tab_vide,where_sortie):
	tab = tab_vide.copy()
	for ii in range(tab_densite.shape[0]): #Pour chaque x
		for jj in range(tab_densite.shape[1]): #Pour chaque y 
			i = ii
			j = jj
			
			d = tab_densite[i,j]
			if d > 0: #si y a des gens de base
				dx = tab_vitesse[0,i,j] #vitesse en x
				dy = tab_vitesse[1,i,j] #vitesse en y 
				#SHIFT
				if dx < 0: #si déplaceemnt en x négatif
					i -= 1
					dx = 1 + dx
				if dy < 0: #si déplacement en y n égatif
					j -= 1
					dy = 1 + dy
				coord = [[i,j] , [i+1,j] , [i,j+1] , [i+1,j+1]] #coordonnée générale
				pourcentage = [(1-dx)*(1-dy) , dx*(1-dy) , (1-dx)*dy , dx*dy] #pourcentage associé
				for k in range(4): #pour chaque endroit à distribuer
					a,b = coord[k]
					tab = random_walk(tab ,a ,b ,pourcentage[k]*d) #faire marche aléatoire
	tab[where_sortie] = 0
	return(tab)


#ça draw , c'est pas du tout opti mais pour le moment on va faire avec
def draw(tab,where_sortie,display,screen):
	display.fill((0,0,0))
	
	for i in range(tab.shape[0]):
		for j in range(tab.shape[1]):
			pos = (i,tab.shape[1] -j-1)
			if tab[i,j]>=0:
				display.set_at(pos,(255*(min(1,tab[i][j])**coef_color),)*3)
			elif tab[i,j] == -1:
				display.set_at(pos,(255,0,0))

	for i in range(len(where_sortie[0])):
		a,b = where_sortie[0][i] , where_sortie[1][i]
		pos = (a,tab.shape[1] -b-1)
		display.set_at(pos,(0,255,0))			
	screen.blit(pygame.transform.scale(display ,(tab.shape[0]*screen_size,tab.shape[1]*screen_size)), (0,0) )
	pygame.display.update()
	


#Initialisation Des tableaux utilisé
tab_densite = csv2tab(file_name)
sortie = [1,1] #Trouver toutes les sorties


tab_angle = get_angle(tab_densite,file_name=file_name,auto_caching=True) #Faire des dingueries avec Djikstra tout ça
tab_vitesse = angle_to_vitesse(v , tab_angle)
tab_vide = gen_mur(tab_densite)
where_sortie = np.where(tab_densite == -2)

#initialisation de l'affichage
pygame.init()
screen = pygame.display.set_mode((tab_densite.shape[0] * screen_size , tab_densite.shape[1] * screen_size))
display = pygame.Surface((tab_densite.shape[0],tab_densite.shape[1]))
clock = pygame.time.Clock()
running = True

#la boucle est bouclé, tu connais
draw(tab_densite,where_sortie,display,screen)
time.sleep(0.5)

tour = 0
N = 10
while running:
	tour += 1
	clock.tick(FPS)
	#INPUT
	for event in pygame.event.get():
		if event.type == pygame.QUIT: #Quit
			sys.exit()
			break
	tab_densite = etape(tab_densite,tab_vitesse,tab_vide,where_sortie)
	draw(tab_densite,where_sortie,display,screen)
	
	
	