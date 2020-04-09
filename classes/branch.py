import numpy as np
from typing import List
from .graph import Graph
from .vertex import Vertex

class Branch:

    lenBonuses = {
        '1': 1,
        '2': 3,
        '3': 4,
        '4': 6,
        '5': 9,
        '6': 11,
        '7': 16,
        '8': 17,
        '9': 25
    }

    def __init__(self, path: List[Vertex], graph: Graph):
        self.path = path
        self.graph = graph

    #Renvoie une liste de nouvelles branches qui sont une expansion possible de celle-ci
    def duplicate(self):
        '''
        Renvoie une liste de branches qui sont des extensions de celle-ci
        '''
        lastVertex = self.path[len(self.path) - 1]
        possiblesVertices: List[str] = self.graph.getSideVerticesForVertex(vertex = lastVertex)
        return [Branch(self.path + [possibleVertex], self.graph) for possibleVertex in possiblesVertices]

    def getScore(self):
        '''
        Renvoie le score que rapporte le mot s'il est est joué
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
