from Szachy.Ruch import RuchC
from Szachy.Bierka import BierkaC


class PionekC(BierkaC):
    """
    Klasa PionekC która dziedziczy po abstarkcyjnej klasie Bierka i przechowująca informacje o pionku \n
    """
    def get_rank(self):
        """
        \n
        :return:typ pionka
        """
        return 'P'

    def getPawnMoves(self, r, c, moves, board, whiteToMove, enpassantPossible):
        """
        Metoda zwracająca wszystkie możliwe ruchy pionka \n
        :param enpassantPossible:  boolean mówiący czy w ruchu zachodzi enpassant
        :param r: wiersz ruchu
        :param c: kolumna ruchu
        :param moves: kontener (tupla) przechowująca możliwe ruchy
        :param board: szachownica trwajacej gry
        :param whiteToMove: booolean mówiący, czy jest ruch
        :return: wszystkie możliwe ruchy pionka
        """
        if whiteToMove:
            if board[r - 1][c] == "--":
                moves.append(RuchC((r, c), (r - 1, c), board))
                if r == 6 and board[r - 2][c] == "--":
                    moves.append(RuchC((r, c), (r - 2, c), board))
            if c - 1 >= 0:  # to be on the board
                if board[r - 1][c - 1][0] == 'b':
                    moves.append(RuchC((r, c), (r - 1, c - 1), board))
                elif (r - 1, c - 1) == enpassantPossible:
                    moves.append(RuchC((r, c), (r - 1, c - 1), board, enpassantPossible=True))
            if c + 1 <= len(board) - 1:
                if board[r - 1][c + 1][0] == 'b':
                    moves.append(RuchC((r, c), (r - 1, c + 1), board))
                elif (r - 1, c + 1) == enpassantPossible:
                    moves.append(RuchC((r, c), (r - 1, c + 1), board, enpassantPossible=True))
        else:
            if board[r + 1][c] == "--":
                moves.append(RuchC((r, c), (r + 1, c), board))
                if r == 1 and board[r + 1][c] == "--":
                    moves.append(RuchC((r, c), (r + 2, c), board))
            if c - 1 >= 0:  # to be on the board

                if board[r + 1][c - 1][0] == 'w':
                    moves.append(RuchC((r, c), (r + 1, c - 1), board))
                elif (r + 1, c - 1) == enpassantPossible:
                    moves.append(RuchC((r, c), (r + 1, c - 1), board, enpassantPossible=True))
            if c + 1 <= len(board) - 1:

                if board[r + 1][c + 1][0] == 'w':
                    moves.append(RuchC((r, c), (r + 1, c + 1), board))
                elif (r + 1, c + 1) == enpassantPossible:
                    moves.append(RuchC((r, c), (r + 1, c + 1), board, enpassantPossible=True))

        return moves

