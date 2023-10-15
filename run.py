# battleship.py test.py - this code is for testing CPU vs CPU game

# Import required libraries
import random  # For generating random numbers
import copy  # For creating deep copies of data structures
import os  # For clearing the terminal screen
import time  # For time-related functionalities
import re # For handling user input expressions


# Constants for map dimensions and default symbol
DEFAULT_MAP_HEIGHT = 10
DEFAULT_MAP_WIDTH = 10
map_height_cpu = "" # empty value for map size, it can be adjusted in settings, if not, function will assign irr DEFAULT_HEIGHT
map_width_cpu = ""# empty value for map size, it can be adjusted in settings, if not, function will assign irr DEFAULT_WIDTH
DEFAULT_SYMBOL = '?'  # Symbol representing an empty cell in the map
DEFAULT_GAPS_BETWEEN_MAPS = True
MAP_ROW_INDEXES = "1234567890"
MAP_COLUMN_INDEXES = "1234567890"

# Initialize 2D maps for CPU and Player
map_cpu_display = []
map_cpu_hidden = []
map_player_hidden = []
map_player_ = []

# Initialize game-related variables
save_map_height = "" # variable to keep for current game settings (when starting game, this will be used)
save_map_width = "" # variable to keep for current game settings (when starting game, this will be used)
save_fleet = {} # variable to keep for current game settings (when starting game, this will be used)
start_time = time.time()  # Record the start time for logging purposes
game_result = None  # Variable to store the game outcome (win, lose)
cpu_shot_log_tmp = []  # Temporarily store CPU actions if a ship is hit

# Initialize a log to store game actions
game_actions_log = []


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
    "Battleship": {"Size": 4, "Quantity":1, "Coordinates": []},
    "Cruiser": {"Size": 3, "Quantity": 2, "Coordinates": []},
    "Submarine": {"Size": 3, "Quantity":1, "Coordinates": []},
    "Destroyer": {"Size": 2, "Quantity": 2, "Coordinates": []},
    "Tugboat": {"Size": 1, "Quantity": 4, "Coordinates": []}
}
fleet_cpu = {} # this will be later used when starting game, to store player fleet information and each ship coordinates
fleet_player = {} # this will be used later to store CPU fleet, to store CPU fleet information and each ship coordinates


