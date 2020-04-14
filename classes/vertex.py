class Vertex:

    lettersValues = {
    'A': 1, 'B': 4, 'C': 2, 'D': 3, 'E': 1, 'F': 4,
    'G': 4, 'H': 4, 'I': 1, 'J': 8, 'K': 10, 'L': 2,
    'M': 2, 'N': 1, 'O': 1, 'P': 3, 'Q': 6, 'R': 1,
    'S': 1, 'T': 1, 'U': 2, 'V': 4, 'W': 10, 'X': 8,
    'Y': 6, 'Z': 4
    }


    def __init__(self, id: int, letter: str, letterMultiplier: int = 1, wordMultiplier: int = 1):
        self.id = id
        self.letter = letter
        self.letterMultiplier = letterMultiplier
        self.wordMultiplier = wordMultiplier

    def getScore(self):
        '''
        Renvoie le score associé à ce sommet, en prenant en compte le multiplicateur 2L ou 3L
        '''
        return Vertex.lettersValues[self.letter]*self.letterMultiplier