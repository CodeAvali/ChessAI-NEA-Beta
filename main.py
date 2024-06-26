#Main.py - Chess AI educational demonstration
#This is the shell of the chess AI program; which GUI.py calls from. 

import numpy as np, Moves_Inital, copy, GUI, threading, time, sys
from timeit import default_timer as timer
import GUI
import random
global board, White_Playing, White_moves, Black_moves, Moves_Tuple, Blocked_Tuple, Time_Stamp, MAX, MIN, move_from, move_to, utility
White_moves, Black_moves = [], []
space = ' '
MAX, MIN = 100000000000, -10000000000
QUEEN_VALUE, ROOK_VALUE, BISHOP_VALUE, KNIGHT_VALUE, PAWN_VALUE = 9, 5, 3, 3, 1

# (2) --------- Essential Functions ------------

def turn(Time_Stamp):
  #INDEPENDENT: Determines the current players turn, depending on time_stamp; and loads Moves_Tuple
  
  if Time_Stamp % 2 == 1: 
    Moves_Tuple = Black_moves
    return False, Moves_Tuple
  else:
    Moves_Tuple = White_moves
    return True, Moves_Tuple

  #----

def load(x_value, y_value, create, data_holder):
  global White_moves, Black_moves, White_Playing, flag_map
  #INDEPENDENT: Shorthand for creating an action when needed

  temp = (x_value, y_value)
  temp = (create, tuple(temp))
  data_holder.append(temp)

  return data_holder

#----

def perform(move_to, move_from, board):
  global White_moves, Black_moves
  #Perform the required action - Clean and call forth explosion system

  Moves_Tuple, has_captured = [], False
  
  #We should check for a castling move
  if CODE_CONVERT[board[move_from[1]][move_from[0]]][2:6] == "King":
    identify_castle(move_to, move_from)
  

  #Performing moves
  score = get(move_to, move_from)
  peice = board[move_from[1]][move_from[0]]  #Collect moving peice into temp variable 
  board[(move_from[1])][(move_from[0])] = Empty_  #Remove moving peice
  board[(move_to[1])][(move_to[0])] = peice #Hence, write the peice into the location 

  #Hence; store new to respective holder
  if White_Playing:                       
    White_moves = clean(move_from, White_moves)
    White_moves = clean(move_to, White_moves)
    Black_moves = clean(move_to, Black_moves)        
    Black_moves = clean(move_from, Black_moves)
  else:  #Otherwise; black player
    Black_moves = clean(move_from, Black_moves)
    Black_moves = clean(move_to, Black_moves)
    White_moves = clean(move_to, White_moves)           
    White_moves = clean(move_from, White_moves)

  return board

  #----

def identify_castle(move_to, move_from):
  #White cases
  if move_from == (4, 7) and board[move_from[1]][move_from[0]] == W_King:
    #Queenside
    if move_to == (6, 7):
      perform_castle((7, 7), (5, 7), True)
    #Kingside
    if move_to == (2, 7):
      perform_castle((0, 7), (3, 7), True)

  #Black cases
  if move_from == (4, 0) and board[move_from[1]][move_from[0]] == B_King:
    
    #Queenside
    if move_to == (2, 0):
      perform_castle((0, 0), (3, 0), False)
    #Kingside
    if move_to == (6, 0):
      perform_castle((7, 0), (5, 0), False)


def perform_castle(move_from, move_to, for_white):
  #Therefore - given the conditions - perform a simple move
  board[move_from[1]][move_from[0]] = Empty_
  board[move_to[1]][move_to[0]] = W_Rook if for_white else B_Rook
  castling_permisions[0 if for_white else 1] = False

#----

def get(move_to, move_from):
  global board, White_moves, Black_moves, Playing, message, has_captured, restlessness

  captured = board[move_to[1]][move_to[0]] #get captured peice
  capturing = board[move_from[1]][move_from[0]]

  if captured == W_En_Passant_Token:
    if capturing == B_Pawn:
      board[4][move_to[0]] = Empty_
      White_moves = clean((move_to[0], 4), White_moves)
  elif captured == B_En_Passant_Token:
    if capturing == W_Pawn:
      board[3][move_to[0]] = Empty_
      Black_moves = clean((move_to[0], 3), Black_moves)
  
  #Check otherwise for a capture for restlessness
  if captured != Empty_:
    restlessness = 0
    has_captured = True

  #----

def promotion(move_to, move_from, current_board):
  global board, White_moves, Black_moves

  #assuming pawn peice has allready been checked
  peice = board[move_from[1]][move_from[0]]

  if move_to[1] == 0:  #Then, white pawn promotion
    current_board[1][move_from[0]] = W_Quee
  elif move_to[1] == 7: #Black, pawn promotion 
    current_board[6][move_from[0]] = B_Quee   

  return current_board

  #Will implement peice choice later - just assuming queen for completeness. 

# (3) --------- Movement properties -----------

def property(move_to, peice, Moves_Tuple):
  global White_Playing
  #MAIN: Calls forth movement properties; to return legal moves etc

  if peice in (W_Pawn, B_Pawn):
    Moves_Tuple += pawn((move_to[0], move_to[1]), White_Playing)
  elif peice in (W_Knig, B_Knig):
    Moves_Tuple += knight((move_to[0], move_to[1]), False)
  elif peice in (W_Rook, B_Rook):
    Moves_Tuple += straight((move_to[0], move_to[1]), False)
  elif peice in (W_Bish, B_Bish):
    Moves_Tuple += diagonal((move_to[0], move_to[1]), False)
  elif peice in (W_Quee, B_Quee):
    Moves_Tuple += diagonal((move_to[0], move_to[1]), False)
    Moves_Tuple += straight((move_to[0], move_to[1]), False)
  elif peice in (W_King, B_King): 
    Moves_Tuple += adjecent((move_to[0], move_to[1]))

  return Moves_Tuple

  #----

