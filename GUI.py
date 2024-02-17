#GUI.py

from tkinter import *
from tkinter.ttk import *             #Additional 
from PIL import Image, ImageTk
import numpy as np
import Moves_Inital 
import main
import statistics
import threading 
import os
from multiprocessing import *
#import time 


#Constants 
WIDTH = 600
HEIGHT = 600
BOARD_SIZE = 8 
SQUARE_SIZE = WIDTH // BOARD_SIZE
global inc, locked
inc = -1

#Normalise character representations
W_Pawn = "♟︎"
B_Pawn = "♙"
W_Bish = '♝'
B_Bish = '♗' 
W_Knig = '♞'
B_Knig = '♘'
W_Rook = '♜'
B_Rook = '♖'
W_Quee = '♛' 
B_Quee = '♕'
W_King = '♚'  
B_King = '♔'
Empty_ = '_'
W_En_Passant_Token = '!'
B_En_Passant_Token = '?'
command = [['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']]

#Tk specific
global board, sprites, types, WHITE, BLACK, White_Playing, message, performed 
performed = 0 
message = ''
White_Playing = True
types = [W_King, B_King, W_Quee, B_Quee, W_Rook, B_Rook, W_Bish, B_Bish, W_Knig, B_Knig, W_Pawn, B_Pawn, W_En_Passant_Token, B_En_Passant_Token]
WHITE = [W_King, W_Quee, W_Rook, W_Bish, W_Knig, W_Pawn, W_En_Passant_Token]
BLACK = [B_King, B_Quee, B_Rook, B_Bish, B_Knig, B_Pawn, B_En_Passant_Token]
EMPTY = [Empty_, W_En_Passant_Token, B_En_Passant_Token]
image_files = ["Peices/W_King.png","Peices/B_King.png","Peices/W_Quee.png","Peices/B_Quee.png","Peices/W_Rook.png","Peices/B_Rook.png","Peices/W_Bish.png","Peices/B_Bish.png","Peices/W_Knig.png","Peices/B_Knig.png","Peices/W_Pawn.png","Peices/B_Pawn.png", "Peices/W_En_Passant_Token", "Peices/B_En_Passant_Token"]
sprites = []
board = main.board
locked = False

#Inital
window = Tk()  
window.geometry('650x640')

display = Text(window, background='PaleTurquoise1', height=2, width=75, state=DISABLED)

s = Style()
s.theme_use('clam')
s.configure('yellow.Vertical.TProgressbar', foreground='purple', background='white')

utility = Progressbar(orient=VERTICAL, length=560, maximum=200, style='yellow.Vertical.TProgressbar')
utility.config(style='yellow.Vertical.TProgressbar')
utility.place(x=620, y=20, width=15)

TROUGH_COLOR = 'white'
BAR_COLOR = 'black'

#Need to learn how to change colour of the progress bar
#https://www.youtube.com/watch?v=N4v9Z0e3TxA

current_utility = 100
utility.step(100)


def callback(e):
    x = e.x
    y = e.y
    print("Pointer is currently at %d, %d" %(x, y))

def players():
    global locked
    #print("PLAYERS RUNNING")
    global White_Playing, board
    Time_Stamp = main.Time_Stamp
    player = main.player
    #print("-------------- players called ---------------------------", Time_Stamp, player)
    if main.player[pointer] != 'Human' and not locked:
        #Perform ai actions
        #print("------------------ CALLED AI -----------------------------")
        locked = True
        reset_command()
        new_thread = threading.Thread(target=main.gameplay_loop((-1, -1), (-1, -1)), name="alt").start()

def reset_command():
    global command 
    command = [['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','','']]
    return command 
    
global last_processed
last_processed = None 

global UPDATE_OPT
UPDATE_OPT = False

def lazy_update(utility_scores, current_processed):
    global UPDATE_OPT
    if UPDATE_OPT:
        update_utility(utility_scores, current_processed)


def simple_update_utility(utility_scores):
    global current_utility
    ENLARGMENT_FACTOR = 1 + (0.05 * main.Time_Stamp)
    utility_value = (statistics.fmean(utility_scores) * ENLARGMENT_FACTOR) + 100
    #Need to ensure it lies within the range;
    if utility_value > 200:
        utility_value = 199.9999
    elif utility_value < 0:
        utility_value = 0.0001
    utility.stop()
    utility.step(utility_value)


