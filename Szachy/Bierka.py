
# ABSTRACT CLASS
from abc import ABC, abstractmethod



class BierkaC(ABC):
    """
    Klasa abstrakcyjna  BierkaC \n
    """
    def __init__(self, r, c):
        """
        Konstruktor klasy \n
        :param r: badany wiersz
        :param c: badana kolumna
        """
        self.rank = '1'

    @abstractmethod
    def get_rank(self):
        pass






