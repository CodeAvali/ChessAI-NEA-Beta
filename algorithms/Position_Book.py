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

    
































###############

# No purpose to keeping an ordered list - O(n)lookup versus O(n) insert and O(nlogn) lookup


def hash_sort(current):
    #As python's inbuilt sorting method is O(nlogn) - there is no benefit to me implemented merge/quick sort
    return current.sort()


def binary_lookup(find, current_hashes):
    #Binary search for hash lookup 

    high = len(current_hashes)
    low = 0 

    while high >= low:

        mid = (high - low) / 2
        if current_hashes[mid] == find:
            return True, mid
        elif current_hashes[mid] > find:
            high = mid - 1
        else:
            low = mid + 1

    return False, None


def insertion_sort(current_hashes):

    #Only have to handle singular inserts
    sorted = False
    position = len(current_hashes)

    while not sorted:
        if current_hashes[position] > current_hashes[position - 1]:
            #Perform a swap backwards
            temp = current_hashes[position - 1]
            current_hashes[position - 1] = current_hashes[position]
            current_hashes[position] = temp
        else:
            sorted = True

        position -= 1 #Decrement pointer
        if position == 0:
            sorted = True
   
   #Return inserted array; along with inserted positon
    return current_hashes, position 


def mark_instance(current_hashes, repeated):

    #Firstly - request for the hash of the current state:
    state_hash = create_hash(main.board)

    #Check for lookup
    found, pointer = binary_lookup(state_hash, current_hashes)
    if found == True:
        #Then increment repeated
        repeated[pointer] += 1
        if repeated[pointer] == 3:
            raise "Threethold repetion"
        
    else:
        #Append new hash
        current_hashes.append(state_hash)
        
        #Then insertion sort to keep sorted




    #Then - sort it to maintain consistency






    return NotImplementedError




    








