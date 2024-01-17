""""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module plateau.py
        Ce module contient l'implémentation de la structure de données
        qui gère le plateau jeu aussi qu'un certain nombre de fonctions
        permettant d'observer le plateau et d'aider l'IA à prendre des décisions
"""
import const
import case
import random

plat= {'nb_lignes' : 2, 'nb_colonnes' : 2,
    'valeurs':[{"mur": False, "objet" : const.AUCUN, "pacmans_presents": {'A'}, "fantomes_presents": None},
                {"mur": False, "objet" : const.AUCUN, "pacmans_presents": None, "fantomes_presents": None}, 
                {"mur": False, "objet" : '.', "pacmans_presents": None, "fantomes_presents": None},
                 {"mur": False, "objet" : const.AUCUN, "pacmans_presents": None, "fantomes_presents": {'a'}}],
                        "nb_pacman":1,"nb_fantomes":1, 
                        "pacmans" : [("A",(0,0))],
                        "fantomes" : [('a',(1,1))]}



def get_nb_lignes(plateau):
    """retourne le nombre de lignes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de lignes du plateau
    """
    return plateau["nb_lignes"]


def get_nb_colonnes(plateau):
    """retourne le nombre de colonnes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de colonnes du plateau
    """
    return plateau["nb_colonnes"]
    

def pos_ouest(plateau, pos):
    """retourne la position de la case à l'ouest de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    if pos[1] == 0:
        return (pos[0], get_nb_colonnes(plateau)-1)
    return (pos[0], pos[1]-1)

def pos_est(plateau, pos):
    """"
        retourne la position de la case à l'est de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    if pos[1]+1 == get_nb_colonnes(plateau):
        return (pos[0], 0)
    return (pos[0], pos[1]+1)

def pos_nord(plateau, pos):
    """retourne la position de la case au nord de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    if pos[0] == 0:
        return (get_nb_lignes(plateau)-1, pos[1])
    return (pos[0]-1, pos[1])

def pos_sud(plateau, pos):
    """retourne la position de la case au sud de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    if pos[0] == get_nb_lignes(plateau)-1:
        return (0, pos[1])
    return (pos[0]+1, pos[1])

def pos_arrivee(plateau,pos,direction):
    """ calcule la position d'arrivée si on part de pos et qu'on va dans
    la direction indiquée en tenant compte que le plateau est un tore
    si la direction n'existe pas la fonction retourne None
    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire d'entiers qui donne la position de départ
        direction (str): un des caractère NSEO donnant la direction du déplacement

    Returns:
        None|tuple: None ou une paire d'entiers indiquant la position d'arrivée
    """
    if direction == "N":
        return pos_nord(plateau, pos)
    elif direction == "S":
        return pos_sud(plateau, pos)
    elif direction == "O":
        return pos_ouest(plateau, pos)
    elif direction == "E":
        return pos_est(plateau, pos)
    return None 

def get_case(plateau, pos):
    """retourne la case qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        dict: La case qui se situe à la position pos du plateau
    """
    nb_colonnes = get_nb_colonnes(plateau)
    return plateau["valeurs"][pos[0]*nb_colonnes+pos[1]]
 
def get_objet(plateau, pos):
    """retourne l'objet qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        str: le caractère symbolisant l'objet
    """
    case_en_cours = get_case(plateau, pos)
    return case_en_cours['objet']

def poser_pacman(plateau, pacman, pos):
    """pose un pacman en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le pacman
        pos (tuple): une paire (lig,col) de deux int
    """
    case_pac = get_case(plateau, pos)
    case.poser_pacman(case_pac,pacman)
    
def poser_fantome(plateau, fantome, pos):
    """pose un fantome en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int
    """
    case_fan = get_case(plateau, pos)
    case.poser_fantome(case_fan, fantome)
    

def poser_objet(plateau, objet, pos):
    """Pose un objet en position pos sur le plateau. Si cette case contenait déjà
        un objet ce dernier disparait

    Args:
        plateau (dict): le plateau considéré
        objet (int): un entier représentant l'objet. const.AUCUN indique aucun objet
        pos (tuple): une paire (lig,col) de deux int
    """
    case_objet = get_case(plateau,pos)
    case.poser_objet(case_objet,objet)


def donne_contenu(nom_fichier):
    """fonction utile pour des tests avec des print de diverses fonctions

    Args:
        nom_fichier (str): nom du fichier txt

    Returns:
        str: le contenu du fichier
    """    
    nom_fichier="source/cartes/"+nom_fichier
    carte=open(nom_fichier,'r')
    return carte.read()

