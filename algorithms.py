# Algorithms - ChessAI educational demonstration
# This is the general programming file for the AI players; which can be read/modified
# Please see the Read.me for specific information on function calls 

import main, GUI
from copy import deepcopy
import time 

# ---- CONTENTS ----#
# (1) ==== Ai Caller ====
# (2) ==== General Ai 'Bookeeping' functions ====
# // (a). Ai_Perform 
# // (b). Adaptive_Ply
# (3) ==== Ai Evaluation functions ====
#// (a). Basic_Evaluate
#// (b). Dive_Minimax_Evaluate
#// (c). Peice_Map_Evaluate
#// (f1). Empty_Evaluate                         !! Block to create own Ai Evaluation Function !!
# (4) ==== Ai Bot Variations/Personalities ====
# // (a). Random_Ai                              ~Simply picks a random possible move
# // (b). Ideal_Pick                             ~Picks the immediately best move at 1 ply
# // (c). Mini_Max_Original                      ~Performs basic minimax at an adaptive ply
# // (d). Mini_Max_Optimised                     ~Minimax with alpha beta prunning; at adaptive ply
# // (e). Average_Friend                         ~Tree traversal optimising for best average value at adaptive ply
# // (f1). Empty_Personality                     !! Block to create own Ai Personality Function !!




#TO DO 
# 1 - REFACTOR ALL AI PERSONALITY FILES TO THIS FILE
# 2 - CREATE AI_CALL TO INSTEAD REPORT BACK UTILITY TO GUI FOR UTILITY BAR
# 3 - INTRODUCE A TIMED FACTOR - To enforce limits. 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# ==== (1) Ai Caller ==== # 

def ai_call():
  #global main.White_moves, main.Black_moves, main.cap, main.Moves_Tuple

  temp, W_moves, B_moves = deepcopy(main.board), deepcopy(main.White_moves), deepcopy(main.Black_moves)    #Create deepcopies of board                                                                           
  start = time.time()                                                                                      #For GUI - start taking time  
  global MAX, MIN, HAZE                                                                                    #Set variables 
  MAX, MIN, HAZE = 1000, -1000, 0.03 
  cap = Adaptive_Ply(W_moves, B_moves, 0)                                                                  #Set the value of cap for the AI
  #print("Running at", cap)
  result = ai_personality()                                                                                #Hence; call the respective ai function - depending on the current personality
  #print("AI RETURNED", result)
  move_from, move_to = (result[0][0], result[0][1]), (result[1][0], result[1][1])                          #Gather the chosen move 
  #print("MOVING", main.board[move_from[1]][move_from[0]], "TO:", main.board[move_to[1]][move_to[0]])
  end = time.time()                                                                                        #Return the time
  total = round(end - start)
  GUI.time[GUI.pointer] -= total
  p#rint(total, "TIME SPENT")

  #Force a call to end the game if this leads to a timeout 
  if GUI.time[GUI.pointer] < 0:
    GUI.finish()
    GUI.timer()

  #Otherwise - return chosen move as if a human action
  return move_from, move_to

#---

def ai_personality():

    #Get personality
    PERSONALITY = ['Avg','Opt']

    current = PERSONALITY[GUI.pointer]

    #Hence, call the respective ai function

    if current == 'Random_Pick':
        result = Random_AI()
    elif current == 'Ideal_Pick':
        result = Ideal_Pick()
    elif current == 'Mini_Max_Original':
        result = Mini_Max_Original()
    elif current == 'Mini_Max_Optimised':
        result = Mini_Max_Optimised()
    elif current == 'Average_Friend':
        result = Average_Friend()
    #Additional ai personalities can simply be appended here:
    #//
    #//
    #//
    #//
    #-------------------------------------------------------
    
    #Then; return the produced move
    return result 

    
# ==== (2) General Ai 'Bookeeping' functions ==== #


