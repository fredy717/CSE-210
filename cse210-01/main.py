import math

BOARD = []
EMPTY_POS = []
ROW_BOARD = 0
COLUMN_BOARD = 0
PLAYERS = []


class Player:

    def __init__(self, name, mark):
        self._name = name
        self._mark = mark
        self._games_won = 0

    def get_name(self):
        return self._name

    def get_mark(self):
        return self._mark

    def get_games_won(self):
        return self._games_won

    def add_game_won(self):
        self._games_won += 1

    name = property(get_name)
    mark = property(get_mark)
    games_won = property(get_games_won)


def allied_squares(square, mark, v, h):
    f = math.floor(square / COLUMN_BOARD)
    c = square % COLUMN_BOARD
    new_row = f + v
    if new_row < 0 or new_row >= ROW_BOARD:
        return 0
    new_column = c + h
    if new_column < 0 or new_column >= COLUMN_BOARD:
        return 0
    pos = (new_row * COLUMN_BOARD + new_column)
    if BOARD[pos] != mark:
        return 0
    else:
        return 1 + allied_squares(pos, mark, v, h)


def has_winner(square, mark):
    allied = allied_squares(square, mark, -1, -1) + allied_squares(square, mark, 1, 1)
    if allied == 2:
        return True
    allied = allied_squares(square, mark, 1, -1) + allied_squares(square, mark, -1, 1)
    if allied == 2:
        return True
    allied = allied_squares(square, mark, -1, 0) + allied_squares(square, mark, 1, 0)
    if allied == 2:
        return True
    allied = allied_squares(square, mark, 0, -1) + allied_squares(square, mark, 0, 1)
    if allied == 2:
        return True


def init_board():
    BOARD.clear()
    EMPTY_POS.clear()
    for i in range(ROW_BOARD * COLUMN_BOARD):
        BOARD.append(' ')
        EMPTY_POS.append(i)


def validate_input(literal, x=1, y=2):
    while True:
        valor = input(literal)
        while not valor.isnumeric():
            print("Only numbers between %s y %s" % (x, y))
            valor = input(literal)
        pos = int(valor)
        if x <= pos <= y:
            return pos
        else:
            print("The value is valid, enter a number between %s y %s" % (x, y))


def insert_mark(mark):
    while True:
        row = validate_input("Row number [1 y %s]: " % ROW_BOARD, 1, ROW_BOARD) - 1
        column = validate_input("Column number [1 y %s]: " % COLUMN_BOARD, 1, COLUMN_BOARD) - 1
        pos = row * COLUMN_BOARD + column
        if BOARD[pos] != ' ':
            print("the box is occupied")
        else:
            BOARD[pos] = mark
            return pos


def draw_board():
    pos = 0
    print("--%s-" % ("--" * (COLUMN_BOARD - 1)))
    for row in range(ROW_BOARD):
        for column in range(COLUMN_BOARD):
            print("|%s" % BOARD[pos], end="")
            pos += 1
        print("|")
        if row < 4:
            print("--%s-" % ("+-" * (COLUMN_BOARD - 1)))
        else:
            print("--%s-" % ("--" * (COLUMN_BOARD - 1)))


def set_players():
    PLAYERS.append(Player(input('Enter name of first player: ').capitalize(), 'X'))
    PLAYERS.append(Player(input('Enter name of second player: ').capitalize(), 'O'))
    starting_player = validate_input(
        'Who will start the game?:\n 1) %s.\n 2) %s.\n' % (PLAYERS[0].name, PLAYERS[1].name))
    if starting_player == '2':
        PLAYERS.remove()


if __name__ == '__main__':
    set_players()
    COLUMN_BOARD = validate_input('Enter column size: ', 1, 10)
    ROW_BOARD = validate_input('Enter row size: ', 1, 10)
    init_board()
    draw_board()
    not_win = True
    markings = 0
    while not_win:
        play = (markings & 1)
        pos = insert_mark(PLAYERS[play].mark)
        if pos == -1:
            draw_board()
            not_win = False
            continue
        EMPTY_POS.remove(pos)
        if has_winner(pos, PLAYERS[play].mark):
            not_win = False
            print('%s, you won.' % PLAYERS[play].name)
        markings += 1
        if len(EMPTY_POS) == 0 and not_win:
            not_win = False
            print("Tied game!")
        draw_board()