def set_case(plateau, pos, une_case):
    """remplace la case qui se trouve en position pos du plateau par une_case

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int
        une_case (dict): la nouvelle case
    """
    nb_colonnes = get_nb_colonnes(plateau)
    plateau["valeurs"][pos[0]*nb_colonnes+pos[1]] = une_case


def plateau(la_chaine, complet=True):
    """Construit un plateau à partir d'une chaine de caractère contenant les informations
        sur le contenu du plateau (voir sujet)

    Args:
        la_chaine (str): la chaine de caractères décrivant le plateau

    Returns:
        dict: le plateau correspondant à la chaine. None si l'opération a échoué
    """
    lignes_fichier=la_chaine.split('\n')
    (nb_ligne,nb_colonne)=(int(lignes_fichier[0].split(';')[0]),int(lignes_fichier[0].split(';')[1]))
    plateau={"nb_lignes":nb_ligne,"nb_colonnes":nb_colonne,"valeurs":[]}
    
    
    for i in range(nb_ligne):
        for j in range(nb_colonne):
            val=lignes_fichier[i+1][j]
            if val == '#':
                plateau["valeurs"].append(case.Case(True))
            elif val in const.PROP_OBJET.keys():
                plateau["valeurs"].append(case.Case(False, val))
            else:
                plateau["valeurs"].append(case.Case())
      
    début_info_pacman=i+2
    plateau["nb_pacman"]=int(lignes_fichier[début_info_pacman])
    début_info_fantomes=début_info_pacman+plateau["nb_pacman"]+1
    plateau["nb_fantomes"]=int(lignes_fichier[début_info_fantomes])
   
    for pacman in range(début_info_pacman+1,début_info_pacman+plateau["nb_pacman"]+1):
        ligne=lignes_fichier[pacman].split(";")
        try:
            plateau["pacmans"]+=[(ligne[0],(int(ligne[1]),int(ligne[2])))]
        except:
            plateau["pacmans"]=[(ligne[0],(int(ligne[1]),int(ligne[2])))]

    for fantomes in range(début_info_fantomes+1,début_info_fantomes+plateau["nb_fantomes"]+1):
        ligne=lignes_fichier[fantomes].split(";")
        try:
            plateau["fantomes"]+=[(ligne[0],(int(ligne[1]),int(ligne[2])))]
        except:
            plateau["fantomes"]=[(ligne[0],(int(ligne[1]),int(ligne[2])))]

    for pac in plateau["pacmans"]:
        poser_pacman(plateau,pac[0],pac[1])
            
    for fan in plateau["fantomes"]:
        poser_fantome(plateau,fan[0],fan[1])

    return plateau

carte=plateau(donne_contenu("carte.txt"))      # pour les tests
    

def enlever_pacman(plateau, pacman, pos):
    """enlève un joueur qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le joueur
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    case_pac = get_case(plateau,pos)
    if case_pac["pacmans_presents"] is None : 
        return False
    if pacman in case_pac["pacmans_presents"] :
        case_pac["pacmans_presents"].remove(pacman)
        set_case(plateau,pos,case_pac)
        return True
    return False


def enlever_fantome(plateau, fantome, pos):
    """enlève un fantome qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    case_fan = get_case(plateau,pos)
    if case_fan["fantomes_presents"] is None : 
        return False
    if fantome in case_fan["fantomes_presents"] :
        case_fan["fantomes_presents"].remove(fantome)
        set_case(plateau,pos,case_fan)
        return True
    return False


def prendre_objet(plateau, pos):
    """Prend l'objet qui se trouve en position pos du plateau et retourne l'entier
        représentant cet objet. const.AUCUN indique qu'aucun objet se trouve sur case

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        int: l'entier représentant l'objet qui se trouvait sur la case.
        const.AUCUN indique aucun objet
    """
    case = get_case(plateau,pos)
    objet = case["objet"]
    if objet != const.AUCUN:
        case["objet"]=const.AUCUN
        return objet
    return const.AUCUN


def case_vide(plateau):
    """choisi aléatoirement sur la plateau une case qui n'est pas un mur et qui
       ne contient ni pacman ni fantome ni objet

    Args:
        plateau (dict): le plateau

    Returns:
        (int,int): la position choisie
    """
    nb_ligne = get_nb_lignes(plateau)
    nb_colonne = get_nb_colonnes(plateau)
    liste_position = []
    exemple_case_vide = case.Case() 
    # on fait une double boucle pour récupérer toutes les cases vides
    for x in range(nb_ligne) :
        for y in range(nb_colonne):
            case_en_cours = get_case((plateau,(x,y)))
            if case_en_cours == exemple_case_vide:
                liste_position.append((x,y))              
    return random.choice(liste_position)  # on choisis une position au hasard parmis les cases vides

