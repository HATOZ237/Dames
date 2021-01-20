
from damier import *
import math

class Damier_py(Damier):

    def __init__(self, couleur: str, nbrecase: int):
        
        Damier.__init__(self, couleur, nbrecase)
        
        self.caseSize = 90

        self.size = int(math.sqrt(self.nbreCase)) * self.caseSize

        self.backgroundFen = 203, 155, 128

        self.screen = pygame.display.set_mode((self.size, self.size))
        self.screen.fill(self.backgroundFen)
        pygame.display.set_caption("Dames")

        y = 0
        line = 0

        while y < self.size:
            if line % 2 != 0:
                x = 90
            else:
                x = 0
            while x < self.size:
                pygame.draw.rect(screen, (80, 80, 80), (x, y, self.caseSize, self.caseSize))
                x = x + (self.caseSize * 2)
            y = y + self.caseSize
            line = line + 1