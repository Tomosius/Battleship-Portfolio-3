# battleship.py test.py - this code is for testing CPU vs CPU game

# Import required libraries
import random  # For generating random numbers
import copy  # For creating deep copies of data structures
import os  # For clearing the terminal screen
import time  # For time-related functionalities


# Constants for map dimensions and default symbol
DEFAULT_MAP_HEIGHT = 10
DEFAULT_MAP_WIDTH = 10
map_height_cpu = "" # empty value for map size, it can be adjusted in settings, if not, function will assign irr DEFAULT_HEIGHT
map_width_cpu = ""# empty value for map size, it can be adjusted in settings, if not, function will assign irr DEFAULT_WIDTH
DEFAULT_SYMBOL = '?'  # Symbol representing an empty cell in the map
DEFAULT_GAPS_BETWEEN_MAPS = True

# Initialize 2D maps for CPU and Player
map_cpu_display = []
map_cpu_hidden = []
map_player_hidden = []
map_player = []

# Initialize game-related variables
save_map_height = "" # variable to keep for current game settings (when starting game, this will be used)
save_map_width = "" # variable to keep for current game settings (when starting game, this will be used)
save_fleet = {} # variable to keep for current game settings (when starting game, this will be used)
start_time = time.time()  # Record the start time for logging purposes
game_result = None  # Variable to store the game outcome (win, lose)
cpu_shot_log_tmp = []  # Temporarily store CPU actions if a ship is hit

# Initialize a log to store game actions
game_actions_log = [
    ["player or CPU", "time", "column", "row", "action outcome"]
]

# Define color codes for different ship statuses
DEFAULT_COLORS = {
    "DarkYellow": "\u001b[33m",  # Single cell ship
    "DarkBlue": "\u001b[34m",  # Horizontal ship
    "DarkGreen": "\u001b[32m",  # Vertical ship
    "DarkRed": "\u001b[31m",  # Damaged or Sunk ship
    "LightGray": "\u001b[37m",  # Miss
    "Reset": "\u001b[0m",  # Reset ANSI escape code in string
}

# Define symbols for different ship statuses
SHIP_SYMBOLS = {
    "Single": [DEFAULT_COLORS["DarkYellow"] + chr(0x25C6) + DEFAULT_COLORS["Reset"]],
    "Horizontal": [
        DEFAULT_COLORS["DarkBlue"] + chr(0x25C0) + DEFAULT_COLORS["Reset"],
        DEFAULT_COLORS["DarkBlue"] + chr(0x25A4) + DEFAULT_COLORS["Reset"]
    ],
    "Vertical": [
        DEFAULT_COLORS["DarkGreen"] + chr(0x25B2) + DEFAULT_COLORS["Reset"],
        DEFAULT_COLORS["DarkGreen"] + chr(0x25A5) + DEFAULT_COLORS["Reset"]
    ],
    "Hit": [DEFAULT_COLORS["DarkRed"] + chr(0x25A6) + DEFAULT_COLORS["Reset"]],
    "Miss": [DEFAULT_COLORS["LightGray"] + chr(0x2022) + DEFAULT_COLORS["Reset"]],
    "SingleSunk": [DEFAULT_COLORS["DarkRed"] + chr(0x25C6) + DEFAULT_COLORS["Reset"]],
    "HorizontalSunk": [
        DEFAULT_COLORS["DarkRed"] + chr(0x25C0) + DEFAULT_COLORS["Reset"],
        DEFAULT_COLORS["DarkRed"] + chr(0x25A4) + DEFAULT_COLORS["Reset"]
    ],
    "VerticalSunk": [
        DEFAULT_COLORS["DarkRed"] + chr(0x25B2) + DEFAULT_COLORS["Reset"],
        DEFAULT_COLORS["DarkRed"] + chr(0x25A5) + DEFAULT_COLORS["Reset"]
    ],
}