def pawn(create, White_Playing):

  global blocked_trait, board
  #from inital, collect the x and y components 

  create_x, create_y = create[0], create[1]

  #Hence, create a tuple containing new moves 

  new = []

  #Directly forward moves; only 1 square
  if create_y - 1 >= 0:
    if (White_Playing) and (board[create_y - 1][create_x] not in PEICE):
      new = load(create_x, create_y - 1, create, new)
  if create_y + 1 <= 7:
    if (not White_Playing) and (board[create_y + 1][create_x] not in PEICE):
       new = load(create_x, create_y + 1, create, new)

  #Handle starting space 2 move rule 

  if (White_Playing and create_y == 6) and (board[4][create_x] not in PEICE) and (board[5][create_x] not in PEICE): 
    new = load(create_x, 4, create, new)
  if (not White_Playing) and (create_y == 1) and (board[3][create_x] not in PEICE) and (board[2][create_x] not in PEICE):
    new = load(create_x, 3, create, new)

  #Handle diagional captures
    
  for delta_x in [-1, 1]:
    new_x = create_x + delta_x
    if 0 <= new_x < 8:
      for delta_y in [-1, 1]:
        new_y = create_y + delta_y
        if 0 <= new_y < 8 and ((White_Playing and board[new_y][new_x] in BLACK and delta_y == -1) or
          (not White_Playing and board[new_y][new_x] in WHITE and delta_y == 1)):
          new = load(new_x, new_y, create, new)
    
  return new  

  #----

def straight(create, gen):
  global Blocked_Tuple, Attack_Tuple, Protected_Tuple

  Blocked_Tuple = []
  Attack_Tuple = []
  Protected_Tuple = []
  #from inital, collect the x and y components

  create_x, create_y = create[0], create[1]

  #Hence, create a tuple of new moves

  new = []

  x_pointer = create_x
  while x_pointer < 7 and not(blocked(create, x_pointer + 1, create_y)):
    x_pointer += 1
    new = load(x_pointer, create_y, create, new)
  x_pointer = create_x
  while x_pointer > 0 and not(blocked(create, x_pointer - 1, create_y)):
    x_pointer -= 1 
    new = load(x_pointer, create_y, create, new)
  y_pointer = create_y 
  while y_pointer < 7 and not(blocked(create, create_x, y_pointer + 1)):
    y_pointer += 1
    new = load(create_x, y_pointer, create, new)
  y_pointer = create_y
  while y_pointer > 0 and not(blocked(create, create_x, y_pointer - 1)): 
    y_pointer -= 1 
    new = load(create_x, y_pointer, create, new)

  if gen:
    #Can cleanout bishop/knight peices for optimisation - CHECK TO SEE IF APPROVED 
    new = []
    for i in range(len(Blocked_Tuple)):
      if board[Blocked_Tuple[i][1][1]][Blocked_Tuple[i][1][0]] not in straight_optimised:
        temp = (move_from, tuple(Blocked_Tuple[i][1]))                                          #move_from
        new.append(temp)
    return new
  else:
    new += Attack_Tuple
    return new
  
  #----

def diagonal(create, gen):#

  #start = timer()
  global Blocked_Tuple, Attack_Tuple, Protected_Tuple
  Blocked_Tuple = []
  Attack_Tuple = []
  Protected_Tuple = []

  #Hence, create a tuple of new moves
  new = []
  create_x, create_y = create[0], create[1]


  x_pointer, y_pointer = create_x, create_y
  while (x_pointer < 7 and y_pointer < 7) and not blocked(create, x_pointer + 1, y_pointer + 1): 
    x_pointer += 1
    y_pointer += 1 
    new = load(x_pointer, y_pointer, create, new)
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer > 0 and y_pointer < 7) and not blocked(create, x_pointer - 1, y_pointer + 1):
    x_pointer -= 1
    y_pointer += 1 
    new = load(x_pointer, y_pointer, create, new)
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer < 7 and y_pointer > 0) and not blocked(create, x_pointer + 1, y_pointer - 1):
    x_pointer += 1
    y_pointer -= 1
    new = load(x_pointer, y_pointer, create, new)
  x_pointer, y_pointer = create_x, create_y 
  while (x_pointer > 0 and y_pointer > 0) and not blocked(create, x_pointer - 1, y_pointer - 1):
    x_pointer -= 1
    y_pointer -= 1
    new = load(x_pointer, y_pointer, create, new)

  if gen:
    #Can cleanout bishop/knight peices for optimisation - CHECK TO SEE IF APPROVED 
    new = []
    for i in range(len(Blocked_Tuple)):
      if board[Blocked_Tuple[i][1][1]][Blocked_Tuple[i][1][0]] not in diagonal_optimised:
        temp = (move_from, tuple(Blocked_Tuple[i][1]))                                          #move_from
        new.append(temp)
    return new
  else:
    new += Attack_Tuple
    return new 
  
  #---

def knight(create, gen):
    
    #start = timer() 

    create_x, create_y = create[0], create[1]
    deltas = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]

    new, Blocked_Tuple = [], []

    for dx, dy in deltas:
        new_position = (create_x + dx, create_y + dy)
        if 0 <= new_position[0] < 8 and 0 <= new_position[1] < 8:
            if not own(create, new_position):
                new = load(new_position[0], new_position[1], create, new)
            else:
                Blocked_Tuple = load(new_position[0], new_position[1], create, Blocked_Tuple)

    if not gen:
      return new
    else:
      return Blocked_Tuple 

  #----

def own(move_from, move_to):
  create_move = board[move_from[1]][move_from[0]]
  create_location = board[move_to[1]][move_to[0]]

  if (create_move in WHITE) and (create_location in WHITE):
    return True
  elif (create_move in BLACK) and (create_location in BLACK):
    return True
  else:  
    return False 
    
#----

def adjecent(create):
    #....
    global W_moves, B_moves

    create_x, create_y, new = create[0], create[1], []
    deltas = [(1, 1), (0, 1), (-1, 1), (1, 0), (-1, 0), (1, -1), (0, -1), (-1, -1)]

    new = [list_load(create_x + dx, create_y + dy, create, new) for dx, dy in deltas if 0 <= create_x + dx < 8 and 0 <= create_y + dy < 8 and not own(create, (create_x + dx, create_y + dy))]

    #Check to see if castling is possible is the player still has castling permisions 
    if castling_permisions[0 if White_Playing else 1]:
      for_white = True if board[create_y][create_x] == W_King else False 
      new += castling(for_white, board)

    return new

  #----

