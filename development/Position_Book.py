import main

current_hash = []
repeated = []

def hash_reset():
    global current_hash, repeated

    current_hash = []
    repeated = []

def create_hash(board):
    count = 0
    #For our hashing function - I am going to consider a numeric integer which will be easy to lookup
    for i in range(0,8):
        for j in range(0, 8):

            if len(board[j][i]) > 1:
                for z in range(0, len(board[j][i])):
                    count += (ord(board[j][i][z]) / (i + 1 + z)) * (j + 1)
            else:
                count+= (ord(board[j][i]) / (i + 1)) * (j + 1)

    return round(count)



def linear_lookup(current_hash, find):
    for i in range(len(current_hash)):
        if current_hash[i] == find:
            return True, i
        
    return False, -1
        


def create_instance():

    #Need to create new hash for current game_state

    new_hash = create_hash(main.board)

    #Then, need to check that hash doesnt already exist

    occurance, pointer = linear_lookup(current_hash, new_hash)

    if occurance:
        repeated[pointer] += 1
        if repeated[pointer] == 3:
            import GUI
            GUI.threefold_repetition()
            #raise "NotImplemented: Threefold repetition"
        
    else:
        current_hash.append(new_hash)
        repeated.append(0)

    return current_hash, repeated 

