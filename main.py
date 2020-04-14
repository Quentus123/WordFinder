from typing import List
from typing import Tuple
from typing import Dict
from classes.graph import Graph
from classes.branch import Branch
from classes.vertex import Vertex
import os
import re
import time

#Fonctions d'aides

def binarySearch( element: str, sortedList: List[str]) -> int:
    '''
    Algorithme de recherche dichotomique.
    Prend en entrées l'élément à rechercher et une liste triée.
    Renvoie l'indice dans la liste si l'élément est trouvé, None sinon.

    Très adapté à la recherche dans de grandes listes triées, au hasard, un dictionnaire de mots.
    '''
    inf = 0
    sup = len(sortedList)-1
    mid = (inf+sup)//2
    while inf < sup :
        if sortedList[mid] == element :
            return mid
        elif sortedList[mid] > element :
            sup = mid-1
        else :
            inf = mid+1
        mid = (inf+sup)//2
    if sortedList[mid] == element:
        return mid
    else:
        return None

def getDictionnaries(filePath: str) -> Tuple[List[str], Dict[str, List[str]]]:
    '''
    Prend en entrée le chemin du fichier contenant les mots.
    Renvoie deux éléments :
    - Une liste de mots qui est le dictionnaire
    - Une dictionnaire de dictionnaires où tous les mots ont été troncaturés d'une longueur donnée en clé

    Le fichier formatté doit correspondre aux contraintes suivantes :
    - Un mot par ligne, réduit de ses espaces latéraux
    - Aucun mot de doit contenir d'accent
    - La liste des mots doit être triées par ordre croissant (IMPORTANT)

    Exemple pour la seconde variable de retour :
    Supposons que notre dictionnaire provenant du fichier txt soit ['ABEILLE', 'BAGUE', 'OUI', 'PYTHON'] la deuxième variable de retour sera :
    {
        '1': ['A', 'B', 'O', 'P'],
        '2': ['AB', 'BA', 'OU', PY],
        '3': ['ABE', 'BAG', 'OUI', 'PYT'],
        '4': ['ABEI', 'BAG', 'OUI', 'PYTH'],
        etc... 
    }
    '''

    # On crée le tableau de mots
    dictionnary: List[str] = []
    with open(filePath) as txt_file: 
        for line in txt_file:
            dictionnary.append(line.upper()[:-1]) #On met en majuscule et on enlève le saut de ligne

    dictionnariesReduced = {
        '1': [word[:1] for word in dictionnary],
        '2': [word[:2] for word in dictionnary],
        '3': [word[:3] for word in dictionnary],
        '4': [word[:4] for word in dictionnary],
        '5': [word[:5] for word in dictionnary],
        '6': [word[:6] for word in dictionnary],
        '7': [word[:7] for word in dictionnary],
        '8': [word[:8] for word in dictionnary],
        '9': [word[:9] for word in dictionnary],
        '10': [word[:10] for word in dictionnary],
        '11': [word[:11] for word in dictionnary],
        '12': [word[:12] for word in dictionnary],
        '13': [word[:13] for word in dictionnary],
        '14': [word[:14] for word in dictionnary],
        '15': [word[:15] for word in dictionnary],
        '16': [word[:16] for word in dictionnary]
    }

    return dictionnary, dictionnariesReduced

def filterIfStringIsStartOfWord(string: str, sortedReducedDictionnary: Dict[str, List[str]]) -> bool:
    '''
    Teste si une chaîne de caractères peut être complétée afin de former un mot.
    Prend en entrées la chaîne de caractères à tester et un ensemble de dictionnaires comme la deuxième variable du return de la fonction getDictionnaries.
    '''
    if binarySearch(element = string, sortedList = sortedReducedDictionnary[str(len(string))]) != None:
        return True
    else:
        return False

