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
import time as delay


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
game_ongoing = False

global UTILITY_OPT
UTILITY_OPT = False

#Inital
window = Tk()  
window.geometry('650x640')
window.iconbitmap("Favicon/W_Pawn.ico")

display = Text(window, background='PaleTurquoise1', height=2, width=75, state=DISABLED)

s = Style()
s.theme_use('clam')
s.configure('yellow.Vertical.TProgressbar', foreground='purple', background='white')

utility = Progressbar(orient=VERTICAL, length=560, maximum=200, style='yellow.Vertical.TProgressbar')
utility.config(style='yellow.Vertical.TProgressbar')
utility.place(x=620, y=20, width=15)

#TROUGH_COLOR = 'white'
#BAR_COLOR = 'black'

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
    global White_Playing, board
    Time_Stamp = main.Time_Stamp
    player = main.player
    if main.player[pointer] != 'Human' and not locked:
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

global THOUGHT_OPT
THOUGHT_OPT = False

def lazy_update(utility_scores, current_processed):
    global performed 
    global THOUGHT_OPT, UTILITY_OPT
    performed = len(utility_scores)
    if not finished:
        #x = threading.Thread(target=update_window, args = ())
        #x.start()
        update_window()
    if THOUGHT_OPT:
        thought_highlighting(current_processed)
    if UTILITY_OPT:
        simple_update_utility(utility_scores)



def update_window():
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


def message_window():

    display.config(state='normal')

    display.tag_configure("tag_name", justify='center')
    display.tag_configure("timing", justify='left')
    display.delete("1.0",END)
    display.insert(END, message)
    display.insert(END, form(time))
    display.update()



    return NotImplementedError 
    


        


def simple_update_utility(utility_scores):
    ENLARGMENT_FACTOR = 10 + (0.05 * main.Time_Stamp)
    utility_value = (statistics.fmean(utility_scores) * ENLARGMENT_FACTOR) + 100
    #Need to ensure it lies within the range;
    if utility_value > 200:
        utility_value = 200
    elif utility_value < 0:
        utility_value = 0
    utility.stop()
    utility.step(utility_value)

    window.update_idletasks()

global flag
flag = False

def thought_highlighting(current_processed):
    global last_processed, command, flag

    #Check for first highlight case 
    if last_processed == None:
        last_processed = current_processed
    
    #Efficnecy improvements - end if not necessary
    elif current_processed == last_processed and flag:
        return -1 

    flag = False

    #Otherwise; perform highlighting for AI thought 
    command = reset_command()
    if current_processed != None:
        command[last_processed[1][1]][last_processed[1][0]] = "PROCESSED"
        command[last_processed[0][1]][last_processed[0][0]] = ''
        if command[current_processed[1][1]][current_processed[1][0]] == "PROCESSED":
            command[current_processed[1][1]][current_processed[1][0]] = "ATTACK"
            command[current_processed[0][1]][current_processed[0][0]] = "SELECT"
            flag = True 
            
    #Then call draw_board() to display highlighting 
    last_processed = current_processed
    draw_board()


def on_click(event):
    locked = True
    global command, WHITE, BLACK, board, White_Playing
    board = main.board

    #Appropriate widget check 
    if str(event.widget) != '.!canvas':
        return -1

    #Get the cordinates for the command 
    x = event.x - (0.5 * SQUARE_SIZE)
    y = event.y - (0.5 * SQUARE_SIZE)
    #Then round to exact; 
    X_location = round((x / SQUARE_SIZE))
    Y_location = round(y / SQUARE_SIZE)
    print("CORDINATES", X_location, Y_location)
    #From there, check that this was not an 'action' click
    if command[Y_location][X_location] == "MOVE" or command[Y_location][X_location] == "ATTACK":
        #Perform the player's move; 
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
        White_Moves = main.White_Moves
        for i in range(len(White_Moves)):
            if command[White_Moves[i][0][1]][White_Moves[i][0][0]] == "SELECT": #That is the clicked peice; 
                command[White_Moves[i][1][1]][White_Moves[i][1][0]] = "MOVE"
                if board[White_Moves[i][1][1]][White_Moves[i][1][0]] in BLACK:
                    command[White_Moves[i][1][1]][White_Moves[i][1][0]] = "ATTACK"

    #For the Black Player
    if board[Y_location][X_location] in BLACK:
        Black_Moves = main.Black_Moves
        for i in range(len(Black_Moves)):
            if command[Black_Moves[i][0][1]][Black_Moves[i][0][0]] == "SELECT": #That is the clicked peice; 
                command[Black_Moves[i][1][1]][Black_Moves[i][1][0]] = "MOVE"
                if board[Black_Moves[i][1][1]][Black_Moves[i][1][0]] in WHITE:
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
            #print(row, col)
            x1 = col * SQUARE_SIZE
            y1 = row * SQUARE_SIZE
            x2 = x1 * SQUARE_SIZE
            y2 = y1 * SQUARE_SIZE
            #Check for the zero case
            if x1 == 0:
                x2 = SQUARE_SIZE
            if y1 == 0:
                y2 = SQUARE_SIZE
            #Determine board colours - If forced by command 
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
    #locked = False
    window.update_idletasks()

    #Hence - or otherwise, get the next player to play - which should be automatic if AI
    #colors = ["white","grey"]


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
      if main.player[pointer] != 'Human' and not finished:
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
        display.config(background='Black', foreground = 'Black')
    finished = True


