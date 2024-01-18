# coding: utf-8
"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module client_joueur.py
        Ce module contient le programme principal d'un joueur
        il s'occupe des communications avec le serveur
            - envois des ordres
            - recupération de l'état du jeu
        la fonction mon_IA est celle qui contient la stratégie de
        jeu du joueur.

"""
import argparse
import random
import client
import const
import plateau
import case
import joueur
from math import *
prec='X'

def calcul_possibilite(p_plateau, ligne, colonne):
    possibilite_p = []
    possibilite_o = []
    possibilite_f = []
    for direction in const.DIRECTIONS:
        plan_ensemble=plateau.analyse_plateau(p_plateau,(ligne, colonne),direction,100)
        #if plan_ensemble["pacmans"][0][1].upper()!=nom:
        if  plan_ensemble is None or "pacmans" not in plan_ensemble:
            pass
        else:
            for i in range(len(plan_ensemble["pacmans"])) :
                possibilite_p.append((plan_ensemble["pacmans"][i][0],plan_ensemble["pacmans"][i][1],direction))

        if plan_ensemble is None or "objets" not in plan_ensemble:
            pass
        else:
            for i in range(len(plan_ensemble["objets"])) :
                possibilite_o.append((plan_ensemble["objets"][i][0], plan_ensemble["objets"][i][1], direction))
            
        if plan_ensemble is None or "fantomes" not in plan_ensemble:
            pass
        else:
            for i in range(len(plan_ensemble["fantomes"])) :
                possibilite_f.append((plan_ensemble["fantomes"][i][0], plan_ensemble["fantomes"][i][1],direction))
                
    return (possibilite_p, possibilite_o, possibilite_f)



def mon_IA(ma_couleur,carac_jeu, plan, les_joueurs):
    """ Cette fonction permet de calculer les deux actions du joueur de couleur ma_couleur
        en fonction de l'état du jeu décrit par les paramètres. 
        Le premier caractère est parmi XSNOE X indique pas de peinture et les autres
        caractères indique la direction où peindre (Nord, Sud, Est ou Ouest)
        Le deuxième caractère est parmi SNOE indiquant la direction où se déplacer.

    Args:
        ma_couleur (str): un caractère en majuscule indiquant la couleur du jeur
        carac_jeu (str): une chaine de caractères contenant les caractéristiques
                                   de la partie séparées par des ;
             duree_act;duree_tot;reserve_init;duree_obj;penalite;bonus_touche;bonus_rechar;bonus_objet           
        plan (str): le plan du plateau comme comme indiqué dans le sujet
        les_joueurs (str): le liste des joueurs avec leur caractéristique (1 joueur par ligne)
        couleur;reserve;nb_cases_peintes;objet;duree_objet;ligne;colonne;nom_complet
    
    Returns:
        str: une chaine de deux caractères en majuscules indiquant la direction de peinture
            et la direction de déplacement

    """
     
    # decodage des informations provenant du serveur
    joueurs={}
    for ligne in les_joueurs.split('\n'):
        lejoueur=joueur.joueur_from_str(ligne)
        joueurs[joueur.get_couleur(lejoueur)]=lejoueur
    le_plateau=plateau.plateau(plan)
    
    # IA complètement aléatoire
    """dir_p=  random.choice("00000")
    dir_f=  random.choice("NESO")
    return dir_p+dir_f"""

    # Création des possibilités
    
    #possibilite pacman
    les_joueurs_p=les_joueurs.split('\n') 
    for l in les_joueurs_p:
        l=l.split(";")
        if l[0]==ma_couleur:
            (ma_ligne_p,ma_colonne_p,nom_p)=(int(l[3]),int(l[4]),l[-1])
    (possibilite_p_p, possibilite_p_o, possibilite_p_f) = calcul_possibilite(le_plateau, ma_ligne_p, ma_colonne_p)
    
    
    #possibilite fantome
    les_joueurs_f=les_joueurs.split('\n') 
    for l in les_joueurs_f:
        l=l.split(";")
        if l[0]==ma_couleur:
            (ma_ligne_f,ma_colonne_f,nom_f)=(int(l[5]),int(l[6]),l[-1])
    (possibilite_f_p, possibilite_f_o, possibilite_f_f) = calcul_possibilite(le_plateau, ma_ligne_f, ma_colonne_f)
   
    #IA PACMAN (les meilleurs)
    dir_a_bannir = ""
    for (distance,nom_f, direction) in possibilite_p_f :
            if distance < 3 and nom_f.upper() != nom_p :
                dir_a_bannir+=direction

    priorite = {const.GLOUTON : 1, const.VALEUR : 2, const.PASSEMURAILLE : 3, const.IMMOBILITE : 4, const.TELEPORTATION : 5, const.VITAMINE : 6}

    meilleure_dist = None
    prio_meilleur  = None
    for (distance,objet,direction) in possibilite_p_o :
        ordre_prio = priorite[objet]
        if meilleure_dist is None or ordre_prio*distance < prio_meilleur*meilleure_dist and direction not in dir_a_bannir :
            meilleure_dist = distance
            prio_meilleur = ordre_prio
            dir_p = direction

    #IA Fantome(de base)
    def aller_vers_fantome():
        meilleur_pacman=min(possibilite_f_p)
        dir_f = meilleur_pacman[2]
        return dir_f

    #IA Fantome (plus inteligent)

    def groupement_de_valeurs(valeurs,max):
        for valeur in range(len(valeurs)-1):
            if valeurs[valeur]
    
    #le calcul est: ((chaque bonus multiplié par son coef)/distance avec tout les bonus)*nombre bonus
    calque=plateau.inondation(le_plateau,(ma_ligne_f,ma_colonne_f))
    numéro_cases=[]
    bonus_a_proximité=plateau.analyse_plateau(le_plateau,(i,j),plateau.directions_possibles(le_plateau,(i,j))[0],1000)
    if "objets" in bonus_a_proximité:
            for bonus in bonus_a_proximité:

            if calque[i][j] is not None:
                possib = plateau.analyse_plateau(le_plateau,(i,j),plateau.directions_possibles(le_plateau,(i,j))[0],3)
                bonus_a_proximité = possib["objets"]
                valeur_bonus=1
                distance=0
                nombre=0
                for bonus in bonus_a_proximité:
                    valeur_bonus*=coeficient[bonus[1]]
                    distance+=abs(calque[i][j]-bonus[0])
                    nombre+=1
                if distance==0:
                    return dir_p+aller_vers_fantome()
                valeur=(((valeur_bonus)/distance)*nombre)
                numéro_cases.append((valeur,(i,j)))
    
    
    meilleur=max(numéro_cases)
    calque_depuis_arrivé=plateau.inondation(le_plateau,(meilleur[1]))
    minim=float("inf")
    
    
    if calque_depuis_arrivé[ma_ligne_f+1][ma_colonne_f] is not None and calque_depuis_arrivé[ma_ligne_f+1][ma_colonne_f]<minim:
        minim=calque_depuis_arrivé[ma_ligne_f+1][ma_colonne_f]
        dir_f="S"
    if calque_depuis_arrivé[ma_ligne_f-1][ma_colonne_f] is not None and calque_depuis_arrivé[ma_ligne_f-1][ma_colonne_f]<minim:
        minim=calque_depuis_arrivé[ma_ligne_f-1][ma_colonne_f]
        dir_f="N"
    if calque_depuis_arrivé[ma_ligne_f][ma_colonne_f+1] is not None and calque_depuis_arrivé[ma_ligne_f][ma_colonne_f+1]<minim:
        minim=calque_depuis_arrivé[ma_ligne_f][ma_colonne_f+1]
        dir_f="E"
    if calque_depuis_arrivé[ma_ligne_f+1][ma_colonne_f-1] is not None and calque_depuis_arrivé[ma_ligne_f+1][ma_colonne_f-1]<minim:
        minim=calque_depuis_arrivé[ma_ligne_f+1][ma_colonne_f-1]
        dir_f="O"
    
    return dir_p+dir_f

if __name__=="__main__":
    parser = argparse.ArgumentParser()  
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    
    args = parser.parse_args()
    le_client=client.ClientCyber()
    le_client.creer_socket(args.serveur,args.port)
    le_client.enregistrement(args.nom_equipe,"joueur")
    ok=True
    while ok:
        ok,id_joueur,le_jeu=le_client.prochaine_commande()
        if ok:
            carac_jeu,le_plateau,les_joueurs=le_jeu.split("--------------------\n")
            actions_joueur=mon_IA(id_joueur,carac_jeu,le_plateau,les_joueurs[:-1])
            le_client.envoyer_commande_client(actions_joueur)
            # le_client.afficher_msg("sa reponse  envoyée "+str(id_joueur)+args.nom_equipe)
    le_client.afficher_msg("terminé")
