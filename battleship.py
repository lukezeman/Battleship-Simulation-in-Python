'''
File: battleship.py
Author: Luke Zeman
Course: CSC 120, Spring 2024
Purpose: This program takes a user-input file and reads the placement of ships
    on a battleship board. The program then reads another user-input file and
    determines if the guesses are hits or misses. The program prints the result
    of each guess and ends the game if all ships are sunk.
'''

import sys

class GridPos:
    '''
    This class represents a position on the grid.

    This class defines methods to store different attributes of a position on 
    the grid.
    '''
    def __init__(self, x_coord, y_coord):
        '''
        This special method initializes attributes of the GridPos object.

        Parameters:
            self -- The object of the class.
            x_coord -- The x-coordinate of the position.
            y_coord -- The y-coordinate of the position.

        Returns: None
        '''
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._ship = None
        self._guessed = False

    def x_coord(self):
        return self._x_coord
    
    def y_coord(self):
        return self._y_coord
    
    def ship(self):
        return self._ship
    
    def set_ship(self, ship):
        self._ship = ship
    
    def guessed(self):
        return self._guessed
    
    def set_guessed(self, value):
        self._guessed = value

    def __str__(self):
        return str((self._x_coord, self._y_coord))

class Board:
    '''
    This class represents a board of a battleship game.

    This class defines methods to place ships on the board and show the grid.
    '''
    def __init__(self):
        '''
        This special method initializes attributes of the Board object.

        Parameters:
            self -- The object of the class.
        
        Returns: None
        '''
        self._grid = []

        for i in range(10):
            row = []
            for j in range(10):
                row.append(GridPos(j, i))
            self._grid.append(row)

        self._collection = []

    def grid(self):
        return self._grid
    
    def collection(self):
        return self._collection

    def show_grid(self):
        '''
        This method prints the board.

        Parameters:
            self -- The object of the class.

        Returns: None
        '''
        for row in self._grid:
            string = ""
            for item in row:
                if item.ship() == None:
                    string += ". "
                else:
                    string += item.ship().type() + " "
            print(string)

    def place_ship(self, ship):
        '''
        This method places a ship object on the board.

        Parameters:
            self -- The object of the class.
            ship -- The ship object to be placed on the board.
        
        Returns: None
        '''
        x_cord1 = ship.pos()[0]
        y_cord1 = ship.pos()[1]
        x_cord2 = ship.pos()[2]
        y_cord2 = ship.pos()[3]
        ship.set_pos([])

        # Horizontal ship.
        if y_cord1 == y_cord2:
            x_min = min(x_cord1, x_cord2)
            x_max = max(x_cord1, x_cord2)
            x_cord1 = x_min
            x_cord2 = x_max
            while x_cord1 <= x_cord2:
                ship.pos().append(tuple([9 - y_cord1, x_cord1]))
                self._grid[9 - y_cord1][x_cord1].set_ship(ship)
                x_cord1 += 1
        # Vertical ship.
        else:
            y_min = min(y_cord1, y_cord2)
            y_max = max(y_cord1, y_cord2)
            y_cord1 = y_min
            y_cord2 = y_max
            while y_cord1 <= y_cord2:
                ship.pos().append(tuple([9 - y_cord1, x_cord1]))
                self._grid[9 - y_cord1][x_cord1].set_ship(ship)
                y_cord1 += 1
        
    def __str__(self):
        return "Grid -> " + self._grid + '\n' + "Ships -> " + self._collection

class Ship:
    '''
    This class represents a ship in a battleship game.
    
    This class defines methods to store different attributes of a ship.
    '''
    def __init__(self, type, size, pos, non_hit):
        self._type = type
        self._size = size
        self._pos = pos
        self._non_hit = non_hit
    
    def type(self):
        return self._type
    
    def size(self):
        return self._size
    
    def pos(self):
        return self._pos
    
    def set_pos(self, list):
        self._pos = list
    
    def non_hit(self):
        return self._non_hit
    
    def hit(self):
        self._non_hit -= 1

    def __str__(self):
        return "Type -> " + self._type + " | " + "Size -> " + str(self._size) \
        + " | " + "Position -> " + str(self._pos) + " | " + "# Non-Hit -> " \
        + str(self._non_hit)

def read_placement_file(placement_file):
    '''
    This function reads a user-input file and returns a board object and a 
    list of file lines.

    Parameters:
        placement_file -- The file to be read.

    Returns: A board object and a list of file lines.
    '''
    file = open(placement_file)
    board = Board()
    known_types = {"A": 5, "B": 4, "S": 3, "D": 3, "P": 2}
    lines = []

    for line in file:
        # Error checking.
        check_out_of_bounds(line)
        check_if_diagonal(line)

        lines.append(line)
        placement = line.strip().split()
        if placement[0] in known_types:
            type = placement[0]
            ship = Ship(type, known_types[type], to_int(placement[1:]), 
                        known_types[type])
            board._collection.append(ship)
            known_types.pop(type)
        else:
            print("ERROR: fleet composition incorrect")
            sys.exit(0)

    if len(known_types) != 0:
        print("ERROR: fleet composition incorrect")
        sys.exit(0)

    file.close()
    return board, lines

