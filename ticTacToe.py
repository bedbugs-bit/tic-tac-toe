import pygame as pg
import sys

pg.init()  # initialize pyGame

''' Initialize rgb values for different colours '''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


''' Set game window width and title '''
gameWindow = pg.display.set_mode((750, 750), 0, 32)  # set window width
pg.display.set_caption('Tic-Tac-Toe')  # set window title


''' Function to initialize game - set it up for a new game '''


def initGame():
    global turn, statusMatrix, gameOver, quitted, winner  # global variables
    gameWindow.fill(BLACK)  # paint window to have a black background

    ''' Draw the 3x3 matrix for Tic-Tac-Toe '''
    pg.draw.line(gameWindow, WHITE, (300, 150),
                 (300, 600), 3)  # vertical line (left)
    pg.draw.line(gameWindow, WHITE, (450, 150),
                 (450, 600), 3)  # vertical line (right)
    pg.draw.line(gameWindow, WHITE, (150, 300),
                 (600, 300), 3)  # horizontal line (top)
    # horizontal line (bottom)
    pg.draw.line(gameWindow, WHITE, (150, 450), (600, 450), 3)

    ''' Display the title "TIC-TAC-TOE" within the game window screen '''
    FONT = pg.font.SysFont(None, 75, bold=True)  # set font styles
    text = FONT.render("TIC-TAC-TOE", True, RED)  # set text and font color
    gameWindow.blit(text, [200, 50])  # set font on the game window
    pg.display.update()  # update the game window with the changes

    ''' Initial Game State '''
    turn = 'O'  # initially, it is O's turn
    # a matrix to keep track of the filled positions
    statusMatrix = [['', '', ''], ['', '', ''], ['', '', '']]
    gameOver = False  # to check if game is over - X wins, O wins, or no one wins but all positions are filled
    quitted = False  # to check if the user has quitted the game
    winner = ''  # game outcome (X wins, O wins, or it is a draw)


''' To update the game window screen display and switch turns '''


def turnUpdate(turn, coordinates):
    if (turn == 'O'):  # if it was O's turn
        # update the block with a circle
        pg.draw.circle(gameWindow, RED, coordinates, 35, 5)
        return 'X'  # next turn: of X
    else:  # if it was X's turn
        # update the block with a rectangle
        coordinates = (coordinates[0]-20, coordinates[1]-20, 40, 40)
        pg.draw.rect(gameWindow, GREEN, coordinates, 5)
        return 'O'  # next turn: of O


''' To check the game status - is the game over, or can it still be continued? '''


