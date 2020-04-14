import numpy as np
from typing import List
from typing import Tuple
from classes.graph import Graph
from classes.branch import Branch
from classes.vertex import Vertex
import os
import sys
import re

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
words_filename = 'liste_francais.txt'

def rechercheDichotomique( element: str, sortedList: List[str]) -> int:
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



# On crée le tableau de mots
words_array: List[str] = []
with open(os.path.join(__location__, words_filename)) as txt_file: 
    for line in txt_file:
      if len(line[:-1]) >= 10:
            continue
      words_array.append(line.upper()[:-1])

words_array_reduced = {
    '1': [word[:1] for word in words_array],
    '2': [word[:2] for word in words_array],
    '3': [word[:3] for word in words_array],
    '4': [word[:4] for word in words_array],
    '5': [word[:5] for word in words_array],
    '6': [word[:6] for word in words_array],
    '7': [word[:7] for word in words_array],
    '8': [word[:8] for word in words_array],
    '9': [word[:9] for word in words_array],
    '10': [word[:10] for word in words_array],
    '11': [word[:11] for word in words_array],
    '12': [word[:12] for word in words_array],
    '13': [word[:13] for word in words_array],
    '14': [word[:14] for word in words_array],
    '15': [word[:15] for word in words_array],
    '16': [word[:16] for word in words_array]
}

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



lettersInGame = '33GHEP2DS33TA3MLQKI2OL22E'
lettersInGame = sys.argv[1]
inputRegex = r'[2-3]{0,2}[A-Z]{1}'
matches = re.findall(inputRegex, lettersInGame)
vertices: List[Vertex] = []
for i in range(0, 16):
    if(len(matches[i]) == 1): # aucun multiplicateur
        vertices.append(Vertex(id = i, letter = matches[i]))
    elif(len(matches[i]) == 2): # multiplicateur de lettre
        vertices.append(Vertex(id = i, letter = matches[i][1], letterMultiplier = int(matches[i][0])))
    else: # len vaut 3 donc il y a un multiplicateur de mot
        vertices.append(Vertex(id = i, letter = matches[i][2], wordMultiplier = int(matches[i][0])))
graph = Graph(vertices = vertices, matrix = matrix)

winningBranchs: List[Branch] = [] # Contiendra les branches 'gagnantes'
for vertexOrigin in graph.vertices:
    branchsQueue: List[Branch] = [Branch(path = [vertexOrigin], graph = graph)]

    while len(branchsQueue) > 0:
        branchToTreat = branchsQueue.pop(0) 
        branchToTreatDuplicates = list(filter(lambda branch : rechercheDichotomique(element = branch.getWord(), sortedList = words_array_reduced[str(len(branch.getWord()))]) != None, branchToTreat.duplicate()))
        branchsQueue = branchsQueue + list(filter(lambda branch : len(branch.path) > 0, branchToTreatDuplicates))
        if rechercheDichotomique(element = branchToTreat.getWord(), sortedList = words_array) != None: #C'est un mot valide !
            try:
                branchIndex = [branch.getWord() for branch in winningBranchs].index(branchToTreat.getWord()) #Ne gérère pas d'erreur si le mot est dans le tableau
                if winningBranchs[branchIndex].getScore() < branchToTreat.getScore(): #On a trouvé une autre façon de faire un mot déjà trouvé mais qui rapporte plus de point
                    winningBranchs[branchIndex] = branchToTreat
            except ValueError: #Le mot n'est pas dans le tableau, on le rajoute
                winningBranchs.append(branchToTreat)

winningBranchs.sort(key = lambda branch : branch.getScore(), reverse = True)
print([[vertex.id for vertex in branch.path] for branch in winningBranchs])
sys.stdout.flush() #API js