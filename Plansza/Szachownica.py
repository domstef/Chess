
from Szachy.Goniec import GoniecC
from Szachy.Król import KrolC
from Szachy.Królowa import KrolowaC
from Szachy.Pionek import PionekC
from Szachy.Skoczek import Knight
from Szachy.Wieża import WiezaC


class Szachownica:
    """
    Główna klasa programu, która przechowuje informacje o grze \n
    """

    def __init__(self):
        """
        Konstruktor klasy \n
        Plansza jest listą wymiaru 8x8 i każdy element listy ma dwa znaki \n
        Pierwszy znak posiada informację o kolorze pionka: "w" albo "b" \n
        Drugi znak jest informacją o typie pionka \n
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()  # coordinates where en passant capture is possible
        self.currentCastlingRight = CasteRights(True, True, True, True)
        self.castleRightLog = [CasteRights(self.currentCastlingRight.white_king_side, self.currentCastlingRight.black_king_side,
                                           self.currentCastlingRight.white_queen_side, self.currentCastlingRight.black_queen_side)]

    def makeMove(self, move):
        """
        Pobiera ruch jako parametr i wykonuje go \n
        :param move: coordinates of the move
        :return: void
        """

        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"

        if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.enpassantPossible = ()  # reset
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # KSC
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'
        self.updateCasteRights(move)
        self.castleRightLog.append(CasteRights(self.currentCastlingRight.white_king_side, self.currentCastlingRight.black_king_side,
                                               self.currentCastlingRight.white_queen_side, self.currentCastlingRight.black_queen_side))

    def undoMove(self):
        """
        Metoda pomocnicza do sprawdzania szacha i mata \n
        Cofa wykonany ruch \n
        Zagnieżdżona instrukcja if aktualizyje pozycję króla \n
        """
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo the enpasantmove
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            # undo 2 square pawn advance
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

    def updateCasteRights(self, move):
        """
        Metoda aktualizujaca spełnione zasady roszady \n
        :param move: tupla z ruchami możliwymi do wykonania
        :return: void
        """
        if move.pieceMoved =='wK':
            self.currentCastlingRight.white_queen_side = False
            self.currentCastlingRight.white_king_side = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.black_king_side = False
            self.currentCastlingRight.black_queen_side = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: # LEFT R
                    self.currentCastlingRight.white_queen_side = False
                elif move.startCol == 7:
                    self.currentCastlingRight.white_king_side = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # LEFT R
                    self.currentCastlingRight.black_queen_side = False
                elif move.startCol == 7:
                    self.currentCastlingRight.black_king_side = False

    def getValidMoves(self):
        """
        Metoda zwracajaca wszystkie ruchy analizując szacha \n
        Iteracja przebiega odwrotnie niż naturalnie, aby nie napotkac problemu z indeksowaniem \n
        :return: wszystkie możliwe ruchy
        """
        tempEnpassantPossible = self.enpassantPossible
        tempCasteRight = CasteRights(self.currentCastlingRight.white_king_side,
                                     self.currentCastlingRight.black_king_side,
                                     self.currentCastlingRight.white_queen_side,
                                     self.currentCastlingRight.black_queen_side)
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            piece = KrolC(self.whiteKingLocation[0], self.whiteKingLocation[1])
            moves = piece.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves, self.whiteToMove,
                                         self.currentCastlingRight, self.board)
        else:
            piece = KrolC(self.whiteKingLocation[0], self.whiteKingLocation[1])
            moves = piece.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves, self.whiteToMove,
                                         self.currentCastlingRight,  self.board)

        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])  # this function switches the players so we need to undo it
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():

                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        # Checkmate or stalemate
        if len(moves) == 0:

            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCasteRight
        return moves

    def inCheck(self):
        """
        Metoda sprawdzajaca czy aktualny gracz jest w szachu \n
        :return: boolean zwracajacy czy jest szach
        """
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        """
        Metoda zwracajaca informację, czy przeciwnik może zaatakować kwadrat o podanych koordynatach \n
        Metoda ta zamienia gracza który ma teraz runde i na jego podstawie analizuje sytuacę na szachownicy \n
        :param r: wiersz badanego kwadratu
        :param c: kolumna badanego kwadratu
        :return: boolean czy kwadrat jest zaatakowany
        """
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        """
        metoda zwraca wszystkie możliwe ruchy ale bez analizowania sytuacji gdy mamy szach \n
        :return: wszystkie możliwe ruchy
        """
        moves = []  # empty list of moves
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]  # black or white
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):

                    if self.board[r][c][1] == 'P':
                        piece = PionekC(r, c)
                        moves = piece.getPawnMoves(r, c, moves, self.board, self.whiteToMove, self.enpassantPossible)
                    elif self.board[r][c][1] == 'R':
                        piece = WiezaC(r, c)
                        moves = (piece.getRookMoves(r, c, moves, self.board, self.whiteToMove))
                    elif self.board[r][c][1] == 'Q':
                        piece = KrolowaC(r, c)
                        moves = (piece.getQueenMoves(r, c, moves, self.board, self.whiteToMove))
                    elif self.board[r][c][1] == 'K':
                        piece = KrolC(r, c)
                        moves = (piece.getKingMoves(r, c, moves, self.board, self.whiteToMove, self.currentCastlingRight))
                    elif self.board[r][c][1] == 'N':
                        piece = Knight(r, c)
                        moves = (piece.getKnightMoves(r, c, moves, self.board, self.whiteToMove))
                    else:
                        piece = GoniecC(r, c)
                        moves = (piece.getBishopMoves(r, c, moves, self.board, self.whiteToMove))
        return moves


class CasteRights:
    """
    Klasa pomocnicza do przechowywania informacji o zasadach roszady \n
    """
    def __init__(self, wks, bks, wqs, bqs):
        """
        Konstruktor klasy \n
        :param wks: Zasada dotycząca krótkiej roszady białych pionków
        :param bks: Zasada dotycząca krótkiej roszady czarnych pionków
        :param wqs: Zasada dotycząca długiej roszady białych pionków
        :param bqs: Zasada dotycząca długiej roszady czarnych pionków
        """
        self.white_king_side = wks
        self.black_king_side = bks
        self.white_queen_side = wqs
        self.black_queen_side = bqs