def checked(for_White):
    global message, finished
    print("CHECKMATE ------------------------------------------------------")
    print("CHECKMATE ----------------------------------------")
    finished = True
    if for_White:
        message = 'White has been checkmated'
        display.config(background='Black', foreground = 'White')
    else:
        message = 'Black has been checkmated'
        display.config(background="White", foreground = 'Black')
    timer()

def fifty_moves():
    global message, finished
    message = 'DRAW: 50 moves rule'
    display.config(bg = 'grey45', fg = 'Black')
    finished = True
    timer()

def stalemate():
    global message, finished
    message = 'DRAW: Stalemate'
    display.config(bg = 'grey45', fg = 'Black')
    finished = True
    timer()


def insufficent():
    global message, finished
    message = 'DRAW: Insufficent material'
    display.config(bg = 'grey45', fg = 'White')
    finished = True
    timer()

def threefold_repetition():
    global message, finished
    message = 'DRAW: Three-fold repetition'
    display.config(bg = 'grey45', fg= 'Black')
    finished = True
    timer()

def default():
    global message, finished
    display.config(bg = 'PaleTurquoise1', fg= 'Black')
    finished = False
    timer()

def reseting():
    global message, finished, game_ongoing
    display.config(bg = 'grey45', fg= 'Black')
    message = "RESET THE GAME PLEASE - reseting"
    finished = True
    timer()


    

def timer():
    global finished, pointer, White_Moves, Black_Moves, game_ongoing


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

    if finished and game_ongoing:
        #update_wins(main.White_Playing)
        main.reset()
        window.update()
        #draw_board()   #Force starts a repeated game 
        finished = True
        game_ongoing = False
        #players()
    else:
        print("PLATERS CALLED VIA TIMER ")
        players()

