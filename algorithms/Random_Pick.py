import random 

# Random_Pick: simply returns a random legal move for that player.
# DEVELOPMENT COMMENTARY - This is easy to implement, but does not provide any play of quality. 

def call(moves_tuple):
  return moves_tuple[random.randint(0, len(moves_tuple)-1)]