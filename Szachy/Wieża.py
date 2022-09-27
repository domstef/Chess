from Szachy.Ruch import RuchC
from Szachy.Bierka import BierkaC


class WiezaC(BierkaC):
    """

    Klasa WiezaC przechowujaca wszystkie informacje o Wieży, dziedziczy po abstrakcyjnej klasie Bierka

    """
    def get_rank(self):
        return 'R'

    @staticmethod
    def getRookMoves(r, c, moves, board, whiteToMove):
        """
        Metoda zwracająca wszystkie możliwe ruchy wieży

        :param r: wiersz w ruchu
        :param c: kolumna w ruchu
        :param moves: ruchy które wykonujemy wieżą
        :param board: szachownica istniejącej gry
        :param whiteToMove: boolean określający czyj jest ruch
        :return: wszystkie możliwe ruchy wieży
        """
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
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
