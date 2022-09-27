from Plansza import Szachownica
from Szachy import Ruch
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}




def main():
    """
    Główna funkcja programu \n
    :return: void
    """
    p.init()
    p.display.set_caption("Szachy")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Szachownica.Szachownica()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    squareSelected = ()
    playerClicks = []
    flag = showStartGame(screen)
    while running and flag:
        for o in p.event.get():
            if o.type == p.QUIT:
                running = False
            elif o.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if squareSelected == (row, col):
                    squareSelected = ()
                    playerClicks = []
                else:
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected)
                if len(playerClicks) == 2:  # after choosing piece to move, we click to move
                    move = Ruch.RuchC(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            squareSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [squareSelected]

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs, validMoves, squareSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Checkmate! Black wins!')
            else:
                drawText(screen, 'Checkmate! White wins!')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate!')
        clock.tick(MAX_FPS)
        p.display.flip()


def showStartGame(screen):
    """
    Metoda wyświetlająca ekran początkowy gry \n
    :param screen: ekran istniejacej gry
    :return: void
    """

    flag = True
    while flag:

        for o in p.event.get():
            if o.type == p.KEYDOWN:
                flag = False
                return True
            elif o.type == p.QUIT:
                flag = False
                return False


        screen.fill((235, 235, 208))
        font = p.font.SysFont('arial', 60)
        line = font.render(f"SZACHY", True, (119, 148, 85))
        screen.blit(line, (150, 100))



        font = p.font.SysFont('arial', 20)
        line2 = font.render(f"Celem gry jest doprowadzenie do mata (zbicia króla przeciwnika)", True, (119, 148, 85))
        line3 = font.render(f"więcej zasad można znaleźć : ", True, (119, 148, 85))
        line5 = font.render(f"pzsshach.pl", True, (119, 148, 85))
        line6 = font.render(f"Naciśnij dowolny klawisz aby kontynuować", True, (119, 148, 85))

        screen.blit(line6, (50, 200))
        screen.blit(line2, (30, 300))
        screen.blit(line3, (50, 350))
        screen.blit(line5, (50, 400))
        p.display.flip()




def loadImages():
    """
    Metoda przechowujaca grafiki reprezentujące bierki \n
    """
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK",
              "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def highlightSquares(screen, gs, validMoves, sqSelected):
    """
    Metoda podświetlajaca kwadrat \n
    :param screen: powierzchnia gry z biblioteki pygame
    :param gs: obiekt klasy szachownica
    :param validMoves: wszystkie dostępne ruchy, które mogą być wykonane
    :param sqSelected: kwadrat, który gracz wybrał
    :return: void
    """
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value
            s.fill(p.Color('red'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('green'))
            for move in validMoves:

                if move.startRow == r and move.startCol == c:

                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

def drawText(screen, text):
    """
    Metoda wyświetlajaca tekst \n
    :param screen: okno istniejącej gry
    :param text: tekst do wyświetlenia
    :return: void
    """
    font = p.font.SysFont('arial', 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)


def drawGameState(screen, gs, validMoves, sqSelected):
    """
    Metoda rysujaca aktualny stan gry w oknie gry \n
    :param validMoves: wszystkie możliwe do wykonania  ruchy w grze
    :param sqSelected: kwadrat wybrany przez gracza
    :param screen: okno istniejącej gry
    :param gs: obiekt klasy szachownica
    :return: void
    """
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    """
    Metoda rysująca szachownicę \n
    :param screen: powierzchnia na której odbywa się gra
    :return: void
    """
    colors = [p.Color((235, 235, 208)), p.Color((119, 148, 85))]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    """
    Metoda do rysowania elementów na szachownicy \n
    :param screen: powierzchnia na której odbywa się gra
    :param board: szachownica na której odbywa się gra
    :return: void
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    p.init()
    main()