def lazy_pin(board, White_Moves, Black_Moves, for_White):
  global move_from, move_to

  checked = []

  if for_White:
    #Perform each possible move; 
    for i in range(len(White_Moves)):
      temp, W_Moves, B_Moves = copy.deepcopy(board), copy.deepcopy(White_Moves), copy.deepcopy(Black_Moves)
      move_from, move_to = W_Moves[i][0], W_Moves[i][1]
      W_Moves, B_Moves, temp = ai_perform(W_Moves, B_Moves, W_Moves[i][0], W_Moves[i][1], temp)                        #W_Moves, B_Moves, temp = ai_perform(W_Move, B_Move, moves[i][0], moves[i][1], temp)
      #Given that; check to see if any of the opposing moves attack the White_King
      valid = True
      #B_Moves, none = OrderMoves(B_Moves, temp, False)
      for j in range(len(B_Moves)):
        if (B_Moves[j][0][0] == B_Moves[j][1][0]) and temp[B_Moves[j][1][1]][B_Moves[j][1][0]] == "B_Pawn":
          continue 
        #Otherwise;
        elif temp[B_Moves[j][1][1]][B_Moves[j][1][0]] == W_King:
          valid = False

      #Therefore; if the move is still valid; append it to checked
      if valid:
        checked.append(White_Moves[i])

  if not for_White:
    #Perform each possible move;
    for i in range(len(Black_Moves)):
      temp, W_Moves, B_Moves = copy.deepcopy(board), copy.deepcopy(White_Moves), copy.deepcopy(Black_Moves)
      move_from, move_to = B_Moves[i][0], B_Moves[i][1]
      W_Moves, B_Moves, temp = ai_perform(W_Moves, B_Moves, B_Moves[i][0], B_Moves[i][1], temp)
      #Given that; check to see if any of the opposing moves attack the Black_King
      valid = True
      for j in range(len(W_Moves)):
        #Special case; pawns are not allowed to capture on thier starting double move 
        if (W_Moves[j][0][0] == W_Moves[j][1][0]) and temp[W_Moves[j][1][1]][W_Moves[j][1][0]] == "W_Pawn":
          continue 
        if temp[W_Moves[j][1][1]][W_Moves[j][1][0]] == B_King:
          valid = False

      #Therefore; if the move is still valid; append it to checked
      if valid:
        checked.append(Black_Moves[i])

  return checked 


#------

def list_load(x_value, y_value, create, data_holder):
  global White_moves, Black_moves, White_Playing, flag_map
  #INDEPENDENT: Shorthand for creating an action when needed

  temp = (x_value, y_value)
  temp = (create, tuple(temp))

  return temp
   
#------

def direct(create):
  new = []
  temp = (move_to, move_to)
  new.append(temp)
  return new

# (4) --------- Legal moves; expansions and validation

def legal(move_to, move_from, move_space): 
  # Validate that move is in moves_tuple

  for i in range(len(move_space)):
    if move_from == move_space[i][0]:
      if move_to == move_space[i][1]:
        return True #is present in 

  #otherwise;
  return False

  #----

def clean(delete, moves_structure):
    #...
    return [move for move in moves_structure if move[0] != delete]

  #----

def blocked(create, move_from_x, move_from_y):
  global Blocked_Tuple, Attack_Tuple, Protected_Tuple

  if (move_from_x < 0 or move_from_x > 7) or (move_from_y < 0 or move_from_y > 7):
    return True #Range check 

  destination = board[move_from_y][move_from_x]

  if (destination in EMPTY):
    return False #location is empty; not blocked

  Blocked_Tuple = load(move_from_x, move_from_y, create, Blocked_Tuple)
  if own(create, (move_from_x, move_from_y)):
    Protected_Tuple = load(move_from_x, move_from_y, create, Protected_Tuple)
  else:
    Attack_Tuple = load(move_from_x, move_from_y, create, Attack_Tuple)
  return True
    
  #----

def generate(move_from, move_to):
  #Create a list of affected peices 
  global White_moves, Black_moves, Blocked_Tuple
  #From the location; get all peices that have been affected

  locations, Blocked_Tuple = [], []

  #for moving_from
  locations += straight(move_from, True)
  locations += diagonal(move_from, True)       
  
  #for moving_to
  locations += straight(move_to, True)
  locations += diagonal(move_to, True)

  #for handling knight edge case
  locations += knight(move_from, True)
  locations += knight(move_to, True)

  #Do direct location
  locations += direct(move_to)

  #Otherwise; ensure that the opponents king is included
  #print(King_location)
  if White_Playing:
    locations = load(King_location[1][0], King_location[1][1], King_location[0], locations)
  else:
    locations += load(King_location[0][0], King_location[0][1], King_location[1], locations)

  return locations 

  #----

def explode(mapping, White_Moves, Black_Moves):
  global White_Playing
  #Hence, after generating a map of affected peices
  for i in range(len(mapping)):
    peice = board[mapping[i][1][1]][mapping[i][1][0]]
    if peice in WHITE:
      White_Playing = True
      White_Moves = clean(mapping[i][1], White_Moves)
      White_Moves = property(mapping[i][1], peice, White_Moves)
    elif peice in BLACK:
      White_Playing = False
      Black_Moves = clean(mapping[i][1], Black_Moves)
      Black_Moves = property(mapping[i][1], peice, Black_Moves)

  #Then, return new legal moves. 
  return White_Moves, Black_Moves

#----

def unique(duplicates):

  # intilize a null list
  unique_list = []

  # traverse for all elements
  for i in duplicates:
      # check if exists in unique_list or not
      if i not in unique_list:
          unique_list.append(i)

  return unique_list

#----

def passant_check(move_from, move_to, en_location):
  global board, White_Playing

  en_flag = False  #Use a boolean flag

  inital_y = move_from[1]
  final_y = move_to[1]
  
  #Check to see if pawn move is elegible for en_passant
  if (inital_y == 1 and final_y == 3) or (inital_y == 6 and final_y == 4): 
    if (move_from[0] - 1) >= 0:   #Do a range check 
      if board[final_y][move_from[0] - 1] in PAWN:
        en_flag = True
    if (move_from[0] + 1) <= 7:   #Opposite range check - prevent error.
      if board[final_y][move_from[0] + 1] in PAWN:
        en_flag = True     

  #If move is elegible for en_passant response, create respective token for player
  if en_flag:
    offset = int((move_from[1] - move_to[1]) / 2) + move_to[1]
    if White_Playing:
      board[offset][move_from[0]] = W_En_Passant_Token     
      en_location[0][0] = offset
      en_location[0][1] = move_from[0]
    else:
      board[offset][move_from[0]] = B_En_Passant_Token
      en_location[1][0] = offset
      en_location[1][1] = move_from[0]

  return en_location  #point to token location 

  #----