def update_utility(utility_scores, current_processed):
    global current_utility, performed, last_processed, command

    #print(utility_scores, current_processed)


    ENLARGMENT_FACTOR = 1
    utility_value = (statistics.fmean(utility_scores) * ENLARGMENT_FACTOR) + 100
    #Need to ensure it lies within the range;
    if utility_value > 200:
        utility_value = 199.9999
    elif utility_value < 0:
        utility_value = 0.0001
    performed = len(utility_scores)

    #check for first highlight
    if last_processed == None:
        last_processed = current_processed

    utility.stop()
    utility.step(utility_value)
    if current_processed != None:
        command[last_processed[1][1]][last_processed[1][0]] = "PROCESSED"
        command[last_processed[0][1]][last_processed[0][0]] = ''
        if command[current_processed[1][1]][current_processed[1][0]] == "PROCESSED":
            command[current_processed[1][1]][current_processed[1][0]] = "ATTACK"
            command[current_processed[0][1]][current_processed[0][0]] = "SELECT"

    last_processed = current_processed
    draw_board()

def on_click(event):
    print("CLICKED ACTION")
    locked = True
    global command, WHITE, BLACK, board, White_Playing
    board = main.board
    #Get the cordinates for the command 
    x = event.x - (0.5 * SQUARE_SIZE)
    y = event.y - (0.5 * SQUARE_SIZE)
    #print("Event called at %d, %d" %(x, y))
    X_location = round((x / SQUARE_SIZE))
    Y_location = round(y / SQUARE_SIZE)
    #From there, check that this was not an 'action' click
    if command[Y_location][X_location] == "MOVE" or command[Y_location][X_location] == "ATTACK":
        #Perform the player's move; 
        print("ALARM - ACTIONING")
        move_to = (X_location, Y_location)                                                   #TO DO
        for i in range(0,8):
            for j in range(0,8):
                if command[j][i] == "SELECT":
                    move_from = (i, j)
        player_testing = ''
        if board[move_from[1]][move_from[0]] in WHITE:
            player_testing = True
        elif board[move_from[1]][move_from[0]] in BLACK:
            player_testing = False
        #print("VALID check, ", player_testing, main.White_Playing)
        if bool(player_testing) == bool_pointer(pointer):
            print("TEST !! PERFORMING GAMEPLAY_LOOP")
            locked = True
            new_thread = threading.Thread(target=main.gameplay_loop(move_from, move_to), name="alt")                                                         #main.gameplay_loop(move_from, move_to)
            command = reset_command()
            locked = False
            #draw_board()
    else:
        print("ALTERNATIVE COND - HIGHLIGHT FIRED")
        highlight(X_location, Y_location)


def bool_pointer(pointer):
    if pointer == 0:
        return True
    else: 
        return False


def highlight(X_location, Y_location):
    global command 
    #Then, Reset command and perform highlighting for that peice.
    command = reset_command()
    command[Y_location][X_location] = "SELECT"
    #From there; check the moves belonging to the respective peice
    board = main.board
    White_Moves, Black_Moves = main.get_moves()
    print(len(White_Moves), len(Black_Moves))
    #For the White Player
    if board[Y_location][X_location] in WHITE:
        print("WHITE COMMAND")
        White_Moves = main.White_Moves
        for i in range(len(White_Moves)):
            if command[White_Moves[i][0][1]][White_Moves[i][0][0]] == "SELECT": #That is the clicked peice; 
                command[White_Moves[i][1][1]][White_Moves[i][1][0]] = "MOVE"
                if board[White_Moves[i][1][1]][White_Moves[i][1][0]] in BLACK:
                    print("SUCCESS")
                    command[White_Moves[i][1][1]][White_Moves[i][1][0]] = "ATTACK"
                    print(command)

    #For the Black Player
    if board[Y_location][X_location] in BLACK:
        Black_Moves = main.Black_Moves
        print("BLACK COMMAND")
        for i in range(len(Black_Moves)):
            if command[Black_Moves[i][0][1]][Black_Moves[i][0][0]] == "SELECT": #That is the clicked peice; 
                command[Black_Moves[i][1][1]][Black_Moves[i][1][0]] = "MOVE"
                if board[Black_Moves[i][1][1]][Black_Moves[i][1][0]] in WHITE:
                    print("FAIL")
                    command[Black_Moves[i][1][1]][Black_Moves[i][1][0]] = "ATTACK"
                                             
    #for draw_board - command is used as a global var - and so call draw_board. 
    draw_board() 