# Game instructions and settings, presented as lists
INSTRUCTIONS = ["1. Ships can be aligned Horizontally or Vertically",
                "2. Ships can NOT be touching each other, but this can be changed in game settings",
                "3. Default game map is size 10 by 10",
                "4. Player has to enter coordinates as follows: Y,X - ROW, COLUMN. Numbers separated by COMMA",
                "5. " "\u001b[34mHORIZONTAL\u001b[0m" " ships will be BLUE color",
                "6. " "\u001b[32mVERTICAL\u001b[0m" " ships will be GREEN color",
                "7. " "\u001b[31mDAMAGED\u001b[0m" " ships will be green color",
                "If you wwant to adjust game settings type " "\u001b[33mY\u001b[0m" " and press ENTER",
                "If you want to start game just press " "\u001b[33mENTER\u001b[0m"]

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
    This function uses different commands for POSIX (Unix/Linux/macOS) and Windows systems.
    """
    if os.name == 'posix':  # Unix/Linux/macOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')

# Game Intro functions
#---------------------
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
def create_initial_game_variables(height, width, symbol, fleet):
    new_map = create_map(width, height, symbol)
    new_map_hidden = copy.deepcopy(new_map)
    new_fleet = copy.deepcopy(fleet)
    return new_map, new_map_hidden, new_fleet


def game_instructions(height, width, symbol, fleet):

    global SHIP_SYMBOLS, INSTRUCTIONS, DEFAULT_MAP_HEIGHT, DEFAULT_MAP_WIDTH, DEFAULT_FLEET
    # genetrating map and fleet, to be displayed on left side , on right side will be instrucions
    tmp_map = create_map(height, width, symbol)
    tmp_fleet = copy.deepcopy(fleet)
    cpu_deploy_all_ships(tmp_map,tmp_fleet)

    while True:
        print_map_and_list(tmp_map, INSTRUCTIONS, "MAP EXAMPLE", 10)
        try:
            # Ask the user if they would like to adjust game settings
            changes = input().capitalize()
            # If the user opts to adjust settings
            if changes in ["Y", "YES"]:
                DEFAULT_MAP_HEIGHT, DEFAULT_MAP_WIDTH, DEFAULT_FLEET = modify_game_setttings(height, width, symbol, fleet)
                continue
            else:

                return False

        # Handle keyboard interrupt to gracefully exit the function
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False


# Game Adjust Settings functions
#------------------------------

def modify_game_setttings(height, width, symbol, fleet):
    """
    Adjust game settings, including the map and BattleShips Fleet.
    This function offers the user a choice to modify the game map,
    modify existing ships, add new ships, or finish adjustments.

    Args:

    Returns:
        bool: True if the game adjustment was interrupted, False otherwise.
    """

    # Start an infinite loop to continuously offer adjustment options to the user
    global  SHIP_SYMBOLS, GAME_ADJUST_MAIN, MAP_ROW_INDEXES, MAP_COLUMN_INDEXES, DEFAULT_MAP_HEIGHT, DEFAULT_MAP_WIDTH, DEFAULT_FLEET

    while True:

        # generating new map to display on left side
        tmp_fleet = copy.deepcopy(fleet) # resetting fleet so new ship alignment can be displayed
        tmp_map = create_map(height, width, symbol)
        tmp_map, tmp_fleet = cpu_deploy_all_ships(tmp_map, tmp_fleet)
        clear_terminal()
        print_map_and_list(tmp_map, GAME_ADJUST_MAIN, "MAP EXAMPLE", )
        try:
            user_input = input().capitalize()
            if not user_input:
                print("Invalid input. Please type F, M, I, S, or 0 - tp return back to Instructions")
                continue
            if user_input == "F":
                DEFAULT_FLEET = modify_game_settings_fleet(height, width, symbol, fleet)

                # adjust fleet
            elif user_input == "M":
                print("M")
                DEFAULT_MAP_HEIGHT, DEFAULT_MAP_WIDTH = modify_game_settings_map(height, width, symbol, fleet)
            elif user_input == "I":
                print("I")
                MAP_ROW_INDEXES, MAP_COLUMN_INDEXES = modify_game_settings_labels(height, width, symbol, fleet)
                # change indexes
            elif user_input == "S":
                print("S")
                # user adjust row-column input type
            elif user_input == "0":
                return height, width, fleet

        # Handle keyboard interrupt to gracefully exit the function
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False


def modify_game_settings_labels(height, width, symbol, fleet):
    input_validation = True
    input_values = [1,2]
    while True:
        try:

            if input_validation == False:
                print(f'You have entered {len(input_values)}, i require just 2: Row symbol and Column')
            print(f" Current game map coordinate system is numeric, if you want to change it, enter 2 symbols.  Rows then columns")
            print(f' First symbol will be rows indexes, if you type number, it will be digits, if you enter letter - will be letters')
            print(f' Second symbol will be column indexes, if you type number, it will be digits, if you enter letter - will be letters')
            user_input = input()
            input_validation, input_values, output_text = validate_user_input(user_input, 2)
            if input_validation == True:
                # creating indexes for rows
                if input_values[0].isdigit():
                    map_rows_indexes = list(range(height + 1))
                elif input_values[0].isalpha():
                    map_rows_indexes =  [chr(97 + i) for i in range(height + 1)]
                # creating indexes for columns
                if input_values[1].isdigit():
                    map_column_indexes = list(range(width + 1))
                elif input_values[1].isalpha():
                    map_column_indexes = [chr(97 + i) for i in range(width + 1)]
                return map_rows_indexes, map_column_indexes





        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False




def modify_game_settings_map(height, width, symbol, fleet):
    input_values = [10,10]
    input_validation = True
    check_result = True
    while True:
        try:
            clear_terminal()
            if input_validation == False:
                if len(input_values) !=2:
                    print(f'You have entered just {len(input_values)} values, i require 2: Height and Width')
                else:
                    for i in range(len(input_values)):
                        print(output_text[i])
            if check_result == False:
                print(f' Sorry but I believe you need bigger size of map for current fleet')

            print(f'Current game map is {height} height and {width} wide. as you hhave selected to modify these parameters, please type height and width and press ENTER')
            user_input = input()
            input_validation, input_values, output_text = validate_user_input(user_input,2,"integer")
            if input_validation == True: # user entered values are valid, now we check can we mae map with given fleet
                tmp_map = create_map(int(input_values[0]),int(input_values[1]), symbol)
                tmp_fleet = copy.deepcopy(fleet)
                #testing if we can fir ships on givem map dimensions
                check_result = game_adjust_check_if_fleet_fits_on_map(tmp_map,tmp_fleet)
                if check_result == True:
                    height = int(input_values[0])
                    width = int(input_values[1])
                    return height, width
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False










def modify_game_settings_fleet(height, width, symbol, fleet):

    while True:
        clear_terminal()
        print("This is game DEFAULT fleet, if you want to modify ship ( ship size and quantity) or delete ship, pplease select ship by typing ship name or ship index and press enter")
        print("Example   Cruiser is index 3")
        print()
        print("If you want to add new ship, please type N and hit ENTER")
        print("To return to main Setings menu, please type 0 (zero) and press ENTER")
        print()
        print_fleet(fleet)

        try:
            user_input = input().capitalize()

            if not user_input:
                print("Invalid input. Please enter a ship name, index, or 0 to go back.")
                continue
            if len(user_input) == 1:
                if user_input.capitalize() == "N":
                    fleet = modify_game_settings_fleet_ad_new_ship(height, width, symbol, fleet)
                elif user_input == "0":
                    return
                else:
                    if ship_name in fleet:
                        changes = modify_game_settings_fleet_single_ship(height, width, symbol, fleet, ship_name)
                        if changes != False:
                            fleet = changes


            elif user_input.isdigit():

                index = int(user_input) - 1  # Convert to zero-based index
                ship_names = list(fleet.keys())
                if 0 <= index < len(ship_names):
                    ship_name = ship_names[index]
                elif user_input == "0":
                    return fleet
                else:
                    print("Invalid index. Please try again.")
                    continue
            else:
                for ship_name_in_fleet in fleet.keys():
                    if user_input.lower() in ship_name_in_fleet.lower():
                        ship_name = ship_name_in_fleet




                    # Handle empty input
            if not user_input:
                print("Invalid input. Please enter a comma-separated pair of digits, or 0 to go back.")
                continue
        # Handle keyboard interrupt to gracefully exit the function
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False



def modify_game_settings_fleet_ad_new_ship(height, width, symbol, fleet):
    """
    Modifies the game settings by adding a new ship to the fleet.

    Parameters:
        height (int): The height of the game map.
        width (int): The width of the game map.
        symbol (str): The symbol used to represent ships.
        fleet (dict): The current state of the fleet.

    Returns:
        height, width (tuple): The new dimensions of the game map.
    """
    validated_user_input_1 = ["ShipName","Size","QTY"]
    check_result = True
    while True:
        try:
            # Clear the terminal (clear_terminal function not shown here)
            clear_terminal()

            # Check if the user entered 3 values for the ship
            if len(validated_user_input_1) != 3:
                print(
                    f'Please make sure you have entered 3 values, as at the moment I can see only {len(validated_user_input_1)} values.')

            # Show the current fleet
            print("This is your current fleet:")
            print_fleet(fleet)

            # If the previous check failed, inform the user
            if check_result == False:
                print(
                    f'I cannot squeeze in new ship {validated_user_input_1[0]} with width {validated_user_input_2[0]} and size {validated_user_input_2[1]} into the current fleet.')
                print(
                    'Because such a new fleet is not rational for the given map size. Try increasing the map size, and then add this ship again.')

            # Get the user input for the new ship
            user_input = input("Please enter Ship name, size, and quantity of ships you want to add to the fleet: ")
            if user_input == "0":
                return fleet
            validation_result_1, validated_user_input_1, output_text_1 = validate_user_input(user_input, 3)

            if validation_result_1:
                # Validate if the last two parts are integers
                new_input = f"{validated_user_input_1[1]},{validated_user_input_1[2]}"
                validation_result_2, validated_user_input_2, output_text_2 = validate_user_input(new_input, 2,
                                                                                                 "integer")

                if validation_result_2:
                    # Create a temporary copy of the fleet and map
                    tmp_fleet = copy.deepcopy(fleet)
                    tmp_map = create_map(height, width, symbol)

                    # Add the new ship to the temporary fleet
                    tmp_fleet[validated_user_input_1[0]] = {"Size": int(validated_user_input_2[0]),
                                                            "Quantity": int(validated_user_input_2[1]),
                                                            "Coordinates": []}

                    # Check if the new fleet fits on the map
                    check_result = game_adjust_check_if_fleet_fits_on_map(tmp_map, tmp_fleet)

                    if check_result:
                        # Update the actual fleet with the new ship
                        fleet[validated_user_input_1[0]] = {"Size": int(validated_user_input_2[0]),
                                                            "Quantity": int(validated_user_input_2[1]),
                                                            "Coordinates": []}
                        return fleet

        except ValueError:
            print("Values you have entered are not valid. Please enter the correct number of values.")


# You would also need the clear_terminal(), print_fleet(), create_map(), and game_adjust_check_if_fleet_fits_on_map() functions, which are not shown here.


def modify_game_settings_fleet_single_ship(height, width, symbol, fleet, ship_name):
    # now we have ship name we want to adjust, lets try doing so:
    ship_size = fleet[ship_name]["Size"]
    ship_qty = fleet[ship_name]["Quantity"]
    input_validation = True
    check_result = True
    while True:
        try:
            clear_terminal()
            if not input_validation:
                print(" len output text", len(output_text))
                print(f'You have entered incorrect information')
                if len(output_text) == 1:
                    print(output_text)
                else:
                    for i in range(len(validated_user_input)):
                        print(output_text[i])
            if check_result == False:
                print(f' I am sorry but i am strugling to fit given ship \u001b[33m{ship_name}\u001b[0m with size \u001b[33m{validated_user_input[0]}\u001b[0m and quantity \u001b[33m{validated_user_input[1]}\u001b[0m on fleet')
            print(
                f"You have selected Ship \u001b[33m{ship_name}\u001b[0m  and it size is \u001b[33m{ship_size}\u001b[0m cells. There are \u001b[33m{ship_qty}\u001b[0m such ships in the current fleet.")

            print("If you want to delete the ship, type 'D' and press enter.")
            print("To change the ship SIZE and Quantity, enter 2 digits separated by a comma.")
            print("Example: 2,1")
            print("To go back, type 0 (zero).")
            user_input = input().strip().upper()
            # Handle empty input
            if not user_input:
                print("Invalid input. Please type something, not just press ENTER. If you want to go back, type 0 and press ENTER")
            elif user_input == "D":
                del fleet[ship_name]
                return fleet
                # Go back to ship selection
            elif user_input == "0":
                return fleet
            # Modify ship details
            else:
                # now we will validate user input
                validation_result, validated_user_input, output_text = validate_user_input(user_input,2,"integer")
                if validation_result == True:
                    tmp_fleet = copy.deepcopy(fleet)
                    tmp_map = create_map(height, width, symbol)
                    tmp_fleet[ship_name]["Size"] = int(validated_user_input[0])
                    tmp_fleet[ship_name]["Quantity"] = int(validated_user_input[1])

                    check_result = game_adjust_check_if_fleet_fits_on_map(tmp_map, tmp_fleet)
                    if check_result == True:
                        print("check result is true")
                        fleet[ship_name]["Size"] = validated_user_input[0]
                        fleet[ship_name]["Quantity"] = validated_user_input[1]
                        return fleet
                else:
                    input_validation = False
                    continue
        except ValueError:
                print("Values you have entered are not valid. Please enter 2 digits separated by a comma.")


# Functions for checking and validating
#------------------------------------------------------

def game_adjust_check_if_fleet_fits_on_map(map, fleet):
    # Declare global variables accessed within the function
    for i in range(50): # will cycle 50 times, if there is any luck to deploy ships with curent configuration, loop will be interupted and returned True
        tmp_fleet = copy.deepcopy(fleet)
        print("above should be fleet no coordinates")
        result = cpu_deploy_all_ships(map, tmp_fleet)
        if result != False:
            return True
        else:
            print("this is another not true result")
            return False


def validate_user_input(input, parts, type=None):
    """
    Splits user input into the specified number of parts and optionally verifies their type.

    Parameters:
        input: The string input provided by the user.
        parts: The number of parts to split the input into.
        type: The expected type of each part (currently only 'integer' is supported).

    Returns:
        A tuple containing a validity flag, the parts if successful, and an output text list.
    """

    # Split the input by any non-alphanumeric character
    split_input = re.split(r'\W+', input)

    # Remove any empty strings from the list
    split_input = [s for s in split_input if s]

    input_valid = True  # Initialize validity flag
    output_text = []  # Initialize output text list

    # Check if the number of parts matches the expected number
    if len(split_input) != parts:
        output_text.append(f"Input should be split into \u001b[33m{parts}\u001b[0m parts.")
        return False, tuple(split_input), output_text

    # If a type is specified, validate each part
    if type == 'integer':
        for i, part in enumerate(split_input):
            if not part.isdigit():
                output_text.append(f'Your input \u001b[33m{part}\u001b[0m is NOT an Integer.')
                input_valid = False  # Set validity flag to False if any part fails
            else:
                output_text.append(f'Your input \u001b[33m{part}\u001b[0m is an Integer.')
                split_input[i] = int(part)

    return input_valid, tuple(split_input), output_text



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
    global MAP_ROW_INDEXES, MAP_COLUMN_INDEXES
    # Print column headers (0, 1, 2, ..., N)
    print("   ", end="")
    for col_index in range(len(game_map[0])):
        print(f"{MAP_ROW_INDEXES[col_index]}  ", end="")

    # Print a separator line between headers and table
    print("\n   " + "=" * (len(game_map[0]) * 3))

    # Loop through each row
    for row_index, row in enumerate(game_map):
        # Print row header
        print(f"{MAP_COLUMN_INDEXES[row_index]} |", end=" ")

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
            print(f"{MAP_COLUMN_INDEXES[col_index]}".rjust(num_digits_map_height + char_width),
                  end="")  # i do not want gap after last index, as it will be not aligned
        else:
            print(f"{MAP_COLUMN_INDEXES[col_index]}".rjust(num_digits_map_height + char_width), end=" ")
    print(gap_str, print_map_left_offset, end=" ")
    for col_index in range(len(map_right[0])):
        # Right-justify the column index with proper spacing
        print(f"{MAP_COLUMN_INDEXES[col_index]}".rjust(num_digits_map_height + char_width), end=" ")
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
        print(f"{MAP_ROW_INDEXES[row_index]}".rjust(num_digits_map_width + 1), end=row_index_separator)
        for value in row_left:
            width = len(str(value))
            # Right-justify the map value with proper spacing
            print(f"{value}".rjust(num_digits_map_height + char_width - (char_width - width)), end=" ")
        # Insert the gap between the two maps
        print(gap_str, end="")
        # Print row for the right map
        print(f"{MAP_ROW_INDEXES[row_index]}".rjust(num_digits_map_width + 1), end=row_index_separator)
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
        print(f"{MAP_COLUMN_INDEXES[col_index]}".rjust(num_digits_map_height + char_width), end=" ")
    print(gap_str, "Instructions")
    print("    ".rjust(num_digits_map_width + 1),"=" * (number_char_table_total))  # Draw a separator line

    # Loop through each row to print map values and instructions
    for row_index in range(max(len(map_left), len(instructions))):
        # Print row for the map
        if row_index < len(map_left):
            print(f"{MAP_ROW_INDEXES[row_index]}".rjust(num_digits_map_width + 1), end=row_index_separator)
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



def print_aligned_log(log_data, gap=10):
    """
    Print log data in aligned columns with predefined labels and customizable gap.

    Args:
        log_data (list): A list of log entries, where each entry is a list containing
            information about the player, time, row, column, and result.
        gap (int): Number of blank spaces between the log columns. Default is 10.

    Example:
        print_aligned_log([['CPU', 0.0658, 4, 5, 'Damaged']], gap=5)
    """

    # Predefined labels for the columns
    labels = ['Player', 'Time', 'Row', 'Column', 'Result']

    # Calculate the maximum width for each column
    max_widths = [0] * len(labels)
    for i in range(len(labels)):
        max_widths[i] = max(len(labels[i]), max(len(str(entry[i])) for entry in log_data))

    # Create a string of blank spaces for the gap between columns
    gap_str = ' ' * gap

    # Print headers with aligned columns and labels
    header_str = " | ".join(f"{labels[i]:<{max_widths[i]}}" for i in range(len(labels)))
    print(header_str)

    # Print log entries with aligned columns
    for entry in log_data:
        entry_str = " | ".join(f"{str(entry[i]):<{max_widths[i]}}" for i in range(len(entry)))
        print(entry_str)


# User Game Play Functions
#-------------------------
def player_shoot_Input(map_display, map_hidden, enemy_fleet):
    global MAP_ROW_INDEXES, MAP_COLUMN_INDEXES, cpu_shot_log_tmp
    input_validation = True
    while True:
        try:
            if input_validation == False:
                print(f' Please enter JUST 2 values, as you have entered {len(input_values)}')
            print(f'Please enter coordinates to shoot, Row and Column, in this pattern')
            user_input = input()
            #checking if user entered 2 values:
            input_validation, input_values, output_text = validate_user_input(user_input,2)
            if input_validation == True:
                row, column = input_validation
                #now checking if entered indexes are present on row and column
                if row in MAP_ROW_INDEXES:
                    row_index = MAP_ROW_INDEXES.index(row)
                    column_index = MAP_COLUMN_INDEXES.index(column)
                    coordinates_check = player_shoot_coordinates_check(row_index,column_index,map_hidden)
            if coordinates_check == True:
                action_perform_shoot("Player", row_index, column_index, map_display, map_hidden, enemy_fleet, cpu_shot_log_tmp)


        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False

def player_shoot_coordinates_check(row, column, gam_map):
    global DEFAULT_SYMBOL, game_actions_log,
    if gam_map[row,column] == DEFAULT_SYMBOL:
        check_result = True
    for log in game_actions_log:
        if row == log[3] and column == log[4]:
            check_result = False
    if check_result == True:
        print("player move to shoot")
    return check_result

def player_deploy_all_ships(map_display, map_hidden, fleet):
    global DEFAULT_SYMBOL. SHIP_SYMBOLS
    for ship_name, ship_info in fleet.items():
        quantity = ship_info["Quantity"]
        size = ship_info["Size"]
        for i in range(quantity):
            map_display, map_hidden , coordinates_list = player_deploy_single_ship(map_display, map_hidden, ship_name, size)
            fleet[ship_name]["Coordinates"].append(coordinates_list)
    return map_display, fleet




def player_deploy_single_ship(map_display, map_hidden, ship_name, ship_size):
    global MAP_ROW_INDEXES, MAP_COLUMN_INDEXES
    input_validation = True
    row_value_correct = True
    column_value_correct = True
    alignment_valid = True
    map_check_result = True
    while True:
        try:
            if input_validation == False:
                print(output_values_message)
            if row_value_correct == False:
                print(row_output_message)
            if column_value_correct == False:
                print(column_output_message)
            if alignment_valid == False:
                print(alignment_mistake_message)
            if map_check_result == False:
                print(message_ship_does_not_fit)
            user_input = input()
            # by ship size we check for 2 or 3 values, if single ship, just coordinates, if bigger ship: coordinates + alignment
            if ship_size == 1:
                input_validation, input_values, output_values_message = validate_user_input(user_input, 2)
            elif ship_size >= 1:
                input_validation, input_values, output_values_message = validate_user_input(user_input, 3)
                # new we check if last 3rd value is letter and is it Vertical or Horizontal, coordinates we will check below
                alignment_text = input_values[2]
                if alignment_text.lower() == "v":
                    alignment = "Vertical"
                elif alignment_text.lower() == "h":
                    alignment = "Horizontal"
                # Constants for known orientations and threshold
                vertical_string = 'vertical'
                horizontal_string = 'horizontal'
                string_threshold = 2  # You can adjust this value to be more or less strict
                # Normalize the user input to lowercase for easier comparison
                normalized_alignment = alignment_text.lower()
                distance_to_vertical = levenshtein_distance(vertical_string,normalized_alignment)
                distance_to_horizontal = levenshtein_distance(horizontal_string, normalized_alignment)
                if distance_to_vertical <= string_threshold and distance_to_vertical <= distance_to_horizontal:
                    alignment = "Vertical"
                    row_value_correct = True
                elif distance_to_horizontal <= string_threshold and distance_to_horizontal <= distance_to_vertical:
                    alignment = "Horizontal"
                    column_value_correct = True
                else:
                    alignment_valid = False
                    alignment_mistake_message = f' I am sorry but i can not determinate what alignment you hhave shosen by your letters {input_values[2]}'
            # now if ammount of values is correct, we check if row and column are within map boundaries
            if input_validation == True:
                input_first_two_values = input_values[0] + "," + input_values[1]
                input_validation_is_integer, row_column, row_column_output = validate_user_input(input_first_two_values, 2, "integer")
                if input_validation_is_integer == True:
                    if row_column[0] in MAP_ROW_INDEXES:
                        row = MAP_ROW_INDEXES.index(row_column[0])
                        row_value_correct = True
                    else:
                        row_output_message = f' I am sorry to say, but there is no such {row} on current map'
                        row_value_correct = False
                    if row_column[1] in MAP_COLUMN_INDEXES:
                        column = MAP_COLUMN_INDEXES.index(row_column[1])
                        column_value_correct = True
                    else:
                        column_output_message = f' I am sorry to say, but there is no such {column} on current map'
                        column_value_correct = False
            # now checking if all input is valid, and user made no typos, then we will check if those coordinates are valid on map:
            if row_value_correct == True and column_value_correct == True and alignment_valid == True:
                # creating of coordinates list:
                coordinates_list = create_coordinate_list(row, column, alignment, ship_size)
                map_check_result = player_deploy_single_ship_check_map_space(map_hidden, coordinates_list)
                if map_check_result == True:
                    # We will deploy ships on hidden and display maps, then if gaps between ships are enabled, we will remove Miss symbols from display map
                    # But we keep Misss symbols on hidden map, so when player deploys next shipp, we rely on hidden map, but player does not see it.

                    # deploy ship on hidden map
                    map_hidden = map_show_ship_or_symbols(map_hidden, coordinates_list, alignment)
                    # deploy ships on display map
                    map_display = map_show_ship_or_symbols(map_display, coordinates_list, alignment)
                    # hide any symbols from display map and show only ships. This is needed if there is gaps between ships
                    map_display = map_show_only_ships(map_display)
                    return map_display, map_hidden, coordinates_list

                else:
                    if ship_size == 1:
                        mesage_string_for_alignment = ""
                    else:
                        mesage_string_for_alignment = f' with alignment {alignment}'
                    message_ship_does_not_fit = f' I am sorry to say, but your given {ship_name} does not fit on current map with given coordinates Row: {row} and Column{column} {mesage_string_for_alignment}'


        except ValueError:
            print("Values you have entered are not valid. Please enter the correct number of values.")



def levenshtein_distance(source_word, target_word):
    """
    Calculate the Levenshtein distance between two strings: source_word and target_word.

    Levenshtein distance is a measure of the similarity between two strings, calculated as
    the minimum number of single-character edits (insertions, deletions, or substitutions)
    required to change one string into the other.

    Parameters:
    - source_word (str): The original string from which to calculate the distance.
    - target_word (str): The target string to which we want to compare the source string.

    Returns:
    int: The Levenshtein distance between source_word and target_word.
    """
    if len(source_word) < len(target_word):
        return levenshtein_distance(target_word, source_word)

    distances = list(range(len(source_word) + 1))
    for target_index, target_char in enumerate(target_word):
        new_distances = [target_index + 1]
        for source_index, source_char in enumerate(source_word):
            if source_char == target_char:
                new_distances.append(distances[source_index])
            else:
                new_distances.append(1 + min((distances[source_index], distances[source_index + 1], new_distances[-1])))
        distances = new_distances
    return distances[-1]



def player_deploy_single_ship_check_map_space(game_map, coordinates_list)
    global DEFAULT_SYMBOL
    #function to check if that space is empty on map
    checking_ship_fits_on_map = True
    for coordinate in coordinates_list:
        row, column = coordinate
        if game_map[row][column] != DEFAULT_SYMBOL:
            checking_ship_fits_on_map = False
            return checking_ship_fits_on_map



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
    return game_map


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

    # Use the global variable GAPS_BETWEEN_MAPS to get True or False for ships NOT touching
    global DEFAULT_GAPS_BETWEEN_MAPS

    # Before we start displaying ships on map, if spaces between ships is True, we will allocate blank space, then depliy ships
    if DEFAULT_GAPS_BETWEEN_MAPS == True:
        game_map = map_allocate_empty_space_for_ship(game_map, coordinates_list)


    # Handle the case for single-cell ships
    if len(coordinates_list) == 1:
        row, column = coordinates_list[0]
        game_map[row][column] = SHIP_SYMBOLS[alignment][0]
        return game_map

    # Handle the case for multi-cell ships
    else:
        row, column = coordinates_list[0]
        game_map[row][column] = SHIP_SYMBOLS[alignment][0]
        for cell in range(1,len(coordinates_list)):
            row, column = coordinates_list[cell]
            game_map[row][column] = SHIP_SYMBOLS[alignment][1]
        return game_map


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



# Game logic functions:
#----------------------

def search_map_for_pattern(game_map, height, width):
    """
    Find all occurrences of a pattern of DEFAULT_SYMBOL in a map and return their coordinates.

    Args:
        game_map (List[List[str]]): The map as a nested list.
        height (int): Height of the pattern to search for.
        width (int): Width of the pattern to search for.

    Returns:
        List[Tuple[int, int]]: A list of coordinates (row, col) where the pattern is found,
        or an empty list if no pattern is found.
    """

    # Reference the global variable for the default symbol
    global DEFAULT_SYMBOL


    # Retrieve the dimensions of the game map
    map_height, map_width = len(game_map), len(game_map[0])

    # Initialize an empty list to collect coordinates where the pattern is found
    coordinates = []
    # Create the pattern using list comprehension
    pattern = [[DEFAULT_SYMBOL] * width for _ in range(height)]

    # Traverse the map to find matching patterns
    for row in range(map_height - height + 1):
        for col in range(map_width - width + 1):
            if all(
                game_map[row + i][col + j] == pattern[i][j]
                for i in range(height)
                for j in range(width)
            ):
                # If the pattern matches, add the coordinates to the list
                coordinates.append([row, col])
    # Check if any coordinates were found
    if not coordinates:
        return False
    else:
        return coordinates



def find_biggest_ship_in_fleet(fleet):
    """
    Find the biggest ship in the fleet by its size.

    Args:
        fleet (dict): A dictionary representing the fleet of ships.
            Each key is a ship name, and each value is another dictionary
            containing 'Size' and 'Quantity'.

    Returns:
        tuple: A tuple containing the name and size of the biggest ship.
        None: If there are no ships with a quantity greater than 0.
    """

    # Filter out ships with zero quantity
    # Create a new dictionary that only includes ships with a quantity greater than zero
    available_ships = {k: v for k, v in fleet.items() if v["Quantity"] > 0}

    # Check if any ships are available
    # Return None if the available_ships dictionary is empty, indicating no available ships
    if not available_ships:
        return False

    # Find the biggest ship based on the 'Size' value in the dictionary
    # Use the max() function with a custom key function to find the ship with the largest size
    biggest_ship = max(available_ships, key=lambda ship: available_ships[ship]["Size"])

    # Retrieve the size of the biggest ship
    biggest_ship_size = available_ships[biggest_ship]["Size"]

    # Print the name and size of the biggest ship for debugging purposes
    print(f"Biggest ship: {biggest_ship}, Size: {biggest_ship_size}")

    # Return a tuple containing the name and size of the biggest ship
    return biggest_ship, biggest_ship_size


def map_search_reduce_width(height, width, game_map):
    """
    Reduce the width dimension and search for the pattern again.
    """
    width -= 1  # Decrease the width by 1
    coordinates = search_map_for_pattern(game_map, height, width)  # Search for pattern
    print("map_search_reduce_width was searching map for coordinates with height ", height, " and width: ", width, " returned coordinates: ", coordinates)
    if coordinates == False:
        print("we have found no coordinates with height and width: ", height, width)
        width += 1  # Restore the width back to the original
        height -= 1  # Decrease the height by 1
        coordinates = search_map_for_pattern(game_map, height, width)  # Search again
        print("map_search_reduce_width was searching map for coordinates with height ", height, " and width: ", width,
              " returned coordinates: ", coordinates)
        if coordinates == False:
            print("we have found no coordinates with height and width: ", height, width)

            width -= 1  # Now reduce both height and width by 1 and return both height and widdth reduced

    return height, width, coordinates

def map_search_reduce_height(height, width, game_map):
    """
    Reduce the height dimension and search for the pattern again.
    """
    height -= 1  # Decrease the height by 1
    coordinates = search_map_for_pattern(game_map, height, width)  # Search for pattern
    print("map_search_reduce_width was searching map for coordinates with height ", height, " and width: ", width, " returned coordinates: ", coordinates)
    if coordinates == False:
        print("we have found no coordinates with height and width: ", height, width)
        height += 1  # Restore the height back to the original
        width -= 1  # Decrease the width by 1
        coordinates = search_map_for_pattern(game_map, height, width)  # Search again
        print("map_search_reduce_width was searching map for coordinates with height ", height, " and width: ", width,
              " returned coordinates: ", coordinates)
        if coordinates == False:
            print("we have found no coordinates with height and width: ", height, width)
            height -= 1  # Now reduce both height and width by 1 and return both height and width reduced

    return height, width, coordinates


def cpu_choose_shooting_coordinates_biggest_ship(fleet_to_search, game_map):
    """
    Choose shooting coordinates for the CPU based on the biggest ship in the fleet.

    Args:
        fleet_to_search (dict): List of ships in the fleet.
        game_map (list): The map to search for shooting coordinates.

    Returns:
        tuple: The chosen shooting coordinates (coordinateX, coordinateY).
    """

    # Declare global variables used in the function
    global DEFAULT_SYMBOL

    # Initialize variables
    coordinates = ""
    height = ""
    width = ""

    # Find the biggest ship in the fleet
    ship_name, ship_size = find_biggest_ship_in_fleet(fleet_to_search)

    # Check if there are any ships left in the fleet
    if ship_name is None:
        print("game over print")  # No ships left, game over
    else:
        # Calculate the initial pattern dimensions based on the biggest ship
        width = ship_size * 2 - 1
        height = ship_size * 2 - 1

        # Attempt to find the pattern in the map
        coordinates = search_map_for_pattern(game_map, height, width)

        # If no suitable coordinates are found, enter a loop to adjust the pattern
        if coordinates == False:
            while coordinates == False:

                # Try searching again with the current pattern dimensions
                coordinates = search_map_for_pattern(game_map, height, width)

                # Break the loop if coordinates are found
                if coordinates != False:
                    print("cpu_choose_shooting_coordinates_biggest_ship found coordinates", coordinates)
                    break

                # Randomly choose which dimension to reduce
                reduction = random.choice(["height", "width"])

                # Log the current unsuccessful dimensions
                print("we have found no coordinates with height and width:", height, width)

                # Reduce the height and search again
                if reduction == "height":
                    height, width, coordinates = map_search_reduce_height(height, width, game_map)

                # Reduce the width and search again
                if reduction == "width":
                    height, width, coordinates = map_search_reduce_width(height, width, game_map)

                # Various exit conditions for the loop
                if (height < ship_size and width <= 1) or (height <= 1 and width < ship_size) or (height < 1 or width < 1):
                    print("we have found no coordinates with height and width:", height, width)
                    break

        # Randomly choose from the found coordinates
        chosen_coordinates = random.choice(coordinates)

        # Validate the format of the chosen coordinates
        if len(chosen_coordinates) != 2:
            print(f"Error: chosen_coordinates contains {len(chosen_coordinates)} values, expected 2.")
            return None, None  # Handle error case

        # Extract the row and column from the chosen coordinates
        coord_row, coord_column = chosen_coordinates

        # Log the details of the chosen pattern
        print("coordinates before selecting center of pattern:", coord_row, coord_column, "height and width:", height, width)

        # Calculate the middle point of the pattern
        middle_width = (width // 2) + random.choice([1, width % 2]) - 1
        middle_height = (height // 2) + random.choice([1, height % 2]) - 1

        # Calculate the final shooting coordinates based on the middle point
        coordinate_column = coord_column + middle_width
        coordinate_row = coord_row + middle_height

        # Log the final shooting coordinates
        print("coordinate_y, coordinate_x", coordinate_row, coordinate_column)

        # Return the final shooting coordinates
        return coordinate_row, coordinate_column



def find_ship_and_coordinates(fleet, target_coordinates):
    """
    Find the details of the ship and its coordinates in the fleet.

    Args:
        fleet (dict): Dictionary containing information about each ship.
        target_coordinates (list): The [row, column] coordinates to search for.

    Returns:
        tuple: Contains ship_name, ship_size, ship_coordinates_list, coordinates_set_id, and coordinates_id.
               If no match is found, returns noneFound for each field.
    """

    # Loop through the fleet dictionary to check each ship's coordinates
    for ship_name, ship_info in fleet.items():

        # Enumerate gives us the index (coordinates_set_id) and the value (ship_coordinates_list)
        for coordinates_set_id, ship_coordinates_list in enumerate(ship_info['Coordinates']):

            try:
                # Try to find the index of the target_coordinates in the ship_coordinates_list
                coordinates_id = ship_coordinates_list.index(target_coordinates)

                # If found, return all the relevant details
                return ship_name, ship_info['Size'], ship_coordinates_list, coordinates_set_id, coordinates_id

            except ValueError:  # ValueError will be raised if target_coordinates is not in ship_coordinates_list
                # If not found, continue to the next set of coordinates
                continue

    # If we've gone through the whole loop and haven't returned yet, the coordinates weren't found in any ship
    return False, False, False, False, False







def cpu_deploy_all_ships(game_map,fleet):
    """
    Deploy all CPU ships on the map.

    Global Variables:
        fleet (dict): Contains the CPU's fleet information.
        DEFAULT_FLEET (dict): Default settings for the fleet.
        game_map (list): 2D map for CPU.
        DEFAULT_SYMBOL (str): Default symbol for empty cells.
        SHIP_SYMBOLS (dict): Dictionary containing ship symbols.

    Updates:
        - fleet: Updated with the ship coordinates.
        - game_map: Updated with deployed ships.

    Returns:
        None
    """

    # Declare global variables for function access
    global DEFAULT_SYMBOL, SHIP_SYMBOLS

    # Initialize the map with default symbols if not already done


    # Creating empty list for ship coordinates, which will be appended to fleet later
    ship_coordinates = []

    # Iterate through each ship type in the fleet configuration
    for ship_name, ship_info in fleet.items():
        quantity = ship_info["Quantity"]  # Extract the number of ships of this type
        size = ship_info["Size"]  # Extract the size of this type of ship

        # Deploy the required number of each ship type
        for i in range(quantity):
            # Initialize variables to keep track of the ship's location and alignment
            location = ""
            alignment = ""
            # Handle single-cell ships separately
            if size == 1:
                alignment = "Single"
                result = search_map_for_pattern(game_map, 1, 1)
                if result == False:
                    return False

            else:
                # Randomly choose alignment for multi-cell ships
                alignment = random.choice(["Horizontal", "Vertical"])


                # Find a suitable location based on the alignment
                if alignment == "Vertical":
                    result = search_map_for_pattern(game_map, size, 1)
                    if result == False: # if no cordinates possible were found with Vertical, we will try Horizontal
                        alignment = "Horizontal"
                        result = search_map_for_pattern(game_map, 1, size)
                        if result == False:
                            return False

                elif alignment == "Horizontal":
                    result = search_map_for_pattern(game_map,1, size)
                    if result == False: # if no coordinates found with Horizontal, we will try Vertical
                        alignment = "Vertical"
                        result = search_map_for_pattern(game_map, size, 1)

                        if result == False:

                            return False
            location = random.choice(result)

            if len(location) == 2:
                # Deploy the ship at the chosen location
                coordinates_list = create_coordinate_list(location[0],location[1], alignment, size)
                map_show_ship_or_symbols(game_map, coordinates_list, alignment)
                # append ship coordinates to fleet
                fleet[ship_name]["Coordinates"].append(coordinates_list)
            if len(location) < 2:
                return False
    game_map = map_show_only_ships(game_map)
    return game_map, fleet


def handle_miss(player, row, column, map_hidden, map_display):
    """
    Handle the scenario where the shot misses any ship.

    Args:
        player (str): The player making the shot ("CPU" or "Human").
        column (int): The column-coordinate of the shot.
        row (int): The row-coordinate of the shot.
        map_hidden (list): The hidden map that tracks shots.
        map_display (list): The displayed map that shows ships.

    Global Variables:
        SHIP_SYMBOLS (dict): Symbols used for different states of the ship.
        start_time (float): The game start time for logging.
        game_actions_log (list): Log of game actions.

    Returns:
        None
    """

    # Declare global variables for ship symbols, start time, and the game actions log
    global SHIP_SYMBOLS, start_time, game_actions_log

    # Calculate the time elapsed since the game started for logging purposes
    timer = time.time() - start_time

    # Create an action outcome message indicating a miss
    action_outcome = 'it was a MISS'

    # Log the miss action into the game actions log
    game_actions_log.append([player, timer, row, column, action_outcome])

    # Update the hidden map at the given row and column to mark the miss
    # Use the symbol designated for "Miss" in the SHIP_SYMBOLS dictionary
    map_hidden[row][column] = SHIP_SYMBOLS["Miss"][0]

    # Update the display map at the given row and column to mark the miss
    # Use the symbol designated for "Miss" in the SHIP_SYMBOLS dictionary
    map_display[row][column] = SHIP_SYMBOLS["Miss"][0]



def action_perform_shoot(player, row, column, map_hidden, map_display, fleet, cpu_shot_log_tmp):
    """
    Perform a shooting action on the game board.
    """
    global game_actions_log, start_time, SHIP_SYMBOLS  # Declare global variables

    # Find the ship details at the given coordinates
    ship_name, ship_size, coordinates_list, coordinates_set_id, coordinates_id = find_ship_and_coordinates(fleet, [row, column])

    try:
        if ship_name != False:  # If a ship is found at the coordinates
            print(f'{player} performed shot on coordinates {row} and {column}, {ship_name} was damaged')
            print("damaged ship cooordinates are: ", coordinates_list)

            # Logic for handling ship hit
            handle_ship_hit(player, row, column, map_hidden, map_display, fleet,
                            ship_name, ship_size, coordinates_list, coordinates_set_id, coordinates_id, cpu_shot_log_tmp)
            return "Hit"

        else:  # If no ship was found at the coordinates
            print(f'{player} performed shot on coordinates {row} and {column}, it was a MISS')

            # Logic for handling missed shot
            handle_miss(player, row, column, map_hidden, map_display)
            return "Miss"

    except Exception as e:  # Handle exceptions
        print(f"An error occurred: {e}")
        return None

def handle_ship_hit(player, row, column, map_hidden, map_display, fleet,
                            ship_name, ship_size, coordinates_list, coordinates_set_id, coordinates_list_id, cpu_shot_log_tmp):
    """
    Handle the logic when a ship is hit.

    Args:
        player (str): The player making the shot ("CPU" or "Human").
        column (int): The column-coordinate of the shot.
        row (int): The row-coordinate of the shot.
        map_hidden (list): The hidden map that tracks shots.
        map_display (list): The displayed map that shows ships.
        fleet (dict): Information about the fleet of ships.
        ship_name (str): Name of the ship that was hit.
        ship_size (int): Size of the ship that was hit.
        coordinates_list (list): List of coordinates of the ship.
        coordinates_id (int): Index of the coordinates in the list.

    Global Variables:
        game_actions_log (list): Log of game actions.
        start_time (float): The game start time for logging.
        SHIP_SYMBOLS (dict): Symbols used for different states of the ship.
        cpu_shot_log_tmp (list): Temporary log for CPU actions.

    Returns:
        None
    """

    # Declare global variables for logging and timing
    global game_actions_log, start_time, SHIP_SYMBOLS
    timer = time.time() - start_time

    # Update the hidden map to indicate a hit
    map_hidden[row][column] = SHIP_SYMBOLS["Hit"][0]
    # Update the display map to indicate a hit
    map_display[row][column] = SHIP_SYMBOLS["Hit"][0]
    game_actions_log.append([player, timer, row, column, "Ship was Damaged"])

    # If the player is the CPU, log its actions
    if player == "CPU":
        # Log the coordinates where the hit occurred in a temporary list
        cpu_shot_log_tmp.append([row, column])

    # Determine the alignment of the ship based on its coordinates
    alignment, coordinates_index = find_first_ship_alignment(coordinates_list)

    # Special case: If the ship is of size 1 and has been hit, mark it as sunk
    if ship_size == 1 and (map_hidden[row][column] == SHIP_SYMBOLS["Hit"][0]):
        map_hidden[row][column] = map_display[row][column]
        ship_sunk = True

    # For ships larger than size 1, iterate through their coordinates to check if all are hit
    if ship_size > 1:
        for coord in coordinates_list:
            row, column = coord  # Extract the row and column from each coordinate
            if map_hidden[row][column] == SHIP_SYMBOLS["Hit"][0]:
                ship_sunk = True  # Mark as sunk if all parts are hit
            else:
                ship_sunk = False  # If any part is not hit, break the loop
                break

    # If the ship is confirmed as sunk, update various states and logs
    if ship_sunk == True:
        alignment += "Sunk"
        print(player, " has sunk ", ship_name, " on coordinates :", row, column)
        handle_ship_sunk(player, fleet, ship_name, ship_size, alignment, coordinates_list, coordinates_set_id, coordinates_list_id, map_display, map_hidden, cpu_shot_log_tmp)


def handle_ship_sunk(player, fleet, ship_name, ship_size, alignment, coordinates_list, coordinates_set_id, coordinates_list_id, map_display,
                     map_hidden, cpu_shot_log_tmp):
    """
    Handle actions and updates for when a ship is sunk.

    Args:
        player (str): The player who sunk the ship ("CPU" or "Human").
        fleet (dict): The current fleet information.
        ship_name (str): The name of the ship that was sunk.
        ship_size (int): The size of the ship.
        coordinates_list (list): The list of coordinates of the ship.
        coordinates_list_id (int): The ID of the ship's coordinates in the fleet.
        map_display (list): The displayed map that shows ships.
        map_hidden (list): The hidden map that tracks shots.
        alignment (str): The alignment of the ship ("Horizontal" or "Vertical").

    Global Variables:
        start_time (float): Game start time.
        cpu_shot_log_tmp (list): Temporary log of CPU actions.
        SHIP_SYMBOLS (dict): Symbols for different ship states.
        game_actions_log (list): Log of game actions.
        game_result (str): The result of the game ("Game Over" or None).
    """

    # Declare global variables
    global start_time, SHIP_SYMBOLS, game_actions_log, game_result


    print(" before updating map, i just want to see map_display, ship_size, coordinates_list[0], alignment, ship_name, fleet", ship_size, coordinates_list[0], alignment, ship_name, coordinates_list_id, coordinates_list)
    print(len(coordinates_list))
    print(alignment)
    map_show_ship_or_symbols(map_display, coordinates_list, alignment)
    map_show_ship_or_symbols(map_hidden, coordinates_list, alignment)
    print_two_maps(map_hidden, map_display, " hidden", "ships", gap = 5)

    # Log the ship-sinking action
    timer = time.time() - start_time
    action_outcome = f'{ship_name} was sunk'
    game_actions_log.append([player, timer, coordinates_list[0][0], coordinates_list[0][1], action_outcome])

    # Update the CPU's temporary shot log if the player is the CPU
    if player == "CPU":
        cpu_shot_log_tmp = update_cpu_shot_log(coordinates_list, cpu_shot_log_tmp)
        print("after updating cpu shoot log", cpu_shot_log_tmp)
    print("now should follow coordinates removal")
    print(" jautiena remove coordinates from fleet ship name", ship_name, "coordinates set id: ", coordinates_set_id)
    remove_coordinates_from_fleet(fleet, ship_name, coordinates_set_id)

    # Check if all ships are sunk (game over)
    if not fleet:
        timer = time.time() - start_time
        action_outcome = 'Game Over'
        game_actions_log.append([player, timer, coordinates_list[0][0], coordinates_list[0][1], action_outcome])
        game_result = "Game Over"


def remove_coordinates_from_fleet(fleet, ship_name, coordinates_list_set_id):
    """
    Removes an entire set of coordinates from a ship and updates its quantity.
    Also removes any empty coordinate sets in the list.

    Parameters:
    - fleet (dict): The fleet information
    - ship_name (str): The name of the ship to update
    - coordinates_list_set_id (int): The index of the set of coordinates to remove
    """
    # Initial logging to display the current state of the fleet coordinates_list_set_id)
    print_fleet(fleet)

    try:
        # Additional logging for debugging
        print()
        print_fleet(fleet)
        print("now we will be removing fleet[ship_name][Coordinates][coordinates_list_set_id]", ship_name, coordinates_list_set_id)

        # Remove the entire set of coordinates from the ship
        del fleet[ship_name]["Coordinates"][coordinates_list_set_id]

        # Remove any empty coordinate sets from the ship's list of coordinates
        fleet[ship_name]["Coordinates"] = [coords for coords in fleet[ship_name]["Coordinates"] if coords]

        # Reduce the quantity of this type of ship by 1
        fleet[ship_name]["Quantity"] -= 1

        # If the quantity of this type of ship reaches zero, remove it from the fleet
        if fleet[ship_name]["Quantity"] <= 0:
            del fleet[ship_name]

        # Final logging to display the updated state of the fleet
        print_fleet(fleet)

    except KeyError:
        # Handle cases where the specified ship name does not exist in the fleet
        print(f"Failed to remove coordinates for {ship_name}.")


def update_cpu_shot_log(coordinates_list, cpu_shot_log_tmp):
    """
    Update the CPU shot log by removing coordinates that are present in
    the provided coordinates_list, implying that a ship has been sunk.

    Parameters:
    - coordinates_list (list): A list of coordinates that are to be removed.

    Returns:
    - list: Updated CPU shot log.
    """

    # Declare global variable to access and modify CPU shot log

    # Exception handling to gracefully manage any runtime errors
    try:
        # Loop through each coordinate pair in coordinates_list
        for coord in coordinates_list:
            # Remove the coordinate pair from cpu_shot_log_tmp if it exists
            # If the coordinate pair doesn't exist, a ValueError will be raised
            cpu_shot_log_tmp.remove(coord)
    except ValueError as e:
        # Handle the case where a coordinate pair is not found in the log
        print(f"Coordinate not found in log: {e}")

    # Return the updated CPU shot log
    return cpu_shot_log_tmp



def find_first_ship_alignment(coordinates_list):
    """
    Attempts to identify the first alignment of a ship based on its coordinates,
    by comparing each coordinate with every other coordinate. Returns the index
    of the first coordinate in that alignment.

    Parameters:
    - log (List[List[int]]): A list of [row, column] coordinates representing the ship's location.

    Returns:
    - tuple: A tuple containing:
        1. A string indicating the first observed alignment ('None', 'Single', 'Horizontal', 'Vertical').
        2. An integer representing the index of the first coordinate in that alignment, or None if not applicable.
    """

    # Handle the case where the log is empty
    # Return 'None' for both the alignment and index
    if len(coordinates_list) == 0:
        return ('None', None)

    # Handle the case where there is only one coordinate in the log
    # In this case, the ship is considered 'Single'
    elif len(coordinates_list) == 1:
        print("based on spu log find_first_ship_alignment as single")
        return ('Single', 0)

    # Loop through each coordinate in the log for comparison
    for i, (row1, column1) in enumerate(coordinates_list):
        # Nested loop to compare the current coordinate with subsequent coordinates
        for j, (row2, column2) in enumerate(coordinates_list[i + 1:], start=i + 1):

            # If the rows are the same across two coordinates, it's horizontally aligned
            if row1 == row2:
                print(" based on cpu log find_first_ship_alignment as Vertical")
                return ('Horizontal', i)
            # If the columns are the same across two coordinates, it's vertically aligned
            elif column1 == column2:
                print("based on cpu log find_first_ship_alignment as horizontal")
                return ('Vertical', i)

    # If no alignment is found, but we know there is coordinates stored in action log, we will return Single and 0
    # This will trigger next function to start looking for potential shots around first coordinates in log
    # return 'None' for both the alignment and index
    return ('None', None)


def select_best_shot_based_on_alignment(map_to_search, cpu_shot_log_tmp):
    """
    Chooses the best coordinates to shoot at based on ship alignment detection.

    Args:
        map_to_search (list of lists): The map to search for ship coordinates.

    Global Variables:
        cpu_shot_log_tmp (list of lists): Temporary log of CPU shots.
        DEFAULT_SYMBOL (str): The default symbol representing untargeted cells in the map.

    Returns:
        tuple: The chosen column and row coordinates to target next based on the identified ship alignment.
               Returns (None, None) if no suitable coordinates are found.
    """
    # Access global variables
    global DEFAULT_SYMBOL

    # Get the alignment and last index from the CPU shot log
    alignment_info = find_first_ship_alignment(cpu_shot_log_tmp)
    print("chosing best shot bbased on log ", cpu_shot_log_tmp, "and alignment is ", alignment_info)

    # Return None if no identifiable ship alignment is found
    if alignment_info is None or alignment_info[0] == 'None':
        return None, None

    # Unpack alignment and last index
    alignment, last_index = alignment_info

    # Get the last shot coordinates
    last_row, last_column = cpu_shot_log_tmp[last_index]

    # Define the boundaries of the map
    max_row = len(map_to_search) - 1
    max_column = len(map_to_search[0]) - 1

    # Initialize a list to store potential shot coordinates
    potential_shots = []
    shifts = []

    # Define possible shifts based on the ship alignment
    if alignment == "Vertical":
        shifts = [[1, 0], [-1, 0]]
    elif alignment == "Horizontal":
        shifts = [[0, 1], [0, -1]]
    elif alignment == "Single":
        shifts = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    # Loop through the shifts to find the potential shots
    for coord in cpu_shot_log_tmp:
        row, column = coord
        for drow, dcolumn in shifts:
            new_row, new_column = row + drow, column + dcolumn

            # Check if the cell is within map boundaries and is untargeted
            if 0 <= new_row <= max_row and 0 <= new_column <= max_column:
                # Then check if the cell hasn't been shot at before
                if map_to_search[new_row][new_column] == DEFAULT_SYMBOL:
                    potential_shots.append([new_row, new_column])
                    print("new potential shots: ", potential_shots)

        if len(potential_shots) > 0:
            break

    if len(potential_shots) == 0:
        print("found noo coordinates on select_best_shot_based_on_alignment")
        shifts = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for coord in cpu_shot_log_tmp:
            row, column = coord
            for drow, dcolumn in shifts:
                new_row, new_column = row + drow, column + dcolumn
                # Check if the new coordinates are within map boundaries and haven't been shot at before
                if 0 <= new_row <= max_row and 0 <= new_column <= max_column:
                    # Then check if the cell hasn't been shot at before
                    if map_to_search[new_row][new_column] == DEFAULT_SYMBOL:
                        potential_shots.append([new_row, new_column])
                        print("new potentail shots: ", potential_shots)
                if len(potential_shots) > 0:
                    break
            if len(potential_shots) > 0:
                break
    # Randomly choose one of the potential shots if any are available
    if len(potential_shots) > 0:
        selected_row, selected_column = random.choice(potential_shots)
        print("found coordinates on select_best_shot_based_on_alignment", selected_row, selected_column)
        return selected_row, selected_column

    # If no potential shots were found, return None, None
    return None, None








def cpu_move(fleet_target, map_target_hidden, map_target_display, cpu_shot_log_tmp):
    """
    Executes the CPU's move during the game.
    Args:
        - fleet_target: Dictionary holding information about the CPU's fleet.
        - map_target_hidden: Hidden map for the CPU. here we perform search and shoot
        - map_target_display: Display map for the CPU. if shoot is success, then display hit or miss
        - cpu_shot_log_tmp: Temporary log for the CPU's shots.


    Global Variables:
    - game_result: Holds the current state of the game ("Game Over" or None).

    - game_actions_log: Log for game actions.
    - start_time: Time when the game started.
    - SHIP_SYMBOLS: Dictionary holding symbols for different ship states.

    Returns:
    - None: Updates global variables as side effects.
    """

    # Declare global variables accessed within the function
    global game_result
    global game_actions_log, start_time, SHIP_SYMBOLS


    # Identify the player as CPU for logging and action purposes
    player = "CPU"

    # Check if there are any damaged but unsunk ships in cpu_shot_log_tmp
    if len(cpu_shot_log_tmp) == 0:
        print("No damaged ships in CPU's temporary log.")
        # If no damaged ships are found, choose coordinates based on the largest ship in the fleet
        row, column = cpu_choose_shooting_coordinates_biggest_ship(fleet_target, map_target_hidden)
        # Perform the shooting action and update the game state
        action_perform_shoot(player, row, column, map_target_hidden, map_target_display, fleet_target, cpu_shot_log_tmp)

        # Check for game over condition
    else:
        print(f"Damaged ships found in CPU's temporary log: {cpu_shot_log_tmp}")
        # If damaged ships are found, focus on sinking them by selecting the best shot based on ship alignment
        row, column = select_best_shot_based_on_alignment(map_target_hidden, cpu_shot_log_tmp)
        # Perform the shooting action and update the game state
        action_perform_shoot(player, row, column, map_target_hidden, map_target_display, fleet_target, cpu_shot_log_tmp)



def cpu_vs_cpu():
    """
    Main game loop for the CPU's Battleship game.

    Global Variables:
    - start_time: Time when the game started.
    - map_cpu_hidden: Hidden map for the CPU.
    - map_cpu_display: Display map for the CPU.
    - cpu_shot_log_tmp: Temporary log for the CPU's shots.
    - game_actions_log: Log for game actions.
    - fleet_cpu: Dictionary holding information about the CPU's fleet.

    Returns:
    - None: Updates global variables and prints game state as side effects.
    """

    # Declare global variables accessed within the function
    global start_time, map_cpu_hidden, map_cpu_display, cpu_shot_log_tmp, game_actions_log, fleet_cpu, DEFAULT_FLEET

    # Initialize the game start time
    start_time = time.time()

    # Clear terminal for a clean game start (assuming the function 'clear_terminal' exists)
    clear_terminal()
    new_map_display = create_map(10,10, DEFAULT_SYMBOL)
    map_cpu_hidden = create_map(10,10, DEFAULT_SYMBOL)
    new_fleet = copy.deepcopy(DEFAULT_FLEET)
    cpu_shot_log_tmp = []


    # Deploy all of CPU's ships (assuming the function 'cpu_deploy_all_ships' exists)
    map_cpu_display , fleet_cpu = cpu_deploy_all_ships(new_map_display, new_fleet)

    # Print both maps to visualize initial game state
    print_two_maps(map_cpu_hidden, map_cpu_display, "hidden_cpu_map", "cpu_map")

    # Print the initial state of CPU's fleet
    print_fleet(fleet_cpu)

    # Main game loop, iterate for 100 turns
    for i in range(100):
        print(f"\nGame turn {i} ******")

        # CPU makes its move
        cpu_move(fleet_cpu, map_cpu_hidden, map_cpu_display, cpu_shot_log_tmp)

        # Print the CPU's shot log and both maps to visualize game state
        print(f"CPU shooting actions log: {cpu_shot_log_tmp}")
        print_two_maps(map_cpu_hidden, map_cpu_display, "hidden_cpu_map", "cpu_map")

        # Print the current state of CPU's fleet
        print_fleet_with_coodinates(fleet_cpu)

        # Check for game over condition
        if len(fleet_cpu) == 0:
            print(f"Game over at move {i}")
            print("GAME OVER")
            break  # Exit the game loop
    return fleet_cpu


#cpu_vs_cpu()


def loop_cpu():
    for i in range(50):
        fleet = cpu_vs_cpu()
        print("this is cpu vs cpu loop number ", i)
        if len(fleet) > 0:
            break

#loop_cpu()


# Run the game
def battleship_game_singe(height, width, symbol, fleet, start_time, game_action_log):
    """
    Main game loop for the CPU's Battleship game.

    Global Variables:
    - start_time: Time when the game started.
    - map_cpu_hidden: Hidden map for the CPU.
    - map_cpu_display: Display map for the CPU.
    - cpu_shot_log_tmp: Temporary log for the CPU's shots.
    - game_actions_log: Log for game actions.
    - fleet_cpu: Dictionary holding information about the CPU's fleet.

    Returns:
    - None: Updates global variables and prints game state as side effects.
    """

    # Declare global variables accessed within the function
    #global start_time, map_cpu_hidden, map_cpu_display, cpu_shot_log_tmp, game_actions_log, fleet_cpu
    map_cpu_display, map_cpu_hidden, fleet_cpu = create_initial_game_variables(height, width, symbol, fleet)



    # Initialize the game start time
    start_time = time.time()

    # Clear terminal for a clean game start (assuming the function 'clear_terminal' exists)
    clear_terminal()

    # Print ASCII art
    #print_acid_effect()

    # Initializing game instructions
    adjust_game = game_instructions(height, width, symbol, fleet)






def tomosius_check():


    # Declare global variables accessed within the function
    global start_time, map_cpu_hidden, map_cpu_display, cpu_shot_log_tmp, game_actions_log, fleet_cpu, DEFAULT_FLEET

    # Initialize the game start time
    start_time = time.time()

    # Clear terminal for a clean game start (assuming the function 'clear_terminal' exists)
    clear_terminal()
    new_map_display = create_map(10, 10, DEFAULT_SYMBOL)
    map_cpu_hidden = create_map(10, 10, DEFAULT_SYMBOL)
    new_fleet = copy.deepcopy(DEFAULT_FLEET)

    # Deploy all of CPU's ships (assuming the function 'cpu_deploy_all_ships' exists)
    result = cpu_deploy_all_ships(new_map_display, new_fleet)
    if result == False:
        print(" tomosius sunday can not deploy ships")
    else:
        map_cpu_display, fleet_cpu = result
        # Print both maps to visualize initial game state
        print_two_maps(map_cpu_hidden, map_cpu_display, "hidden_cpu_map", "cpu_map")

        # Print the initial state of CPU's fleet
        print_fleet_with_coodinates(fleet_cpu)
        print_map(map_cpu_display)





#tomosius_check()
#print_aligned_log(game_actions_log, 5)
#cpu_vs_cpu()
#print_aligned_log(game_actions_log, 10)
#loop_cpu()

battleship_game(DEFAULT_MAP_HEIGHT, DEFAULT_MAP_WIDTH, DEFAULT_SYMBOL, DEFAULT_FLEET, start_time, game_actions_log)