# Define the default fleet configuration
DEFAULT_FLEET = {
    "AircraftCarrier": {"Size": 5, "Quantity": 1, "Coordinates": []},
    "Battleship": {"Size": 4, "Quantity":2, "Coordinates": []},
    "Cruiser": {"Size": 3, "Quantity": 2, "Coordinates": []},
    "Submarine": {"Size": 3, "Quantity":1, "Coordinates": []},
    "Destroyer": {"Size": 2, "Quantity": 2, "Coordinates": []},
    "Tugboat": {"Size": 1, "Quantity": 4, "Coordinates": []}
}
fleet_cpu = {} # this will be later used when starting game, to store player fleet information and each ship coordinates
fleet_player = {} # this will be used later to store CPU fleet, to store CPU fleet information and each ship coordinates


# Game instructions and settings, presented as lists
INSTRUCTIONS = ("1. Ships can be aligned Horizontally or Vertically",
                "2. Ships can NOT be touching each other, but this can be changed in game settings",
                "3. Default game map is size 10 by 10",
                "4. Player has to enter coordinates as follows: Y,X - ROW, COLUMN. Numbers separated by COMMA",
                "5. " "\u001b[34mHORIZONTAL\u001b[0m" " ships will be BLUE color",
                "6. " "\u001b[32mVERTICAL\u001b[0m" " ships will be GREEN color",
                "7. " "\u001b[31mDAMAGED\u001b[0m" " ships will be green color",
                "If you wwant to adjust game settings type " "\u001b[33mY\u001b[0m" " and press ENTER",
                "If you want to start game just press " "\u001b[33mENTER\u001b[0m")

GAME_ADJUST_MAIN = ["If you to adjust your FLEET, type" "\u001b[33mF\u001b[0m" " and press enter",
                    "If you want to change MAP size, type " "\u001b[33mM\u001b[0m" " and press enter",
                    "If you want to change coordinate system Indexes from numbers to letters, type" "\u001b[33mI\u001b[0m" " and press enter",
                    "If you want to change coordinate entering style from ROW+COLUMN to COLUMN+ROW, type " "\u001b[33mS\u001b[0m" " and press enter",
                    "",
                    "To return to main menu, press " "\u001b[33m0\u001b[0m" " and press enter"]

# Helper Functions
# ----------------

def clear_terminal():
    """
    Clear the terminal screen.
    This function uses different commands for POSIX (Unix/Linux/MacOS) and Windows systems.
    """
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')


def print_acid_effect():
    """
    Prints a text art of an acid-like effect to the terminal.

    This function performs the following steps:
    1. Clears the terminal screen for a clean start.
    2. Prints each character of the `acid_text` string one by one with a slight delay.
    3. Waits for a short moment to let the user view the effect.
    4. Clears the terminal screen again.

    Note: The function uses the `os` and `time` modules.
    """
    # ASCII art representation of the acid effect
    acid_logo = """
                              _  |____________|  _
                       _=====| | |            | | |==== _
                 =====| |.---------------------------. | |====
   <--------------------'   .  .  .  .  .  .  .  .   '--------------/
     \\                                                             /
      \\_______________________________________________WWS_________/
  wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
   wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww

    """
    acid_text = """
██████   █████  ████████ ████████ ██      ███████ ███████ ██   ██ ██ ██████       ██████   █████  ███    ███ ███████ 
██   ██ ██   ██    ██       ██    ██      ██      ██      ██   ██ ██ ██   ██     ██       ██   ██ ████  ████ ██      
██████  ███████    ██       ██    ██      █████   ███████ ███████ ██ ██████      ██   ███ ███████ ██ ████ ██ █████   
██   ██ ██   ██    ██       ██    ██      ██           ██ ██   ██ ██ ██          ██    ██ ██   ██ ██  ██  ██ ██      
██████  ██   ██    ██       ██    ███████ ███████ ███████ ██   ██ ██ ██           ██████  ██   ██ ██      ██ ███████ 
    """

    # Step 1: Clear the terminal
    clear_terminal()

    # Step 2: Print the text character by character
    for char in acid_logo:
        print(char, end='', flush=True)  # Using flush=True to force the output to be printed
        time.sleep(0.001)  # Delay of 0.005 seconds for each character

    # Step 3: Wait for a moment to let the user view the effect
    time.sleep(1)

    # Step 4: Clear the terminal again
    clear_terminal()

    # Step 5: Print the text character by character
    for char in acid_text:
        print(char, end='', flush=True)  # Using flush=True to force the output to be printed
        time.sleep(0.001)  # Delay of 0.005 seconds for each character

    # Step 3: Wait for a moment to let the user view the effect
    time.sleep(1)

    # Step 4: Clear the terminal again
    clear_terminal()