def directions_possibles(plateau,pos,passemuraille=False):
    """ retourne les directions vers où il est possible de se déplacer à partir
        de la position pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): un couple d'entiers (ligne,colonne) indiquant la position de départ
        passemuraille (bool): indique si on s'autorise à passer au travers des murs 
    
    Returns:
        str: une chaine de caractères indiquant les directions possibles
              à partir de pos
    """
    direction_possible = ""
    for direction in 'NSEO':
        pos_ar = pos_arrivee(plateau, pos, direction)
        if pos_ar is not None:
            if not(case.est_mur(get_case(plateau,pos_ar))) or passemuraille:
                direction_possible += direction
    return direction_possible


def deplacer_pacman(plateau, pacman, pos, direction, passemuraille=False):
    """Déplace dans la direction indiquée un joueur se trouvant en position pos
        sur le plateau si c'est possible

    Args:
        plateau (dict): Le plateau considéré
        pacman (str): La lettre identifiant le pacman à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement
        passemuraille (bool): un booléen indiquant si le pacman est passemuraille ou non

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du pacman 
                   (None si le pacman n'a pas pu se déplacer)
    """
    directions = directions_possibles(plateau,pos,passemuraille)
    nouvelle_position = None
    if direction == 'N' and 'N' in directions :
        nouvelle_position = pos_nord(plateau,pos)
    elif direction == 'S' and 'S' in directions:
        nouvelle_position = pos_sud(plateau,pos)
    elif direction == 'E' and 'E' in directions :
        nouvelle_position = pos_est(plateau,pos)
    elif direction == 'O' and 'O' in directions:
        nouvelle_position = pos_ouest(plateau,pos)
    else:
        return None
    case_actuelle = get_case(plateau,pos)
    if case_actuelle['pacmans_presents'] is not None and pacman in case_actuelle['pacmans_presents'] :   
        enlever_pacman(plateau,pacman,pos)
        poser_pacman(plateau,pacman,nouvelle_position)
        return nouvelle_position
    return None

def deplacer_fantome(plateau, fantome, pos, direction):
    """Déplace dans la direction indiquée un fantome se trouvant en position pos
        sur le plateau


        plateau (dict): Le plateau considéré
        fantome (str): La lettre identifiant le fantome à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du fantome
                   None si le joueur n'a pas pu se déplacer
    """
    
    directions = directions_possibles(plateau,pos)
    nouvelle_position = None
    if 'N' in directions and direction == 'N':
        nouvelle_position = pos_nord(plateau,pos)
    elif direction == 'S' and 'S' in directions :
        nouvelle_position = pos_sud(plateau,pos)
    elif direction == 'E' and 'E' in directions :
        nouvelle_position = pos_est(plateau,pos)
    elif direction == 'O' and 'O' in directions:
        nouvelle_position = pos_ouest(plateau,pos)
    else:
        return None
    enlever_fantome(plateau,fantome,pos)
    poser_fantome(plateau,fantome,nouvelle_position)
    return nouvelle_position                    

#---------------------------------------------------------#
    


def inondation(plateau,position):
    calque=[]
    for _ in range(plateau["nb_lignes"]):
        calque.append([None]*plateau["nb_colonnes"])
    calque[position[0]][position[1]]=1
    fin=False
    while not fin:
        fin=True
        for i in range(len(calque)):
            for j in range(len(calque[0])):
                if calque[i][j] is not None and get_case(plateau,(i,j))!="#":
                    num=calque[i][j]+1
                    dir_pos=directions_possibles(plateau,(i,j))
                    if len(dir_pos)==0:
                        return None
                    voisins=[]
                    for dire in dir_pos:
                        voisins.append(pos_arrivee(plateau,(i,j),dire))
                    for voisin in voisins:
                        if calque[voisin[0]][voisin[1]] is None or calque[voisin[0]][voisin[1]]>num :
                            calque[voisin[0]][voisin[1]]=num
                            fin=False
    return calque





