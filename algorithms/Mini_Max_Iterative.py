import main, copy, random, GUI

# Mini_Max_Iterative - An prunning heavy lossy version of minimax
# Achieves 4 depth play comfortably - but tends to lose information and therefore often loses against loseless algorithms

def call(board, W_Move, B_Move, White_Playing, alpha, beta, depth):

  if main.insufficent_material(board) and depth != main.cap:
    return 0  #As insufficent for any capture - if losing; should play towards capture

  #Stalemate condition of no valid moves
  if (len(W_Move) == 0 and White_Playing) or (len(B_Move) == 0 and not White_Playing) and depth != main.cap:
    return 0 
  
  #Otherwise; if root node return utility
  if depth == 0: 
    return main.peice_square_optimised(board, W_Move, B_Move) 

  moves, value, scores= [], [], []

  if White_Playing:
    best = main.MIN
    moves = main.OrderMoves(W_Move, board, True)
    #Check for checkmate & pinned moves    
    if main.king_attacked(B_Move, board) and depth != main.cap:
      moves = main.lazy_pin(board, moves, B_Move, True)
      if len(moves) == 0:
        return (-500 + (-100 * depth))
      else:
        depth = min(main.cap - 1, 2) #Quiesence check search                                                                 
    #Then; need to iterate through all children 
    for i in range(len(moves)):
      temp = copy.deepcopy(board)

      #Hence; perform the move                                                                                            
      W_Moves, B_Moves, temp = main.ai_perform(W_Move, B_Move, moves[i][0], moves[i][1], temp)

      #If captured; perform 2*bounds check
      if depth != main.cap:
        capture_value = main.peice_square_optimised(temp, W_Moves, B_Moves)
        if capture_value > (depth * beta):
          return capture_value

      value = call(temp, W_Moves, B_Moves, False, alpha, beta, depth - 1)  #Pass min-max to other player.
      #AB Prunning WhitePlayer
      best = max(best, value)
      if best > beta:            
        break  #Prune Node
      alpha = max(alpha, best)
      if depth == main.cap:
        scores.append(value + random.uniform(0, main.HAZE))
        GUI.lazy_update(scores, moves[scores.index(max(scores))])

    if depth != main.cap:
      return best #Return the played (maximised) score for the state.

  elif not White_Playing:
    best = main.MAX
    moves = main.OrderMoves(B_Move, board, False)
    #Check for checkmate & pinned moves    
    if main.king_attacked(W_Move, board) and depth != main.cap:
      moves = main.lazy_pin(board, W_Move, moves, False)
      if len(moves) == 0:
        return (500 + (100 * depth))
      else:
        depth = min(main.cap - 1, 2)
    #Then iterate through all children
    for i in range(len(moves)):
      temp = copy.deepcopy(board)

      #Hence; perform the move
      W_Moves, B_Moves, temp = main.ai_perform(W_Move, B_Move, moves[i][0], moves[i][1], temp)

      #If captured; perform 2*bounds check
      if depth != main.cap:
        capture_value = main.peice_square_optimised(temp, W_Moves, B_Moves)
        if capture_value < (depth * alpha):
          return capture_value

      #Otherwise
      value = call(temp, W_Moves, B_Moves, True, alpha, beta, depth - 1) #Pass min-max to other player. 
      #AB Prunning BlackPlayer
      best = min(best, value)
      if best < alpha:      
        #print("BROKEN", i)
        break #Prune Node
      beta = min(beta, best)
      if depth == main.cap:
        scores.append(value + random.uniform(-main.HAZE, 0))
        GUI.lazy_update(scores, moves[scores.index(min(scores))])
    
    if depth != main.cap:
      return best #Return the played (minimised) score for the state.
  
  #Return ideal move
  if depth == main.cap:
    if not scores:
      raise "MINI_MAX_Iterative: NoScoresError"
    return moves[scores.index(max(scores))] if White_Playing else moves[scores.index(min(scores))]