# Initial game start functions
#-----------------------------

# Main Functions
# --------------

def create_map(width, height, symbol):
    """
    Initialize a 2D map with a default symbol.

    Args:
        width (int): The width of the map.
        height (int): The height of the map.
        symbol (str): The default symbol to fill the map with.

    Returns:
        List[List[str]]: A 2D list initialized with the default symbol.
    """
    return [[symbol for _ in range(height)] for _ in range(width)]

# Print functions
#----------------

def print_fleet(fleet):
    """Print the fleet information in a formatted manner.

    Args:
        fleet (dict): Dictionary containing fleet information.
    """
    print("{:<20} {:<10} {:<10}".format(
        "ShipType", "Size", "Quantity"))
    print("=" * 40)
    for ship, ship_details in fleet.items():
        size = ship_details["Size"]
        quantity = ship_details["Quantity"]
        print("{:<20} {:<10} {:<10} ".format(
            ship, size, quantity))



def print_fleet_with_coodinates(fleet):
    """Print the fleet information in a formatted manner.

    Args:
        fleet (dict): Dictionary containing fleet information.
    """
    print("{:<20} {:<10} {:<10} {:<50}".format(
        "ShipType", "Size", "Quantity", "Coordinates"))
    print("=" * 40)
    for ship, ship_details in fleet.items():
        size = ship_details["Size"]
        quantity = ship_details["Quantity"]
        coordinates = str(ship_details["Coordinates"])  # Convert the list to a string
        print("{:<20} {:<10} {:<10} {:<50}".format(
            ship, size, quantity, coordinates))

def print_map(game_map):
    """
    Print the game map in a human-readable format.

    Args:
        game_map (list): A 2D list representing the game map,
                         where each cell contains the status of a ship
                         or water.

    Output:
        The function will print the game map to the console.
    """

    # Print column headers (0, 1, 2, ..., N)
    print("   ", end="")
    for col_index in range(len(game_map[0])):
        print(f"{col_index}  ", end="")

    # Print a separator line between headers and table
    print("\n   " + "=" * (len(game_map[0]) * 3))

    # Loop through each row
    for row_index, row in enumerate(game_map):
        # Print row header
        print(f"{row_index} |", end=" ")

        # Loop through each cell in the row
        for value in row:
            # Print the cell value followed by two spaces
            print(f"{value}  ", end="")

        # Move to the next line at the end of each row
        print()


