import inspect
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
magic_matrix = [8, 1, 6, 3, 5, 7, 4, 9, 2]
turn_multiplayer = 0
first_player_moves = []
second_player_moves = []
first_player_win_flag = False
second_player_win_flag = False
game_over_flag = False
end_data = {}


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


def game_over(param):
    global game_over_flag
    game_over_flag = True

    if param == 'Tie':
        end_data['message'] = '================== Game Tied, No-one Wins =================='

    else:
        end_data['message'] = '================== Congratulations, ' + param + ' Wins =================='


def check_winner():
    global turn_multiplayer, first_player_moves, second_player_moves, first_player_win_flag, second_player_win_flag

    for comb in combinations(first_player_moves, 3):
        if sum(comb) == 15:
            first_player_win_flag = True
            break
        # print(comb, "X COMB")

    for comb in combinations(second_player_moves, 3):
        if sum(comb) == 15:
            second_player_win_flag = True
            break
        # print(comb, "O COMB")

    if first_player_win_flag or second_player_win_flag:
        turn_multiplayer = 8
    print(not first_player_win_flag)
    if turn_multiplayer == 8:

        if first_player_win_flag:
            for button in buttons:
                if buttons[button]['state'] is not tk.DISABLED:
                    buttons[button]['state'] = tk.DISABLED

            print("First Player Wins")
            game_over('FirstPlayer')

        elif second_player_win_flag:
            for button in buttons:
                if buttons[button]['state'] is not tk.DISABLED:
                    buttons[button]['state'] = tk.DISABLED

            print('Second PLayer wins')
            game_over('SecondPlayer')

        else:
            print('DRAW')
            game_over('Tie')


def multiplayer_move(pressed_button, button_value, param):
    global turn_multiplayer, first_player_moves, second_player_moves
    # check_winner()
    pressed_button['state'] = tk.DISABLED

    if turn_multiplayer % 2 == 0:
        pressed_button.config(image=param[0], height=125, width=166)
        first_player_moves.append(button_value)

    else:
        pressed_button.config(image=param[1], height=125, width=166)
        second_player_moves.append(button_value)

    turn_multiplayer += 1
    check_winner()
    print(first_player_moves, second_player_moves)


def button_press_callback(button_data):
    game_type = button_data[2]
    button_value = button_data[3]
    pressed_button = button_data[0]

    if game_type == 'OnePlayer':
        print('LOGIC COMING SOON')

    else:
        multiplayer_move(pressed_button, button_value, button_data[1])

    # print(button_data)


class UiBoard(tk.Frame):

    def __init__(self, *args, **kwargs):
        # print(args)
        self.game_type = None
        tk.Frame.__init__(self, args[0], bg='black')

        button_marks = pre_process()
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        self.game_type = the_class
        # print(self.game_type)

        for button in buttons:
            i = int(button[len(button) - 1])
            row = int(i / 3)
            col = i % 3
            buttons[button] = tk.Button(self, text='-', relief=tk.GROOVE, height=8, width=23)
            buttons[button].config(
                command=lambda
                    data=[buttons[button], button_marks, self.game_type, magic_matrix[i]]: button_press_callback(
                    data))
            buttons[button].grid(row=row, column=col, sticky="nsew")
            buttons[button].grid_rowconfigure(row, weight=0)
            buttons[button].grid_columnconfigure(col, weight=0)

# app = UiBoard(root)
# app.pack()
# root.mainloop()
