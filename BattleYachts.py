# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Daniel Fuhrmann
#               Jaron Thompson
#               Kyle Moore
# Section:      517
# Assignment:   Project 517
# Date:         7 December 2022
#
# ######################## Imports ######################## #
import numpy as np
from colorama import Fore, Style

# ######################## Globals ######################## #
ai_queue = []
ai_last_hit = None
sum_boat_length = 18
player_1_hit_counter = 0
player_2_hit_counter = 0
board_length = 9
AI = True
boat_list_p1 = []
boat_list_p2 = []
p1_board = [['~' for j in range(board_length)] for i in range(board_length)]
p2_board = [['~' for j in range(board_length)] for i in range(board_length)]
p1_wins = 0
p2_wins = 0
ai_wins = 0


# ####################### Functions ####################### #
def ask_for_move():
    """
    Ask the player to enter a point.

    Returns:
        list containing [y,x]
    """
    guess_point = None
    try:
      #take user coordinates
        guess_point = input("Enter a point in the format x,y: ")
        guess_point = guess_point.split(',')
        guess_point[0] = int(guess_point[0])
        guess_point[1] = int(guess_point[1])

        if not check_in_bounds(p1_board, guess_point):
          #raise error if out of bounds
            raise
    except:
        print(Fore.RED + Style.BRIGHT + "You entered an invalid point. Try again." + Fore.RESET + Style.NORMAL)
        #guess_point = ask_for_move()
        return ask_for_move()

    # Just switched these
    return [guess_point[1] - 1, guess_point[0] - 1]


def check_is_water(player_board, guess_point):
    """
    Check if board coordinates is equal to a water symbol.

    Parameters:
        player_board (list)
        guess_point (list) - coordinate in the format [x,y]

    Returns:
        boolean: True - point is water | False - point is not water
    """
    if player_board[guess_point[0]][guess_point[1]] == '~':
      #check if water symbol
        return True
    else:
        return False


def check_is_boat(player_board, guess_point):
    """
    Check if board coordinates is equal to a boat symbol.

    Parameters:
        player_board (list)
        guess_point (list) - coordinate in the format [x,y]

    Returns:
        boolean: True - point is boat | False - point is not boat
    """
    if player_board[guess_point[0]][guess_point[1]] == '^':
      #check if boat symbol
        return True
    else:
        return False


def is_win():
    """
    Checks to see if either player has won. Prints win message and displays both player's boards

    Returns:
        Boolean
    """
    global sum_boat_length
    global player_1_hit_counter
    global player_2_hit_counter

    global p1_wins
    global p2_wins
    global ai_wins
#check if hits are equal to the amount of bot lengths
    if player_1_hit_counter == sum_boat_length:
        print(Fore.MAGENTA + Style.BRIGHT + "##############\n"
                                            "#            #\n"
                                            "#  Player 1  #\n"
                                            "#  You Won!  #\n"
                                            "#            #\n"
                                            "##############\n" + Fore.RESET + Style.NORMAL)

        p1_wins += 1
        return True

    elif player_2_hit_counter == sum_boat_length:
        if AI:
            print(Fore.MAGENTA + Style.BRIGHT + "##############\n"
                                                "#            #\n"
                                                "#     AI     #\n"
                                                "#    Won!    #\n"
                                                "#            #\n"
                                                "##############\n" + Fore.RESET + Style.NORMAL)
        else:
            print(Fore.MAGENTA + Style.BRIGHT + "##############\n"
                                                "#            #\n"
                                                "#  Player 2  #\n"
                                                "#  You Won!  #\n"
                                                "#            #\n"
                                                "##############\n" + Fore.RESET + Style.NORMAL)

        print(Fore.BLUE + Style.BRIGHT + "PLAYER 1's board:" + Fore.RESET + Style.NORMAL)  # Prints player 1's board
        display_board(p1_board, True)
        if AI:
            print(Fore.RED + Style.BRIGHT + "AI's board:" + Fore.RESET + Style.NORMAL)  # Prints AI's board if applicable
        else:
            print(Fore.RED + Style.BRIGHT + "PLAYER 2's board:" + Fore.RESET + Style.NORMAL)  # Prints Player 2's board if applicable
        display_board(p2_board, True)
        if AI:
            ai_wins += 1
            return True
        else:
            p2_wins += 1
            return True
    else:
        return False


