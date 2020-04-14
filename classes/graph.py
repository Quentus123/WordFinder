from typing import List
from .vertex import Vertex

class Graph:

    def __init__(self, vertices: [Vertex], matrix: List[List[int]]):
        self.vertices = vertices
        self.matrix = matrix

    def getSideVerticesForVertex(self, vertex: Vertex) -> List[Vertex]:
        '''
        Renvoie tous les sommets atteignables à partir du sommet donné en entrée
        '''
        verticesReturn: List[Vertex] = []
        line = self.matrix[vertex.id]
        for i in range(0, len(line)):
            #Si c'est 1 alors il y a une arête
            if (line[i] == 1):
                verticesReturn.append(self.vertices[i])
        
        return verticesReturn