window.bind('<Button-1>', on_click if not locked else None)

def on_chess_click(event):
    global locked
    if not locked: #set a cap 
        produce = threading.Thread(target=on_click(event), name="board").start()

#Images for peices 
inc = -1

board = [[B_Rook, B_Knig, B_Bish, B_Quee, B_King, B_Bish, B_Knig, B_Rook],
        [B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn], 
        [W_Rook, W_Knig, W_Bish, W_Quee, W_King, W_Bish, W_Knig, W_Rook]]

window.title('ChessAI [Board]')

#Canvas creation 
canvas = Canvas(window, width=WIDTH, height=HEIGHT)
canvas.grid(row=0, column=0)
display.grid(row=1, column=0)

types = [W_King, B_King, W_Quee, B_Quee, W_Rook, B_Rook, W_Bish, B_Bish, W_Knig, B_Knig, W_Pawn, B_Pawn] 
WHITE = [W_King, W_Quee, W_Rook, W_Bish, W_Knig, W_Pawn, W_En_Passant_Token]
BLACK = [B_King, B_Quee, B_Rook, B_Bish, B_Knig, B_Pawn, B_En_Passant_Token]

image_files = ["Peices/W_King.png","Peices/B_King.png","Peices/W_Quee.png","Peices/B_Quee.png","Peices/W_Rook.png","Peices/B_Rook.png","Peices/W_Bish.png","Peices/B_Bish.png","Peices/W_Knig.png","Peices/B_Knig.png","Peices/W_Pawn.png","Peices/B_Pawn.png"] # "Peices/W_En_Passant_Token.png","Peices/B_En_Passant_Token.png"]
sprites = []
#Hence; draw on the canvas

def draw_board():
    global inc, command, sprites, White_Playing
    colors, sprites, inc, board = ["white", "grey"], [], -1, main.board
    for row in range(-1, BOARD_SIZE):
        for col in range(-1, BOARD_SIZE):
            #rint(row, col)
            x1 = col * SQUARE_SIZE
            y1 = row * SQUARE_SIZE
            x2 = x1 * SQUARE_SIZE
            y2 = y1 * SQUARE_SIZE
            #Check for the zero case
            if x1 == 0:
                x2 = SQUARE_SIZE
            if y1 == 0:
                y2 = SQUARE_SIZE
            #Determine board colours - If forced by a peice selection 
            if command[row][col] == "SELECT":
                color = 'blue'
            elif command[row][col] == "MOVE":
                color = 'green'
            elif command[row][col] == "ATTACK":
                color = 'red'
            elif (board[row][col] == W_En_Passant_Token) or (board[row][col] == B_En_Passant_Token):
                color = 'purple'
            elif command[row][col] == "PROCESSED":
                color = 'yellow'
            else:
                color = colors[(row+col)%2]
            #Otherwise - display the sprite. 
            if board[row][col] not in EMPTY:
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                display_image(col, row, x1, y1)
            else:  #Normal case - display grid structure
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            #Then regardless - pass to next player
    locked = False
    window.update_idletasks()

    #Hence - or otherwise, get the next player to play - which should be automatic if AI


def get_contents():  
    return board 

def display_message():
    global message 
    if not finished:
      message = ''
      if bool_pointer(pointer):
        message = 'White player turn' + '  [' + str(main.player[0]) + ']'
      elif not bool_pointer(pointer):
        message = 'Black player turn' + '  [' + str(main.player[1]) + ']'
      if main.player[pointer] != 'Human':
          cap = len(main.White_moves if bool_pointer(pointer) else main.Black_moves)
          message += '    ' + str(performed) + '/' + str(cap)
    return message 
    

def display_image(col, row, x1, y1):
    global inc, sprites, types, board

    board = main.board

    for i in range(len(types)):
        if board[row][col] == types[i]:
            sprites.append(ImageTk.PhotoImage(file=image_files[i]))
            inc = (len(sprites)-1)

    canvas.create_image(x1 + (0.5 * SQUARE_SIZE), y1 + (0.5 * SQUARE_SIZE), image=sprites[inc])
    


#Timer objects
global mins, sec, minute, second, time, MOVE_BONUS, pointer, finished
time = [300, 300]
pointer, Move_BONUS = 0, 5
finished = False
mins = StringVar()
sec = StringVar()

