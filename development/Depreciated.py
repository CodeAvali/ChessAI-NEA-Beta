import main

def diagonal_dangerous(create, gen):
    global diagional_new

    diagional_new, Blocked_Tuple, Attack_Tuple = [], [], []
    create_x, create_y = create[0], create[1]

    def generate_moves(x_direction, y_direction):
      global diagional_new
      x_pointer, y_pointer = create_x + x_direction, create_y + y_direction
      while 0 <= x_pointer < 8 and 0 <= y_pointer < 8 and not main.blocked(create, x_pointer, y_pointer):
        diagional_new = main.load(x_pointer, y_pointer, create, diagional_new)
        x_pointer += x_direction
        y_pointer += y_direction
    
    generate_moves(1, 1)  # Diagonal down-right
    generate_moves(-1, 1)  # Diagonal down-left
    generate_moves(1, -1)  # Diagonal up-right
    generate_moves(-1, -1)  # Diagonal up-left

    if gen:
        diagionaL_new = [(create, tuple(Blocked_Tuple[i][1])) for i in range(len(Blocked_Tuple))]
        return diagional_new
    else:
        diagional_new += Attack_Tuple 
        return diagional_new

  #----
    
def straight_dangerous(create, gen):                                                           #Check to see if actually possibly slower later; 
    global straight_new

    straight_new, Blocked_Tuple = [], []
    create_x, create_y = create[0], create[1]

    def generate_moves(x_direction, y_direction):
        global straight_new
        x_pointer, y_pointer = create_x + x_direction, create_y + y_direction
        while 0 <= x_pointer < 8 and 0 <= y_pointer < 8 and not main.blocked(create, x_pointer, y_pointer):
            straight_new = main.load(x_pointer, y_pointer, create, straight_new)
            x_pointer += x_direction
            y_pointer += y_direction

    generate_moves(1, 0) # Horizontal right
    generate_moves(-1, 0) # Horizontal left
    generate_moves(0, 1)  # Vertical down
    generate_moves(0, -1)  # Vertical up

    if gen:
        straight_new = [(create, tuple(Blocked_Tuple[i][1])) for i in range(len(Blocked_Tuple))]  # if board[Blocked_Tuple[i][0][1]][Blocked_Tuple[i][1][0]] not in straight_optimised]
        return straight_new
    else:
        return straight_new

  #----
    
def belonging(move_from, Moves_Tuple):
  #INDEPENDENT HELPER: Output legal moves 
  
  kept = []
  for i in range(len(Moves_Tuple)-1):
    if move_from == Moves_Tuple[i][0]:
      kept.append(Moves_Tuple[i])

  print("Possible moves", kept)

  #----

  def attacked(create):
    global flag_map, White_Playing 

  
    peice = main.board[create[1]][create[0]]

    pointer = 0
    if main.White_Playing:
      pointer = 1

    if flag_map[create[1]][create[0]][pointer] >= 1:
      print(create, "is attacked", flag_map[create[1]][create[0]][pointer], pointer)
      return True
    else: 
      return False
    
#----
    
def basic_utility(board, W_Move, B_Move):
  score = (len(W_Move) - len(B_Move)) / 10

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

#--------

def mini_max(board, W_Moves, B_Moves, depth):
  global White_Playing
  moves = W_Moves if White_Playing else B_Moves
  scores = []

  if White_Playing and W_Moves == []:
    return 0
  elif B_Moves == []:
    return 0

  for i in range(len(moves)):
    if board[moves[i][0][1]][moves[i][0][0]] != Empty_:
      temp = copy.deepcopy(board)
      #perform the move
      W_Moves, B_Moves, temp = ai_perform(W_Moves, B_Moves, moves[i][0], moves[i][1], temp)
      value = bad_evaluate(temp, W_Moves, B_Moves)

      if depth > 1:
        temp_best_move = mini_max(temp, W_Moves, B_Moves, depth - 1)
        W_Moves, B_Moves, temp = ai_perform(W_Moves, B_Moves, moves[i][0], moves[i][1], temp)
        value = bad_evaluate(temp, W_Moves, B_Moves)
        #check for no possible moves
      scores.append(value)
      #print("SCORES", scores)

  if White_Playing:
    best_move = moves[scores.index(max(scores))]
    White_Playing = False
  else:
    best_move = moves[scores.index(min(scores))]
    White_Playing = True

  return best_move

