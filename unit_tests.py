import unittest
import numpy as np
import string
import re
from typing import List

from classes.graph import Graph
from classes.vertex import Vertex
from classes.branch import Branch


class GraphTests(unittest.TestCase):

    def setUp(self):
        line_a = [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        line_b = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        line_c = [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        line_d = [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        line_e = [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        line_f = [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0]
        line_g = [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0]
        line_h = [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        line_i = [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]
        line_j = [0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]
        line_k = [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1]
        line_l = [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1]
        line_m = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0]
        line_n = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0]
        line_o = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]
        line_p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0]
        matrix = [line_a, line_b, line_c, line_d, line_e, line_f, line_g, line_h,
                  line_i, line_j, line_k, line_l, line_m, line_n, line_o, line_p]


        lettersInGame = '33GHEP2DS33TA3MLQKI2OL22E'
        inputRegex = r'[2-3]{0,2}[A-Z]{1}'
        matches = re.findall(inputRegex, lettersInGame)
        print(matches)
        vertices: List[Vertex] = []
        for i in range(0, 16):
            if(len(matches[i]) == 1): # aucun multiplicateur
                vertices.append(Vertex(id = i, letter = matches[i]))
            elif(len(matches[i]) == 2): # multiplicateur de lettre
                vertices.append(Vertex(id = i, letter = matches[i][1], letterMultiplier = int(matches[i][0])))
            else: # len vaut 3 donc il y a un multiplicateur de mot
                vertices.append(Vertex(id = i, letter = matches[i][2], wordMultiplier = int(matches[i][0])))
        self.graph = Graph(vertices = vertices, matrix = matrix)

    def test_sides_vertices_with_vertex_1(self):
        # Arrange
        vertexToTest = Vertex(id = 0, letter = '') #Seul l'id nous intéresse

        # Act
        result = [vertex.id for vertex in self.graph.getSideVerticesForVertex(vertex = vertexToTest)]

        # Assert
        expected = [1, 4, 5]
        assert(result == expected)

    def test_sides_vertices_with_letter_15(self):
        # Arrange
        vertexToTest = Vertex(id = 15, letter = '') #Seul l'id nous intéresse

        # Act
        result = [vertex.id for vertex in self.graph.getSideVerticesForVertex(vertex = vertexToTest)]

        # Assert
        expected = [10, 11, 14]
        assert(result == expected)

    def test_sides_vertices_with_letter_5(self):
        # Arrange
        vertexToTest = Vertex(id = 5, letter = '') #Seul l'id nous intéresse

        # Act
        result = [vertex.id for vertex in self.graph.getSideVerticesForVertex(vertex = vertexToTest)]

        # Assert
        expected = [0, 1, 2, 4, 6, 8, 9, 10]
        assert(result == expected)

    def test_word_with_ED(self):
        #Arrange
        vertex1 = self.graph.vertices[2]
        vertex2 = self.graph.vertices[4]
        branch = Branch([vertex1, vertex2], self.graph)

        #Act
        result = branch.getWord()
        print('RESULT' + result)

        #Assert
        expected = 'ED'
        assert(result == expected)

    def test_word_with_PYTHON(self):
        #Arrange
        vertex1 = Vertex(0, 'P')
        vertex2 = Vertex(0, 'Y')
        vertex3 = Vertex(0, 'T')
        vertex4 = Vertex(0, 'H')
        vertex5 = Vertex(0, 'O')
        vertex6 = Vertex(0, 'N')
        branch = Branch([vertex1, vertex2, vertex3, vertex4, vertex5, vertex6], self.graph)

        #Act
        result = branch.getWord()

        #Assert
        expected = 'PYTHON'
        assert(result == expected)

    def test_word_score_with_GDEIK(self):
        #Arrange
        verticesToTest = [self.graph.vertices[0], self.graph.vertices[4], self.graph.vertices[15], self.graph.vertices[12], self.graph.vertices[11]] #Irréaliste évidemment
        branchToTest = Branch(path = verticesToTest, graph = self.graph)

        #Act
        result = branchToTest.getScore()

        #Assert
        expected = 141
        assert(result == expected)


if __name__ == '__main__':
    unittest.main()