def find_direction(start_point, end_point):  # Function not in original plan
    """
    Determines the direction of motion based on the start and endpoints entered.

    Parameters:
        start_point (list)
        end_point (list)

    Returns:
        direction (str)
    """

    if start_point[0] == end_point[0]:  # Determines if x coordinates are the same
        if start_point[1] > end_point[1]:  # up: start point > end point
            direction = "up"
        elif start_point[1] < end_point[1]:  # down: start point < end point
            direction = "down"
        else:
            direction = "ERROR"

    elif start_point[1] == end_point[1]:  # Determines if y coordinates are the same
        if start_point[0] > end_point[0]:  # left: start point > end point
            direction = "left"
        elif start_point[0] < end_point[0]:  # right: start point < end point
            direction = "right"
        else:
            direction = "ERROR"
    else:
        direction = "ERROR"

    return direction


def boat_coordinates(start_point, end_point):
    """
    Finds the coordinates of the boat between start and end point

    Parameters:
        start_point (list) - coordinate in the format [x,y]
        end_point (list) - coordinate in the format [x,y]

    Returns:
        List containing all consecutive points between the start and end point.
    """
    if find_direction(start_point, end_point) == 'right':
        
        if int(end_point[0]) != int(start_point[0]):

            # empty list to store coordinates
            new_list = []
            
            for i in range(start_point[0],end_point[0]):
                # append each coordinate
                new_list.append([i + 1, end_point[1]])

            new_list.append(start_point)
            return new_list
    # repeat for other directions
    if find_direction(start_point, end_point) == 'left':

        if int(end_point[0]) != int(start_point[0]):
            new_list = []
            for i in range(end_point[0],start_point[0]):
                new_list.append([i + 1, start_point[1]])
            new_list.append(end_point)
            return new_list
    if find_direction(start_point, end_point) == 'down':

        print(end_point[0],start_point[0])
        if int(end_point[0]) == int(start_point[0]):

            new_list = []
            if end_point[1] > start_point[1]:

                print(end_point[1])
                for i in range(start_point[1],end_point[1]):

                    new_list.append([start_point[0], i + 1])
                new_list.append(start_point)
                return new_list
            elif end_point[1] > start_point[1]:
                for i in range(start_point[1],end_point[1]):
                    new_list.append([start_point[0], i + 1])
                new_list.append(end_point)
                return new_list
    if find_direction(start_point, end_point) == 'up':

        if int(end_point[0]) == int(start_point[0]):
            new_list = []
            for i in range(end_point[1],start_point[1]):
                new_list.append([start_point[0], i + 1])
            new_list.append(end_point)
            return new_list


def is_ship_sunk(player, player_board, guess_point):
    """
    Checks to see if ship is sunk

    Parameters:
        player (str) - either "player1" or "player2"
        player_board (list)
        guess_point (list)

    Returns:
        boolean: True - ship is sunk | False - ship is not sunk
    """

    start_point = None
    end_point = None
  
    if player == "player1":
        # loop through list to find where the start and endpoint coordinates are upon hit
        for i in boat_list_p1:
            start_point = [i[0], i[1]]
            end_point = [i[3], i[2]]  # flipped these

            if i[0] == i[3]:
              end_point[1] += -1
            if i[1] == i[2]:
              end_point[0] += -1
          
            x, y = guess_point[0], guess_point[1]

            if start_point[0] <= x <= end_point[0] and start_point[1] <= y <= end_point[1]:
                break

    if player == "player2":
        for i in boat_list_p2:
            start_point = [i[0], i[1]]
            end_point = [i[2], i[3]]

            x, y = guess_point[0], guess_point[1]

            if start_point[0] <= x <= end_point[0] and start_point[1] <= y <= end_point[1]:
                break

    new_list = boat_coordinates(start_point, end_point)
    if new_list is None:
        return False
    # print(new_list, "New list right here")
    counter = 0
    boat_len = len(new_list)
  #making coordinates
    x_coordinates = []
    y_coordinates = []
    for coord in new_list:
      x_coordinates.append(coord[0])
      y_coordinates.append(coord[1])
    for i in range(len(player_board)):
      for j in range(len(player_board)):
        if (player_board[i][j] == '*') and (i in x_coordinates) and (j in y_coordinates):          
          counter += 1
    if counter == boat_len:
        return True
    else:
        return False