def print_two_maps(map_left, map_right, label_left, label_right, gap=10):
    """
    Print two 2D maps side by side with labels and a customizable gap.

    Args:
        map_left (list): A 2D list representing the first map.
        map_right (list): A 2D list representing the second map.
        label_left (str): Label for the first map.
        label_right (str): Label for the second map.
        gap (int): Number of blank spaces between the two maps. Default is 10.
    """

    # Constants for character dimensions and formatting
    char_width = len("X")  # Width of a single character (assuming monospaced font)

    # Calculate the maximum number of digits in row and column indices
    num_digits_map_width = len(str(len(map_left[0])))
    num_digits_map_height = len(str(len(map_left)))

    # Create a string of blank spaces for the gap between maps
    gap_str = ' ' * gap

    # Calculate the left-side offset for aligning map and row indices
    row_index_separator = " | "
    print_map_left_offset = " " * (num_digits_map_height + len(row_index_separator))

    # Center-align the labels for both maps
    number_char_table_total = (len(map_left[0]) * (num_digits_map_width + char_width + 1))
    label_left_centered = label_left.center(number_char_table_total)
    label_right_centered = label_right.center(number_char_table_total)

    # Print the centered labels for both maps
    print(f"{print_map_left_offset}{label_left_centered}{gap_str}{print_map_left_offset} {label_right_centered}")

    # Print column headers for both maps
    print(print_map_left_offset, end=" ")
    for col_index in range(len(map_left[0])):
        if col_index == len(map_left[0]) - 1:  # Check if it's the last column index
            print(f"{col_index}".rjust(num_digits_map_height + char_width),
                  end="")  # i do not want gap after last index, as it will be not aligned
        else:
            print(f"{col_index}".rjust(num_digits_map_height + char_width), end=" ")
    print(gap_str, print_map_left_offset, end=" ")
    for col_index in range(len(map_right[0])):
        # Right-justify the column index with proper spacing
        print(f"{col_index}".rjust(num_digits_map_height + char_width), end=" ")
    print()
    # Print the horizontal separator line
    # This step prints a separator line to visually separate the maps
    separator_length_left = len(map_left[0]) * (num_digits_map_width + char_width + 1)
    separator_length_right = len(map_right[0]) * (num_digits_map_width + char_width + 1)
    print(print_map_left_offset + "=" * separator_length_left, end=gap_str)
    print(" " + print_map_left_offset + "=" * separator_length_right)

    # Loop through each row to print map values
    for row_index, (row_left, row_right) in enumerate(zip(map_left, map_right)):
        # Print row for the left map
        print(f"{row_index}".rjust(num_digits_map_width + 1), end=row_index_separator)
        for value in row_left:
            width = len(str(value))
            # Right-justify the map value with proper spacing
            print(f"{value}".rjust(num_digits_map_height + char_width - (char_width - width)), end=" ")
        # Insert the gap between the two maps
        print(gap_str, end="")
        # Print row for the right map
        print(f"{row_index}".rjust(num_digits_map_width + 1), end=row_index_separator)
        for value in row_right:
            width = len(str(value))
            # Right-justify the map value with proper spacing
            print(f"{value}".rjust(num_digits_map_height + char_width - (char_width - width)), end=" ")
        # Move to the next line
        print()



def print_map_and_list(map_left, instructions, label_left, gap=10):
    """
    Print a 2D map and a list side by side with labels and a customizable gap.

    Args:
        map_left (list): A 2D list representing the first map.
        instructions (list): A list of strings representing the instructions.
        label_left (str): Label for the first map.
        gap (int): Number of blank spaces between the map and the instructions. Default is 10.
    """

    # Constants for character dimensions and formatting
    char_width = len("X")  # Width of a single character (assuming monospaced font)

    # Calculate the maximum number of digits in row and column indices
    num_digits_map_width = len(str(len(map_left[0])))
    num_digits_map_height = len(str(len(map_left)))

    # Create a string of blank spaces for the gap between map and instructions
    gap_str = ' ' * gap

    # Calculate the left-side offset for aligning map and row indices
    row_index_separator = " | "
    print_map_left_offset = " " * (num_digits_map_height + len(row_index_separator))

    # Center-align the label for the map
    number_char_table_total = (len(map_left[0]) * (num_digits_map_width + char_width + 1))
    label_left_centered = label_left.center(number_char_table_total)

    # Print the centered label for the map
    print(f"{print_map_left_offset}{label_left_centered}")

    # Print column headers for the map
    print(print_map_left_offset, end=" ")
    for col_index in range(len(map_left[0])):
        print(f"{col_index}".rjust(num_digits_map_height + char_width), end=" ")
    print(gap_str, "Instructions")
    print("    ".rjust(num_digits_map_width + 1),"=" * (number_char_table_total))  # Draw a separator line

    # Loop through each row to print map values and instructions
    for row_index in range(max(len(map_left), len(instructions))):
        # Print row for the map
        if row_index < len(map_left):
            print(f"{row_index}".rjust(num_digits_map_width + 1), end=row_index_separator)
            for value in map_left[row_index]:
                width = len(str(value))
                print(f"{value}".rjust(num_digits_map_height + char_width - (char_width - width)), end=" ")
        else:
            print(" " * (num_digits_map_width + num_digits_map_height + len(row_index_separator) + char_width * len(
                map_left[0])), end="")

        # Insert the gap between the map and the instructions
        print(gap_str, end="")

        # Print instruction for the row
        if row_index < len(instructions):
            print(instructions[row_index])
        else:
            print()