def count_down():
    global time, pointer, finished, message 
    increment = 0
    window.update()
    while not finished:
        increment += 10
        window.after(10)
        if time[pointer] > -1 and increment == 1000:
            minute, second = (time[pointer] // 60, time[pointer] % 60)
            sec.set(second)
            mins.set(minute)
            increment = 0
            #Update the time
            window.update()
            if (time[pointer] == 0):
                finish()
            time[pointer] -= 1
            timer()
        players()


def finish():
    global message, finished
    if pointer == 1:
        message = 'White won by timeout!'
        display.config(background='White', foreground = 'Black')
    else:
        message = 'Black won by timeout!'
        display.config(background='Black', foreground = 'White')
    finished = True


def checked(for_White):
    global message, finished
    if for_White:
        message = 'White has been checkmated'
        display.config(background='Black', foreground = 'White')
    else:
        message = 'Black has been checkmated'
        display.config(background="White", foreground = 'Black')
    finished = True
    timer()

def fifty_moves():
    global message, finished
    message = 'DRAW: 50 moves rule'
    display.config(bg = 'grey45', fg = 'White')
    finished = True
    timer()

def stalemate():
    global message, finished
    message = 'DRAW: Stalemate'
    display.config(bg = 'grey45', fg = 'White')
    finished = True
    timer()


def insufficent():
    global message, finished
    message = 'DRAW: Insufficent material'
    display.config(bg = 'grey45', fg = 'White')
    finished = True
    timer()

def default():
    global message, finished
    message = ''
    display.config(bg = 'PaleTurquoise1', fg= 'Black')
    finished = False


    

def timer():
    global finished, pointer, White_Moves, Black_Moves
    display.config(state='normal')
    if not finished:
      warning()
    display.tag_configure("tag_name", justify='center')
    display.tag_configure("timing", justify='left')
    display.delete("1.0",END)
    display.insert(END, display_message())
    display.insert(END, form(time))
    display.tag_add("tag_name", "1.0", "end")
    display.tag_add("timing", "1.0", "1.0") 
    display.update()
    display.config(state='disabled')
    window.update_idletasks()
    window.update()

    if finished: 
        update_wins(main.White_Playing)
        main.reset()
        window.update()
        draw_board()
        #window.after(50000)
        #window.destroy()
        #counter.join()
        #White_Moves = Moves_Inital.White_moves_original
        #Black_Moves = Moves_Inital.Black_moves_original
        window.after(5000)
        finished = False
        players()
    else:
        players()

def update_wins(for_White):
    if for_White:
        current_file = 'Ai_file1.txt'
    else:
        current_file = 'Ai_file2.txt'

    file = open(current_file)
    content = file.readlines()
    current_wins = int(content[9]) + 1
    print("GOT CURRENT WINS", current_wins)
    content[9] = str(current_wins)

    # and write everything back
    with open(current_file, 'w') as file:
       file.writelines(content)

    file.close()


global forced
forced = ''

def next_turn():
    global forced
    if main.player[pointer] != 'Human':
        window.after(10)
        if forced != '':
           forced = threading.Thread(target=main.gameplay_loop((-1, -1), (-1, -1)), name="forced")
           forced = ''

def warning():
    left = time[pointer]
    display.config(background='PaleTurquoise1')
    if left <= 10:
        if left % 2 == 0:
          display.config(background='red')
    elif left <= 60:
        if left % 5 == 0:
          display.config(background='yellow')
    elif left % 15 == 0:
        display.config(background='grey')


def form(time):
    global pointer 
    minute, second = (time[pointer] // 60, time[pointer] % 60)
    if int(second) < 10:
        second = "0" + str(second)
    message = "                       " + str(minute) + ":" + str(second)
    return message 

#----

def console():
    #TO DO - FOR QUALITY - POSITION THE TOP LEVEL WINDOW RELATIVE TO...
    #https://www.tutorialspoint.com/python-tkinter-how-to-position-a-toplevel-widget-relative-to-the-root-window




    global console_window, entry_info, current_file, start_option, white_option, black_option
    from tkinter import font 
    current_file = 'Ai_file1.txt'
    underline_font = font.Font(underline=TRUE, family="Helvetica",size=10)
    regular_font = font.Font(underline=FALSE, family="Helvetica",size=10)
    link_font = font.Font(underline=TRUE, family="Helevetica", size=10)



    console_window = Toplevel()
    console_window.title('ChessAi [Console]')
    console_window.geometry('320x640')
    start_option = Button(console_window, text = 'Start game?', command=begin, width=50)
    start_option.grid(row=0, column=0, columnspan=1)   
    white_option = Text(console_window, height = 1, width = 45, bg = 'White', font=regular_font)
    white_option.grid(row=1, column=0, columnspan=1)   
    var = StringVar()
    var = "White Player"
    white_option.insert(END, var)
    #display_console.insert(END, display_message())
    black_option = Text(console_window, height = 1, width = 45, bg='Grey', fg = 'White', font=regular_font)
    black_option.grid(row=2, column=0)
    black_option.insert(END, 'Black Player')

    #modify_option = Checkbutton(console_window, text="Modifying White file").grid(row = 3, column = 0)
    
    label_text = StringVar()
    label = Label(console_window, textvariable=label_text, width=52, anchor=W, background=None) #TO DO - CHANGE COLOUR CORRESPONDINGLY https://stackoverflow.com/questions/42942534/how-to-change-the-color-of-a-tkinter-label-programmatically 
    label_text.set("Off")

    check= Checkbutton(console_window,  text="Change current File", variable=label_text,
                   onvalue="Modifying Black file...", offvalue="Modifying White file...", command=change_current_file)

    label.grid(row=4, column = 0, rowspan=1)
    check.grid(row = 3, column = 0)


    #

    Label(console_window, text="Personality").grid(row=5, sticky=W)
    Label(console_window, text="Depth").grid(row=6, sticky=W)
    Label(console_window, text="Endgame_Transition").grid(row=7, sticky=W)
    Label(console_window, text="Restlessness").grid(row=8, sticky=W)
    Label(console_window, text="Queen_Value").grid(row=9, sticky=W)
    Label(console_window, text="Rook_Value").grid(row=10, sticky=W)
    Label(console_window, text="Bishop_Value").grid(row=11, sticky=W)
    Label(console_window, text="Knight_Value").grid(row=12, sticky=W)
    Label(console_window, text="Pawn_Value").grid(row=13, sticky=W)

    #Alternative

    entry_info = [
        {"widget": Entry(console_window, width=30), "line": 1},
        {"widget": Entry(console_window, width=30), "line": 2},
        {"widget": Entry(console_window, width=30), "line": 3},
        {"widget": Entry(console_window, width=30), "line": 4},
        {"widget": Entry(console_window, width=30), "line": 5},
        {"widget": Entry(console_window, width=30), "line": 6},
        {"widget": Entry(console_window, width=30), "line": 7},
        {"widget": Entry(console_window, width=30), "line": 8},
        {"widget": Entry(console_window, width=30), "line": 9},
    ]

    row_num = 5
    #Pack the entry widgets
    for entry in entry_info:
        entry["widget"].grid(row=row_num, sticky=E)
        entry["widget"].delete(0, END)
        entry["widget"].insert(END, get_file_val(row_num-4))
        row_num += 1

    #Bind the write_file_val function to the event of any changes 
    for entry in entry_info:
        entry["widget"].bind("<KeyRelease>", lambda event, widget=entry["widget"], line=entry["line"]: write_file_val(widget, line))

    #Nonclamature and additional options 
        
    def make_hyperlink(label, callback):
        label.config(cursor="hand2")
        label.bind("<Button-1>", lambda event: callback())

    def open_readme():
        url = 'https://github.com/CodeAvali/ChessAI-NEA-Beta/blob/main/README.md'
        webbrowser.open_new(url)


    tip = Label(console_window, width = 45, text="For clarification on constants, see:", font=regular_font, background="White")
    tip.grid(row = 14, sticky=W)
    tip_link = Label(console_window, width = 45, text="Read.me", font=link_font, background="White", foreground="Blue")
    tip_link.grid(row=15, sticky=W)
    make_hyperlink(tip_link, open_readme)
    #tip.insert(END, "For clarrification on what the constants do, please see the read.me")          #TO LINK: README 
                                                                                                    #https://www.tutorialspoint.com/how-to-create-hyperlink-in-a-tkinter-text-widget#:~:text=Tkinter%20Text%20widgets%20are%20generally,using%20HyperLinkManager%20snippet%20in%20Python.
    additional = Label(console_window, text="Aditional Options:", font=underline_font)
    additional.grid(row=16, sticky = 'W')

    #
    highlighting_choice = BooleanVar()
    highlighting_choice.set(FALSE)

    highlighting_option= Checkbutton(console_window,  textvariable=highlighting_choice, variable=highlighting_choice, onvalue="Highlighting enabled - (Very costly)", offvalue="No AI Highlighting", command=allow_highlighting)
    highlighting_option.grid(row=17, sticky='W')

    utility_choice = StringVar()
    utility_choice= Checkbutton(console_window,  textvariable=utility_choice, variable=utility_choice, onvalue="AI utility updates enabled - (costly)", offvalue="No Ai Utility updates", command=allow_utility)
    utility_choice.grid(row=18, sticky='W')

    #Repeat option 
    Label(console_window, text="Repeated games").grid(row=19, sticky='W')
    Repeat_Option = Entry(console_window, width=30)
    Repeat_Option.grid(row=19, sticky='E')

    #Change associated file
    Label(console_window, text="Change file identifer").grid(row=20, sticky='W')
    Change_file = Entry(console_window, width=30)
    Change_file.grid(row=20, sticky='E')

    
    console_window.update()

    #Handle links 
    import webbrowser

    def open_git():
        url = 'https://www.youtube.com/watch?v=xvFZjo5PgG0'
        webbrowser.open_new(url)


    #Ownership
    copymark = Label(console_window, width = 45, text="Made by CodeAvali -> To Github", font=regular_font, foreground="Blue")
    copymark.grid(row = 25, sticky='W', pady=175)                                       #TO DO - LINK: https://www.tutorialspoint.com/how-to-create-hyperlink-in-a-tkinter-text-widget#:~:text=Tkinter%20Text%20widgets%20are%20generally,using%20HyperLinkManager%20snippet%20in%20Python.
    make_hyperlink(copymark, open_git)

#----

def get_file_val(num):
    global current_file

    current = open(current_file)
    content = current.readlines()
    return str(content[num-1]).strip()

#----

def write_file_val(widget, line):
    global current_file

    #Get the written contents from the entry box 
    new = widget.get()
    current = open(current_file)
    content = current.readlines()
    content[line-1] = str(new) + '\n'
    current.close()

    # and write everything back
    with open(current_file, 'w') as file:
       file.writelines(content)


#---
       
def change_current_file():
    global current_file, entry_info

    #Toggle current_file

    if current_file == 'Ai_file1.txt':
        current_file = 'Ai_file2.txt'
    else:
        current_file = 'Ai_file1.txt'

    #Therefore - then reload all entry values
    row_num = 5
    #Pack the entry widgets
    for entry in entry_info:
        entry["widget"].grid(row=row_num, sticky=E)
        entry["widget"].delete(0, END)
        entry["widget"].insert(END, get_file_val(row_num-4))
        row_num += 1


    console_window.update()
    console_window.update_idletasks()

#-----
    
def update_personality_tag(White_Playing, Personality, wins):
    var = StringVar()
    if White_Playing:
        var = Personality + "   [Ai_file1] " #+ str(wins)
        white_option.delete("1.0","end")
        white_option.insert(END, var)
    else:
        var = Personality + "   [Ai_file2] " #+ str(wins)
        black_option.delete("1.0","end")
        black_option.insert(END, var)
    
def allow_highlighting():
    global UPDATE_OPT
    if UPDATE_OPT:
        UPDATE_OPT = False
    else:
        UPDATE_OPT = True
    print("I like colours")
    #raise NotImplementedError

def allow_utility():
    print("YAY")
    console_window.update()

def begin():
    global counter, command 
    command = reset_command()
    start_option.config(text = 'AI Enabled: Please do not change any values')
    counter = threading.Thread(target=count_down(), name="counter").start()

console()

def players():
    global White_Playing, board
    Time_Stamp = main.Time_Stamp
    player = main.player
    #print("-------------- players called ---------------------------", Time_Stamp, player)
    if main.player[pointer] != 'Human':
        #Perform ai actions
        print("------------------ CALLED AI -----------------------------")
        new_thread = threading.Thread(target=main.gameplay_loop((-1, -1), (-1, -1)), name="alt").start()

#Start the game
def start_game():
    print("STARTING GAME -----------------------------------------------")
    global White_Playing 
    console()
    draw_board()
    players()
    window.mainloop()


#Need to check for clicks

def on_click(event):
    command = [['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','',''],
               ['','','','','','','','']]
 

window.mainloop()

#TK progress bar
# https://stackoverflow.com/questions/13510882/how-to-change-ttk-progressbar-color-in-python