def display_board(player_board, show=True):
    """
    Takes in a board as a 2d list and prints out the 2d
    list in the console with colors.

    Parameters:
      player_board (list)
      show (bool) - show boats (True/False)
    """
    print("  ", end="")
    for i in range(len(player_board)):
        print(i + 1, end=" ")
    print()
    count = 1
    for row in player_board:
        print(count, end=" ")
        for character in row:
            if character == "~":  # ~ - water marker
                print(Fore.BLUE + Style.BRIGHT + "~" + Fore.RESET + Style.NORMAL, end=" ")
            elif character == "*":  # * - boat hit marker
                print(Fore.RED + Style.BRIGHT + "*" + Fore.RESET + Style.NORMAL, end=" ")
            elif character == "#":  # # - miss marker
                print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "#" + Fore.RESET + Style.NORMAL, end=" ")
            elif character == "^":  # ^ - boat marker
                if show:
                    print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "^" + Fore.RESET + Style.NORMAL, end=" ")
                else:
                    print(Fore.BLUE + Style.BRIGHT + "~" + Fore.RESET + Style.NORMAL, end=" ")
            else:
                print(character, end=" ")
        print()
        count += 1


def calc_endpoint(start, length, direction):
    """
    Calculates the endpoint based on the given parameters.

    Parameters:
        start (list)
        length (int)
        direction (str)

    Returns:
        End coordinates
    """

    if direction == "up":  # start point > end point
        x_coordinate = start[0]
        y_coordinate = start[1] - length + 1

        return [x_coordinate, y_coordinate]

    elif direction == "down":  # start point < end point
        x_coordinate = start[0]
        y_coordinate = start[1] + length - 1

        return [x_coordinate, y_coordinate]

    elif direction == "right":  # start point < end point
        x_coordinate = start[0] + length - 1
        y_coordinate = start[1]

        return [x_coordinate, y_coordinate]

    elif direction == "left":  # start point > end point
        x_coordinate = start[0] - length + 1
        y_coordinate = start[1]

        return [x_coordinate, y_coordinate]

    else:
        print(Fore.RED + Style.BRIGHT + "An Error has occurred" + Fore.RESET + Style.NORMAL)
        return -1, -1


def check_in_bounds(player_board, guess_point):
    """
    Checks if the given point is greater than 0 and less than the length of the player_board.

    Parameters:
        player_board (list)
        guess_point (list)

    Returns:
        Boolean
    """
    # Valid coordinates:
    # 1 <= x <= horizontal length of board
    # 1 <= y <= vertical length of board
    if guess_point[0] < 1 or guess_point[0] > len(player_board[0]):
        return False
    elif guess_point[1] < 1 or guess_point[1] > len(player_board):
        return False
    else:
        return True


def place_ship(player, player_board, start_point, end_point):
    """
    Makes sure both points are within the bounds of the board. Make sure the points do not overlap with another
    boat on that players board. Updates the  players board. Add ship to dictionary.

    Parameters:
      player (str)
      player_board (list)
      start_point (list)
      end_point (list)

    Returns:
        None

    """
    # Adds the start and end point of the boat to a list holding all the start and end points a player's boats
    # In the form [[x1, y1, x2, y2], [x1, y1, x2, y2]]
    boat_coordinates = start_point + end_point

    if player == "player1":
        boat_list_p1.append(boat_coordinates)
    elif player == "player2":
        boat_list_p2.append(boat_coordinates)

    if check_in_bounds(player_board, start_point) and check_in_bounds(player_board, end_point):

        coordinate_adjust = {"up": -1, "down": 1, "left": -1, "right": 1}  # values to change the start coordinate by
        direction = find_direction(start_point, end_point)

        # Adjusts the coordinates so that values entered by user line up with list index
        start_point[0] -= 1
        start_point[1] -= 1

        end_point[0] -= 1
        end_point[1] -= 1

        if direction == "up":
            while start_point[1] >= end_point[1]:
                player_board[start_point[1]][start_point[0]] = "^"
                start_point[1] += coordinate_adjust[direction]
        elif direction == "down":
            while start_point[1] <= end_point[1]:
                player_board[start_point[1]][start_point[0]] = "^"
                start_point[1] += coordinate_adjust[direction]

        elif direction == "left":
            while start_point[0] >= end_point[0]:
                player_board[start_point[1]][start_point[0]] = "^"
                start_point[0] += coordinate_adjust[direction]
        elif direction == "right":
            while start_point[0] <= end_point[0]:
                player_board[start_point[1]][start_point[0]] = "^"
                start_point[0] += coordinate_adjust[direction]
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid points were entered" + Fore.RESET + Style.NORMAL)
          

