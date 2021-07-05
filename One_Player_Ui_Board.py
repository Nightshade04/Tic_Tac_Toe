import inspect
import math
import tkinter as tk
from itertools import combinations

from PIL import ImageTk, Image

# root = tk.Tk()

buttons = {
    'button0': None,
    'button1': None,
    'button2': None,
    'button3': None,
    'button4': None,
    'button5': None,
    'button6': None,
    'button7': None,
    'button8': None
}

board = {
    '0': 'Normal',
    '1': 'Normal',
    '2': 'Normal',
    '3': 'Normal',
    '4': 'Normal',
    '5': 'Normal',
    '6': 'Normal',
    '7': 'Normal',
    '8': 'Normal'
}

magic_matrix = [8, 1, 6, 3, 5, 7, 4, 9, 2]
turn_multiplayer = 0
first_player_moves = []
second_player_moves = []
first_player_win_flag = False
second_player_win_flag = False
game_over_flag = False
end_data = None
x_pos_in_board = None
o_pos_in_board = None
scores = {
    "FirstPlayer": 1,
    "SecondPlayer": -1,
    "Tie": 0
}

'''
# necessary code for pre-processing images and other commonly used methods 
'''


def popup(msg):
    popup_dialog = tk.Tk()
    popup_dialog.wm_title('!!!')
    label = tk.Label(popup_dialog, text=msg)
    label.pack(side="top", fill='x', expand=True)
    button = tk.Button(popup_dialog, text='Okay', command=popup_dialog.destroy)
    button.pack()
    # popup.after(3000, lambda: popup.destroy())
    popup_dialog.mainloop()


def pre_process():
    path = "resources/img/XImage.png"
    image = Image.open(path)
    image = image.resize((150, 125), Image.ANTIALIAS)
    x_img = ImageTk.PhotoImage(image)

    path = "resources/img/OImage.png"
    image = Image.open(path)
    image = image.resize((150, 125), Image.ANTIALIAS)
    o_img = ImageTk.PhotoImage(image)
    return [x_img, o_img]


def game_over(param, comb=None):
    global game_over_flag, end_data
    game_over_flag = True

    for button in buttons:
        if buttons[button]['state'] is not tk.DISABLED:
            buttons[button]['state'] = tk.DISABLED

    if param == 'Tie':
        end_data = '================== Game Tied, No-one Wins =================='

    else:
        print(comb, "From here")
        for button_value in comb:
            index = magic_matrix.index(button_value)
            buttons['button' + str(index)].config(background='green')

        end_data = '================== Congratulations, ' + param + ' Wins =================='

    popup(end_data)


def check_winner(first_player_moves_local, second_player_moves_local):
    global turn_multiplayer, first_player_win_flag, second_player_win_flag, x_pos_in_board, o_pos_in_board

    for comb_x in combinations(first_player_moves_local, 3):
        if sum(comb_x) == 15:
            first_player_win_flag = True
            print(comb_x, "X COMB")
            x_pos_in_board = comb_x
            break

    for comb_o in combinations(second_player_moves_local, 3):
        if sum(comb_o) == 15:
            second_player_win_flag = True
            print(comb_o, "O COMB")
            o_pos_in_board = comb_o
            break

    if first_player_win_flag or second_player_win_flag:
        turn_multiplayer = 9

    if turn_multiplayer >= 9:

        if first_player_win_flag:
            # game_over('FirstPlayer', comb_x)
            return 'FirstPlayer'

        elif second_player_win_flag:
            # game_over('SecondPlayer', comb_o)
            return 'SecondPlayer'

        else:
            # game_over('Tie')
            return 'Tie'
    else:
        return None


def check_winner_minimax(first_player_moves_local, second_player_moves_local):
    first_player_win_flag_local, second_player_win_flag_local = False, False

    for comb_x in combinations(first_player_moves_local, 3):
        if sum(comb_x) == 15:
            first_player_win_flag_local = True
            break

    for comb_o in combinations(second_player_moves_local, 3):
        if sum(comb_o) == 15:
            second_player_win_flag_local = True
            break

    game_continue_flag = False

    if first_player_win_flag_local:
        # game_over('FirstPlayer', comb_x)
        return 'FirstPlayer'

    elif second_player_win_flag_local:
        # game_over('SecondPlayer', comb_o)
        return 'SecondPlayer'

    else:
        for button in board:
            if board[button] == 'Normal':
                game_continue_flag = True

        if game_continue_flag is True:
            return None
        else:
            # game_over('Tie')
            return 'Tie'


