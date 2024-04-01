import main
import copy

# Mini-Max: Basic implementation of classical Mini_Max; considers adversial gameplay and makes moves
# However, lack of any efficency leads to significant slowdown past 2 depth. 

def call(board, W_Move, B_Move, White_Playing, depth):
  moves = W_Move if White_Playing else B_Move
  scores = []

  #Root node - get utility value 
  if depth == 0:
    return main.peice_square_optimised(board, W_Move, B_Move)
    #return bad_evaluate(board, W_Move, B_Move)
  
  for i in range(len(moves)):
    if board[moves[i][0][1]][moves[i][0][0]] != main.Empty_:
      temp = copy.deepcopy(board)
      temp, W_Move, B_Move = copy.deepcopy(board), copy.deepcopy(W_Move), copy.deepcopy(B_Move)
      #Perform the move
      W_Move, B_Move, temp = main.ai_perform(W_Move, B_Move, moves[i][0], moves[i][1], temp)
      #Then pass into minimax recursively 
      scores.append(call(temp, W_Move, B_Move, not White_Playing, depth - 1))

  #If at root node, then return 'optimal move'
  if depth == main.cap:
    return moves[scores.index(max(scores))] if White_Playing else moves[scores.index(min(scores))]                                                              
  
  #If a called instance, then return chosen adversial move 
  else:
    if White_Playing:
      return max(scores)
    else:
      return min(scores)