def on_hit(player_board, guess_point, player):
    """
    Add to hit counter. If computer then add to queue of things to hit (must be water)

    Parameters:
        player_board (list)
        guess_point (list)
        player (str) - either "player1" or "player2"

    Returns:
        player_board
    """
    global ai_queue
    global ai_last_hit
    global player_1_hit_counter
    global player_2_hit_counter

    # sum_boat_length += 1
    if player == "player1":
        player_2_hit_counter += 1  # Takes in an enemy board so these need to switch
    else:
        player_1_hit_counter += 1

    x, y = guess_point

    player_board[x][y] = '*'

    if AI and player == "player1":  # Should be player 1 here
        if x > 0:  #Check the edges
            if check_is_water(player_board, [x - 1, y]) \
                    or check_is_boat(player_board, [x - 1, y]):
                ai_queue.append([x - 1, y])
        if x < board_length - 1:
            if check_is_water(player_board, [x + 1, y]) \
                    or check_is_boat(player_board, [x + 1, y]):
                ai_queue.append([x + 1, y])
        if y > 0:
            if check_is_water(player_board, [x, y - 1]) \
                    or check_is_boat(player_board, [x, y - 1]):
                ai_queue.append([x, y - 1])
        if y < board_length - 1:
            if check_is_water(player_board, [x, y + 1]) \
                    or check_is_boat(player_board, [x, y + 1]):
                ai_queue.append([x, y + 1])

        if ai_last_hit is None:  # check to make sure it is not none
            ai_last_hit = [guess_point[0], guess_point[1]]
            return

        if ai_last_hit[0] == guess_point[0]:  # Determine which way iit wants to go
            for i in range(len(ai_queue) - 1, -1, -1):
                if ai_queue[i][0] != ai_last_hit[0]:
                    ai_queue.pop(i)
        elif ai_last_hit[1] == guess_point[1]:
            for i in range(len(ai_queue) - 1, -1, -1):
                if ai_queue[i][1] != ai_last_hit[1]:
                    ai_queue.pop(i)
        else:
          pass  # This should never happen


        for i in range(len(ai_queue) - 1, -1, -1):

            if not check_is_water(player_board, ai_queue[i]) \
                    and not check_is_boat(player_board, ai_queue[i]):
                ai_queue.pop(i)

            for j in range(len(ai_queue) - 1, -1, -1):  # Make sure to remove duplicates in the queue
                if i != j:
                    if ai_queue[i] == ai_queue[j]:
                        ai_queue.pop(j)
                        break

        ai_last_hit = [guess_point[0], guess_point[1]]

        # print(type(player), type(player_board), type(guess_point[0]))
        if is_ship_sunk(player, player_board, guess_point):
            ai_last_hit = None
            ai_queue.clear()  # Check this later

    return player_board


def update_board(player_board, guess_point, player):
    """
    Takes in player board. Updates the board

    Parameters:
        player_board (list)
        guess_point (list)
        player (str) - either "player1" or "player2"

    Returns:
        player_board
    """

    x, y = guess_point

  
    if check_is_boat(player_board, guess_point):  # Ship symbol
        # run on hit
        on_hit(player_board, guess_point, player)

    if check_is_water(player_board, guess_point):
        player_board[x][y] = "#"  # Need a splash symbol

    if guess_point in ai_queue and player == "player1":
        # print(ai_queue)
        ai_queue.remove(guess_point)
    

    return player_board


