"""
def start_game(start_play):
    for key in start_play:
        if start_play[key] != 'X' or start_play[key] != 'O':
            print()
            position = int(input('Please Enter Position Between 1:9:'))
            if 1 <= position <= 10:
                marker = input('Please Enter  X or O? ').upper()
                if marker == 'X' or marker == 'O':
                    marker_right(start_play, position, marker)
                else:
                    if marker != "X" or marker != "O":
                        marker_wrong(position, marker)
            else:
                print('Please Enter Correct Number between 1:9')
            continue
    else:
        print('\n', "Unfortunately there is no winner")
        no_winner()


def marker_right(new_board, position, marker):
    new_board.update({position: marker})
    display_board(new_board)
    check_winner(new_board)


def marker_wrong(position, marker):
    while not (marker == 'X' or marker == 'O'):
        print('Please Enter X or O ')
        marker = input('Do you want to be X or O? ').upper()
    else:
        marker_right(position, marker)


def check_winner(win):
    if win[1] == win[5] == win[9]:
        end_game()
    elif win[3] == win[5] == win[7]:
        end_game()
    for p in range(1, 8, 3):
        if win[p] == win[p + 1] == win[p + 2]:
            end_game()
    for p2 in range(1, 4):
        if win[p2] == win[p2 + 3] == win[p2 + 6]:
            end_game()


def end_game():
    print('\n', '####################               Congratulations, you are the winner              #################### ', '\n')
    no_winner()


def no_winner():
    play_again = input('Do you want to play again? y or n').upper()
    if play_again == 'Y':
        one_more_time = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
        display_board(one_more_time)
        start_game(one_more_time)
    else:
        print('\n', 'Thank you for playing the game and wish you have a good time')
        quit()


def display_board(board):
    print('\n', '                         ', board[1], '  |  ', board[2], '  |  ', board[3])
    print('\n', '                        ', ' ____  ______  _____')
    print('\n', '                         ', board[4], '  |  ', board[5], '  |  ', board[6])
    print('\n', '                        ', ' ____  ______  _____')
    print('\n', '                         ', board[7], '  |  ', board[8], '  |  ', board[9])


osama = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
print('########################          Welcome to Tic Tac Toe!           ########################')
display_board(osama)
start_game(osama)

##################################################################################################################
"""


# make game play by 2Player
def start_game(start_play):
    for key in start_play:
        if start_play[key] != 'X' or start_play[key] != 'O':
            print()
            position = int(input('Please Enter Position Between 1:9:'))
            if 1 <= position <= 10:
                marker = input('Please Enter  X or O? ').upper()
                if marker == 'X' or marker == 'O':
                    marker_right(start_play, position, marker)
                else:
                    if marker != "X" or marker != "O":
                        marker_wrong(position, marker)
            else:
                print('Please Enter Correct Number between 1:9')
            continue
    else:
        print('\n', "Unfortunately there is no winner")
        no_winner()


def marker_right(new_board, position, marker):
    new_board.update({position: marker})
    display_board(new_board)
    check_winner(new_board)


def marker_wrong(position, marker):
    while not (marker == 'X' or marker == 'O'):
        print('Please Enter X or O ')
        marker = input('Do you want to be X or O? ').upper()
    else:
        marker_right(position, marker)


def check_winner(win):
    if win[1] == win[5] == win[9]:
        end_game()
    elif win[3] == win[5] == win[7]:
        end_game()
    for p in range(1, 8, 3):
        if win[p] == win[p + 1] == win[p + 2]:
            end_game()
    for p2 in range(1, 4):
        if win[p2] == win[p2 + 3] == win[p2 + 6]:
            end_game()


def end_game():
    print('\n', '####################               Congratulations, you are the winner              #################### ', '\n')
    no_winner()


def no_winner():
    play_again = input('Do you want to play again? y or n').upper()
    if play_again == 'Y':
        one_more_time = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
        display_board(one_more_time)
        start_game(one_more_time)
    else:
        print('\n', 'Thank you for playing the game and wish you have a good time')
        quit()


def display_board(board):
    print('\n', '                         ', board[1], '  |  ', board[2], '  |  ', board[3])
    print('\n', '                        ', ' ____  ______  _____')
    print('\n', '                         ', board[4], '  |  ', board[5], '  |  ', board[6])
    print('\n', '                        ', ' ____  ______  _____')
    print('\n', '                         ', board[7], '  |  ', board[8], '  |  ', board[9])


osama = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
print('########################          Welcome to Tic Tac Toe!           ########################')
display_board(osama)
start_game(osama)