def ai_perform(W_Moves, B_Moves, move_from, move_to, temp):
  global White_Playing, board
  holder = board
  board = temp

  #Need to perform the move, like normally as in perform()
  peice = board[move_from[1]][move_from[0]]  #Collect moving peice into temp variable 
  board[(move_from[1])][(move_from[0])] = main.Empty_  #Remove moving peice
  board[(move_to[1])][(move_to[0])] = peice #Hence, write the peice into the location 

  #Hence; we should clean out the respective move set
  if peice in main.WHITE:
    White_Playing = True
    W_Moves = main.clean(move_from, W_Moves)
    W_Moves = main.clean(move_to, W_Moves)
    B_Moves = main.clean(move_to, B_Moves)
  elif peice in main.BLACK:
    White_Playing = False
    B_Moves = main.clean(move_from, B_Moves)
    B_Moves = main.clean(move_to, B_Moves)
    W_Moves = main.clean(move_to, W_Moves)
  
  #Pawn promotions are important for the end_game 
  if temp[move_from[1]][move_from[0]] in main.PAWN:
    #en_location = passant_check(move_from, move_to, en_location)
    #Likewise, if pawn check for promotion
    main.promotion(move_to, move_from)

  #print("LENGTH before", len(W_Moves), len(B_Moves))
  
  #Generate new legal moves
  map = main.generate(move_to, move_from) #rev
  W_Moves, B_Moves = main.explode(map, W_Moves, B_Moves)
  #print(len(W_Moves), len(B_Moves))

  #print("LENGTH after", len(W_Moves), len(B_Moves))
  board = holder

  return W_Moves, B_Moves, temp

#----

def Adaptive_Ply():
    #TO DO - implement a performance factor 
    return 4

#----

global PEICE_WEIGHTING
PEICE_WEIGHTING = {main.B_King: 1000, 
             main.B_Quee: 9,
             main.B_Rook: 5,
             main.B_Bish: 3, 
             main.B_Knig: 3,
             main.B_Pawn: 1,
             main.W_King: 1000, 
             main.W_Quee: 9,
             W_Rook: 5,
             W_Bish: 3, 
             W_Knig: 3, 
             W_Pawn: 1,
             Empty_: 0}

def OrderMoves(Moves, board):
  moveScore, fuzz = [], False
  for move in Moves:
    movingPeiceType = board[move[0][1]][move[0][0]]
    capturePeiceType = board[move[1][1]][move[1][0]]
    moveScoreGuess = (1 * PEICE_WEIGHTING[movingPeiceType])


    #Prioritise capturing opponents peices with the least value peices
    if board[move[1][1]][move[1][0]] != Empty_:             #Therefore, is a capture
      moveScoreGuess += (-2 * PEICE_WEIGHTING[movingPeiceType]) + (7 * PEICE_WEIGHTING[capturePeiceType])

    if CODE_CONVERT[board[move[1][1]][move[1][0]]][2:6] == "King":
      fuzz = True
    #Check for local pawns
      
    #Otherwise;
    moveScore.append(moveScoreGuess)
  #Order moves 

  sortedMoves = [Moves for _,Moves in sorted(zip(moveScore,Moves))].reverse()
  #sortedMoves.reverse()
  return sortedMoves, fuzz

# ==== (3) Ai Evaluation functions ==== # 

PIECE_VALUES = {               #This gives the non Colour-coded values for utility 
    'Pawn': 1,
    'Knig': 3,
    'Bish': 3,
    'Rook': 5,
    'Quee': 9,
    'King': 100,               #TO DO: Should create some scale based on depth
}

CODE_CONVERT = {               #This allows for a quick exchange from code to string 
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
}













def Basic_Evaluate():
    raise NotImplementedError

def Dive_Minimax_Evaluate():
    raise NotImplementedError

def Peice_Map_Evaluate():
    raise NotImplementedError

# ==== (4) Ai Bot Variations/Personalities ==== # 

def Random_AI():
    raise NotImplementedError

def Ideal_Pick():
    raise NotImplementedError

def Mini_Max_Original():
    raise NotImplementedError

def Mini_Max_Optimised():
    raise NotImplementedError

def Average_Friend():
    raise NotImplementedError