def get_random_valid_point(player_board):
    """
    Use numpy import to get a random point within the bounds of the board. Make sure it is valid.

    Parameters:
        player_board (list)

    Returns:
          Random x and y coordinate
    """
    rand_row = int(np.random.randint(0, board_length))  # Generates random y coordinate
    rand_col = int(np.random.randint(0, board_length))  # Generates random x coordinate

    while not check_is_water(player_board, (rand_row, rand_col)):
        rand_row = int(np.random.randint(0, board_length))
        rand_col = int(np.random.randint(0, board_length))

    return rand_row, rand_col


def get_random_ai_point(player_board):
    """
    Use numpy import to get a random point within the bounds of the board. Make sure it is valid.

    Parameters:
        player_board (list)

    Returns:
        Random x and y coordinate
    """
    rand_row = int(np.random.randint(0, board_length))
    rand_col = int(np.random.randint(0, board_length))

    while not check_is_water(player_board, (rand_row, rand_col)) \
            and not check_is_boat(player_board, (rand_row, rand_col)):  # Make sure it is valid
        rand_row = int(np.random.randint(0, board_length))
        rand_col = int(np.random.randint(0, board_length))

    return [rand_row, rand_col]


def smart_hit(player_board, player):
    '''
    This will determine will the next hit will be
    if the length of the ai_queue is zero it will hit a random point
    '''
    global ai_queue  # need the global variable

    if len(ai_queue) == 0:
        update_board(player_board, get_random_ai_point(player_board), player)
    else:
        update_board(player_board, ai_queue[0], player)


def place_boat_random(player_board, boat_length):
    """
    Generate random boat direction. Make sure all values are valid. If so, place boat else try again.

    Parameters:
        player_board (list)
        boat_length (int)

    Returns:
        player_board
    """

    ship_array = []

    random_point = get_random_valid_point(player_board)

    dir = int(np.random.randint(0, 2))  # Horizontal or vertical

    for i in range(boat_length):
        if dir == 0:
            ship_array.append((random_point[0], random_point[1] + i))
        else:
            ship_array.append((random_point[0] + i, random_point[1]))

    for i in ship_array:
        if i[0] >= board_length or i[1] >= board_length:  # Make sure it is in bounds
            # print(i[0], i[1])
            return place_boat_random(player_board, boat_length)

        if not check_is_water(player_board, i):  # Make sure
            # print("clips another boat", ship_array)
            return place_boat_random(player_board, boat_length)

    for i in ship_array:
        player_board[i[0]][i[1]] = "^"

    boat_list_p2.append([ship_array[0][0], ship_array[0][1], ship_array[-1][0], ship_array[-1][1]])

    return player_board


def ai_place_boats():
    """
    Places boats for AI
    """
    place_boat_random(p2_board, 5)  # place boat of length 5
    place_boat_random(p2_board, 4)
    place_boat_random(p2_board, 4)
    place_boat_random(p2_board, 3)
    place_boat_random(p2_board, 2)


def get_boat_input():
    """
    Gets input from user to place boats. Uses a try except statement and other verifications to ensure valid user input.

    Returns:
        Tuple of point (list) and direction (str)
    """
    try:
        point = input("Enter a point in the format x,y: ")
        point = point.split(',')  # str to list
        point[0] = int(point[0])  # str to int
        point[1] = int(point[1])

        if not check_in_bounds(p1_board, point):  # If point is not in bounds, code will throw a run time error
            raise

        directions = ["up", "down", "left", "right"]
        direction = input("What direction do you want the boat to go in? (up/down/left/right): ")
        while direction not in directions:  # Runs until either "up", "down", "left", "right" is entered by the user
            print(Fore.RED + Style.BRIGHT + "Try again." + Fore.RESET + Style.NORMAL)
            direction = input("What direction do you want the boat to go in? (up/down/left/right): ")
    except:
        print(Fore.RED + Style.BRIGHT + "You entered an invalid point. Try again." + Fore.RESET + Style.NORMAL)
        point, direction = get_boat_input()

    return point, direction


def enough_boats(player_board):
    """
    Checks if user placed ships in a valid place.

    Parameters:
        player_board (list)
    
    Returns:
        Boolean for whether enough boats are on the board.
    """
    num_ships = 0
    for row in player_board:
        for char in row:
            if char == "^":
                num_ships += 1  # Counts number of boat pieces on the board
    return num_ships == sum_boat_length