# Map manipulating functions
#---------------------------


def create_coordinate_list(row, column,alignment,ship_size):
    coordinates_list = []
    if ship_size == 1:
        coordinates_list.append([row,column])
    else:
        if alignment == "Horizontal" or alignment == "HorizontalSunk":
            for cell in range(ship_size):
                coordinates_list.append([row, column + cell])
        if alignment == "Vertical" or alignment == "VerticalSunk":
            for cell in range(ship_size):
                coordinates_list.append([row + cell, column])
    return  coordinates_list


def map_allocate_empty_space_for_ship(game_map, coordinates_list):
    """
    Creating empty space around ship, so ships can not be touching each other. So function will create pattern of Miss symbols, so when deploying ships, they can not be touching. when deployment of all ships is completed, these symbols will be changed back to DEFAULT_SYMBOL

    Args:
        game_map (list): The 2D map where the ship will be deployed.
        ship_size (int): The length of the ship.
        coordinates (list): Starting coordinates [row, column] for the ship.
        alignment (str): The alignment of the ship ("Horizontal" or "Vertical").

    Global Variables:
        SHIP_SYMBOLS (dict): Dictionary containing ship symbols.

    Returns:
        None

    """

    # Use the global variable SHIP_SYMBOLS to get the ship symbols
    global SHIP_SYMBOLS

    blank_space = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]


    #creating big pattern of default symbols
    blank_space_coordinates_list = []
    for space in blank_space:
        blank_row, blank_column = space
        for coordinate in  coordinates_list:
            new_row, new_column = coordinate
            new_blank_row, new_blank_column = blank_row + new_row, blank_column + new_column
            blank_space_coordinates_list.append([new_blank_row, new_blank_column])

    # now applying all spaces to map
    for new_space in blank_space_coordinates_list:
        b_row, b_column = new_space
        if 0 <= b_row < len(game_map) and 0 <= b_column < len(game_map[0]):
            game_map[b_row][b_column] = SHIP_SYMBOLS["Miss"][0]


def map_show_ship_or_symbols(game_map, coordinates_list, alignment):
    """
    Deploy a single ship on the map.

    Args:
        game_map (list): The 2D map where the ship will be deployed.
        length (int): The length of the ship.
        coordinates (list): Starting coordinates [row, column] for the ship.
        alignment (str): The alignment of the ship ("Horizontal" or "Vertical").
        ship_name (str): The name of the ship.
        fleet (dict): Dictionary containing fleet information.

    Global Variables:
        SHIP_SYMBOLS (dict): Dictionary containing ship symbols.

    Returns:
        list: Nested list of .ship coordinates
    """
    # Use the global variable SHIP_SYMBOLS to get the ship symbols
    global SHIP_SYMBOLS

    # Use the global variable GAPS_BETWEEN_MAPS to get Trye or False for ships NOT touching
    global DEFAULT_GAPS_BETWEEN_MAPS

    # Before we start displaying ships on map, if spaces between ships is True, we will allocate blank space, then depliy ships
    if DEFAULT_GAPS_BETWEEN_MAPS == True:
        map_allocate_empty_space_for_ship(game_map, coordinates_list)


    # Handle the case for single-cell ships
    if len(coordinates_list) == 1:
        row, column = coordinates_list[0]
        game_map[row][column] = SHIP_SYMBOLS[alignment][0]

    # Handle the case for multi-cell ships
    else:
        row, column = coordinates_list[0]
        game_map[row][column] = SHIP_SYMBOLS[alignment][0]
        for cell in range(1,len(coordinates_list)):
            row, column = coordinates_list[cell]
            game_map[row][column] = SHIP_SYMBOLS[alignment][1]


def map_show_only_ships(game_map):
    """
    function to remove Miss symbols from map and replace them with DEFAULT_SYMBOL, so map shows just ships
    :param game_map:
    :return:
    """
    global SHIP_SYMBOLS, DEFAULT_SYMBOL
    for row in range(len(game_map)):
        for column in range(len(game_map[0])):
            if game_map[row][column] == SHIP_SYMBOLS["Miss"][0]:
                game_map[row][column] = DEFAULT_SYMBOL
    return game_map

