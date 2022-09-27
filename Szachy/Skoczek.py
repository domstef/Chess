from Szachy.Ruch import RuchC
from Szachy.Bierka import BierkaC


class Knight(BierkaC):
    """
    Klasa która przechowuje informacje o skoczku, dziedziczy po abstrakcyjnej klasie Bierka \n
    """
    def get_rank(self):
        return 'N'

    def getKnightMoves(self, r, c, moves, board, whiteToMove):
        """
        Metoda zwracająca wszystkie możliwe ruchy skoczka \n
        :param r: wiersz ruchu
        :param c: kolumna ruchu
        :param moves: kontener przechowujacy wszystkie możliwe ruchy
        :param board: szachownica istniejacej gry
        :param whiteToMove: boolean określajacy czyj jest ruch
        :return: wszystkie możliwe ruchy skoczka
        """
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (2, -1), (2, 1), (1, 2), (1, -2))

        allyColor = 'w' if whiteToMove else 'b'

        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0]
                end_col = c + d[1]
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = board[end_row][end_col]
                    if end_piece[0] != allyColor:  # albo puste albo wrog
                        moves.append(RuchC((r, c), (end_row, end_col), board))

        return moves