def player1_place_boats():
    """
    Places boats based on user input.
    """
    global p1_board  # Resets player 2's board
    p1_board = [['~' for j in range(board_length)] for i in range(board_length)]

    print(Fore.BLUE + Style.BRIGHT + "PLAYER 1 Place your ships." + Fore.RESET + Style.NORMAL)
    display_board(p1_board, False)  # Prints a blank board for reference while user places their ships
    print("^ Reference Board ^")

    # ### Boat Length 5 ### #
    print("Enter the start point of a ship with length 5:")
    start_point, direction = get_boat_input()

    place_ship("player1", p1_board, start_point, calc_endpoint(start_point, 5, direction))

    display_board(p1_board, True)  # Prints player 2's board with their ship placed on the board

    # ### Boat Length 4 ### #

    print("Enter the start point of a ship with length 4:")
    start_point, direction = get_boat_input()

    place_ship("player1", p1_board, start_point, calc_endpoint(start_point, 4, direction))

    display_board(p1_board, True)

    # ### Boat Length 4 ### #

    print("Enter the start point of a ship with length 4:")
    start_point, direction = get_boat_input()

    place_ship("player1", p1_board, start_point, calc_endpoint(start_point, 4, direction))

    display_board(p1_board, True)

    # ### Boat Length 3 ### #

    print("Enter the start point of a ship with length 3:")
    start_point, direction = get_boat_input()

    place_ship("player1", p1_board, start_point, calc_endpoint(start_point, 3, direction))

    display_board(p1_board, True)

    # ### Boat Length 2 ### #

    print("Enter the start point of a ship with length 2:")
    start_point, direction = get_boat_input()

    place_ship("player1", p1_board, start_point, calc_endpoint(start_point, 2, direction))

    display_board(p1_board, True)


def player2_place_boats():
    """
    Places boats based on user input.
    """
    global p2_board  # Resets player 2's board
    p2_board = [['~' for j in range(board_length)] for i in range(board_length)]

    print(Fore.RED + Style.BRIGHT + "PLAYER 2 Place your ships." + Fore.RESET + Style.NORMAL)
    display_board(p2_board, False)  # Prints a blank board for reference while user places their ships
    print("^ Reference Board ^")

    # ### Boat Length 5 ### #
    print("Enter the start point of a ship with length 5:")
    start_point, direction = get_boat_input()

    place_ship("player2", p2_board, start_point, calc_endpoint(start_point, 5, direction))

    display_board(p2_board, True)  # Prints player 2's board with their ship placed on the board

    # ### Boat Length 4 ### #

    print("Enter the start point of a ship with length 4:")
    start_point, direction = get_boat_input()

    place_ship("player2", p2_board, start_point, calc_endpoint(start_point, 4, direction))

    display_board(p2_board, True)

    # ### Boat Length 4 ### #

    print("Enter the start point of a ship with length 4:")
    start_point, direction = get_boat_input()

    place_ship("player2", p2_board, start_point, calc_endpoint(start_point, 4, direction))

    display_board(p2_board, True)

    # ### Boat Length 3 ### #

    print("Enter the start point of a ship with length 3:")
    start_point, direction = get_boat_input()

    place_ship("player2", p2_board, start_point, calc_endpoint(start_point, 3, direction))

    display_board(p2_board, True)

    # ### Boat Length 2 ### #

    print("Enter the start point of a ship with length 2:")
    start_point, direction = get_boat_input()

    place_ship("player2", p2_board, start_point, calc_endpoint(start_point, 2, direction))

    display_board(p2_board, True)


def print_start():
    """
    Prints title and legend.
    """
    print(Fore.GREEN + Style.BRIGHT + "##################################\n"
                                      "#                                #\n"
                                      "#    WELCOME TO BATTLE YACHTS    #\n"
                                      "#                                #\n"
                                      "##################################\n\n\n" + Fore.RESET + Style.NORMAL)

    print("Legend:")  # Legend prints all the characters that will be used on the board
    print(Fore.BLUE + Style.BRIGHT + "~" + Fore.RESET + Style.NORMAL, end=" | ")
    print("Water Symbol")
    print(Fore.RED + Style.BRIGHT + "*" + Fore.RESET + Style.NORMAL, end=" | ")
    print("Yacht Hit Symbol")
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "#" + Fore.RESET + Style.NORMAL, end=" | ")
    print("Miss Symbol")
    print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "^" + Fore.RESET + Style.NORMAL, end=" | ")
    print("Yacht symbol\n")