def button_press_callback(button_data):
    game_type = button_data[2]
    button_value = button_data[3]
    pressed_button = button_data[0]

    single_player_move(pressed_button, button_value, button_data[1])


'''
# Method that governs single player moves
'''


# def max_alpha_beta(self, alpha, beta):
#     maxv = -2
#     px = None
#     py = None
#
#     result = self.is_end()
#
#     if result == 'X':
#         return (-1, 0, 0)
#     elif result == 'O':
#         return (1, 0, 0)
#     elif result == '.':
#         return (0, 0, 0)
#
#     for i in range(0, 3):
#         for j in range(0, 3):
#             if self.current_state[i][j] == '.':
#                 self.current_state[i][j] = 'O'
#                 (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
#                 if m > maxv:
#                     maxv = m
#                     px = i
#                     py = j
#                 self.current_state[i][j] = '.'
#
#                 # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
#                 if maxv >= beta:
#                     return (maxv, px, py)
#
#                 if maxv > alpha:
#                     alpha = maxv
#
#     return (maxv, px, py)
#
#
# def min_alpha_beta(self, alpha, beta):
#     minv = 2
#
#     qx = None
#     qy = None
#
#     result = self.is_end()
#
#     if result == 'X':
#         return (-1, 0, 0)
#     elif result == 'O':
#         return (1, 0, 0)
#     elif result == '.':
#         return (0, 0, 0)
#
#     for i in range(0, 3):
#         for j in range(0, 3):
#             if self.current_state[i][j] == '.':
#                 self.current_state[i][j] = 'X'
#                 (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
#                 if m < minv:
#                     minv = m
#                     qx = i
#                     qy = j
#                 self.current_state[i][j] = '.'
#
#                 if minv <= alpha:
#                     return (minv, qx, qy)
#
#                 if minv < beta:
#                     beta = minv
#
#     return (minv, qx, qy)

def minimax(depth, maximizing_player, first_player_moves_local, second_player_moves_local, local_board):
    base_condition_check_value = check_winner_minimax(first_player_moves_local, second_player_moves_local)

    if base_condition_check_value is not None:
        return scores[base_condition_check_value]

    else:
        if maximizing_player is False:
            best_score = math.inf
            for button in local_board:
                if local_board[button] == 'Normal':
                    local_board[button] = 'Disabled'
                    second_player_moves_local.append(magic_matrix[int(button)])
                    current_score = minimax(depth + 1, True, first_player_moves_local, second_player_moves_local,
                                            local_board)
                    local_board[button] = 'Normal'
                    second_player_moves_local.pop()
                    if current_score < best_score:
                        best_score = current_score
            return best_score

        else:
            best_score = -math.inf
            for button in local_board:
                if local_board[button] == 'Normal':
                    board[button] = 'Disabled'
                    first_player_moves_local.append(magic_matrix[int(button)])
                    current_score = minimax(depth + 1, False, first_player_moves_local, second_player_moves_local,
                                            local_board)
                    local_board[button] = 'Normal'
                    first_player_moves_local.pop()
                    if current_score > best_score:
                        best_score = current_score
            return best_score


def ai_move(first_player_moves_local, second_player_moves_local):
    global magic_matrix

    button_to_be_pressed = None
    button_pos_in_magic_matrix = -1
    best_score = math.inf

    for button in board:
        print(button, board[button], "From here")
        if board[button] == 'Normal':
            board[button] = 'Disabled'
            second_player_moves_local.append(magic_matrix[int(button)])
            current_score = minimax(0, True, first_player_moves_local, second_player_moves_local, board)
            board[button] = 'Normal'
            second_player_moves_local.pop()
            if current_score < best_score:
                best_score = current_score
                button_to_be_pressed = buttons['button' + str(button)]
                button_pos_in_magic_matrix = int(button)

    print(best_score, first_player_moves_local, second_player_moves_local, "This is what computer chose")
    return [button_to_be_pressed, button_pos_in_magic_matrix]