def createVerticesFromString(string: str) -> List[Vertex]:
    '''
    Traite l'entrée des sommets du graphe de l'utilisateur.
    Prend en entrées la chaîne rentrée par l'utilisateur.
    Renvoie la liste des sommets.

    Le pattern de l'entrée adopté est le suivant:
    - Les lettres sont rentrées de gauche à droite, en suivant la numérotation du graphe
    - Si la lettre ne contient aucun bonus, on écrit simplement la lettre, par exemple : A
    - Si la lettre contient un bonus de multiplication de lettre, on écrit le multiplicateur une fois suivi de la lettre, par exemple : 3A
    - Si la lettre contient un bonus de multiplication de mot, on écrit deux fois le multiplicateur suivi de la lettre, par exemple : 22A
    - Aucun espace
    '''
    inputRegex = r'[2-3]{0,2}[A-Z]{1}'
    matches = re.findall(inputRegex, string)
    vertices: List[Vertex] = []
    for i in range(0, 16):
        if(len(matches[i]) == 1): # aucun multiplicateur
            vertices.append(Vertex(id = i, letter = matches[i]))
        elif(len(matches[i]) == 2): # multiplicateur de lettre
            vertices.append(Vertex(id = i, letter = matches[i][1], letterMultiplier = int(matches[i][0])))
        else: # len vaut 3 donc il y a un multiplicateur de mot
            vertices.append(Vertex(id = i, letter = matches[i][2], wordMultiplier = int(matches[i][0])))
    return vertices

#Début de l'algorithme
#Etape 1 : Définition des variables

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
dictionnary, dictionnariesReduced = getDictionnaries(filePath = os.path.join(__location__, 'liste_francais.txt'))

matrix: List[List[int]] = [
    [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0]
]


print('''
Les lettres du graphe doivent être rentrées dans le format suivant :

    - Les lettres sont rentrées de gauche à droite, en suivant la numérotation du graphe
    - Si la lettre ne contient aucun bonus, on écrit simplement la lettre, par exemple : A
    - Si la lettre contient un bonus de multiplication de lettre, on écrit le multiplicateur une fois suivi de la lettre, par exemple : 3A
    - Si la lettre contient un bonus de multiplication de mot, on écrit deux fois le multiplicateur suivi de la lettre, par exemple : 22A
    - Possibilité ou non de mettre un espace entre les cases

    Exemple : e p n 3i 22e 33a e r h 2a t 22v 2e s e 3o ou epn3i22e33aerh2at22v2ese3o
''')
lettersInGame = input('Rentrez les lettres du graphe : ').upper().replace(' ', '') #L'entrée de l'utilisateur, mis en majuscule
start = time.time()
graph = Graph(vertices = createVerticesFromString(string = lettersInGame), matrix = matrix)


#Etape 2 : On parcourt le graphe

winningBranchs: List[Branch] = [] # Contiendra les branches 'gagnantes', c'est-à-dire qui correspondent à un mot
for vertexOrigin in graph.vertices:
    branchsQueue: List[Branch] = [Branch(path = [vertexOrigin], graph = graph)]

    while len(branchsQueue) > 0:
        branchToTreat = branchsQueue.pop(0) 
        #C'est dans la ligne suivante que la magie s'opère
        #Puisqu'on supprime les branches qui, même étendues autant de fois que l'on souhaite, ne peuvent pas former de mot valide
        branchToTreatDuplicates = [branch for branch in branchToTreat.duplicate() if len(branch.path) > 0 and filterIfStringIsStartOfWord(string = branch.getWord(), sortedReducedDictionnary = dictionnariesReduced)]
        branchsQueue = branchsQueue + branchToTreatDuplicates
        if binarySearch(element = branchToTreat.getWord(), sortedList = dictionnary) != None: #C'est un mot valide !
            try:
                branchIndex = [branch.getWord() for branch in winningBranchs].index(branchToTreat.getWord()) #Ne gérère pas d'erreur si le mot est dans le tableau
                if winningBranchs[branchIndex].getScore() < branchToTreat.getScore(): #On a trouvé une autre façon de faire un mot déjà trouvé mais qui rapporte plus de point
                    winningBranchs[branchIndex] = branchToTreat
            except ValueError: #Le mot n'est pas dans le tableau, on le rajoute
                winningBranchs.append(branchToTreat)

#Plus qu'à trier pour faire apparaître les gros scores en premier
winningBranchs.sort(key = lambda branch : branch.getScore(), reverse = True)
end = time.time()
print(end - start)
print([[branch.getWord(), branch.getScore()] for branch in winningBranchs])

