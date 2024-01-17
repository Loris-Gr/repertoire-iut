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

    possibilite_p = []
    possibilite_o = []
    possibilite_f = []
    les_joueurs=les_joueurs.split('\n') 
    for l in les_joueurs:
        l=l.split(";")
        if l[0]==ma_couleur:
            (ma_ligne,ma_colonne,nom)=(int(l[5]),int(l[6]),l[-1])

    for direction in const.DIRECTIONS:
        plan_ensemble=plateau.analyse_plateau(le_plateau,(ma_ligne,ma_colonne),direction,100)
        #if plan_ensemble["pacmans"][0][1].upper()!=nom:
        if  plan_ensemble is None or "pacmans" not in plan_ensemble:
            pass
        else:
            possibilite_p.append((plan_ensemble["pacmans"][0][0],plan_ensemble["pacmans"][0][1],direction))

        if plan_ensemble is None or "objets" not in plan_ensemble:
            pass
        else:
            for i in range(len(plan_ensemble["objets"])) :
                possibilite_o.append((plan_ensemble["objets"][i][0], plan_ensemble["objets"][i][1], direction))
            
        if plan_ensemble is None or "fantomes" not in plan_ensemble:
            pass
        else:
            possibilite_f.append((plan_ensemble["fantomes"][0][0], plan_ensemble["fantomes"][0][1],direction))
    
    #IA PACMAN (les meilleurs)
    dir_a_bannir = ""
    """for (distance,_, direction) in possibilite_f :
            if distance < 3 :
                dir_a_bannir+=direction"""

    priorite = {const.GLOUTON : 1, const.VALEUR : 2, const.PASSEMURAILLE : 3, const.IMMOBILITE : 4, const.TELEPORTATION : 5, const.VITAMINE : 100}
    
    meilleure_dist = None
    prio_meilleur  = 200
    for (distance,objet,direction) in possibilite_o :
        print(distance,objet,direction)
        ordre_prio = priorite[objet]   
        print(ordre_prio)
        if meilleure_dist is None or ordre_prio*distance < prio_meilleur*meilleure_dist  :  #and direction not in dir_a_bannir
            meilleure_dist = distance
            prio_meilleur = ordre_prio
            dir_p = direction
    print(dir_p)

    #IA Fantome(de base)
    
    meilleur_pacman=min(possibilite_p)
    dir_f = meilleur_pacman[2]

    #IA Fantome (plus inteligent)
    
    #le calcul est: ((chaque bonus multiplié par son coef)/distance avec tout les bonus)*nombre bonus
    """arrivé=False
    if not arrivé:
        calque=plateau.inondation(plan,(ma_ligne,ma_colonne))
        numéro_cases=[]
        nombre=0
        for i in range(plateau.get_nb_lignes(plan)):
            for j in range(plateau.get_nb_colonnes(plan)):
                if const.LES_OBJETS in plateau.get_objet(plateau.get_case(plan,(i,j))):
                    valeur_bonus=0
                    distance=0
                    for bonus in plateau.get_objet(plateau.get_case(plan,(i,j))):
                        valeur_bonus*=coeficients[bonus]
                    for bonus in plateau.get_objet(plateau.get_case(plan,(i,j))):
                        distance+=abs(calque[i][j]-calque[bonus[0][bonus[1]]])
                    valeur=((valeur_bonus)/distance)*
                    numéro_cases.append(valeur)
                    nombre=0
        meilleur=max(numéro_cases)
        meilleur_pacman=min(possibilite_p)
        dir_f = meilleur_pacman[2]
        """
    
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