def single_player_move(pressed_button, button_value, button_images):
    global turn_multiplayer, first_player_moves, second_player_moves
    # check_winner()
    pressed_button['state'] = tk.DISABLED
    pressed_button.config(image=button_images[0], height=8, width=23)
    first_player_moves.append(button_value)
    board[str(magic_matrix.index(button_value))] = 'Disabled'
    turn_multiplayer += 1
    # user_pressed_buttons.append(pressed_button)

    game_over_function_call_flag = check_winner(first_player_moves, second_player_moves)

    if game_over_function_call_flag is not None:
        if first_player_win_flag is True:
            game_over('FirstPlayer', x_pos_in_board)

    # Start looking for moves of computer player

    ai_pressed_button_data = ai_move(first_player_moves, second_player_moves)
    ai_pressed_button = ai_pressed_button_data[0]
    ai_pressed_button_value = magic_matrix[ai_pressed_button_data[1]]

    if ai_pressed_button is not None and ai_pressed_button_data[1] != -1:
        ai_pressed_button['state'] = tk.DISABLED
        ai_pressed_button.config(image=button_images[1], height=8, width=23)
        board[str(ai_pressed_button_data[1])] = 'Disabled'
        second_player_moves.append(ai_pressed_button_value)
        # ai_pressed_buttons.append(ai_pressed_button)

    turn_multiplayer += 1

    game_over_function_call_flag = check_winner(first_player_moves, second_player_moves)
    if game_over_function_call_flag is not None:
        if second_player_win_flag is True:
            game_over('SecondPlayer', o_pos_in_board)

    if game_over_function_call_flag == 'Tie':
        game_over('Tie')

    print("Person Move {}, Computer Move {}".format(first_player_moves, second_player_moves), end='\n')


# Class for enabling use of this board in other places
class OnePlayerUiBoard(tk.Frame):
    global buttons
    button_marks = None

    def __init__(self, *args, **kwargs):
        global end_data
        # print(args)
        self.game_type = None
        tk.Frame.__init__(self, args[0], bg='black')

        OnePlayerUiBoard.button_marks = pre_process()
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        self.game_type = the_class

        end_data = 'This is' + str(self.game_type) + ' Mode!!!'
        # print(self.game_type)

        for button in buttons:
            i = int(button[len(button) - 1])
            row = int(i / 3)
            col = i % 3
            buttons[button] = tk.Button(self, text='-', relief=tk.GROOVE, height=8, width=23)
            buttons[button].config(command=lambda
                data=[buttons[button], OnePlayerUiBoard.button_marks, self.game_type,
                      magic_matrix[i]]: button_press_callback(
                data))
            buttons[button].grid(row=row, column=col, sticky="nsew")
            buttons[button].grid_rowconfigure(row, weight=row)
            buttons[button].grid_columnconfigure(col, weight=col)

    def reset_board(self):
        global turn_multiplayer, first_player_moves, second_player_moves, first_player_win_flag, second_player_win_flag, game_over_flag, end_data

        turn_multiplayer = 0
        first_player_moves = []
        second_player_moves = []
        first_player_win_flag = False
        second_player_win_flag = False
        game_over_flag = False
        end_data = None

        for button in board:
            board[button] = 'Normal'

        for button in buttons:
            i = int(button[len(button) - 1])
            row = int(i / 3)
            col = i % 3
            buttons[button] = tk.Button(self, text='-', relief=tk.GROOVE, height=8, width=23)
            buttons[button].config(command=lambda
                data=[buttons[button], OnePlayerUiBoard.button_marks, self.game_type,
                      magic_matrix[i]]: button_press_callback(
                data))
            buttons[button].grid(row=row, column=col, sticky="nsew")
            buttons[button].grid_rowconfigure(row, weight=0)
            buttons[button].grid_columnconfigure(col, weight=0)
        pass

# app = UiBoard(root)
# app.pack()
# root.mainloop()
