from typing import List
from .graph import Graph
from .vertex import Vertex

class Branch:

    #lenBonuses contient les bonus de score accordés en fonction de la longueur d'un mot
    lenBonuses = {
        '1': 1, '2': 3, '3': 4,
        '4': 6, '5': 9, '6': 11,
        '7': 16, '8': 17, '9': 25
    }

    def __init__(self, path: List[Vertex], graph: Graph):
        self.path = path
        self.graph = graph

    def duplicate(self):
        '''
        Renvoie une liste de branches qui sont des extensions de celle-ci.
        On prend en compte le fait que les chemins doivent être élémentaires.
        '''
        lastVertex = self.path[len(self.path) - 1]
        possiblesVertices: List[str] = self.graph.getSideVerticesForVertex(vertex = lastVertex)
        return [Branch(self.path + [possibleVertex], self.graph) for possibleVertex in possiblesVertices if possibleVertex not in self.path]

    def getScore(self):
        '''
        Renvoie le score que rapporte le mot formé par la branche s'il est est joué
        '''
        score = 0
        wordMultiplier = 1
        for vertex in self.path:
            score += vertex.getScore()
            wordMultiplier *= vertex.wordMultiplier
        return score*wordMultiplier + Branch.lenBonuses.get(str(len(self.path)), 30)

    def getWord(self) -> str:
        '''
        Renvoie le mot correspondant à la branche
        '''
        return ''.join([vertex.letter for vertex in self.path])