def update_wins(for_White):
    if for_White:
        current_file = file[0]
    else:
        current_file = file[1]

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
    



    global console_window, entry_info, current_file, start_option, white_option, black_option, check, label_text, Time_Option, Repeat_Option, Change_file
    from tkinter import font 
    current_file = file[0]
    underline_font = font.Font(underline=TRUE, family="Helvetica",size=10)
    regular_font = font.Font(underline=FALSE, family="Helvetica",size=10)
    link_font = font.Font(underline=TRUE, family="Helevetica", size=10)



    console_window = Toplevel()
    console_window.title('ChessAi [Console]')
    console_window.geometry('320x640')
    start_option = Button(console_window, text = 'Start game?', command=begin, width=51)
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

    #Creating label
    label_text = StringVar()
    label = Label(console_window, textvariable=label_text, width=53, anchor=W, background=None) 
    label_text.set("Modifying White file...")

    #Checkbutton for file change
    check= Checkbutton(console_window,  text="Change current File", variable=label_text,
                   onvalue="Modifying Black file...", offvalue="Modifying White file...", command=change_current_file)

    #As using assignments, have to later push to position method
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

    #Combobox(console_window, width=30, state = "readonly", values=["Human","Random_Pick"]).grid(row=5, sticky=E)

    #

    entry_info = [
        {"widget": Combobox(console_window, width=30, state = "readonly", values=["Human","Random_Pick","Order_Pick","Mini_Max_Original","Mini_Max_Optimised","Mini_Max_Aware","AI_Created_1","AI_Created_2"]), "line": 1},
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
        if row_num == 5:
            #Combo-box widget
            entry["widget"].bind("<<ComboboxSelected>>", write_personality_val)
            index = get_combo_index()
            entry["widget"].current(index)
        entry["widget"].grid(row=row_num, sticky=E)
        if row_num != 5:
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
    highlighting_choice = StringVar()
    highlighting_choice.set('OFF')

    highlighting_option= Checkbutton(console_window, textvariable=highlighting_choice, variable=highlighting_choice, text="No AI highlighting", onvalue="AI Highlighting enabled (very costly)", offvalue="AI Highlighting disabled", command=allow_highlighting)
    highlighting_option.grid(row=17, sticky='W')

    utility_choice = StringVar()
    utility_choice= Checkbutton(console_window, textvariable=utility_choice, variable=utility_choice, onvalue="AI utility updates enabled - (costly)", offvalue="No Ai Utility updates", command=allow_utility)
    utility_choice.grid(row=18, sticky='W')

    #Inital Time option
    Label(console_window, text="Inital Time").grid(row=19, sticky='W')
    Time_Option = Entry(console_window, width=30)
    Time_Option.bind("<KeyRelease>", update_inital_time)
    Time_Option.grid(row=19, sticky='E')
    Time_Option.insert(0, 300)
    
    #Repeat option 
    Label(console_window, text="Repeated games").grid(row=20, sticky='W')
    Repeat_Option = Entry(console_window, width=30)
    Repeat_Option.grid(row=20, sticky='E')
    Repeat_Option.insert(0, 0)

    #Change associated file
    Label(console_window, text="Change file identifer").grid(row=21, sticky='W')
    Change_file = Entry(console_window, width=30)
    Change_file.bind("<KeyRelease>", update_file)
    Change_file.grid(row=21, sticky='E')
    Change_file.insert(0, file[0])


    #Handle links 
    import webbrowser

    def open_git():
        url = 'https://github.com/CodeAvali/ChessAI-NEA-Beta/blob/main/README.md?plain=1'
        webbrowser.open_new(url)


    #Ownership
    copymark = Label(console_window, width = 45, text="Made by CodeAvali -> To Github", font=regular_font, foreground="Blue")
    copymark.grid(row = 25, sticky='W', pady=155)                                       
    make_hyperlink(copymark, open_git)

#----
    
def update_file(event):
    global file, current_file

    #Need to verify that the file is legitmate and exists
    value = Change_file.get()
    valid = False

    try:
        current = open(value)
        valid = True
    except:
        valid = False

    #If valid, write to file 
    if current_file == file[0] and valid:
        file[0] = value
        current_file = value
    elif valid:
        file[1] = value
        current_file = value
        
    row_num = 5
    #Pack the entry widgets - to reload them 
    for entry in entry_info:
        if row_num == 5:
            #Combo-box widget
            index = get_combo_index()
            entry["widget"].current(index)
        if row_num != 5:
            entry["widget"].delete(0, END)
            entry["widget"].insert(END, get_file_val(row_num-4))
        row_num += 1

    
#-------



    
def update_inital_time(event):
    global Time_Option, time

    value = Time_Option.get()
    valid = True

    #Validation structure
    try:
        test = int(value)
    except:
        valid = False
    
    #Then update time or fix
    if valid:
        value = int(value)
        time[0] = value
        time[1] = value
    else:
        #Set as lazy 1
        Time_Option.delete(0,"")
        Time_Option.insert(0,1)







    
def get_combo_index():

    #Open file and read first line
    personality = get_file_val(1)

    #Iterate to find index - Linear search is applicable for a small number of options 
    values = ["Human","Random_Pick","Order_Pick","Mini_Max_Original","Mini_Max_Optimised","Mini_Max_Aware","AI_Created_1","AI_Created_2"]
    for index in range(0, len(values)-1):
        if str(values[index]) == personality:
            return index 
        
    return 0 #Otherwise; default to just human 

#----

def write_personality_val(event):
    global current_file, entry_info

    #Get the combo index and find value
    entry = entry_info[0]
    result = entry["widget"].get()

    print("PERSONALITY", result)

    #Given the known result - write to the file
    current = open(current_file)
    content = current.readlines()
    content[0] = str(result) + '\n'
    current.close()

    # And write everything back
    with open(current_file, 'w') as file:
        file.writelines(content)



def get_file_val(num):
    global current_file

    #Open file and read lines
    current = open(current_file)
    content = current.readlines()

    #Return respective line
    return str(content[num-1]).strip()

#----

def write_file_val(widget, line):
    global current_file

    #Get the written contents from the entry box 
    new = widget.get()
    print("WRITE CALLED", new, widget)
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

    if current_file == file[0]:
        current_file = file[1]
    else:
        current_file = file[0]

    #Therefore - then reload all entry values
    row_num = 5
    #Pack the entry widgets
    for entry in entry_info:
        if row_num == 5:
            index = get_combo_index()
            entry["widget"].current(index)
        #Normal case..
        entry["widget"].grid(row=row_num, sticky=E)
        entry["widget"].delete(0, END)
        entry["widget"].insert(END, get_file_val(row_num-4))
        row_num += 1

    Change_file.delete(0, END)
    Change_file.insert(0, current_file)


    console_window.update()
    console_window.update_idletasks()

#-----
    
def update_personality_tag(White_Playing, Personality, wins):
    var = StringVar()
    if White_Playing:
        var = Personality + "   [" + file_type_strip(main.current_file) + "]"
        white_option.delete("1.0","end")
        white_option.insert(END, var)
    else:
        var = Personality + "   [" + file_type_strip(main.current_file) + "]"
        black_option.delete("1.0","end")
        black_option.insert(END, var)

###
        
def repeat_game():
    #Code for repeated games - according to repeated_option widget
    value = Repeat_Option.get()
    valid = False
    #Validate for int, and above 0
    try:
        value = int(value)
        if value > 0:
            valid = True
    except:
        valid = False
    #Decrement widget value
    if valid == True:
        Repeat_Option.delete(0, END)
        Repeat_Option.insert(END,int(value)-1)
        #Start game again after delay
        delay.sleep(2)
        begin() 





def file_type_strip(string):
    return string.replace('.txt','')

#---
global file 
file = ['Ai_file1.txt','Ai_file2.txt']

def file_validated(address):

    # Required variables for valdiation
    current = open(file[address])
    content = current.readlines()
    failed = []

    for line in range(1, 9):
        #Attempt float conversion
        try:
            test = float(content[line])
        except:  
            failed.append(line + 1)

    if len(failed) >= 1:
        console_error(failed)
        #Prevent the AI from being enabled
        return False 
    else:
        #Allow the AI to be enabled 
        return True



def console_error(failed):

    # Replace non-float entries with 'FloatError' message
    increment = 0 

    for entry in entry_info:
        increment += 1
        if increment in failed:
            entry["widget"].delete(0, END)
            entry["widget"].insert(END, "FloatError")

        




    
def allow_highlighting():
    global THOUGHT_OPT, command 
    if THOUGHT_OPT:
        THOUGHT_OPT = False
        command = reset_command()
    else:
        THOUGHT_OPT = True
    print("I like colours")
    #raise NotImplementedError

def allow_utility():
    global UTILITY_OPT
    print("YAY")
    if UTILITY_OPT:
        UTILITY_OPT = False
    else:
        UTILITY_OPT = True
    print(UTILITY_OPT)
    console_window.update()

#----

def begin():
    global counter, command, check, game_ongoing, finished, current_file

    if game_ongoing:
        #Reset the game 
        finished = True
        game_ongoing = False
        start_option.config(text='Enable AI')
        #main.reset()
        #draw_board()   #ISSUE: Appears to have some 'memory' - 
    else:
      

      white_valid = file_validated(0)

      if not white_valid:
        if current_file == file[1]:
          check.invoke()
          file_validated(0)
      else: 
        #Check if black file is valid
        black_valid = file_validated(1)
        if white_valid and not black_valid:
            #Need to display black file - if on white
            if current_file == file[0]:
              check.invoke()
              file_validated(1)

        else:
          #Game can start
          game_ongoing = True
          finished = False
          command = reset_command()
          default()
          update_inital_time(0)

          #Should check that player is updated immediately
          main.reset_load(True)
          main.reset_load(False)
          




          start_option.config(text = 'AI Enabled: Press again to reset')
          counter = threading.Thread(target=count_down(), name="counter").start()
          #counter = Process(target=count_down(), name="counter").start()


console()

def players():
    global White_Playing, board
    Time_Stamp = main.Time_Stamp
    player = main.player
    if main.player[pointer] != 'Human' and game_ongoing:
        #Perform ai actions
        
        #main.after(10, threading.Thread(target=main.gameplay_loop((-1, -1), (-1, -1)), name="alt").start() )
        print("------------------ CALLED AI -----------------------------")
        #new_thread = Process(target=main.gameplay_loop((-1, -1), (-1, -1)), name="alt").start()
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