def checkGameStatus(turn, xoMatrix, updatePos):
    # turn - the player who made the last move
    # xoMatrix - the matrix that is keeping track of the marked positions
    # updatePos - the position of the last move made - tuple (x,y) - where x = row index, y = column index
    ''' Diagonal Win '''
    if (updatePos[0] == updatePos[1]):  # move made at one of the principal diagonal positions
        # check if all the elements in the principal diagonal are the same
        if (xoMatrix[0][0] == xoMatrix[1][1] == xoMatrix[2][2]):
            # if all the elements in the principal diagonal are the same, draw a line marking the end of game with a win
            pg.draw.line(gameWindow, BLUE, (125, 125), (625, 625), 5)
            # True => gameOver; turn => player who played the last move
            return (True, turn + " Wins!")

    # move made at one of the positions on the other diagonal
    if (updatePos[0]+updatePos[1] == 2):
        # check if all the elements in the diagonal are the same
        if (xoMatrix[0][2] == xoMatrix[1][1] == xoMatrix[2][0]):
            # if all the elements in the principal diagonal are the same, draw a line marking the end of game with a win
            pg.draw.line(gameWindow, BLUE, (625, 125), (125, 625), 5)
            # True => gameOver; turn => player who played the last move
            return (True, turn + " Wins!")

    ''' Vertical Win '''  # column index remains same
    flag = True  # a flag that has been used to check status
    for i in range(0, 3):  # iterate over all elements of the column where the last move was made
        # if any of the elements in the column is not the same as the player who made the last move
        if (xoMatrix[updatePos[0]][i] != turn):
            flag = False  # it is not a verticle win
            break  # come out of the loop

    if flag:  # if flag is true, i.e., it is a vertical win
        # draw a line marking the end of game with a win
        pg.draw.line(gameWindow, BLUE, (125, 150 *
                     updatePos[0]+225), (625, 150*updatePos[0]+225), 5)
        # True => gameOver; turn => player who played the last move
        return (True, turn + " Wins!")

    ''' Horizontal Win '''  # row index remains same
    flag = True  # a flag that has been used to check status
    for i in range(0, 3):  # iterate over all elements of the row where the last move was made
        # if any of the elements in the row is not the same as the player who made the last move
        if (xoMatrix[i][updatePos[1]] != turn):
            flag = False  # it is not a horizontal win
            break  # come out of the loop

    if flag:  # if flag is true, i.e., it is a horizontal win
        # draw a line marking the end of game with a win
        pg.draw.line(
            gameWindow, BLUE, (150*updatePos[1]+225, 125), (150*updatePos[1]+225, 625), 5)
        # True => gameOver; turn => player who played the last move
        return (True, turn + " Wins!")

    ''' Matrix not Full '''
    for i in range(0, 3):  # iterate over rows
        for j in range(0, 3):  # iterate over columns
            # if an element in the status matrix is found to be empty, the game is not over
            if (xoMatrix[i][j] == ''):
                # False => game not over, can still be continued; '' => no conclusion/ result of the game
                return (False, '')

    ''' No Win, but Matrix Full '''
    return (True, " Draw! ")  # True => gameOver; Draw, since no one won as per the above conditions!


initGame()  # initialize the game on program run by calling the method - on running the file for the first time


