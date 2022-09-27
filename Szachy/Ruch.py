class RuchC:
    """
    Klasa przechowująca wszystkie informcje dotyczące ruchów w grze \n
    """
    rankToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRank = {v: k for k, v in rankToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}

    colsToFiles = {v: k for k, v in filesToCols.items()}

    rankToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}

    def __init__(self, startSq, endSq, board, enpassantPossible=False, isCastleMove = False):
        """
        Konstruktor badanej klasy \n
        :param startSq: koordynaty kwadratu, od którego zaczynamy ruch (tuple)
        :param endSq: koordynaty kwadratu, na którym kończymy ruch (tuple)
        :param board: szachownica istniejącej gry
        :param enpassantPossible parametr opcjonalny do przeprowadzenia enpassant
        """
        self.board = board
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)

        self.isEnpassantMove = enpassantPossible
        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'
        self.isCastleMove = isCastleMove
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        """
        Metoda nadpisujaca moveID \n
        :param other: ruch do nadpisania
        :return: boolean czy ruchy są identyczne (sprawdzane w instrukcji warunkowej poniżej)
        """
        if isinstance(other, RuchC):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        """
        Metoda pomocnicza zwracająca ruch w notacji szachowej \n
        :return: ruch w notacji szachowej
        """
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        """
        Metoda zwracajaca koordynaty konketnego kwadratu szachownicy \n
        :param r: wiersz opisujacy kwadrat
        :param c: kolumna opisująca kwadrat
        :return: opis ruchu w notacji szachowej
        """
        return self.colsToFiles[c] + self.rowsToRank[r]