###

def OrderMoves(Moves, temp, for_White):
  #color_multiplier_dict = {'W': 1, 'B': -1, 'E': 0}

  PIECE_VALUES = {
    'Pawn': PAWN_VALUE,
    'Knig': KNIGHT_VALUE,
    'Bish': BISHOP_VALUE,
    'Rook': ROOK_VALUE,
    'Quee': QUEEN_VALUE,
    'King': 100,   
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

  start = time.time()

  moveScore, checked = [], []
  fuzz = False
  for move in Moves:
    movingPeiceType = CODE_CONVERT[temp[move[0][1]][move[0][0]]]
    capturePeiceType = CODE_CONVERT[temp[move[1][1]][move[1][0]]]
    #color_multiplier = color_multiplier_dict[movingPeiceType[0]]
    moveScoreGuess = (1 * abs(PIECE_VALUES[movingPeiceType[2:6]]))

    #Move validation for AI legal moves
    #if (color_multiplier == 1) and not for_White:
      #print("BLACK GOT WHITE MOVE?")
      #continue 

    #elif (color_multiplier == -1) and for_White:
      #print("WHITE GOT BLACK MOVE?")
      #continue

    #elif (color_multiplier == 0):
      #print("AI GOT NULL MOVE", movingPeiceType)
      #continue 

    #Prioritise capturing opponents peices with the least value peices
    if capturePeiceType != Empty_:             #Therefore, is a capture
      moveScoreGuess += (-2 * abs(PIECE_VALUES[movingPeiceType[2:6]])) + (7 * abs(PIECE_VALUES[capturePeiceType[2:6]]))

    if capturePeiceType[2:6] == "King":
      fuzz = True
    #Check for local pawns
      
    #Otherwise;
    checked.append(move)
    moveScore.append(moveScoreGuess)

  #Order moves 
  #if (len(Moves) - len(checked)) > 0:
    #print(len(Moves) - len(checked), "ERROR FACTOR")

  sortedMoves = [checked for _,checked in sorted(zip(moveScore,checked))]
  sortedMoves.reverse()
  return sortedMoves, fuzz



#####



#---- 
  
def dive_min_max(board, W_Capture, B_Capture, White_Playing, alpha, beta, depth): 

  #print(depth, len(attacking(W_Capture)), len(attacking(B_Capture)))

  if (len(W_Capture) == 0 and White_Playing) or (len(B_Capture) == 0 and not White_Playing):
    return peice_square_optimised(board, W_Capture, B_Capture) + len(W_Capture) - len(B_Capture)
  
  if depth == -3:
    #print("OCEAN FLOOR", len(W_Capture), len(B_Capture))
    return peice_square_optimised(board, W_Capture, B_Capture)

  if White_Playing:
    best = MIN
    #Then otherwise; we should 'skip stones' - restricting to the capturing moves. 
    for i in range(len(W_Capture)):
      temp = copy.deepcopy(board)
      W_Move, B_Move, temp = ai_perform(W_Capture, B_Capture, W_Capture[i][0], W_Capture[i][1], temp)    #Problem line 
      value = dive_min_max(temp, attacking(W_Move), attacking(B_Move), False, alpha, beta, depth - 1)
    #Though this likely is not necessary; AB prunning 
      best = max(best, value)
      alpha = max(alpha, best)
      if beta <= alpha:         #<=
        break             #As ab declares path as unreasonable. 

    if W_Capture == []:
      return peice_square_optimised(board, W_Capture, B_Capture)
    else:
      return best #Therefore - takes maximised diving score.
  
  if not White_Playing:
    best = MAX
    #Verifiy that all moves are captures
    #Then otherwise, we should 'skip stones' - restricting to the capturing moves. 
    for i in range(len(B_Capture)):
      temp = copy.deepcopy(board)
      W_Move, B_Move, temp = ai_perform(W_Capture, B_Capture, B_Capture[i][0], B_Capture[i][1], temp)
      value = dive_min_max(temp, attacking(W_Move), attacking(B_Move), True, alpha, beta, depth - 1)
    #Though this is not like necessary, AB prunning 
      best = min(best, value)
      beta = min(beta, best)
      if beta <= alpha:     #<=
        break              #As ab declares path as unreasonable 

    if B_Capture == []:
      return peice_square_optimised(board, W_Capture, B_Capture)
    else:
      return best #Therefore - take minimised diving score. 

######################### 

import statistics 
SAMPLE_FACTOR = 1

def average_friend(board, W_Move, B_Move, White_Playing, alpha, beta, depth):
  global cap, SAMPLE_FACTOR 

  moves, value, scores = [], [], []

  if insufficent_material(board) and depth != cap:
    return [0]  #As insufficent for any capture - if losing; should play towards capture
  
  if (len(W_Move) == 0 or len(B_Move) == 0) and depth != cap:
    return [0] #As stalemate natrually 

  if depth == 0: 
    normal = peice_square_optimised(board, W_Move, B_Move)
    return normal 

  if White_Playing:
    best = MIN
    moves, fuzz = OrderMoves(W_Move, board, True)
    if fuzz and depth != cap:
      B_Move = lazy_pin(board, W_Move, B_Move, False)
      if len(B_Move) == 0 and king_attacked(W_Move, board):
        return (100 + (25 * depth))
    #Then; need to iterate through all children 
    for i in range(len(moves)):
      temp = copy.deepcopy(board)
      #Hence; perform the move                                                                                            #TO DO; Implement instant return for kings; Check to see if ab can be shared. 
      W_Moves, B_Moves, temp = ai_perform(W_Move, B_Move, moves[i][0], moves[i][1], temp)
      value = average_friend(temp, W_Moves, B_Moves, False, alpha, beta, depth - 1)  #Pass min-max to other player.
      scores.append(value + random.uniform(-HAZE, HAZE))
      #Now; do alpha beta prunning
      best = max(best, value)
      alpha = max(alpha, best)
      if beta <= alpha:            #<=
        break                    #Prune the tree as limits reached.

    if depth != cap:
      return statistics.fmean(sorted(scores, reverse=True)[:SAMPLE_FACTOR])

  elif not White_Playing:
    best = MAX
    moves, fuzz = OrderMoves(B_Move, board, False)
    if fuzz and depth != cap:
      W_Move = lazy_pin(board, W_Move, B_Move, True)
      if len(W_Move) == 0 and king_attacked(B_Move, board):
        return (-100 + (-25 * depth))
    #Then iterate through all children
    for i in range(len(moves)):
      temp = copy.deepcopy(board)
      #Hence; perform the move
      W_Moves, B_Moves, temp = ai_perform(W_Move, B_Move, moves[i][0], moves[i][1], temp)
      value = average_friend(temp, W_Moves, B_Moves, True, alpha, beta, depth - 1) #Pass min-max to other player. 
      scores.append(value + random.uniform(-HAZE, HAZE))
      #Now; do alpha beta prunning.
      best = min(best, value)
      beta = min(beta, best)
      if beta <= alpha:      #<=
        break                  #Prune the tree as limits reached - if playing optimally; nodes arent considered. 
    
    if depth != cap:
      return statistics.fmean(sorted(scores, reverse=False)[:SAMPLE_FACTOR]) #Return the played (minimised) score for the state.
     
  if depth == cap:        #ORIGINAL CONDITION.
    print(scores, "For white player", max(scores), "For black player", min(scores), "cap confirmed - global", cap)
    return moves[scores.index(max(scores))] if White_Playing else moves[scores.index(min(scores))]

#----
  
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
  #rint(total, "TIME SPENT")

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



######

def ideal_pick(board, moves_tuple):         #Need to refactor - NOT actually 'ideal' or is it? 
  moves = moves_tuple 
  scores = []

  for i in range(len(moves)):
    temp = copy.deepcopy(board)

    value = peice_square_optimised(board, moves_tuple, moves_tuple)

    scores.append(value + random.uniform(-HAZE, HAZE))

    if White_Playing:
      GUI.lazy_update(scores, moves[scores.index(max(scores))])
    else: 
      GUI.lazy_update(scores, moves[scores.index(min(scores))])


  if White_Playing: 
    best_move = moves[scores.index(max(scores))]
  else:
    best_move = moves[scores.index(min(scores))]

  return best_move[0], best_move[1]

#https://blog.devgenius.io/simple-min-max-chess-ai-in-python-2910a3602641 - From here, do referencing.

#----------

def mini_max(board, W_Move, B_Move, White_Playing, depth):
  global total_nodes
  moves = W_Move if White_Playing else B_Move
  scores = []

  #Root node - get utility value 
  if depth == 0:
    return peice_square_optimised(board, W_Move, B_Move)
    #return bad_evaluate(board, W_Move, B_Move)
  
  for i in range(len(moves)):
    if board[moves[i][0][1]][moves[i][0][0]] != Empty_:
      temp = copy.deepcopy(board)
      temp, W_Move, B_Move = copy.deepcopy(board), copy.deepcopy(W_Move), copy.deepcopy(B_Move)
      #Perform the move
      W_Move, B_Move, temp = ai_perform(W_Move, B_Move, moves[i][0], moves[i][1], temp)
      #Then pass into minimax recursively 
      scores.append(mini_max(temp, W_Move, B_Move, not White_Playing, depth - 1))

  #If at root node, then return 'optimal move'
  if depth == cap:
    return moves[scores.index(max(scores))] if White_Playing else moves[scores.index(min(scores))]                                                              
  
  #If a called instance, then return chosen adversial move 
  else:
    if White_Playing:
      return max(scores)
    else:
      return min(scores)

#======
    
FROM - https://ntietz.com/blog/alpha-beta-pruning/

def optimised_min_max(board, W_Move, B_Move, White_Playing, alpha, beta, depth):
  global cap, total_nodes

  if insufficent_material(board) and depth != cap:
    return 0  #As insufficent for any capture - if losing; should play towards capture

  #Stalemate condition of no valid moves
  if (len(W_Move) == 0 and White_Playing) or (len(B_Move) == 0 and not White_Playing) and depth != cap:
    return 0 
  
  #Otherwise; if root node return utility
  if depth == 0: 
    return peice_square_optimised(board, W_Move, B_Move) 

  moves, value, scores= [], [], []

  if White_Playing:
    best = MIN
    moves = OrderMoves(W_Move, board, True)
    #Check for checkmate & pinned moves    
    if king_attacked(B_Move, board) and depth != cap:
      moves = lazy_pin(board, moves, B_Move, True)
      if len(moves) == 0:
        return (-500 + (-100 * depth))
      else:
        depth = min(cap - 1, 2) #Quiesence check search                                                                 
    #Then; need to iterate through all children 
    for i in range(len(moves)):
      temp = copy.deepcopy(board)
      #Hence; perform the move                                                                                            
      W_Moves, B_Moves, temp = ai_perform(W_Move, B_Move, moves[i][0], moves[i][1], temp)
      value = optimised_min_max(temp, W_Moves, B_Moves, False, alpha, beta, depth - 1)  #Pass min-max to other player.
      #AB Prunning WhitePlayer
      best = max(best, value)
      if best > beta:            
        #print("BROKEN", i)
        break  #Prune Node
      alpha = max(alpha, best)
      if depth == cap:
        scores.append(value + random.uniform(0, HAZE))
        #GUI.lazy_update(scores, moves[scores.index(max(scores))])

    if depth != cap:
      return best #Return the played (maximised) score for the state.

  elif not White_Playing:
    best = MAX
    moves = OrderMoves(B_Move, board, False)
    #Check for checkmate & pinned moves    
    if king_attacked(W_Move, board) and depth != cap:
      moves = lazy_pin(board, W_Move, moves, False)
      if len(moves) == 0:
        return (500 + (100 * depth))
      else:
        depth = min(cap - 1, 2)
    #Then iterate through all children
    for i in range(len(moves)):
      temp = copy.deepcopy(board)
      #Hence; perform the move
      W_Moves, B_Moves, temp = ai_perform(W_Move, B_Move, moves[i][0], moves[i][1], temp)
      value = optimised_min_max(temp, W_Moves, B_Moves, True, alpha, beta, depth - 1) #Pass min-max to other player. 
      #AB Prunning BlackPlayer
      best = min(best, value)
      if best < alpha:      
        #print("BROKEN", i)
        break #Prune Node
      beta = min(beta, best)
      if depth == cap:
        scores.append(value + random.uniform(-HAZE, 0))
        #GUI.lazy_update(scores, moves[scores.index(min(scores))])
    
    if depth != cap:
      return best #Return the played (minimised) score for the state.
  
  #Return ideal move
  if depth == cap:
    if not scores:
      raise "MINI_MAX_OPTIMISED: NoScoresError"
    return moves[scores.index(max(scores))] if White_Playing else moves[scores.index(min(scores))]