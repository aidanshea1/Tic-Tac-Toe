import pygame
import math

pygame.init()
display_width = 600
display_height = 600
font = pygame.font.Font(pygame.font.get_default_font(), 36)

board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
human = -1
computer = 1
infinity = math.inf

surface = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Tic Tac Toe")

# draws an X in the cell the player clicked
def draw_x(xpos, ypos):
    # top left corner of cell
    xcoord = int(xpos * 200)
    ycoord = int(ypos * 200)
    pygame.draw.line(surface, (0, 0, 0), (xcoord + 20, ycoord + 20), (xcoord + 180, ycoord + 180), 10)
    pygame.draw.line(surface, (0, 0, 0), (xcoord + 180, ycoord + 20), (xcoord + 20, ycoord + 180), 10)
    pygame.display.flip()


def draw_o(xpos, ypos):
    xcenter = int((xpos * 200) + 100)
    ycenter = int((ypos * 200) + 100)
    pygame.draw.circle(surface, (0, 0, 0), (xcenter, ycenter), 80, 10)
    pygame.display.flip()


# draws grid lines
def grid():
    pygame.draw.line(surface, (0, 0, 0), (200, 0), (200, 600), 5)
    pygame.draw.line(surface, (0, 0, 0), (400, 0), (400, 600), 5)
    pygame.draw.line(surface, (0, 0, 0), (0, 200), (600, 200), 5)
    pygame.draw.line(surface, (0, 0, 0), (0, 400), (600, 400), 5)
    pygame.display.flip()


def win(board, player):
    # 3 rows, 3 colums, 2 diagionals to check for
    possible = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    if [player, player, player] in possible:
        return True
    else:
        return False

def available(board):
    options = []
    for x, row in enumerate(board):
        for y, index in enumerate(row):
            if index == 0:
                options.append([x, y])
    return options


def score(board):
    if win(board, human):
        return -1
    elif win(board, computer):
        return 1
    else:
        return 0


# returns array contaoning coordinates of best move
# best = [row, index, score]
def minimax(board, depth, player):
    if player == computer:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, infinity]
    # if game is over
    if depth == 0 or win(board, human) or win(board, computer):
        if win(board, human):
            score = -1
        elif win(board, computer):
            score = 1
        else:
            score = 0
        return [-1, -1, score]

    for spots in available(board):
        row = spots[0]
        index = spots[1]
        board[row][index] = player
        score = minimax(board, depth - 1, -player)
        board[row][index] = 0
        score[0] = row
        score[1] = index

    if player == computer:
        if score[2] > best[2]:
            best = score
    else:
        if score[2] < best[2]:
            best = score
    return best

def valid(row, index):
    if [row, index] in available(board):
        return True
    else:
        return False

def ai_move(board):
    # figure out best move using board
    depth = len(available(board))
    move = minimax(board, depth, computer)
    row = move[0]
    index = move[1]
    board[row][index] = 1

    # draw move into surface
    draw_o(index, row)


# fill in gameboard and grid lines
surface.fill((0, 0, 255))
grid()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # human turn
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos_x = pos[0] // 200
            pos_y = pos[1] // 200
            draw_x(pos_x, pos_y)
            board[pos_y][pos_x] = -1

            # computer turn
            ai_move(board)
            print(board)


            if win(board, human):
                surface.fill((0, 0, 255))
                text_surface = font.render("You Win!", True, (0, 0, 0))
                surface.blit(text_surface, dest = (230, 300))
                pygame.display.flip()
                
            if win(board, computer):
                surface.fill((0, 0, 255))
                text_surface = font.render("You Lose!", True, (0, 0, 0))
                surface.blit(text_surface, dest = (230, 300))
                pygame.display.flip()