def analyse_plateau(plateau, pos, direction, distance_max):
    """calcul les distances entre la position pos est les différents objets et
        joueurs du plateau si on commence par partir dans la direction indiquée
        en se limitant à la distance max. Si il n'est pas possible d'aller dans la
        direction indiquée à partir de pos, la fonction doit retourner None

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distances
        distance_max (int): un entier indiquant la distance limite de la recherche
    Returns:
        dict: un dictionnaire de listes. 
                Les clés du dictionnaire sont 'objets', 'pacmans' et 'fantomes'
                Les valeurs du dictionnaire sont des listes de paires de la forme
                    (dist,ident) où dist est la distance de l'objet, du pacman ou du fantome
                                    et ident est l'identifiant de l'objet, du pacman ou du fantome
            S'il n'est pas possible d'aller dans la direction indiquée à partir de pos
            la fonction retourne None
    """ 
    res=dict()
    positions_bonus=[]
    for i in range(plateau["nb_lignes"]):
        for j in range(plateau["nb_colonnes"]):
            case_en_cours=get_case(plateau,(i,j))
            if case_en_cours["objet"] is not const.AUCUN:
                for nom in case_en_cours["objet"]:
                    identite=nom
                positions_bonus.append(((i,j),identite,"objets"))
            
            if case_en_cours["pacmans_presents"] is not None:
                for nom in case_en_cours["pacmans_presents"]:
                    identite=nom
                positions_bonus.append(((i,j),identite,"pacmans"))
            
            if case_en_cours["fantomes_presents"] is not None:
                for nom in case_en_cours["fantomes_presents"]:
                    identite=nom
                positions_bonus.append(((i,j),identite,"fantomes"))
    
    
    pos=pos_arrivee(plateau,pos,direction)
    if case.est_mur(get_case(plateau,pos)):
        return None
    for bonus in positions_bonus:
        calque=inondation(plateau,pos)
        if calque is None:
            return None
        if calque[bonus[0][0]][bonus[0][1]]<=distance_max:
            try:
                res[bonus[2]].append((int(calque[bonus[0][0]][bonus[0][1]]),str(bonus[1])))
            except:
                res[bonus[2]]=[(int(calque[bonus[0][0]][bonus[0][1]]),str(bonus[1]))]
    for cle in res.values():
        cle.sort()
    return res




def direction_inverse(direction):
    """renvoie l'inverse d'une direction

    Args:
        direction (str): lettre de direction

    Returns:
        str|None : inverse de la description
    """    
    if direction == "E":
        return "O"
    elif direction == "O":
        return "E"
    elif direction == "S":
        return "N"
    elif direction == "N":
        return "S"
    return None


def prochaine_intersection(plateau,pos,direction):
    """calcule la distance de la prochaine intersection
        si on s'engage dans la direction indiquée

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position de départ
        direction (str): la direction choisie

    Returns:
        int: un entier indiquant la distance à la prochaine intersection
             -1 si la direction mène à un cul de sac.
    """
    dist = 0
    temp = pos
    while len(directions_possibles(plateau, temp)) >= 2:
        if direction not in directions_possibles(plateau, temp, False):
            direc = directions_possibles(plateau, temp, False).replace(direction_inverse(direction), "")
            return prochaine_intersection(plateau,pos,direc) + dist
        dist += 1
        temp = pos_arrivee(plateau, temp, direction)
        if len(directions_possibles(plateau, temp)) >= 3:
            return dist-1
    return -1


# A NE PAS DEMANDER
def plateau_2_str(plateau):
        res = str(get_nb_lignes(plateau))+";"+str(get_nb_colonnes(plateau))+"\n"
        pacmans = []
        fantomes = []
        for lig in range(get_nb_lignes(plateau)):
            ligne = ""
            for col in range(get_nb_colonnes(plateau)):
                la_case = get_case(plateau,(lig, col))
                if case.est_mur(la_case):
                    ligne += "#"
                    les_pacmans = case.get_pacmans(la_case)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                else:
                    obj = case.get_objet(la_case)
                    les_pacmans = case.get_pacmans(la_case)
                    les_fantomes= case.get_fantomes(la_case)
                    ligne += str(obj)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                    for fantome in les_fantomes:
                        fantomes.append((fantome,lig,col))
            res += ligne+"\n"
        res += str(len(pacmans))+'\n'
        for pac, lig, col in pacmans:
            res += str(pac)+";"+str(lig)+";"+str(col)+"\n"
        res += str(len(fantomes))+"\n"
        for fantome, lig, col in fantomes:
            res += str(fantome)+";"+str(lig)+";"+str(col)+"\n"
        return res
    
