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