''' Keep the game window open until the user does not opt to close it '''
while not quitted:

    # get all the events on the pyGame window
    for event in pg.event.get():
        # if the user clicks the close button or presses the escape key
        if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            quitted = True  # quit the game
        elif (event.type == pg.KEYDOWN) and (event.key == pg.K_KP_ENTER or event.key == pg.KSCAN_KP_ENTER or event.key == pg.K_RETURN or event.key == pg.KSCAN_RETURN):  # if the user presses the enter key
            initGame()  # replay the game (First Step: take the game state to the initial state)

    # until gameOver is false, i.e., the game can be continued
    while not gameOver:
        ''' Get all events on the game window '''
        for event in pg.event.get():
            # if the user clicks the cross button on the window, end the game and close the window
            if (event.type == pg.QUIT):
                pg.quit()
                sys.exit(0)

            # if the user clicks on the screen, get the mouse position and do the markings/ proceed with the game accordingly
            if (event.type == pg.MOUSEBUTTONDOWN):
                # get position (coordinates) of the mouse click. It is a tuple with the coordinates in the form of a tuple (x,y)
                mousePosition = event.pos

                ''' Get coordinates to mark/ position to update according to the location of mouseclick '''
                if (mousePosition[0] > 150 and mousePosition[0] < 300):  # mouse in first column
                    # mouse in the first row (of the first column) - position (0,0)
                    if (mousePosition[1] > 150 and mousePosition[1] < 300):
                        # used for drawing rectangle/ circle according to the turn
                        coordinates = (225, 225)
                        # used to check if the position is already occupied, and to update it if not
                        updatePos = (0, 0)
                    # mouse in the second row (of the first column) - position (1,0)
                    elif (mousePosition[1] > 300 and mousePosition[1] < 450):
                        # used for drawing rectangle/ circle according to the turn
                        coordinates = (225, 375)
                        # used to check if the position is already occupied, and to update it if not
                        updatePos = (1, 0)
                    # mouse in the third row (of the first column) - position (2,0)
                    elif (mousePosition[1] > 450 and mousePosition[1] < 600):
                        # used for drawing rectangle/ circle according to the turn
                        coordinates = (225, 525)
                        # used to check if the position is already occupied, and to update it if not
                        updatePos = (2, 0)

                # mouse in second column
                elif (mousePosition[0] > 300 and mousePosition[0] < 450):
                    # mouse in the first row (of the second column) - position (0,1)
                    if (mousePosition[1] > 150 and mousePosition[1] < 300):
                        # used for drawing rectangle/ circle according to the turn
                        coordinates = (375, 225)
                        # used to check if the position is already occupied, and to update it if not
                        updatePos = (0, 1)
                    # mouse in the second row (of the second column) - position (1,1)
                    elif (mousePosition[1] > 300 and mousePosition[1] < 450):
                        # used for drawing rectangle/ circle according to the turn
                        coordinates = (375, 375)
                        # used to check if the position is already occupied, and to update it if not
                        updatePos = (1, 1)
                    # mouse in the third row (of the second column) - position (2,1)
                    elif (mousePosition[1] > 450 and mousePosition[1] < 600):
                        # used for drawing rectangle/ circle according to the turn
                        coordinates = (375, 525)
                        # used to check if the position is already occupied, and to update it if not
                        updatePos = (2, 1)

                # mouse in third column
                elif (mousePosition[0] > 450 and mousePosition[0] < 600):
                    # mouse in the first row (of the third column) - position (0,2)
                    if (mousePosition[1] > 150 and mousePosition[1] < 300):
                        # used for drawing rectangle/ circle according to the turn
                        coordinates = (525, 225)
                        # used to check if the position is already occupied, and to update it if not
                        updatePos = (0, 2)
                    # mouse in the second row (of the third column) - position (1,2)
                    elif (mousePosition[1] > 300 and mousePosition[1] < 450):
                        # used for drawing rectangle/ circle according to the turn
                        coordinates = (525, 375)
                        # used to check if the position is already occupied, and to update it if not
                        updatePos = (1, 2)
                    # mouse in the third row (of the third column) - position (2,2)
                    elif (mousePosition[1] > 450 and mousePosition[1] < 600):
                        # used for drawing rectangle/ circle according to the turn
                        coordinates = (525, 525)
                        # used to check if the position is already occupied, and to update it if not
                        updatePos = (2, 2)

                ''' Update the game window, status matrix and turn if the position requested for is not already filled '''
                if (statusMatrix[updatePos[0]][updatePos[1]] == ''):  # check if the position requested for is empty or already occupied
                    # proceed if the position is empty
                    # update the status matrix
                    statusMatrix[updatePos[0]][updatePos[1]] = turn
                    # check for game over (by either win or draw), returns a tuple (gameOver, result)
                    res = checkGameStatus(turn, statusMatrix, updatePos)
                    # update game board and turn
                    turn = turnUpdate(turn, coordinates)
                    # gameOver => stored in res, at index 0 => is the game over, or can be continued
                    gameOver = res[0]
                    # winner => stored in res, at index 1 => stores the winner status => X Wins, Y Wins, Draw or none?
                    winner = res[1]
                    pg.display.update()  # update the game window with the changes made

    ''' Display the result and continue/ quit instructions when the game is over '''
    FONT = pg.font.SysFont(
        None, 75, bold=True)  # set the font styles for displaying the result
    text = FONT.render(winner, True, WHITE)  # set result text and font colour
    gameWindow.blit(text, [275, 650])  # update the result on the game window
    # set the font style to display the continue/ quit instructions
    FONT = pg.font.SysFont(None, 30)
    # set text message and its font colour
    text = FONT.render(
        "Escape to quit the game boss, press enter to play again! :)", True, RED)
    gameWindow.blit(text, [200, 700])  # set the message on the game window
    pg.display.update()  # update the game window with the changes made
