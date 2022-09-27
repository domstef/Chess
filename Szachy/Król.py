
from Szachy.Bierka import BierkaC
from Szachy.Ruch import RuchC

class KrolC(BierkaC):
    """
    Klasa KrolC przechowująca wszystkie informacje o królu, dziedziczy po abstrakcyjnej klasie Bierka \n
    """
    def get_rank(self):
        return 'K'

    def getKingMoves(self, r, c, moves, board, whiteToMove, currentCastlinRight):
        """
        Metoda zwracajaca wszystkie możliwe ruchy króla \n
        :param r: wiersz ruchu
        :param c: kolumna ruchu
        :param moves: kontener (tupla) przechowująca możliwe ruchy
        :param board: szachownica trwajacej gry
        :param whiteToMove: booolean mówiący, czy jest ruch
        :return: wszystkie możliwe ruchy króla
        """
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = 'w' if whiteToMove else 'b'
        for i in range(8):
            end_row = r + directions[i][0]
            end_col = c + directions[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = board[end_row][end_col]
                if end_piece[0] != allyColor:  # empty or enemy
                    moves.append(RuchC((r, c), (end_row, end_col), board))

        return moves

    def getCastleMoves(self, r, c, moves,  whiteToMove, currentCastlinRight, board):
        """
        Generuje wszystkie możliwe ruchy króla w przypadku roszady \n
        :param board: szachownica trwajacej gry
        :param currentCastlinRight: tupla z zasadami roszady i informacją które są spełnione a które nie
        :param whiteToMove: boolean okreslający czyj jest ruch
        :param r: wiersz ruchu
        :param c: kolumna ruchu
        :param moves: tupla z możliwymi ruchami
        :return: wszystkie możliwe ruchy w przypadku roszady
        """


        if (whiteToMove and currentCastlinRight.white_king_side) or (not whiteToMove and currentCastlinRight.black_king_side):
            moves = self.getKingSideCastleMoves(r, c, moves,  board)
        if (whiteToMove and currentCastlinRight.white_queen_side) or (not whiteToMove and currentCastlinRight.black_queen_side):
            moves = self.getQueenSideCastleMoves(r, c, moves,  board)
        return moves

    def getKingSideCastleMoves(self, r, c, moves,  board):
        """
        Generuje wszystkie możliwe ruchy króla w przypadku roszady krótkiej \n
        :param r: wiersz ruchu
        :param c: kolumna ruchu
        :param moves: tupla z możliwymi ruchami
        :return: wszystkie możliwe ruchy w przypadku roszady krótkiej
        """
        if board[r][c+1] == "--" and board[r][c+2] == "--":
             moves.append(RuchC((r, c), (r, c + 2), board, isCastleMove=True))
        return moves


    def getQueenSideCastleMoves(self, r, c, moves,  board):
        """
        Generuje wszystkie możliwe ruchy króla w przypadku roszady długiej \n
        :param r: wiersz ruchu
        :param c: kolumna ruchu
        :param moves: tupla z możliwymi ruchami
        :return: wszystkie możliwe ruchy w przypadku roszady długiej
        """
        if board[r][c - 1] == "--" and board[r][c - 2] == "--" and board[r][c-3]:
            moves.append(RuchC((r, c), (r, c - 2), board, isCastleMove=True))
        return moves