def insufficent_material(board):

  #Conditions for insufficent material
  #NO PAWNS
  #Both players have one of:
  #1. A lone king
  #2. A king and bishop
  #3. A king and up to two knights      #Hence just need to just check the number of bishops 
  
  bishops, immediate = [0,0], [W_Pawn, W_Rook, W_Quee, B_Pawn, B_Rook, B_Quee]

  for y in range(0, 8):
    for x in range(0, 8):

      if (board[y][x]) in immediate:
        return False  #Immediately as none of the conditions
      elif (CODE_CONVERT[board[y][x]])[2:6] == "Bish":
        if (CODE_CONVERT[board[y][x][0]])[0] == "W":
          bishops[0] += 1 
        else:
          bishops[1] += 1 
      
  #Hence - determine the overall result
      
  if (bishops[0]) != 2 and (bishops[1]) != 2:
    return True 
  else:
    return False
  

#----
  
def castling(for_white, board):
  #Generates legal castling moves

  rights = []

  if for_white:
    #Queenside
    if (board[7][4] == W_King) and (board[7][0]) == W_Rook:
      #Check that the other positions are empty
      if (board[7][3] == Empty_) and (board[7][2] == Empty_) and (board[7][1] == Empty_):                        
        rights = load(2, 7, (4, 7), rights)
    #Kingside
    if (board[7][4] == W_King) and (board[7][7] == W_Rook):
      if (board[7][5] == Empty_) and (board[7][6] == Empty_):
        rights = load(6, 7, (4, 7), rights)

  if not for_white:
    #King position as start (0, 4)

    #If conditions
    if (board[0][4] == B_King) and (board[0][0] == B_Rook):
      #Check that the other positions are empty - queenside 
      if (board[0][3] == Empty_) and (board[0][2] == Empty_) and (board[0][1] == Empty_):
        rights = load(2, 0, (4, 0), rights)
    if (board[0][4] == B_King) and (board[0][7] == B_Rook):
      if (board[0][5] == Empty_) and (board[0][6] == Empty_):
        rights = load(6, 0, (4, 0), rights)
  
  return rights

# (1) ---------- Loaded values

def reset():
  global board, Moves_Tuple, Blocked_Tuple, Protected_Tuple, Attack_Tuple, White_Moves, Black_Moves, en_location, en_flag, King_location, Checked, player, utility, restlessness, castling_permisions, Time_Stamp, White_Playing, White_moves, Black_moves

  time.sleep(1)
  board = [[B_Rook, B_Knig, B_Bish, B_Quee, B_King, B_Bish, B_Knig, B_Rook],
        [B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn], 
        [W_Rook, W_Knig, W_Bish, W_Quee, W_King, W_Bish, W_Knig, W_Rook]]

  global White_Moves, Black_Moves, castling_permisions 

  Moves_Tuple = []
  Blocked_Tuple = []
  Attack_Tuple = []
  Protected_Tuple = []
  White_Moves = copy.deepcopy(Moves_Inital.White_moves_original)
  Black_Moves = copy.deepcopy(Moves_Inital.Black_moves_original)
  White_moves = copy.deepcopy(Moves_Inital.White_moves_original)
  Black_moves = copy.deepcopy(Moves_Inital.Black_moves_original)

  en_location = [[-1, -1], [-1, -1]]    #first index array is used for White; 2nd index array is used for Black 
  en_flag = -1
  King_location = [[7, 4], [0, 4]]
  Checked = False
  utility = 0 
  restlessness = 0 

  castling_permisions = [True, True]
  White_moves, Black_moves = refresh_moves(White_moves, Black_moves, board)
  White_Moves, Black_Moves = White_moves, Black_moves
  store_it(White_moves, Black_moves)

  #Other

  if White_Playing:
    White_Playing = False
    Time_Stamp = 1
    GUI.pointer = 1
  else:
    White_Playing = True
    Time_Stamp = 0
    GUI.pointer = 0

  GUI.game_ongoing = False
  #Check if there is a value in Repeat_Option - repeat game if necessary
  GUI.repeat_game()


#---


def get_moves():
  global White_Moves, Black_Moves
  return White_Moves, Black_Moves
  
W_Pawn = '♟︎'
B_Pawn = '♙'
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

WHITE = [W_Pawn, W_Bish, W_Knig, W_Rook, W_Quee, W_King, W_En_Passant_Token]
BLACK = [B_Pawn, B_Bish, B_Knig, B_Rook, B_Quee, B_King, B_En_Passant_Token]
PEICE = [W_Pawn, W_Bish, W_Knig, W_Rook, W_Quee, W_King, B_Pawn, B_Bish, B_Knig, B_Rook, B_Quee, B_King]
KNIGHT = [W_Knig, B_Knig]
PAWN = [W_Pawn, B_Pawn]
EMPTY = [Empty_, W_En_Passant_Token, B_En_Passant_Token]
KING = [W_King, B_King]
straight_optimised = [W_Bish, B_Bish, Empty_]
diagonal_optimised = [W_Rook, B_Rook, Empty_]


board = [[B_Rook, B_Knig, B_Bish, B_Quee, B_King, B_Bish, B_Knig, B_Rook],
        [B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn], 
        [W_Rook, W_Knig, W_Bish, W_Quee, W_King, W_Bish, W_Knig, W_Rook]]

global White_Moves, Black_Moves, castling_permisions 

Moves_Tuple = []
Blocked_Tuple = []
Attack_Tuple = []
Protected_Tuple = []
White_Moves = copy.deepcopy(Moves_Inital.White_moves_original)
Black_Moves = copy.deepcopy(Moves_Inital.Black_moves_original)
en_location = [[-1, -1], [-1, -1]]    #first index array is used for White; 2nd index array is used for Black 
en_flag = -1
King_location = [[7, 4], [0, 4]]
Checked = False
player = ['Ai_file1.txt','Ai_file2.txt']     #CHANGE TO BE EMPTY STRING
utility = 0 
restlessness = 0 

castling_permisions = [True, True]
global total_nodes
total_nodes = 0
MG_SCALE = 1
EG_SCALE = 0




#----- AI TESTS

def ai_time():
  time.sleep(1)
  GUI.time[GUI.pointer] -= 1
  GUI.timer()


