import main

# Order_Pick picks the most ideal move according to a secondary heuristic. 
# Utility is determined by the secondary heuristic, which here is managed by OrderMoves. 
# Development Commentary: Having only fixed rules leads to ridgid ('capture heavy') play. 

def call(board, moves_tuple):

  #Order moves according to secondary heuristic 
  if main.White_Playing:
    moves = main.OrderMoves(moves_tuple, board, True)
  else:
    moves = main.OrderMoves(moves_tuple, board, False)

  #Then return the 'best' move - located index position 0; for worst move, change to len(moves).
  return moves[0]