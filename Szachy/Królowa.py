from Szachy.Ruch import RuchC
from Szachy.Bierka import BierkaC


class KrolowaC(BierkaC):
    """
    Klasa KrolowaC przechowująca wszystkie informacje o Królowej \n
    """
    def get_rank(self):
        return 'Q'

    def getQueenMoves(self, r, c, moves, board, whiteToMove):
        """
        Metoda zwracająca wszystkie możliwe ruchy królowej \n
        :param r: wiersz ruchu
        :param c: kolumna ruchu
        :param moves: kontener (tupla) przechowująca możliwe ruchy
        :param board: szachownica trwajacej gry
        :param whiteToMove: booolean mówiący, czy jest ruch
        :return: wszystkie możliwe ruchy królowej
        """
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = 'b' if whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(RuchC((r, c), (end_row, end_col), board))
                    elif end_piece[0] == enemyColor:
                        moves.append((RuchC((r, c), (end_row, end_col), board)))
                        break
                    else:
                        break
                else:
                    break
        return moves