def ai_call():
  global White_moves, Black_moves, cap, Moves_Tuple
  #Create deepcopies 
  temp, W_moves, B_moves = copy.deepcopy(board), copy.deepcopy(White_moves), copy.deepcopy(Black_moves)

  #Get ai personality files from respective and start timing
  ai_load(White_Playing)
  start = time.time()

  #Create conditions for peice_value transitions
  global MG_SCALE, EG_SCALE
  EG_SCALE = min((END_GAME_TRANSITION / 100)* (Time_Stamp // 2), 1)
  MG_SCALE = max(0, 1 - EG_SCALE)

  global MAX, MIN, HAZE
  MAX, MIN, HAZE = 1000, -1000, (restlessness / RESTLESSNESS_FACTOR)**2
  cap = DEPTH
  

  #Pass to respective ai
  result = ai_personality(W_moves, B_moves, cap, Moves_Tuple, temp)
  move_from, move_to = (result[0][0], result[0][1]), (result[1][0], result[1][1])

  #Handle ai time back to GUI - and to terminate the game if the time has run out 
  total = round(time.time() - start)
  GUI.time[GUI.pointer] -= total

  #Finally, return back the chosen move 
  return move_from, move_to


#---


def ai_load(for_white):
  global QUEEN_VALUE, ROOK_VALUE, BISHOP_VALUE, KNIGHT_VALUE, PAWN_VALUE, PERSONALITY, DEPTH, RESTLESSNESS_FACTOR, END_GAME_TRANSITION, WINS, current_file

  if for_white:
    current_file = GUI.file[0]
    file = open(GUI.file[0], 'r') 
  else:
    current_file = GUI.file[1]
    file = open(GUI.file[1], 'r')

  PERSONALITY = str(file.readline().strip())
  DEPTH = max(1, round(float(file.readline().strip())))
  END_GAME_TRANSITION = float(file.readline().strip())
  RESTLESSNESS_FACTOR = max(1, round(float(file.readline().strip())))
  QUEEN_VALUE = float(file.readline().strip())
  ROOK_VALUE = float(file.readline().strip())
  BISHOP_VALUE = float(file.readline().strip())
  KNIGHT_VALUE = float(file.readline().strip())
  PAWN_VALUE = float(file.readline().strip())
  WINS = str(file.readline().strip())

  file.close()

#----

def ai_personality(W_moves, B_moves, cap, Moves_Tuple, temp):

    #Get personality
    current = PERSONALITY

    start = time.time()

    # Update the player tag is there is a change between current personality and player
    if current != player[0 if White_Playing else 1]:
      player[0 if White_Playing else 1] = str(current)
      GUI.update_personality_tag(White_Playing, player[0 if White_Playing else 1], WINS)

    #Hence, call the respective ai function
    if current == 'Human':
      return selected
    elif current == 'Mini_Max_Original':
        import algorithms.Mini_Max_Original
        result = algorithms.Mini_Max_Original.call(temp, W_moves, B_moves, White_Playing, cap)
    elif current == 'Mini_Max_Optimised':
        import algorithms.Mini_Max_Optimised
        result = algorithms.Mini_Max_Optimised.call(temp, W_moves, B_moves, White_Playing, MIN, MAX, cap)
    elif current == 'Random_Pick':
        import algorithms.Random_Pick
        result = algorithms.Random_Pick.call(Moves_Tuple)
    elif current == 'Order_Pick':
        import algorithms.Order_Pick
        result = algorithms.Order_Pick.call(board, Moves_Tuple)
    elif current == 'Mini_Max_Aware':
        import algorithms.Mini_Max_Iterative
        result = algorithms.Mini_Max_Iterative.call(temp, W_moves, B_moves, White_Playing, MIN, MAX, cap)
    #Additional ai personalities can simply be appended here:
    #//
    #//
    #//
    #//
    #-------------------------------------------------------
        
    print(time.time()-start, "TIME SPENT")
    
    #Then; return the produced move
    return result 

#-------

def reset_load(White_Playing):
  global current_file

  #Need to find and open respective file
  if White_Playing:
    current_file = GUI.file[0]
    file = open(current_file, 'r') 
  else:
    current_file = GUI.file[1]
    file = open(current_file, 'r')

  #Get personality value
  current = str(file.readline().strip())

  #Need to check if current personality meets player
  if current != player[0 if White_Playing else 1]:
    player[0 if White_Playing else 1] = str(current)
    GUI.update_personality_tag(White_Playing, player[0 if White_Playing else 1], 0)


#-----

def attacking(Move_List):
  valid = []
  for move in range(len(Move_List)):
    if board[Move_List[move][1][1]][Move_List[move][1][0]] != Empty_:
      valid.append(Move_List[move])
  return valid 

#----
import random

def OrderMoves(Moves, temp, for_White):

  PIECE_VALUES = {
    'Pawn': PAWN_VALUE,
    'Knig': KNIGHT_VALUE,
    'Bish': BISHOP_VALUE,
    'Rook': ROOK_VALUE,
    'Quee': QUEEN_VALUE,
    'King': 2,   
    'pty_': 0,
    'En_P': 0 
  }

  CODE_CONVERT = {
    "♟︎": "W_Pawn",
    "♙": "B_Pawn",
    '♝': "W_Bish",
    '♗': "B_Bish",
    '♞': "W_Knig",
    '♘': "B_Knig",
    '♜': "W_Rook",
    '♖': "B_Rook",
    '♛': "W_Quee",
    '♕': "B_Quee",
    '♚': "W_King",
    '♔': "B_King",
    '_': "Empty_",
    '!': "W_En_Passant_Token",
    '?': "B_En_Passant_Token",
    '_': "Empty_"
  }

  moveScore = []
  for move in Moves:
    movingPeiceType = CODE_CONVERT[temp[move[0][1]][move[0][0]]]
    capturePeiceType = CODE_CONVERT[temp[move[1][1]][move[1][0]]]

    #Maximum Value Victim, Minimum Value Attacker - ordering secondary heuristic
    moveScoreGuess = (1 * PIECE_VALUES[movingPeiceType[2:6]])
    if capturePeiceType != Empty_:             
      moveScoreGuess += (-1 * PIECE_VALUES[movingPeiceType[2:6]]) + (7 * (PIECE_VALUES[capturePeiceType[2:6]]))

      #Additional development score - reward 'progressing'
      moveScoreGuess += (move[0][1] - move[1][1]) / 2 if for_White else (move[1][1] - move[0][1]) / 2

    #Should do a check that the king is not threatened
    #if capturePeiceType[2:6] == "King":
      #threat = True
    #...
      
    #Otherwise;
    moveScore.append(moveScoreGuess)

  sortedMoves = [Moves for _,Moves in sorted(zip(moveScore,Moves), reverse=True)]
  return sortedMoves


######################

global BISHOP, ROOK, QUEEN, scoring, PEICE_WEIGHTING 
BISHOP = [W_Bish, B_Bish]
ROOK = [W_Rook, B_Rook]
QUEEN = [W_Quee, B_Quee]

PEICE_WEIGHTING = {
             B_King: -1000, 
             B_Quee: -9,
             B_Rook: -5,
             B_Bish: -3, 
             B_Knig: -3,
             B_Pawn: -1,
             B_En_Passant_Token: -0.1, 
             W_King: 1000,
             W_Quee: 9,
             W_Rook: 5,
             W_Bish: 3, 
             W_Knig: 3, 
             W_Pawn: 1,
             W_En_Passant_Token: -0.1, 
             Empty_: 0
}

PEICE_VALUE_KEYWORDS = {
     "B_King": -100, 
     "B_Quee": -9,
     "B_Rook": -5,
     "B_Bish": -3,
     "B_Knig": -3,
     "B_Pawn": -1,
     "W_King": 100, 
     "W_Quee": 9,
     "W_Rook": 5,
     "W_Bish": 3, 
     "W_Knig": 3,
     "W_Pawn": 1,
     "W_En_Passant_Token": -0.2, 
     "B_En_Passant_Token": 0.2,
}

#----
global color_multiplier_dict, MOBILITY_FACTOR
color_multiplier_dict = {'W': 1, 'B': -1, 'E': 0}

MOBILITY_FACTOR = 8

def peice_square_optimised(board, W_Move, B_Move):
  score = (len(W_Move) - len(B_Move)) / MOBILITY_FACTOR

  PIECE_VALUES = {
    'Pawn': PAWN_VALUE,
    'Knig': KNIGHT_VALUE,
    'Bish': BISHOP_VALUE,
    'Rook': ROOK_VALUE,
    'Quee': QUEEN_VALUE,
    'King': 100,              
}
  
  PIECE_SQUARE_VALUES = { 
  'Pawn': [[ 350,   400,   450,   500,  500,   450,  400,  350],
           [98, 134,  61,  95,  68, 126, 34, -11 ],
           [-6,   7,  26,  31,  65,  56, 25, -20 ],
           [-14,  13,   6,  21,  49,  12, 17, -23],
           [-37,  -2,  -5,  22,  73,   6, 10, -40],                 #Changed to POTS evaluation as more discrete values :) - from chessprogramming wiki
           [-30,  -4,  -4, 20,   15,   3, 33, -26],
           [-35,  -1, -20, -23, -15,  24, 38, -22],
           [ 350,   400,   450,   500,  500,   450,  400,  350]],

  'Knig': [[-167, -89, -34, -49,  61, -97, -15, -107],
           [-73, -41,  72,  36,  23,  62,   7,  -17],
           [-47,  60,  37,  65,  84, 129,  73,   44],
           [-9,  17,  19,  53,  37,  69,  18,   22],
           [-13,   4,  16,  13,  28,  19,  21,   -8],
           [-23,  -9,  12,  10,  19,  17,  25,  -16],
           [-29, -53, -12,  -3,  -1,  18, -14,  -19],
           [-105, -21, -58, -33, -17, -28, -19,  -23]],

  'Bish': [[-29,   4, -81, -37, -25, -42,   7,  -8],
           [-26,  16, -18, -13,  30,  59,  18, -47],
           [-16,  37,  43,  40,  35,  50,  37,  -2],
           [-4,   5,  19,  50,  37,  37,   7,  -2],
           [-6,  13,  13,  26,  34,  12,  10,   4],
           [0,  15,  15,  15,  14,  27,  18,  10],
           [4,  15,  16,   0,   7,  21,  33,   1],
           [-33,  -3, 0, -21, -13, 0, -39, -21]],

  'Rook': [[32,  42,  32,  51, 63,  9,  31,  43],
     [27,  32,  58,  62, 80, 67,  26,  44],
     [-5,  19,  26,  36, 17, 45,  61,  16],
    [-24, -11,   7,  26, 24, 35,  -8, -20],
    [-36, -26, -12,  -1,  9, -7,   6, -23],
    [-45, -25, -16, -17,  3,  0,  -5, -33],
    [-44, -16, -20,  -9, -1, 11,  -6, -71],
    [-19, -29,   1,  17, 16,  7, -45, -26]],

  'Quee': [[-28,   0,  29,  12,  59,  44,  43,  45],
    [-24, -39,  -5,   1, -16,  57,  28,  54],
    [-13, -17,   7,   8,  29,  56,  47,  57],
    [-27, -27, -16, -16,  -1,  17,  -2,   1],
    [ -9, -26,  -9, -10,  -2,  -4,   3,  -3],
    [-14,   2, -11,  -2,  -5,   2,  14,   5],
    [-35,  -8,  11,   2,   8,  15,  -3,   1],
    [-1, -18,  -9,  10, -15, -25, -31, -50]],

  'King' : [[-0.65,  0.23,  0.16, -0.15, -0.56, -0.34,   0.02,  0.13],
     [0.29,  -0.01, -0.2,  -0.07,  -0.08,  -0.04, -0.38, -0.29],
     [-0.09,  0.24,   0.02, -0.16, -0.20,   0.06,  0.22, -0.22],
    [-0.17, -0.2, -0.12, -0.27, -0.3, -0.25, -0.14, -0.36],
    [-0.49,  -0.01, -0.27, -0.39, -0.46, -0.44, -0.33, -0.51],
    [-1.4, -1.4, -2.2, -4.6, -4.4, -3.0, -1.5, -2.7],
    [  0.1,   0.7,  -0.8, -6.4, -4.3, -1.6,   0.9,   0.8],
    [-1.5,  3.6,  4.2, -5.4,   0.8, -2.8,  4.2,  1.4]],
  }  

  PEICE_SQUARE_VALUES_EG = {
  'Pawn': [[450, 500, 550, 600, 600, 550, 500, 450, 350],
           [350,   400,   450,   500,  500,   450,  400,  350],
           [178, 173, 158, 134, 147, 132, 165, 187],
           [94, 100,  85,  67,  56,  53,  82,  84],
           [32,  24,  13,   5,  -2,   4,  17,  17],
           [4,   7,  -6,   1,   0,  -5,  -1,  -8],
           [-1, 3, -11, -4, -5, -10, -6, -13],
           [450, 500, 550, 600, 600, 550, 500, 450, 350]],

  'Knig': [[-58, -38, -13, -28, -31, -27, -63, -99],
           [-25,  -8, -25,  -2,  -9, -25, -24, -52],
           [-24, -20,  10,   9,  -1,  -9, -19, -41],
           [-17,   3,  22,  22,  22,  11,   8, -18],
           [-18,  -6,  16,  25,  16,  17,   4, -18],
           [-23,  -3,  -1,  15,  10,  -3, -20, -22],
           [-42, -20, -10,  -5,  -2, -20, -23, -44],
           [-29, -51, -23, -15, -22, -18, -50, -64]],

  'Bish': [[-14, -21, -11,  -8, -7,  -9, -17, -24],
           [-8,  -4,   7, -12, -3, -13,  -4, -14],
           [2,  -8,   0,  -1, -2,   6,   0,   4],
           [-3,   9,  12,   9, 14,  10,   3,   2],
           [-6,   3,  13,  19,  7,  10,  -3,  -9],
           [-12,  -3,   8,  10, 13,   3,  -7, -15],
           [-14, -18,  -7,  -1,  4,  -9, -15, -27],
           [-23,  -9, -23,  -5, -9, -16,  -5, -17]],

  'Rook': [[13, 10, 18, 15, 12,  12,   8,   5],
           [11, 13, 13, 11, -3,   3,   8,   3],
           [7,  7,  7,  5,  4,  -3,  -5,  -3],
           [4,  3, 13,  1,  2,   1,  -1,   2],
           [3,  5,  8,  4, -5,  -6,  -8, -11],
           [-4,  0, -5, -1, -7, -12,  -8, -16],
           [-6, -6,  0,  2, -9,  -9, -11,  -3],
           [-9,  2,  3, -1, -5, -13,   4, -20]],

  'Quee': [[-9,  22,  22,  27,  27,  19,  10,  20],
           [-17,  20,  32,  41,  58,  25,  30,   0],
           [-20,   6,   9,  49,  47,  35,  19,   9],
           [3,  22,  24,  45,  57,  40,  57,  36],
           [-18,  28,  19,  47,  31,  34,  39,  23],
           [-16, -27,  15,   6,   9,  17,  10,   5],
           [-22, -23, -30, -16, -16, -23, -36, -32],
           [-33, -28, -22, -43,  -5, -32, -20, -41]],

  'King': [[-0.74, -0.35, -0.18, -0.18, -0.11, 0.15, 0.04, -0.17],
           [-0.12, 0.17, 0.14, 0.17, 0.17, 0.38, 0.23, 0.11],
           [0.1, 0.17, 0.23, 0.15, 0.3, 0.45, 0.44, 0.13],
           [-0.08, 0.22, 0.24, 0.15, 0.2, 0.45, 0.44, 0.13],
           [-0.18, -0.04, 0.21, 0.24, 0.27, 0.23, 0.09, -0.11],
           [-0.19, -0.03, 0.11, 0.21, 0.23, 0.16, 0.07, -0.09],
           [-0.27, -0.11, 0.04, 0.13, 0.14, 0.04, -0.05, -0.17],
           [-0.53, -0.34, -0.21, -0.11, -0.28, -0.14, -0.24, -0.43]]
  }

  for y, row in enumerate(board):
    for x, piece_code, in enumerate(row):
      peice = CODE_CONVERT[piece_code]
      color_multiplier = color_multiplier_dict[peice[0]]

      if peice[2:6] in PIECE_SQUARE_VALUES:
        #score = ((PIECE_SQUARE_VALUES[peice[2:6]][y if (color_multiplier == 1) else (7 - y)][x] + 100) * (MG_SCALE / 10)) + ((PEICE_SQUARE_VALUES_EG[peice[2:6]][y if (color_multiplier == 1) else (7 - y)][x] + 100) * (EG_SCALE / 10)) * color_multiplier * PIECE_VALUES[peice[2:6]]
        #print(score, peice[2:6])

        factor = (PIECE_SQUARE_VALUES[peice[2:6]][y if (color_multiplier == 1) else (7-y)][x] + 100) * (MG_SCALE)
        factor_EG = (PEICE_SQUARE_VALUES_EG[peice[2:6]][y if (color_multiplier == 0) else (7-y)][x] + 100) * (EG_SCALE)
        combined = (factor + factor_EG) / 100
        score += (color_multiplier * PIECE_VALUES[peice[2:6]]) * combined
        #print(peice[2:6], score, factor, factor_EG, combined)
  
  return score 

#----

CODE_CONVERT = {
  "♟︎": "W_Pawn",
  "♙": "B_Pawn",
  '♝': "W_Bish",
  '♗': "B_Bish",
  '♞': "W_Knig",
  '♘': "B_Knig",
  '♜': "W_Rook",
  '♖': "B_Rook",
  '♛': "W_Quee",
  '♕': "B_Quee",
  '♚': "W_King",
  '♔': "B_King",
  '_': "Empty_",
  '!': "W_En_Passant_Token",
  '?': "B_En_Passant_Token",
  '_': "Empty_"
}

#-----------

def ai_perform(W_Moves, B_Moves, move_from, move_to, temp):
  global White_Playing, board                                                       
  holder, board = board, temp

  #Need to perform the move, like normally as in perform()
  peice = board[move_from[1]][move_from[0]]  
  board[(move_from[1])][(move_from[0])] = Empty_  
  board[(move_to[1])][(move_to[0])] = peice 

  #Hence; we should clean out the respective move set
  W_Moves = clean(move_from, W_Moves)
  W_Moves = clean(move_to, W_Moves)
  B_Moves = clean(move_to, B_Moves)
  B_Moves = clean(move_from, B_Moves)

  #Need to check for en_passant in pawn moves
  if temp[move_from[1]][move_from[0]] in PAWN:
    en_location = passant_check(move_from, move_to, en_location)
    #Likewise, if pawn check for promotion
    board = promotion(move_to, move_from, board)
  
  #Generate new legal moves
  map = generate(move_to, move_from) 
  W_Moves, B_Moves = explode(map, W_Moves, B_Moves)

  #Return to the original values of the ai
  temp, board = board, holder
  return W_Moves, B_Moves, temp

#-----

def restless(has_captured, pawn_move):
  global restlessness 
  restlessness += 1 #Increment restlessness
  #Then just need to check that a move is not a capture 
  if pawn_move:
    restlessness = 0 

  
#----

def bad_evaluate(temp, W_Moves, B_Moves):

  score = (len(W_Moves) - len(B_Moves)) / 10

  PEICE_VALUES = {
    'Pawn': 1,
    'Knig': 3,
    'Bish': 3,
    'Rook': 5,
    'Quee': 9,
    'King': 100,
  }

  score = 0
  for y, row in enumerate(board):
    for x, peice_code in enumerate(row):
      peice = CODE_CONVERT[peice_code]
      color_multipler = color_multiplier_dict[peice[0]]
      #Then add to score if peice
      if peice[2:6] in PEICE_VALUES:
        score += color_multipler * PEICE_VALUES[peice[2:6]]

  return score 
  

##############################

def squareUnderAttack(location, attacking):
  #Determine if the current square is under attack 
  for move in enumerate(attacking):
    y_location, x_location = move[1][1][1], move[1][1][0]
    if (y_location, x_location) == location:
      return True
  return False

#=============================


def store_it(White_moves, Black_moves):
  global White_Moves, Black_Moves
  White_Moves, Black_Moves = White_moves, Black_moves

#----

def open_it():
  global White_Moves, Black_Moves
  return White_Moves, Black_Moves


#----

def king_attacked(Opposing_moves, board):
  for i in range(len(Opposing_moves)):
    if CODE_CONVERT[board[Opposing_moves[i][1][1]][Opposing_moves[i][1][0]]][2:6] == "King":
      return True
  return False


def refresh_moves(White_moves, Black_moves, board):
  #Helper function to recreate all moves when a player is no longer in check - Should note this is NOT IDEAL. Manually calls a mapping for ALL positions

  map = []
  #Create a mapping for all positions 
  for i in range(0, 8):
    for j in range(0, 8):
      if board[j][i] != Empty_:

        map = load(i, j, (i, j), map)

  White_moves, Black_moves = explode(map, White_moves, Black_moves)

  return White_moves, Black_moves 

# (5) --------- Main gameplay loop

White_Playing = True 
Time_Stamp = 0

global White_Threatened, Black_Threatened
White_Threatened, Black_Threatened = False, False 

def gameplay_loop(click1, click2):
  global Time_Stamp, board, en_location, move_from, move_to, tot, White_Playing, Moves_Tuple, White_moves, Black_moves, White_Moves, Black_Moves, has_captured, White_Threatened, Black_Threatened, selected
  White_moves, Black_moves = open_it()
  pawn_move, has_captured = False, False
  selected = (click1, click2)

  if not GUI.finished:
    #Pass the turn to the next player                     #Temp fix need to fix bug

    White_Playing, Moves_Tuple = turn(Time_Stamp)
    White_Playing = GUI.bool_pointer(GUI.pointer)
    print(White_Playing)
    Time_Stamp += 1

    #Need to check for Stalemate
    if len(Moves_Tuple) == 0:
      GUI.stalemate()
      return 0
  
    # Asking the user for a move
    Valid = False
    map = []
  
    if not Valid:

      move_from, move_to = click1, click2
    
      #Get the input - determine if current player is human or AI
      if player[(Time_Stamp - 1) % 2] == 'Human':

        move_from, move_to = click1, click2
      
      else:
        holder = board
        move_from, move_to = ai_call()
        board = holder 

        if GUI.time[GUI.pointer] < 0:
          GUI.finish()
          return None 

      #Perform exceptions; 
      Valid = legal(move_to, move_from, Moves_Tuple)
      
    if Valid:

      #Check to see if the move is elegible for enpassant 
      if board[move_from[1]][move_from[0]] in PAWN:
        en_location = passant_check(move_from, move_to, en_location)
        #Likewise, if pawn check for promotion
        board = promotion(move_to, move_from, board)
        pawn_move = True 

      #Increment restlessness for 50 move counter
      restless(has_captured, pawn_move)
        
      #Printing inputs
  
      board = perform(move_to, move_from, board)    
      map += generate(move_to, move_from)

      if (White_Playing) and board[en_location[1][0]][en_location[1][1]] == B_En_Passant_Token:
        board[en_location[1][0]][en_location[1][1]] = Empty_
      if (not White_Playing) and board[en_location[0][0]][en_location[0][1]] == W_En_Passant_Token:
        board[en_location[0][0]][en_location[0][1]] = Empty_

      map = unique(map)

      White_moves, Black_moves = explode(map, White_moves, Black_moves)

      if board[move_to[1]][move_to[0]] in KING: 
        if White_Playing:
          King_location[0][1] = move_to[0]
          King_location[0][0] = move_to[1]
        else:
          King_location[1][1] = move_to[0]
          King_location[1][0] = move_to[1]
          
      map = []
      map = load(King_location[1][1], King_location[1][0], King_location[1], map)
      map = load(King_location[0][1], King_location[0][0], King_location[0], map)
      White_moves, Black_moves = explode(map, White_moves, Black_moves)

      if restlessness >= 50:
        #50 non-progressing moves have occured
        GUI.fifty_moves()
        return None
      else:
        GUI.draw_board()

      print("----- PERFORMANCE CHECKS ------")            
      print("Complexity, white moves", len(White_moves))
      print("Complexity, black moves", len(Black_moves))

      new_White_Threatened, new_Black_Threatened = king_attacked(Black_moves, board), king_attacked(White_moves, board)
      if new_White_Threatened != White_Threatened:
        White_moves, Black_moves = refresh_moves(White_moves, Black_moves, board)
        White_Threatened = new_White_Threatened
      elif new_Black_Threatened != Black_Threatened:
        White_moves, Black_moves = refresh_moves(White_moves, Black_moves, board)
        Black_Threatened = new_Black_Threatened

      White_moves = OrderMoves(White_moves, board, True)
      Black_moves = OrderMoves(Black_moves, board, False)

      #Checkmate engine here - handles pinned moves; stalemate and checkmate
      
      if insufficent_material(board):
        GUI.insufficent()

      #Generate all legal moves =- checking for pinned peices
      White_valid, Black_valid = lazy_pin(board, White_moves, Black_moves, True), lazy_pin(board, White_moves, Black_moves, False)

      if len(White_valid) == 0:
        if king_attacked(Black_moves, board):
          GUI.checked(True)
          return None
        else:
          GUI.stalemate()
          return None 

      if len(Black_valid) == 0:
        #Need to see if the position is checkmate or not 
        if king_attacked(White_moves, board): 
          GUI.checked(False)
          return None 
        else:                                                                               
          GUI.stalemate()
          return None 
      
      White_Playing, Moves_Tuple = turn(Time_Stamp)
      
      store_it(White_valid, Black_valid)

      if White_Playing and GUI.pointer == 1:
        GUI.pointer = 0 
      elif not White_Playing and GUI.pointer == 0:
        GUI.pointer = 1

      utility = [peice_square_optimised(board, White_valid, Black_valid)]
      GUI.simple_update_utility(utility)

      GUI.locked = False

####################
## End of main.py ##