def to_int(list):
    '''
    This function converts a list of strings to a list of integers.

    Parameters:
        list -- A list of strings.
    
    Returns: A list of integers.
    '''
    for i in range(len(list)):
        list[i] = int(list[i])
    return list

def check_out_of_bounds(placement):
    '''
    This function checks if a ship is out-of-bounds and exits the program
    accordingly.

    Parameters:
        placement -- A string representing the placement of a ship.

    Returns: None
    '''
    temp = placement.strip().split()
    for num in temp[1:]:
        if int(num) < 0 or int(num) >= 10:
            print("ERROR: ship out-of-bounds: " + placement.strip())
            sys.exit(0)

def check_if_diagonal(placement):
    '''
    This function checks if a ship is diagonal and exits the program 
    accordingly.

    Parameters:
        placement -- A string representing the placement of a ship.

    Returns: None
    '''
    temp = placement.strip().split()
    if temp[1] != temp[3] and temp[2] != temp[4]:
        print("ERROR: ship not horizontal or vertical: " + placement.strip())
        sys.exit(0)

def check_overlap(ship, grid, line):
    '''
    This function checks if a ship overlaps with another ship and exits the
    program accordingly.

    Parameters:
        ship -- A Ship object.
        grid -- A 2D list of GridPos objects.
        line -- A string representing the placement of a ship.

    Returns: None
    '''
    stored = []
    for row in grid:
        for item in row:
            if item.ship() != None:
                stored.extend(item.ship().pos())
    ship_pos = get_coords(ship)
    for coord in ship_pos:
        if coord in stored:
            print("ERROR: overlapping ship: " + line.strip())
            sys.exit(0)

def check_wrong_size(ship, line):
    '''
    This function checks if a ship is the correct size and exits the program
    accordingly.

    Parameters:
        ship -- A Ship object.
        line -- A string representing the placement of a ship.

    Returns: None
    '''
    sizes = {"A": 5, "B": 4, "S": 3, "D": 3, "P": 2}
    if sizes[ship.type()] != len(ship.pos()):
        print("ERROR: incorrect ship size: " + line)
        sys.exit(0)

def guess(file_name, board):
    '''
    This function reads a user-input file and determines if a guess invalid, 
    and calls the hit_or_miss function if it's valid.

    Parameters:
        file_name -- The file to be read.
        board -- The board object.

    Returns: None
    '''
    ships_alive = ["A", "B", "S", "D", "P"]
    file = open(file_name)
    for line in file:
        guess = to_int(line.strip().split())
        if guess[0] < 0 or guess[0] >= 10 or guess[1] < 0 or guess[0] >= 10:
            print("illegal guess")
        else:
            hit_or_miss(guess, board, ships_alive, file)

def hit_or_miss(guess, board, ships_alive, file):
    '''
    This function determines if a guess is a hit or miss and prints the result.

    Parameters:
        guess -- A list of integers representing a guess.
        board -- The board object.
        ships_alive -- A list of strings representing the ships that are still
            alive.
        file -- The file to be read.

    Returns: None
    '''
    x_coord = guess[0]
    y_coord = 9 - guess[1]
    item = board.grid()[y_coord][x_coord]

    if item.ship() == None:
        if item.guessed():
            print("miss (again)")
        else:
            print("miss")
            item.set_guessed(True)
    else:
        if item.guessed():
            print("hit (again)")
        else:
            # Registers a hit, checks if sunk and if all ships are sunk.
            item.ship().hit()
            item.set_guessed(True)
            if item.ship().non_hit() == 0:
                ships_alive.pop(ships_alive.index(item.ship().type()))
                print("{} sunk".format(item.ship().type()))

                if len(ships_alive) == 0:
                    print("all ships sunk: game over")
                    file.close()
                    sys.exit(0)
            else:
                print("hit")

def get_coords(ship):
    '''
    This function returns a list of coordinates of a ship.

    Parameters:
        ship -- A Ship object.
    
    Returns: A list of tuples representing the coordinates of a ship.
    '''
    x_cord1 = ship.pos()[0]
    y_cord1 = ship.pos()[1]
    x_cord2 = ship.pos()[2]
    y_cord2 = ship.pos()[3]
    positions = []

    # Horizontal ship.
    if y_cord1 == y_cord2:
        x_min = min(x_cord1, x_cord2)
        x_max = max(x_cord1, x_cord2)
        x_cord1 = x_min
        x_cord2 = x_max
        while x_cord1 <= x_cord2:
            positions.append(tuple([9 - y_cord1, x_cord1]))
            x_cord1 += 1
    # Vertical ship.
    else:
        y_min = min(y_cord1, y_cord2)
        y_max = max(y_cord1, y_cord2)
        y_cord1 = y_min
        y_cord2 = y_max
        while y_cord1 <= y_cord2:
            positions.append(tuple([9 - y_cord1, x_cord1]))
            y_cord1 += 1

    return positions

def main():
    placement_file = input()
    board, lines = read_placement_file(placement_file)

    for index in range(len(board._collection)):
        check_overlap(board._collection[index], board._grid, lines[index])
        board.place_ship(board._collection[index])
        check_wrong_size(board._collection[index], lines[index])

    guess_file = input()
    guess(guess_file, board)

main()