# ######################### Main ########################## #
turn = 0
# Player1 => evens
# Player2 => odds

print_start()
repeat = True
while repeat:

    ans = input("Do you want to play against a person or AI?: ")
    if ans == "person":
        AI = False
        player1_place_boats()
        while not enough_boats(p1_board):  # Checks if all boats were placed validly on the board
            print(Fore.RED + Style.BRIGHT + "Your yacht placements were invalid. Try again" + Fore.RESET + Style.NORMAL)
            player1_place_boats()

        print("\n" * 50)
        input("Press Enter")

        player2_place_boats()
        while not enough_boats(p2_board):  # Checks if all boats were placed validly on the board
            print(Fore.RED + Style.BRIGHT + "Your yacht placements were invalid. Try again" + Fore.RESET + Style.NORMAL)
            player2_place_boats()

        while not is_win():
            print("\n" * 50)  # Prints blank lines to clear the board
            if turn % 2 == 0:
                input(Fore.BLUE + Style.BRIGHT + "PLAYER 1: Press Enter" + Fore.RESET + Style.NORMAL)
            else:
                input(Fore.RED + Style.BRIGHT + "PLAYER 2: Press Enter" + Fore.RESET + Style.NORMAL)

            if turn % 2 == 0:  # player 1 turn
                print(Fore.BLUE + Style.BRIGHT + "PLAYER 1 Your board:" + Fore.RESET + Style.NORMAL)
                display_board(p1_board, True)
                print(Fore.RED + Style.BRIGHT + "Opponent's board:" + Fore.RESET + Style.NORMAL)
                display_board(p2_board, False)
                update_board(p2_board, ask_for_move(), "player2")

            else:  # player 2 turn
                print(Fore.RED + Style.BRIGHT + "PLAYER 2 Your board:" + Fore.RESET + Style.NORMAL)
                print("Your board:")
                display_board(p2_board, True)
                print(Fore.BLUE + Style.BRIGHT + "Opponent's board:" + Fore.RESET + Style.NORMAL)
                display_board(p1_board, False)
                update_board(p1_board, ask_for_move(), "player1")
            turn += 1

    elif ans == "AI":
        AI = True
        ai_place_boats()
        player1_place_boats()
        while not enough_boats(p1_board):  # Checks if all boats were placed validly on the board
            print(Fore.RED + Style.BRIGHT + "Your yacht placements were invalid. Try again" + Fore.RESET + Style.NORMAL)
            player1_place_boats()

        print("\n" * 50)
        print("Your Board: ")
        display_board(p1_board, True)
        print("AI Board")
        display_board(p2_board, False)

        while not is_win():

            if turn % 2 == 0:
                update_board(p2_board, ask_for_move(), "player2")
                # player turn
            else:
                smart_hit(p1_board, "player1")
                print("Your Board after AI guess: ")
                display_board(p1_board, True)
                print("AI Board after your guess: ")
                display_board(p2_board, False)
            turn += 1
    else:
        print(Fore.RED + Style.BRIGHT + "You entered invalid input. Do you still want to play?" + Fore.RESET + Style.NORMAL)

    print(f"Player 1 wins: {p1_wins} | Player 2 wins: {p2_wins} | AI wins: {ai_wins}")  # Score board
  
    if input("Do you want to play again?(yes or no): ") != "yes":
        repeat = False
    else:
      ai_queue = []
      ai_last_hit = None
      sum_boat_length = 18
      player_1_hit_counter = 0
      player_2_hit_counter = 0
      board_length = 9
      AI = True
      boat_list_p1 = []
      boat_list_p2 = []
      p1_board = [['~' for j in range(board_length)] for i in range(board_length)]
      p2_board = [['~' for j in range(board_length)] for i in range(board_length)]
