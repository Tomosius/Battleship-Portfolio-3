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
MAP_ROW_INDEXES = [0,1,2,3,4,5,6,7,8,9]
MAP_COLUMN_INDEXES =[0,1,2,3,4,5,6,7,8,9]

# Initialize game-related variables
game_result = True  # Variable to store the game outcome if it is True - game is ongoing
cpu_shot_log_tmp = []  # Temporarily store CPU actions if a ship is hit
start_time = time.time() # tamer will start with game

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
    "Cruiser": {"Size": 3, "Quantity": 1, "Coordinates": []},
    "Submarine": {"Size": 3, "Quantity":1, "Coordinates": []},
    "Destroyer": {"Size": 2, "Quantity": 2, "Coordinates": []},
    "Tugboat": {"Size": 1, "Quantity": 3, "Coordinates": []}
}


# Game instructions and settings, presented as lists
INSTRUCTIONS = ["1. Ships can be aligned Horizontally or Vertically",
                "2. Ships can NOT be touching each other, but this can be changed in game settings",
                "3. Default game map is size 10 by 10",
                "4. Player has to enter coordinates as follows: Y,X - ROW, COLUMN. Numbers separated by COMMA",
                "5. \u001b[34mHORIZONTAL\u001b[0m ships will be BLUE color",
                "6. \u001b[32mVERTICAL\u001b[0m ships will be GREEN color",
                "7. \u001b[31mDAMAGED\u001b[0m ships will be green color",
                "If you want to adjust game settings type \u001b[33mY\u001b[0m and press ENTER",
                "If you want to start game just press \u001b[33mENTER\u001b[0m"]

GAME_ADJUST_MAIN = ["If you to adjust your FLEET, type \u001b[33mF\u001b[0m and press enter",
                    "If you want to change MAP size, type \u001b[33mM\u001b[0m and press enter",
                    "If you want to change coordinate system Indexes from "
                    "numbers to letters, type \u001b[33mI\u001b[0m and press enter",
                    "If you want to disable GAPS between ships, type \u001b["
                    "33mG\u001b[0m and press enter",
                    "",
                    "To return to main menu, press \u001b[33m0\u001b[0m and press enter"]

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

"""Game Intro functions
---------------------"""
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


"""Initial game start functions
-----------------------------"""


def create_initial_game_variables(height, width, symbol, fleet):
    """
    Creates and returns the initial game variables for the Battleship game.

    Parameters:
    - height (int): The height of the game map.
    - width (int): The width of the game map.
    - symbol (str): The default symbol to fill the game map with.
    - fleet (dict): The initial fleet configuration.

    Returns:
    - tuple: A tuple containing:
        1. new_map (list of lists): The initialized game map.
        2. new_map_hidden (list of lists): A hidden copy of the game map.
        3. new_fleet (dict): A deep copy of the initial fleet configuration.
    """

    # Create the game map with the given dimensions and default symbol.
    # The function 'create_map' is assumed to be defined elsewhere in the code.
    map_display = create_map(width, height, symbol)

    # Create a deep copy of the game map to serve as the hidden map.
    # Deep copy ensures that changes to one map won't affect the other.
    map_hidden = copy.deepcopy(map_display)

    # Create a deep copy of the initial fleet configuration.
    # This allows us to manipulate the fleet during the game without affecting the original configuration.
    new_fleet = copy.deepcopy(fleet)

    # Return the newly created game variables as a tuple.
    return map_hidden, map_display, new_fleet


def game_instructions():
    """
    Displays the game instructions and allows the player to adjust game settings.

    Global Variables:
    - SHIP_SYMBOLS: Dictionary holding symbols for different ship states.
    - INSTRUCTIONS: String containing game instructions.
    - DEFAULT_MAP_HEIGHT, DEFAULT_MAP_WIDTH: Default dimensions of the game map.
    - DEFAULT_FLEET: Default fleet configuration.
    - MAP_ROW_INDEXES, MAP_COLUMN_INDEXES: Default row and column labels.
    - DEFAULT_GAPS_BETWEEN_MAPS: Default gap between the two displayed maps.

    Returns:
    - tuple: A tuple containing updated game settings or False if interrupted.
    """

    # Declare global variables accessed within the function
    global SHIP_SYMBOLS, INSTRUCTIONS, DEFAULT_MAP_HEIGHT, DEFAULT_MAP_WIDTH, DEFAULT_FLEET, MAP_ROW_INDEXES, MAP_COLUMN_INDEXES, DEFAULT_GAPS_BETWEEN_MAPS

    # Initialize default game settings
    height = DEFAULT_MAP_HEIGHT
    width = DEFAULT_MAP_WIDTH
    gaps_on_map = DEFAULT_GAPS_BETWEEN_MAPS
    fleet = copy.deepcopy(DEFAULT_FLEET)

    # Create a temporary map and fleet for demonstration purposes
    tmp_map = create_map(height, width, DEFAULT_SYMBOL)
    tmp_fleet = copy.deepcopy(DEFAULT_FLEET)

    # Deploy ships on the temporary map
    tmp_map, tmp_fleet = cpu_deploy_all_ships(tmp_map, tmp_fleet, gaps_on_map)

    # Main loop to display instructions and handle user input
    while True:
        # Display the example map alongside the game instructions
        print_map_and_list(tmp_map, INSTRUCTIONS, "MAP EXAMPLE", 10)

        try:
            # Prompt the user to decide whether to adjust the game settings
            changes = input(\n).capitalize()

            # If the user opts to adjust settings
            if changes in ["Y", "YES"]:
                # Call the function to modify game settings
                height, width, fleet, gaps_on_map = modify_game_settings(height, width, fleet, gaps_on_map)
                continue  # Continue the loop to display updated settings
            if changes == "0":
                # Return the final game settings
                return height, width, fleet, gaps_on_map

            else:
                # Return the final game settings
                return height, width, fleet, gaps_on_map

        # Handle keyboard interrupt to exit the function gracefully
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False  # Return False to indicate interruption

"""Game Adjust Settings functions
------------------------------"""

def modify_game_settings(height, width, fleet, gaps_on_map):
    """
    Adjusts game settings based on user input. The settings include map dimensions,
    fleet configuration, row and column labels, and gaps between maps.

    Args:
    - height (int): The height of the map.
    - width (int): The width of the map.
    - fleet (dict): The current fleet configuration.
    - label_row (list): The row labels.
    - label_column (list): The column labels.
    - gaps_on_map (bool): Current setting for gaps between ships on the map.

    Returns:
    - tuple: Updated game settings if the adjustment was successful.
    - bool: False if the game adjustment was interrupted.
    """

    # Declare global variables accessed within the function
    global SHIP_SYMBOLS, GAME_ADJUST_MAIN

    # Main loop to continuously offer adjustment options to the user
    while True:
        # Create a temporary map and fleet for demonstration purposes
        tmp_fleet = copy.deepcopy(fleet)  # Reset the fleet for new ship alignment
        tmp_map = create_map(height, width, DEFAULT_SYMBOL)

        # Deploy ships on the temporary map
        tmp_map, tmp_fleet = cpu_deploy_all_ships(tmp_map, tmp_fleet, gaps_on_map)

        # Clear the terminal and display the current state
        clear_terminal()
        print_map_and_list(tmp_map, GAME_ADJUST_MAIN, "MAP EXAMPLE", 10)

        try:
            # Get user input for which setting to adjust
            user_input = input(\n).capitalize()

            # Validate user input
            if not user_input:
                print("Invalid input. Please type \u001b[33mF\u001b[0m, "
                      "\u001b[33mM\u001b[0m, \u001b[33mI\u001b[0m, \u001b["
                      "33mG\u001b[0m or just \u001b[33m0\u001b[0m  to return "
                      "back to Instructions.")
                continue

            # Modify fleet settings
            if user_input == "F":
                fleet = modify_game_settings_fleet(height, width, fleet, gaps_on_map)

            # Modify map dimensions
            elif user_input == "M":
                height, width = modify_game_settings_map(height, width, fleet, gaps_on_map)

            # Modify row and column labels
            elif user_input == "I":
                modify_game_settings_labels(height, width, fleet, gaps_on_map)

            # Modify gap settings
            elif user_input == "G":
                gaps_on_map = modify_game_settings_gaps(height, width, fleet, gaps_on_map)

            # Exit the loop and return the final settings
            elif user_input == "0":
                return height, width, fleet, gaps_on_map

            # Invalid input
            else:
                print("Invalid option. Please try again.")

        # Handle keyboard interrupt to gracefully exit the function
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False  # Return False to indicate interruption


# Further updating the function to handle cases where the user input is just one letter
def modify_game_settings_gaps(height, width, fleet, gaps_on_map):
    """
    Allows the user to enable or disable the requirement for gaps between ships on the game map.

    Args:
    - height (int): The height of the game map.
    - width (int): The width of the game map.
    - fleet (dict): The current state of the fleet.
    - gaps_on_map (bool): Current setting for gaps between ships on the map (True if enabled, False otherwise).

    Returns:
    - bool: Updated setting for gaps between ships on the map.
    """

    # Infinite loop to keep asking the user for input until a valid response is received
    while True:
        try:
            # Omitted the map and fleet manipulations for demonstration

            # Get the user's input
            user_input = input(
                "Would you like to change the gap settings? (YES/NO/True/False) ")

            # Normalize the user input for easier comparison
            normalized_input = user_input.lower()

            # Initialize possible answers
            possible_answers_enable = ["yes", "true", "y", "t", "enable", "on"]
            possible_answers_disable = ["no", "false", "n", "f", "disable",
                                        "off"]

            # Initialize result variables
            answer_valid = False
            closest_match = ""

            # Check for a non-empty response
            if len(normalized_input) > 0:

                # If the user input is just one letter, directly match it with the possible answers
                if len(normalized_input) == 1:
                    if normalized_input in [ans[0] for ans in
                                            possible_answers_enable]:
                        return True  # Enable gaps between ships
                    elif normalized_input in [ans[0] for ans in
                                              possible_answers_disable]:
                        return False  # Disable gaps between ships
                    else:
                        print(
                            "Invalid input. Please type YES, NO, True, or False.")
                        continue  # Skip to the next iteration

                # Step 1: Check first letter
                if normalized_input[0] in [ans[0] for ans in
                                           possible_answers_enable]:
                    possible_answers = possible_answers_enable
                elif normalized_input[0] in [ans[0] for ans in
                                             possible_answers_disable]:
                    possible_answers = possible_answers_disable
                else:
                    print("Invalid input. Please type YES, NO, True, or False.")
                    continue  # Skip to the next iteration

                # Step 2: Check for common matching letters
                max_common_letters = 0
                for ans in possible_answers:
                    common_letters = len(set(normalized_input) & set(ans))
                    if common_letters > max_common_letters:
                        max_common_letters = common_letters
                        closest_match = ans

                # Decide the setting based on the closest match
                if closest_match in possible_answers_enable:
                    gaps_on_map = True  # Enable gaps between ships
                    answer_valid = True
                elif closest_match in possible_answers_disable:
                    gaps_on_map = False  # Disable gaps between ships
                    answer_valid = True

                if answer_valid:
                    return gaps_on_map
                else:
                    print("Invalid input. Please type YES, NO, True, or False.")
            else:
                print("No input detected. Please type YES, NO, True, or False.")

        # Handle any keyboard interrupts to exit the loop gracefully
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return gaps_on_map  # Return the current setting in case of an interruption



def modify_game_settings_labels(height, width, fleet, gaps_on_map):
    """
    Allows the user to customize the row and column labels on the game map.

    Args:
    - height (int): The height of the game map.
    - width (int): The width of the game map.
    - fleet (dict): The current state of the fleet.
    - label_row (list): Current row labels for the game map.
    - label_column (list): Current column labels for the game map.
    - gaps_on_map (bool): Current setting for gaps between ships on the map.

    Returns:
    - list, list: New row and column indexes for the map if adjustments were successful.
    - bool: False if the game adjustment was interrupted.
    """

    # Declare the global variable for the default symbol used in the map
    global DEFAULT_SYMBOL, MAP_ROW_INDEXES, MAP_COLUMN_INDEXES

    input_validation = True  # Initialize input validation flag
    input_values = [1, 2]  # Initialize the list to store the user input values
    # Start an infinite loop to continuously offer adjustment options to the user
    while True:

        try:
            # Create a temporary map and a deep copy of the fleet for demonstration purposes
            tmp_map = create_map(height, width, DEFAULT_SYMBOL)
            tmp_fleet = copy.deepcopy(fleet)

            # Deploy the fleet on the temporary map for demonstration
            tmp_map, tmp_fleet = cpu_deploy_all_ships(tmp_map, fleet, gaps_on_map)

            # Define the text to display alongside the map
            tmp_text = [
                "Changing Labeling on map Row and Column",
                "Current game map coordinate system is \u001b[33mNumeric\u001b["
                "0m. To "
                "change it, enter 2 symbols: Rows then Columns.",
                "The first symbol will be for row indexes. Use a number for digits or a letter for alphabets.",
                "The second symbol will be for column indexes. Use a number for digits or a letter for alphabets."
            ]

            # Display the map and instructions side by side
            print_map_and_list(tmp_map, tmp_text, "Map Example", 10)

            # Check if the previous input was invalid and display a warning
            if not input_validation:
                print(
                    f'You have entered {len(input_values)} values. Only 2 are required: one for Row and one for Column.')

            # Now reseting values back after print Out
            input_validation = True  # Initialize input validation flag
            input_values = [1, 2]  # Initialize the list to store the user input values

            # Take user input
            user_input = input(\n)
            if user_input == "0":
                return

            # Validate user input
            input_validation, input_values, output_text = validate_user_input(user_input, 2)


            # If input is valid, proceed to adjust row and column indexes
            if input_validation:
                # Create row indexes based on the first symbol
                if input_values[0].isdigit():
                    MAP_ROW_INDEXES = list(range(height + 1))
                elif input_values[0].isalpha():
                    MAP_ROW_INDEXES = [chr(97 + i) for i in range(height + 1)]

                # Create column indexes based on the second symbol
                if input_values[1].isdigit():
                    MAP_COLUMN_INDEXES = list(range(width + 1))
                elif input_values[1].isalpha():
                    MAP_COLUMN_INDEXES = [chr(97 + i) for i in range(width + 1)]

                return

        # Handle any keyboard interrupts to exit the loop gracefully
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False  # Return False to indicate that the adjustment was interrupted


def modify_game_settings_map(height, width, fleet, gaps_on_map):
    """
    Allows the user to customize the dimensions of the game map.

    Args:
    - height (int): The current height of the game map.
    - width (int): The current width of the game map.
    - fleet (dict): The current state of the fleet.
    - label_row (list): Current row labels for the game map.
    - label_column (list): Current column labels for the game map.
    - gaps_on_map (bool): Current setting for gaps between ships on the map.

    Returns:
    - int, int: New dimensions for the game map if adjustments were successful.
    - bool: False if the game adjustment was interrupted.
    """

    # Declare the global variable for the default symbol used in the map
    global DEFAULT_SYMBOL, MAP_ROW_INDEXES, MAP_COLUMN_INDEXES

    input_values = [10, 10]  # Initialize the list to store the user input values
    input_validation = True  # Initialize input validation flag
    check_result = True  # Initialize a flag to check if the fleet fits on the map
    # Start an infinite loop to continuously offer adjustment options to the user
    while True:
        try:
            # Clear the terminal for a fresh display
            clear_terminal()

            # Create a temporary map and a deep copy of the fleet for demonstration purposes
            tmp_map = create_map(height, width, DEFAULT_SYMBOL)
            tmp_fleet = copy.deepcopy(fleet)

            # Deploy the fleet on the temporary map for demonstration
            tmp_map, tmp_fleet = cpu_deploy_all_ships(tmp_map, tmp_fleet, gaps_on_map)

            # Define the text to display alongside the map
            tmp_text = [
                "Now you can change game MAP settings",
                "Current settings are:",
                f"Map height is set to {height}",
                f"Map width is set to {width}",
                "If you would like to change it, please enter new Height and Width"
            ]

            # Display the map and instructions side by side
            print_map_and_list(tmp_map, tmp_text, "Map Example", 10)

            # Check if the previous input was invalid and display a warning
            if not input_validation:
                if len(input_values) != 2:
                    print(f'You have entered just {len(input_values)} values, I require 2: Height and Width.')

            if not check_result: # Check if the fleet doesn't fit on the map and display a warning

                print('Sorry, but I believe you need a bigger map for the current fleet.')

            # Take user input
            user_input = input(\n)

            # Validate the user input
            input_validation, input_values, output_text = validate_user_input(user_input, 2, "integer")

            # If the input is valid, proceed to check if the fleet fits on the map with the new dimensions
            if input_validation:
                # before we try if game fits all ships, we need to change Row and column labels, otherwise map can not be printed:
                if input_values[0] > len(MAP_ROW_INDEXES):
                    # Create Row indexes based on the second symbol
                    if str(MAP_ROW_INDEXES[0]).isdigit():
                        MAP_ROW_INDEXES = list(range(input_values[0] + 1))
                    elif str(MAP_ROW_INDEXES[0]).isalpha():
                        MAP_ROW_INDEXES = [chr(97 + i) for i in range(input_values[0] + 1)]

                if input_values[1] > len(MAP_COLUMN_INDEXES):
                    # Create Column indexes based on the second symbol
                    if str(MAP_COLUMN_INDEXES[1]).isdigit():
                        MAP_COLUMN_INDEXES = list(range(input_values[1] + 1))
                    elif str(MAP_COLUMN_INDEXES[1]).isalpha():
                        MAP_COLUMN_INDEXES = [chr(97 + i) for i in range(input_values[1] + 1)]

                # create temporary map to test with
                tmp_map = create_map(int(input_values[0]), int(input_values[1]), DEFAULT_SYMBOL)
                tmp_fleet = copy.deepcopy(fleet)

                # Test if the fleet can fit on the map with the new dimensions
                check_result = game_adjust_check_if_fleet_fits_on_map(tmp_map, tmp_fleet, gaps_on_map)

                # If the fleet fits, update the map dimensions
                if check_result:
                    height = int(input_values[0])
                    width = int(input_values[1])
                    return height, width

            else:
                input_validation = False
                continue

        # Handle any keyboard interrupts to exit the loop gracefully
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False  # Return False to indicate that the adjustment was interrupted


def modify_game_settings_fleet(height, width, fleet, gaps_on_map):
    """
    Allows the user to customize the fleet of ships.

    Args:
    - height (int): The current height of the game map.
    - width (int): The current width of the game map.
    - fleet (dict): The current state of the fleet.
    - label_row (list): Current row labels for the game map.
    - label_column (list): Current column labels for the game map.
    - gaps_on_map (bool): Current setting for gaps between ships on the map.

    Returns:
    - dict: New fleet dictionary if adjustments were successful.
    - bool: False if the game adjustment was interrupted.
    """
    global DEFAULT_SYMBOL  # Declare the global variable for the default symbol used in the map

    while True:
        # Clear the terminal for a fresh display
        user_input = ""
        clear_terminal()

        # Create a temporary map and a deep copy of the fleet for demonstration purposes
        tmp_map = create_map(height, width, DEFAULT_SYMBOL)
        tmp_fleet = copy.deepcopy(fleet)

        tmp_map, tmp_fleet = cpu_deploy_all_ships(tmp_map, tmp_fleet, gaps_on_map)
        print_map_and_fleet_aligned_columns(tmp_map, tmp_fleet, "Map Example", 10)

        # Display user instructions
        print("This is the game DEFAULT fleet. If you want to modify a ship (size and quantity) or delete a ship, please select the ship by typing its name or index and press Enter.")
        print("Example: Cruiser is index 3")
        print("If you want to add a new ship, please type N and hit ENTER.")
        print("To return to the main Settings menu, please type 0 (zero) and press ENTER.")

        try:
            user_input = input(\n).capitalize()

            if not user_input:
                print("Invalid input. Please enter a ship name, index, or 0 to go back.")
                continue

            if user_input == "N":
                fleet = modify_game_settings_fleet_add_new_ship(height, width, fleet, gaps_on_map)
            elif user_input == "0":
                return fleet
            elif user_input.isdigit():
                if user_input == "0":
                    return fleet

                index = int(user_input) - 1
                ship_names = list(fleet.keys())
                if 0 <= index < len(ship_names):
                    ship_name = ship_names[index]
                    fleet = modify_game_settings_fleet_single_ship(height, width, fleet, gaps_on_map, ship_name)

            else:
                closest_ship_name = find_closest_ship_name(user_input, fleet)
                if closest_ship_name:
                    fleet = modify_game_settings_fleet_single_ship(height, width, fleet, gaps_on_map, closest_ship_name)



        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False


def find_closest_ship_name(user_input, fleet):
    """
    Find the closest matching ship name in the fleet based on the following criteria:
    1. Direct substring match.
    2. First letter matching and common matching letters.
    3. Minimum Levenshtein distance.

    Args:
        user_input (str): The user input for finding the closest ship.
        fleet (dict): The fleet dictionary containing ship details.

    Returns:
        str: The closest matching ship name.
    """

    # Initialize variables to keep track of closest matches
    closest_match = None
    smallest_distance = float("inf")

    # Convert the user input to lowercase for case-insensitive comparison
    user_input = user_input.lower()

    # If the user input is just one letter, return the closest match based on that letter
    if len(user_input) == 1:
        for ship_name in fleet.keys():
            if user_input == ship_name[0].lower():
                return ship_name

    # First, look for a direct substring match
    for ship_name in fleet.keys():
        if user_input in ship_name.lower():
            return ship_name

    # Second, check for first letter matching and common matching letters
    possible_ships = []
    for ship_name in fleet.keys():
        if user_input[0] == ship_name[0].lower():
            possible_ships.append(ship_name)

    if possible_ships:
        max_common_letters = 0
        for ship_name in possible_ships:
            common_letters = len(set(user_input) & set(ship_name.lower()))
            if common_letters > max_common_letters:
                max_common_letters = common_letters
                closest_match = ship_name

        if closest_match:
            return closest_match

    # Fall back to using Levenshtein distance
    for ship_name in fleet.keys():
        # Calculate the distance
        distance = levenshtein_distance(user_input, ship_name.lower())

        # Update the closest match if a smaller distance is found
        if distance < smallest_distance:
            closest_match = ship_name
            smallest_distance = distance

    return closest_match


def modify_game_settings_fleet_add_new_ship(height, width, fleet, gaps_on_map):
    """
    Allows the user to add a new ship to the fleet.

    Args:
    - height (int): The height of the game map.
    - width (int): The width of the game map.
    - fleet (dict): The current state of the fleet.
    - label_row (list): Current row labels for the game map.
    - label_column (list): Current column labels for the game map.
    - gaps_on_map (bool): Current setting for gaps between ships on the map.

    Returns:
    - dict: Updated fleet dictionary if a new ship was successfully added.
    """

    # Access the global variable for the default symbol used on the map
    global DEFAULT_SYMBOL

    # Initialize variables for user input validation and fleet fitting check
    validated_user_input_1 = ["ShipName", "Size", "QTY"]
    check_result = True
    validated_user_input_2 = []
    # Start an infinite loop to continuously offer adjustment options to the user
    while True:

        try:
            # Clear the terminal screen
            clear_terminal()

            # Create a temporary map and a deep copy of the fleet for demonstration
            tmp_map = create_map(height, width, DEFAULT_SYMBOL)
            tmp_fleet = copy.deepcopy(fleet)

            # Deploy the fleet on the temporary map for demonstration
            tmp_map, tmp_fleet = cpu_deploy_all_ships(tmp_map, tmp_fleet, gaps_on_map)

            # Display the map and fleet side by side
            print_map_and_fleet_aligned_columns(tmp_map, tmp_fleet, "Map Example", 10)

            # Validate that the user has entered exactly 3 values for the new ship
            if len(validated_user_input_1) != 3:
                print(f'Please make sure you have entered 3 values; currently, I see only {len(validated_user_input_1)} values.')

            # Inform the user if the new ship cannot fit on the map

            if not check_result:
                print(f'Cannot fit the new ship {validated_user_input_1[0]} with size {validated_user_input_2[0]} and '
                      f'quantity {validated_user_input_2[1]} into the current fleet.')
                print('Consider increasing the map size before adding this new ship.')



            # Capture the user's input for the new ship
            user_input = input("Please enter the Ship name, size, and quantity of ships you want to add to the fleet: ")

            # Exit if the user enters '0'
            if user_input == "0":
                return fleet

            # Validate the user's input
            validation_result_1, validated_user_input_1, output_text_1 = validate_user_input(user_input, 3)

            # Check if the first validation succeeded
            if validation_result_1:
                # Validate the size and quantity to ensure they are integers
                new_input = f"{validated_user_input_1[1]},{validated_user_input_1[2]}"
                validation_result_2, validated_user_input_2, output_text_2 = validate_user_input(new_input, 2, "integer")

                # If the second validation also succeeds
                if validation_result_2:
                    # Make a deep copy of the current fleet and map for testing
                    tmp_fleet = copy.deepcopy(fleet)
                    tmp_map = create_map(height, width, DEFAULT_SYMBOL)

                    # Add the new ship to the temporary fleet
                    tmp_fleet[validated_user_input_1[0]] = {"Size": int(validated_user_input_2[0]),
                                                            "Quantity": int(validated_user_input_2[1]),
                                                            "Coordinates": []}

                    # Check if the updated fleet can fit on the map
                    check_result = game_adjust_check_if_fleet_fits_on_map(tmp_map, tmp_fleet, gaps_on_map)

                    # If the new fleet fits, update the actual fleet
                    if check_result:
                        fleet[validated_user_input_1[0]] = {"Size": int(validated_user_input_2[0]),
                                                            "Quantity": int(validated_user_input_2[1]),
                                                            "Coordinates": []}
                        return fleet
                    else:
                        continue

        except ValueError:
            print("Values you have entered are not valid. Please enter the correct number of values.")


def modify_game_settings_fleet_single_ship(height, width, fleet, gaps_on_map, ship_name):
    """
    Allows the user to modify or delete a single existing ship from the fleet.

    Args:
    - height (int): The height of the game map.
    - width (int): The width of the game map.
    - fleet (dict): The current state of the fleet.
    - label_row (list): Current row labels for the game map.
    - label_column (list): Current column labels for the game map.
    - gaps_on_map (bool): Current setting for gaps between ships on the map.
    - ship_name (str): The name of the ship to be modified.

    Returns:
    - dict: Updated fleet dictionary if the ship was successfully modified or deleted.
    """

    # Access the global variable for the default symbol used on the map
    global DEFAULT_SYMBOL

    # Initialize variables
    ship_size = fleet[ship_name]["Size"]
    ship_qty = fleet[ship_name]["Quantity"]
    input_validation = True
    check_result = True
    validated_user_input = ''
    output_text = ""
    # Start an infinite loop for user interaction
    while True:

        try:
            # Clear terminal screen for a fresh view
            clear_terminal()

            # Create a temporary map and deep copy of the fleet for demonstration
            tmp_map = create_map(height, width, DEFAULT_SYMBOL)
            tmp_fleet = copy.deepcopy(fleet)

            # Deploy this temporary fleet onto the temporary map
            tmp_map, tmp_fleet = cpu_deploy_all_ships(tmp_map, tmp_fleet, gaps_on_map)

            # Display the map and fleet side-by-side
            print_map_and_fleet_aligned_columns(tmp_map, tmp_fleet, "Map Example", 10)

            # Display validation and fitting errors, if any
            if not input_validation:
                print("You have entered incorrect information.")
                print(output_text[0])
                input_validation = True  #Reseting value

            if not check_result:
                print(f'Cannot fit the ship {ship_name} with size {validated_user_input[0]} and quantity {validated_user_input[1]} into the current fleet.')
                check_result = True  # Resetting value

            # Display current ship details
            print(f"You have selected the ship {ship_name}. It has a size of {ship_size} cells and there are {ship_qty} such ships in the current fleet.")

            # Capture user's next action
            user_input = input("To delete the ship, type 'D'. To modify, enter size and quantity (e.g., 2,1). To go back, type 0: ").strip().upper()

            # Validate user input
            if not user_input:
                print("Invalid input. Please try again.")
            elif user_input == "D":
                del fleet[ship_name]
                return fleet
            elif user_input == "0":
                return fleet
            else:
                validation_result, validated_user_input, output_text = validate_user_input(user_input, 2, "integer")

                # If input is valid, attempt to modify the ship
                if validation_result:
                    tmp_fleet = copy.deepcopy(fleet)
                    tmp_map = create_map(height, width, DEFAULT_SYMBOL)
                    tmp_fleet[ship_name]["Size"] = int(validated_user_input[0])
                    tmp_fleet[ship_name]["Quantity"] = int(validated_user_input[1])

                    # Check if the modified fleet fits on the map
                    check_result = game_adjust_check_if_fleet_fits_on_map(tmp_map, tmp_fleet, gaps_on_map)

                    if check_result:
                        fleet[ship_name]["Size"] = int(validated_user_input[0])
                        fleet[ship_name]["Quantity"] = int(validated_user_input[1])
                        return fleet
                else:
                    input_validation = False

        except ValueError:
            print("Invalid input. Please enter size and quantity as two digits separated by a comma.")


"""Functions for checking and validating
--------------------------------------"""


def game_adjust_check_if_fleet_fits_on_map(map, fleet, gaps_on_map):
    """
    Checks if the entire fleet can be deployed on the given map.

    This function attempts to deploy the fleet on the map multiple times.
    If it succeeds at least once, it returns True. Otherwise, it returns False.

    Args:
    - map (list of lists): The game map represented as a 2D list.
    - fleet (dict): The current state of the fleet.

    Returns:
    - bool: True if the fleet can be deployed on the map, False otherwise.
    """

    # Loop 50 times to try and fit the fleet on the map
    # This accounts for the randomness in ship placement
    for i in range(50):
        # Create a deep copy of the fleet for temporary manipulation
        tmp_fleet = copy.deepcopy(fleet)

        # Try to deploy all ships in the fleet onto the map
        # The 'cpu_deploy_all_ships' function returns False if deployment is not possible
        result = cpu_deploy_all_ships(map, tmp_fleet, gaps_on_map)

        # If deployment was successful, break the loop and return True
        if not result :
            return result

    # If we've gone through all 50 attempts without success, return False
    print("Unable to fit the fleet on the map after 50 attempts.")
    return True


def validate_user_input(input_str, parts, type=None):
    """
    Validates user input by splitting it into a specified number of parts and optionally verifies their type.

    Parameters:
        input_str (str): The user-provided input string.
        parts (int): The expected number of parts to split the input into.
        type (str, optional): The expected data type for each part, currently supports only 'integer'.

    Returns:
        tuple: A tuple containing three elements:
            - A boolean indicating if the input is valid.
            - A tuple of the split parts.
            - A list of string messages indicating the validation status for each part.
    """

    # Use a regular expression to split the input into parts by any non-alphanumeric character,
    # while also removing any empty strings.
    split_input = re.split(r'[^A-Za-z0-9]+', input_str)
    # Initialize a flag to keep track of whether the entire input is valid
    input_valid = True

    # Initialize a list to hold text that describes the validation status for each part
    output_text = []

    # Check if the number of parts obtained from the split operation matches the expected number of parts
    if len(split_input) != parts:
        output_text.append(f'Input should be split into {parts} parts.')
        return False, tuple(split_input), output_text

    # If a specific data type is expected for each part, perform type validation
    if type == 'integer':
        for i, part in enumerate(split_input):
            # Check if the part is an integer
            if not part.isdigit():
                output_text.append(f'Your input "{part}" is NOT an Integer.')
                input_valid = False  # Mark the input as invalid if even one part fails the type check
            else:
                output_text.append(f'Your input "{part}" is an Integer.')
                # Convert the part to an integer for future use
                split_input[i] = int(part)

    # Return the final validity flag, the tuple of validated parts, and the list of validation messages
    return input_valid, tuple(split_input), output_text


"""Main Functions
--------------"""

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

"""Print functions
----------------"""

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



def print_map(map_game):
    """
    Print the game map in a human-readable format.

    Args:
        map_game (list): A 2D list representing the game map,
                         where each cell contains the status of a ship
                         or water.

    Output:
        The function will print the game map to the console.
    """
    # Global variables for row and column indexes
    global MAP_ROW_INDEXES, MAP_COLUMN_INDEXES

    # Print column headers (0, 1, 2, ..., N)
    print("   ", end="")
    for col_index in range(len(map_game[0])):
        print(f"{MAP_ROW_INDEXES[col_index]}  ", end="")

    # Print a separator line between headers and table
    print("\n   " + "=" * (len(map_game[0]) * 3))

    # Loop through each row
    for row_index, row in enumerate(map_game):
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
    # Global variables for row and column indexes
    global MAP_ROW_INDEXES, MAP_COLUMN_INDEXES

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


def print_map_and_fleet_aligned_columns(map_left, fleet, label_left, gap=10):
    """
    Print a 2D map and a fleet dictionary with aligned columns side by side, and with a customizable gap.

    Args:
        map_left (list): A 2D list representing the first map.
        fleet (dict): A dictionary representing the fleet.
        label_left (str): Label for the first map.
        gap (int): Number of blank spaces between the map and the fleet information. Default is 10.
    """
    # Global variables for row and column indexes
    global MAP_ROW_INDEXES, MAP_COLUMN_INDEXES

    # Constants for character dimensions and formatting
    char_width = len("X")  # Width of a single character (assuming monospaced font)

    # Calculate the maximum number of digits in row and column indices for map_left
    num_digits_map_width = len(str(len(map_left[0])))
    num_digits_map_height = len(str(len(map_left)))

    # Create a string of blank spaces for the gap between map and fleet
    gap_str = ' ' * gap

    # Calculate the left-side offset for aligning map and row indices
    row_index_separator = " | "
    print_map_left_offset = " " * (num_digits_map_height + len(row_index_separator))

    # Center-align the label for map_left
    number_char_table_total = (len(map_left[0]) * (num_digits_map_width + char_width + 1))
    label_left_centered = label_left.center(number_char_table_total)

    # Print the centered label for map_left
    print(f"{print_map_left_offset}{label_left_centered}")

    # Print column headers for map_left
    print(print_map_left_offset, end=" ")
    for col_index in range(len(map_left[0])):
        print(f"{MAP_COLUMN_INDEXES[col_index]}".rjust(num_digits_map_height + char_width), end=" ")

    # Calculate the maximum lengths for the ship name, size, and quantity columns for alignment
    max_ship_name_length = max(len(ship) for ship in fleet.keys())
    max_size_length = len("Size")
    max_quantity_length = len("Quantity")

    # Generate the header for the fleet information
    fleet_header = f"{'Ship Name':<{max_ship_name_length}} | {'Size':>{max_size_length}} | {'Quantity':>{max_quantity_length}}"
    print(gap_str, fleet_header)
    print("    ".rjust(num_digits_map_width + 1), "=" * (number_char_table_total))  # Draw a separator line

    # Convert the fleet dictionary to a list of formatted strings with aligned columns
    fleet_str_lines = [
        f"{ship:<{max_ship_name_length}} | {props['Size']:>{max_size_length}} | {props['Quantity']:>{max_quantity_length}}"
        for ship, props in fleet.items()]

    # Loop through each row to print map values and fleet information
    for row_index in range(max(len(map_left), len(fleet_str_lines))):
        # Print row for map_left
        if row_index < len(map_left):
            print(f"{MAP_ROW_INDEXES[row_index]}".rjust(num_digits_map_width + 1), end=row_index_separator)
            for value in map_left[row_index]:
                width = len(str(value))
                print(f"{value}".rjust(num_digits_map_height + char_width - (char_width - width)), end=" ")
        else:
            # Print spaces to align with the map when the map is shorter than the fleet information
            print(" " * (num_digits_map_width + num_digits_map_height + len(row_index_separator) + char_width * len(
                map_left[0])), end="")

        # Insert the gap between the map and the fleet
        print(gap_str, end="")

        # Print fleet information for the row
        if row_index < len(fleet_str_lines):
            print(fleet_str_lines[row_index])
        else:
            print()


def print_aligned_log(log_data, gap=10):
    """
    Prints log data in aligned columns with predefined labels and a customizable gap.

    Args:
        log_data (list): A list of log entries. Each entry is a list containing
                         information about the player, time, row, column, and result.
        gap (int): Number of blank spaces between the log columns. Default is 10.

    Example:
        print_aligned_log([['CPU', 0.0658, 4, 5, 'Damaged']], gap=5)
    """

    # Predefined labels for the columns
    labels = ['Player', 'Time', 'Row', 'Column', 'Result']

    # Calculate the maximum width for each column to align the data
    max_widths = [0] * len(labels)
    for i in range(len(labels)):
        max_widths[i] = max(len(labels[i]), max(len(str(entry[i])) for entry in log_data))

    # Create a string filled with blank spaces for the gap between columns
    gap_str = ' ' * gap

    # Print the header row with labels, aligning each column based on its maximum width
    header_str = " | ".join(f"{labels[i]:<{max_widths[i]}}" for i in range(len(labels)))
    print(header_str)

    # Print each log entry, aligning each column based on its maximum width
    for entry in log_data:
        entry_str = " | ".join(f"{str(entry[i]):<{max_widths[i]}}" for i in range(len(entry)))
        print(entry_str)

    # No return statement is needed as the function prints directly to the console


"""User Game Play Functions
-------------------------"""


def player_shoot_input(map_hidden, map_display, enemy_fleet):
    """
    Handles the player's shooting action by taking input coordinates and updating the game state.

    Args:
        map_hidden (list): The hidden 2D map of CPU, which we are targeting.
        map_display (list): The 2D map that is visible to the player.
        enemy_fleet (dict): The enemy fleet's information.

    Returns:
        - fleet_target: Dictionary holding information about the CPU's fleet.
        - map_hidden: Hidden map here we perform search and shoot
        - map_display: Display map if shoot is success, then display hit or miss
    """

    # Global variables for row and column indexes and the CPU's shot log
    global MAP_ROW_INDEXES, MAP_COLUMN_INDEXES, cpu_shot_log_tmp

    # Flag to track whether the user's input is valid
    input_validation = True
    coordinate_value_correct = True
    row = ""
    column = ""
    input_values = ""
    column_index = ""
    coordinates_check = ""
    row_index = ""
    coordinate_return_message = ""
    coordinate_value_correct = True
    while True:
        try:
            # If the last input was invalid, print an error message
            if not input_validation:
                clear_terminal()
                print_two_maps(map_hidden, map_display, "CPU Map", "Player Map",
                               10)
                print(f' Please enter JUST 2 values, as you have entered {len(input_values)}')
                input_validation = True # Resetting validation
            if not coordinate_value_correct:
                clear_terminal()
                print_two_maps(map_hidden, map_display, "CPU Map", "Player Map",
                               10)
                print(coordinate_return_message)

            # Prompt the user for coordinates to shoot at
            print(f'Please enter coordinates to shoot, Row and Column, in this pattern')

            user_input = input(\n)

            # Validate the user's input to ensure it contains exactly two values
            input_validation, input_values, output_text = validate_user_input(user_input, 2)

            # Determine the correct input type based on MAP_ROW_INDEXES and MAP_COLUMN_INDEXES.
            input_row = get_corrected_input(input_values[0], MAP_ROW_INDEXES)
            input_column = get_corrected_input(input_values[1], MAP_COLUMN_INDEXES)

            if input_row in MAP_ROW_INDEXES:
                row = MAP_ROW_INDEXES.index(input_row)
                row_value_correct = True
                row_return_message = ""
            else:
                row_value_correct = False
                row_return_message = f'There is no such Row on current map with index {input_row}'

            if input_column in MAP_COLUMN_INDEXES:
                column = MAP_COLUMN_INDEXES.index(input_column)
                column_value_correct = True
                column_return_message = ""
            else:
                column_value_correct = False
                column_return_message = f'There is no such Column on current map with index {input_column}'

            # Now we will add both validation, and if both are true, code will continue, otherwise it will trigger
            # error and print out
            coordinate_value_correct = row_value_correct and column_value_correct

            # Creating return message if it needs to be printed out
            if row_return_message and column_return_message:
                coordinate_return_message = row_return_message + "\n" + column_return_message
            else:
                coordinate_return_message = row_return_message + column_return_message
            # If the input is valid
            if coordinate_value_correct:
                if row in MAP_ROW_INDEXES:
                    row_index = MAP_ROW_INDEXES.index(row)
                    column_index = MAP_COLUMN_INDEXES.index(column)
                    coordinates_check = ""

                    # Check if the coordinates are already shot at
                    coordinates_check = player_shoot_coordinates_check(row_index, column_index, map_hidden)

            # If the coordinates are valid and haven't been shot at, perform the shooting action
            if coordinates_check:
                map_hidden, map_display, fleet = action_perform_shoot("Player",
                                                                      map_hidden,
                                                                      map_display,
                                                                      row_index,
                                                                      column_index,
                                                                      enemy_fleet,
                                                                      cpu_shot_log_tmp)
                return map_hidden, map_display, fleet
            else:
                coordinate_value_correct = False
                coordinate_return_message = f'Sorry but you have already used these coordinates'

        # Handle keyboard interrupts to exit the game gracefully
        except KeyboardInterrupt:
            print("Game adjustment interrupted.")
            return False


def player_shoot_coordinates_check(row, column, map_game):
    """
    Checks if the provided coordinates have already been targeted.

    Args:
        row (int): Row index on the game map.
        column (int): Column index on the game map.
        map_game (list): The 2D array representing the game map.

    Returns:
        bool: True if the coordinates are valid for shooting, False otherwise.
    """

    # Access the global variables
    global DEFAULT_SYMBOL, game_actions_log

    # Initialize result flag to True
    check_result = True

    # Check if the coordinate on the game map is the default symbol (meaning not yet targeted)
    if map_game[row][column] == DEFAULT_SYMBOL:
        check_result = True

    # Loop through the game action logs to see if this coordinate has already been targeted
    for log in game_actions_log:
        if int(row) == log[2] and int(column) == log[3] and log[0] == "Player":
            check_result = False  # Set result flag to False if coordinate has been targeted

    return check_result  # Return the result flag


def player_deploy_all_ships(map_hidden, map_display, fleet, gaps_on_map):
    """
    Deploys all ships for the player on the given maps.

    Args:
        map_display (list): The 2D array representing the display map.
        map_hidden (list): The 2D array representing the hidden map.
        fleet (dict): A dictionary containing the details of the fleet.
        gaps_on_map (bool): The gaps between ships on the map.

    Returns:
        tuple: Updated map_display and fleet dictionary with deployed ship coordinates.
    """

    # Access the global variables for default and ship symbols
    global DEFAULT_SYMBOL, SHIP_SYMBOLS

    # Loop through each ship type in the fleet
    for ship_name, ship_info in fleet.items():

        # Extract the quantity and size for each ship type
        quantity = ship_info["Quantity"]
        size = ship_info["Size"]

        # Loop to deploy each ship of the current type
        for i in range(quantity):
            # Deploy a single ship and get updated maps and coordinates
            map_hidden, map_display, coordinates_list = (
                player_deploy_single_ship(
                map_hidden, map_display, ship_name, size, gaps_on_map, fleet))

            # Append the coordinates of the deployed ship to the fleet dictionary
            fleet[ship_name]["Coordinates"].append(coordinates_list)

    # Return the updated display map and fleet dictionary
    return map_display, fleet


def player_deploy_single_ship(map_hidden, map_display, ship_name, ship_size,
                              gaps_on_map, fleet):
    """
    Handles the deployment of a single ship for the player on the game board.

    Args:
        map_display (list): 2D list representing the display map.
        map_hidden (list): 2D list representing the hidden map.
        ship_name (str): The name of the ship to be deployed.
        ship_size (int): The size of the ship.
        gaps_on_map (bool): Flag to indicate if gaps are allowed between ships on the map.

    Returns:
        tuple: Returns updated display map, hidden map, and coordinates list where the ship is deployed.
    """
    global MAP_ROW_INDEXES, MAP_COLUMN_INDEXES  # Global constants for row and column indexes
    # Initialization of various validation flags

    input_validation = True
    coordinate_value_correct = True
    alignment_value_correct = True
    map_check_result = True
    alignment = ""
    alignment_mistake_message = ""
    column = ""
    row = ""
    coordinate_return_message = ""
    input_values = ""
    message_ship_does_not_fit = ""
    output_values_message = ""

    while True:  # Main loop for user interaction

        try:
            clear_terminal()
            print_map_and_fleet_aligned_columns(map_display,fleet, "Player Map", 10)
            if ship_size == 1:
                print(f'Please enter  2 values: coordinates (Row, Column) for ship {ship_name} deployment')
            else:
                print(f'Please enter 3 values: coordinates (Row, Column) for ship {ship_name} deployment and alignment')

            # Display error messages based on the flags
            if not input_validation:
                for message in output_values_message:
                    print(message)
            if not coordinate_value_correct:
                print(coordinate_return_message)
            if not alignment_value_correct:
                print(alignment_mistake_message)
            if not map_check_result:
                print(message_ship_does_not_fit)

            input_validation = True
            coordinate_value_correct = True
            alignment_value_correct = True
            map_check_result = True


            # Collect user input
            user_input = input(\n)
            # checking if user has entered any information
            if len(user_input)>0:

                # Validate input based on ship size
                # If ship size = 1, then we just allocate alignment, as it is irrelevant
                if ship_size == 1:
                    input_validation, input_values, output_values_message = validate_user_input(user_input, 2)
                    alignment = "Single"

                # If ship size is more then 1 cell, we neet to validate, it is 3 values entered
                elif ship_size > 1:
                    input_validation, input_values, output_values_message = validate_user_input(user_input, 3)
                    if input_validation:
                        # Now we check if last 3rd value is letter and is it Vertical or Horizontal, coordinates we will check below
                        alignment_text = input_values[2]

                        # If user entered just one letter, we will try to get alignment
                        if alignment_text.lower() == "v":
                            alignment = "Vertical"
                        elif alignment_text.lower() == "h":
                                alignment = "Horizontal"

                        # If alignment can not be detected, or it is complicated string:
                        else:
                            alignment_value_correct, alignment, alignment_mistake_message = user_input_detect_alignment(alignment_text)
                    else:
                        continue

            # Alignment is sorted, now we check coordinates:
            # Determine the correct input type based on MAP_ROW_INDEXES and MAP_COLUMN_INDEXES.
            input_row = get_corrected_input(input_values[0], MAP_ROW_INDEXES)
            input_column = get_corrected_input(input_values[1], MAP_COLUMN_INDEXES)

            if input_row in MAP_ROW_INDEXES:
                row = MAP_ROW_INDEXES.index(input_row)
                row_value_correct = True
                row_return_message = ""
            else:
                row_value_correct = False
                row_return_message = f'There is no such Row on current map with index {input_row}'

            if input_column in MAP_COLUMN_INDEXES:
                column = MAP_COLUMN_INDEXES.index(input_column)
                column_value_correct = True
                column_return_message = ""
            else:
                column_value_correct = False
                column_return_message = f'There is no such Column on current map with index {input_column}'

            # Now we will add both validation, and if both are true, cdde will continu, otherwise it will trigger error and print out
            coordinate_value_correct = row_value_correct and column_value_correct

            # Creating return message if it needs to be printed out
            if row_return_message and column_return_message:
                coordinate_return_message = row_return_message + "\n" + column_return_message
            else:
                coordinate_return_message = row_return_message + column_return_message

            # If all inputs are valid, proceed to deploy the ship
            if coordinate_value_correct == True and alignment_value_correct == True:
                coordinates_list = create_coordinate_list(row, column, alignment, ship_size)
                map_check_result , message_ship_does_not_fit= player_deploy_single_ship_check_map_space(map_hidden, coordinates_list)

                if map_check_result:
                       # Deploy the ship and update maps
                    map_hidden = map_show_ship_or_symbols(map_hidden, coordinates_list, alignment, gaps_on_map)
                    map_display = map_show_ship_or_symbols(map_display, coordinates_list, alignment, gaps_on_map)
                    map_display = map_show_only_ships(map_display)
                    return map_hidden, map_display, coordinates_list
            else:
                continue
            if not user_input:
                continue

        except ValueError:
            print("Values you have entered are not valid. Please enter the correct number of values.")


def get_corrected_input(input_value, map_indexes):
    """
    Converts the user input to the appropriate type based on the type of indexes used in the map.

    The function checks the type of the first index in the map_indexes list and then converts
    the user input to either an integer or a string accordingly.

    Args:
        input_value (str): The user input value that needs to be converted.
        map_indexes (list): A list of indexes used in the map, which could be either integers or strings.

    Returns:
        int or str or None: Returns the converted input value if successful; otherwise returns None.
    """

    # Check the type of the first element in map_indexes to determine if it's a letter or number.
    if isinstance(map_indexes[0], int):
        # If the map uses integer indexes, convert the input to an integer.
        return int(input_value)

    elif isinstance(map_indexes[0], str):
        # If the map uses letter indexes, convert the input to lower-case.
        return input_value.lower()

    else:
        # Handle other types as needed. For now, return None to indicate unsuccessful conversion.
        return None


def user_input_check_input_is_integer(row, column):
    """
    Validates whether the row and column provided by the user are valid integers and exist in MAP_ROW_INDEXES and MAP_COLUMN_INDEXES.

    Args:
        row (str): The row value entered by the user.
        column (str): The column value entered by the user.

    Returns:
        tuple: Returns a tuple containing four elements:
               1. value_correct (bool): True if both row and column are valid, False otherwise.
               2. row (int): The index of the row in MAP_ROW_INDEXES.
               3. column (int): The index of the column in MAP_COLUMN_INDEXES.
               4. return_message (str): A message explaining why validation failed, if it did.
    """

    # Initialize the validation flag and message
    value_correct = False
    return_message = ""

    # Concatenate row and column inputs for validation
    input_first_two_values = row + "," + column

    # Validate if the user inputs for row and column are integers
    input_validation_is_integer, row_column, row_column_output = validate_user_input(input_first_two_values, 2,
                                                                                     "integer")

    # If the inputs are valid integers, proceed to specific row and column validation
    if input_validation_is_integer:

        # Validate the row against MAP_ROW_INDEXES
        if row_column[0] in MAP_ROW_INDEXES:
            row = MAP_ROW_INDEXES.index(row_column[0])
            value_correct = True
            return_message = ""
        else:
            value_correct = False
            return_message = f'I am sorry, but there is no such {row} on the current map'

        # Validate the column against MAP_COLUMN_INDEXES
        if row_column[1] in MAP_COLUMN_INDEXES:
            column = MAP_COLUMN_INDEXES.index(row_column[1])
            value_correct = True
            return_message = ""
        else:
            value_correct = False
            return_message = f'I am sorry, but there is no such {column} on the current map'

    # If the inputs are not integers, set the validation flag to False and prepare an error message
    else:
        value_correct = False
        return_message = f'I am sorry, but values you have typed in are not integers'

    # Return the final validation flag, row and column indices, and any return messages
    return value_correct, row, column, return_message


# Updating the function to handle cases where the first letter might be missing
def user_input_detect_alignment(alignment_text):
    """
    Determine the alignment based on user input.

    This function starts by checking the first letter to see if it matches the first letter
    of known orientations ('Vertical' and 'Horizontal'). It then checks for common matching
    letters to make the final decision. It also accounts for cases where the first letter might be missing.

    Args:
        alignment_text (str): The user's input text for alignment.

    Returns:
        tuple: A tuple containing:
            - alignment_valid (bool): Whether the alignment could be determined.
            - alignment (str): The determined alignment ('Vertical' or 'Horizontal').
            - alignment_mistake_message (str): A message for the case when alignment could not be determined.
    """

    # Normalized constants for known orientations
    vertical_string = 'vertical'
    horizontal_string = 'horizontal'

    # Normalize the user input for easier comparison
    normalized_alignment = alignment_text.lower()

    # Initialize result variables
    alignment = ""
    alignment_valid = False
    alignment_mistake_message = ""

    # Step 1: Check first letter
    # If the first letter doesn't match either, keep possibilities open for both alignments
    if normalized_alignment[0] == vertical_string[0]:
        possible_alignments = ["Vertical"]
    elif normalized_alignment[0] == horizontal_string[0]:
        possible_alignments = ["Horizontal"]
    else:
        possible_alignments = ["Vertical", "Horizontal"]

    # Step 2: Check for common matching letters
    common_letters_vertical = len(
        set(normalized_alignment) & set(vertical_string))
    common_letters_horizontal = len(
        set(normalized_alignment) & set(horizontal_string))

    if "Vertical" in possible_alignments and common_letters_vertical > common_letters_horizontal:
        alignment = "Vertical"
        alignment_valid = True
    elif "Horizontal" in possible_alignments and common_letters_horizontal > common_letters_vertical:
        alignment = "Horizontal"
        alignment_valid = True

    # Handle the case where alignment couldn't be determined
    if not alignment_valid:
        alignment_mistake_message = f"I am sorry, but I cannot determine the alignment from the input: {alignment_text}"

    return alignment_valid, alignment, alignment_mistake_message



def levenshtein_distance(source_word, target_word):
    """
    Calculate the Levenshtein distance between two strings.

    The Levenshtein distance is a measure of the similarity between two strings.
    It is calculated as the minimum number of single-character edits needed to
    transform one string into the other.

    Args:
        source_word (str): The source string for comparison.
        target_word (str): The target string for comparison.

    Returns:
        int: The Levenshtein distance between the two strings.
    """

    # If the source word is shorter than the target word, swap them.
    if len(source_word) < len(target_word):
        return levenshtein_distance(target_word, source_word)

    # Initialize a list of distances. Each index i in this list will eventually
    # contain the Levenshtein distance between the first i characters of source_word
    # and the first j characters of target_word.
    distances = list(range(len(source_word) + 1))

    # Loop through each character in the target word.
    for target_index, target_char in enumerate(target_word):
        # Initialize a new list of distances for this iteration.
        new_distances = [target_index + 1]

        # Loop through each character in the source word.
        for source_index, source_char in enumerate(source_word):
            # If the characters match, the cost is zero, otherwise the cost is one.
            cost = 0 if source_char == target_char else 1

            # The new distance is the minimum between deleting from source,
            # deleting from target, or substituting.
            new_distance = min(
                distances[source_index] + 1,  # Deletion
                distances[source_index + 1] + 1,  # Insertion
                distances[source_index] + cost  # Substitution
            )
            new_distances.append(new_distance)

        # Update the list of distances.
        distances = new_distances
    return distances[-1]  # The last element is the Levenshtein distance between the two full words.


def player_deploy_single_ship_check_map_space(map_game, coordinates_list):
    """
    Check if a ship can be deployed at the given coordinates on the game map.

    This function checks if the specified coordinates on the game map are empty,
    allowing for the ship to be deployed.

    Args:
        map_game (list): The 2D list representing the game map.
        coordinates_list (list): A list of tuples, each containing the row and column index.

    Returns:
        bool: True if the ship can be deployed, False otherwise.
    """
    global DEFAULT_SYMBOL  # Use the globally defined default symbol for an empty cell

    # Initialize variable to True. Will set to False if any coordinate is occupied.
    checking_ship_fits_on_map = True
    message_text = ""

    # Loop through each coordinate in the list
    for coordinate in coordinates_list:
        row, column = coordinate  # Unpack the tuple into row and column

        # Checking if coordinates are within map boundaries
        if 0 <= row < len(map_game) and 0 <= column < len(map_game[0]):

            # If coordinates are within map, we check if it is empty space
            if map_game[row][column] != DEFAULT_SYMBOL:
                checking_ship_fits_on_map = False  # Set to False as the cell is occupied
                message_text = f' sorry but it appears there is another ship there, choose different coordinates'
            else:
                message_text = ""
        else:
            checking_ship_fits_on_map = False
            message_text = f' sorry but with given coordinates, this part of ship [{row}, {column}] will be out of map boundaries'

    # If the loop completes, the ship fits and the function will return True
    return checking_ship_fits_on_map, message_text



"""Map manipulating functions
---------------------------"""


def create_coordinate_list(row, column, alignment, ship_size):
    """
    Create a list of coordinates where the ship will be placed on the map.

    This function generates a list of coordinates based on the starting row and column,
    the alignment of the ship, and the size of the ship.

    Args:
        row (int): The starting row index for the ship.
        column (int): The starting column index for the ship.
        alignment (str): The orientation of the ship ("Horizontal" or "Vertical").
        ship_size (int): The size of the ship.

    Returns:
        list: A list of coordinates where the ship will be placed.
    """

    # Initialize an empty list to store the coordinates
    coordinates_list = []

    # If the ship size is 1, it only occupies one cell
    if ship_size == 1:
        coordinates_list.append([row, column])

    # For larger ships, we need to calculate the additional coordinates based on alignment
    else:
        # If the ship is aligned horizontally
        if alignment == "Horizontal" or alignment == "HorizontalSunk":
            for cell in range(ship_size):
                coordinates_list.append([row, column + cell])

        # If the ship is aligned vertically
        if alignment == "Vertical" or alignment == "VerticalSunk":
            for cell in range(ship_size):
                coordinates_list.append([row + cell, column])

    return coordinates_list


def map_allocate_empty_space_for_ship(map_game, coordinates_list):
    """
    Allocate empty space around a ship on a 2D map.

    This function modifies the given map_game to ensure that ships cannot be
    deployed touching each other. It marks the empty space around a ship with
    'Miss' symbols. After all ships are deployed, these symbols will be changed
    back to DEFAULT_SYMBOL.

    Args:
        map_game (list): The 2D map where the ship will be deployed.
        coordinates_list (list): List of coordinates where the ship is located.

    Global Variables:
        SHIP_SYMBOLS (dict): Dictionary containing ship symbols.

    Returns:
        list: Modified game map with empty spaces around the ship.
    """

    # Access the global variable SHIP_SYMBOLS for ship symbols
    global SHIP_SYMBOLS

    # Define the relative positions for empty space around a single cell
    blank_space = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]

    # Initialize an empty list to store the coordinates for empty spaces
    blank_space_coordinates_list = []

    # Calculate the actual positions for empty space around each cell of the ship
    for space in blank_space:
        blank_row, blank_column = space
        for coordinate in coordinates_list:
            new_row, new_column = coordinate
            new_blank_row, new_blank_column = blank_row + new_row, blank_column + new_column
            blank_space_coordinates_list.append([new_blank_row, new_blank_column])

    # Update the map to allocate empty space around the ship
    for new_space in blank_space_coordinates_list:
        b_row, b_column = new_space
        if 0 <= b_row < len(map_game) and 0 <= b_column < len(map_game[0]):
            map_game[b_row][b_column] = SHIP_SYMBOLS["Miss"][0]

    return map_game


def map_show_ship_or_symbols(map_game, coordinates_list, alignment, map_with_gaps=True):
    """
    Deploy a ship or symbols on a 2D game map.

    This function modifies the 2D game map to show the ship or symbols
    at the specified coordinates and alignment.

    Args:
        map_game (list): The 2D map where the ship will be deployed.
        coordinates_list (list): List of coordinates where the ship is located.
        alignment (str): The alignment of the ship ("Horizontal" or "Vertical").
        map_with_gaps (bool): Whether to include gaps between ships on the map. Default is True.

    Global Variables:
        SHIP_SYMBOLS (dict): Dictionary containing ship symbols.
        DEFAULT_GAPS_BETWEEN_MAPS (bool): Default setting for gaps between ships.

    Returns:
        list: Modified 2D game map with the ship or symbols deployed.
    """

    # Use global variables for ship symbols and default gap settings
    global SHIP_SYMBOLS
    global DEFAULT_GAPS_BETWEEN_MAPS

    # If gaps are enabled, allocate empty space around the ship before deploying it
    if map_with_gaps:
        map_game = map_allocate_empty_space_for_ship(map_game, coordinates_list)

    # Case for single-cell ships
    if len(coordinates_list) == 1:
        row, column = coordinates_list[0]
        map_game[row][column] = SHIP_SYMBOLS[alignment][0]
        return map_game

    # Case for multi-cell ships
    else:
        row, column = coordinates_list[0]
        map_game[row][column] = SHIP_SYMBOLS[alignment][0]

        # Loop through the rest of the coordinates to place the ship symbols
        for cell in range(1, len(coordinates_list)):
            row, column = coordinates_list[cell]
            map_game[row][column] = SHIP_SYMBOLS[alignment][1]

        return map_game


def map_show_only_ships(map_game):
    """
    Replace 'Miss' symbols on the game map with the default symbol.

    This function goes through each cell in the 2D game map and replaces
    any 'Miss' symbols with the default symbol, effectively showing only ships
    on the map.

    Args:
        map_game (list): The 2D game map to be modified.

    Global Variables:
        SHIP_SYMBOLS (dict): Dictionary containing the symbols for different ship states.
        DEFAULT_SYMBOL (str): The symbol representing an empty cell on the map.

    Returns:
        list: The modified 2D game map with only ship symbols.
    """

    # Use global variables for ship symbols and the default symbol
    global SHIP_SYMBOLS, DEFAULT_SYMBOL

    # Loop through each row in the 2D game map
    for row in range(len(map_game)):
        # Loop through each column in the current row
        for column in range(len(map_game[0])):
            # If the current cell contains a 'Miss' symbol, replace it with the default symbol
            if map_game[row][column] == SHIP_SYMBOLS["Miss"][0]:
                map_game[row][column] = DEFAULT_SYMBOL

    return map_game


""" Game logic functions:
----------------------"""

def search_map_for_pattern(map_game, height, width):
    """
    Search for occurrences of a pattern of DEFAULT_SYMBOL on the map and return their coordinates.

    This function iterates through the game map to find all occurrences of a pattern
    of DEFAULT_SYMBOL of the specified height and width. The coordinates of the top-left
    corner of each found pattern are returned.

    Args:
        map_game (List[List[str]]): The 2D game map.
        height (int): The height of the pattern to search for.
        width (int): The width of the pattern to search for.

    Global Variables:
        DEFAULT_SYMBOL (str): The default symbol representing an empty cell on the map.

    Returns:
        List[Tuple[int, int]]: A list of coordinates (row, col) where the pattern is found.
                               Returns an empty list if no pattern is found.
    """

    # Reference the global variable for the default symbol
    global DEFAULT_SYMBOL

    # Retrieve the dimensions of the game map
    map_height, map_width = len(map_game), len(map_game[0])

    # Initialize an empty list to collect coordinates where the pattern is found
    coordinates = []

    # Create the pattern using list comprehension
    pattern = [[DEFAULT_SYMBOL] * width for _ in range(height)]

    # Traverse the map to find matching patterns
    for row in range(map_height - height + 1):
        for col in range(map_width - width + 1):
            # Check if the section of the map matches the pattern
            if all(
                map_game[row + i][col + j] == pattern[i][j]
                for i in range(height)
                for j in range(width)
            ):
                # If the pattern matches, add the coordinates to the list
                coordinates.append((row, col))

    return coordinates  # Return the list of coordinates where the pattern is found


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

    # Initialize an empty dictionary to store available ships
    available_ships = {}
    # Loop through each ship in the fleet
    for ship_name, ship_info in fleet.items():

        # Check if the ship has a quantity greater than zero
        if ship_info["Quantity"] > 0:
            # If so, add it to the available_ships dictionary
            available_ships[ship_name] = ship_info

    # Check if any ships are available
    if not available_ships:
        return None

    # Find the biggest ship based on the 'Size' value in the dictionary
    biggest_ship = max(available_ships,
                       key=lambda ship: available_ships[ship]["Size"])

    # Retrieve the size of the biggest ship
    biggest_ship_size = available_ships[biggest_ship]["Size"]

    # Return a tuple containing the name and size of the biggest ship
    return biggest_ship, biggest_ship_size


def map_search_reduce_width(height, width, map_game):
    """
    Reduce the width dimension and search for the pattern again.

    This function attempts to find a pattern of DEFAULT_SYMBOL on the game map with
    given dimensions. If not found, it reduces the width by 1 and tries again.
    If it still doesn't find any, it reduces both height and width by 1.

    Args:
        height (int): The height of the pattern to search for.
        width (int): The width of the pattern to search for.
        map_game (List[List[str]]): The 2D game map.

    Returns:
        Tuple: Returns the final height, width, and coordinates where the pattern is found.
    """

    # Reduce the width by 1
    width -= 1
    # Search for the pattern with the new dimensions
    coordinates = search_map_for_pattern(map_game, height, width)

    # If no coordinates were found
    if not coordinates:
        # Restore the width back to the original value
        width += 1
        # Decrease the height by 1
        height -= 1

        # Search for the pattern again with the new dimensions
        coordinates = search_map_for_pattern(map_game, height, width)

        # If still no coordinates were found
        if not coordinates:
            # Now reduce both height and width by 1
            width -= 1

    return height, width, coordinates  # Return the final height, width, and found coordinates



def map_search_reduce_height(height, width, map_game):
    """
    Reduce the height dimension and search for the pattern again.

    This function attempts to find a pattern of DEFAULT_SYMBOL on the game map with
    given dimensions. If not found, it reduces the height by 1 and tries again.
    If it still doesn't find any, it reduces both height and width by 1.

    Args:
        height (int): The height of the pattern to search for.
        width (int): The width of the pattern to search for.
        map_game (List[List[str]]): The 2D game map.

    Returns:
        Tuple: Returns the final height, width, and coordinates where the pattern is found.
    """

    # Reduce the height by 1
    height -= 1
    # Search for the pattern with the new dimensions
    coordinates = search_map_for_pattern(map_game, height, width)

    # If no coordinates were found
    if not coordinates:

        # Restore the height back to the original value
        height += 1
        # Decrease the width by 1
        width -= 1

        # Search for the pattern again with the new dimensions
        coordinates = search_map_for_pattern(map_game, height, width)

        # If still no coordinates were found
        if not coordinates:
            # Now reduce both height and width by 1
            height -= 1

    return height, width, coordinates  # Return the final height, width, and found coordinates




def cpu_choose_shooting_coordinates_biggest_ship(fleet_to_search, map_game):
    """
    Choose shooting coordinates for the CPU based on the biggest ship in the fleet.

    Args:
        fleet_to_search (dict): List of ships in the fleet.
        map_game (list): The map to search for shooting coordinates.

    Returns:
        tuple: The chosen shooting coordinates (coordinateX, coordinateY).
    """

    # Declare global variables used in the function
    global DEFAULT_SYMBOL, game_result

    # Initialize variables
    width = ""
    # Find the biggest ship in the fleet
    ship_name, ship_size = find_biggest_ship_in_fleet(fleet_to_search)

    # Check if there are any ships left in the fleet
    if ship_name is None:
        game_result = False
    else:
        # Calculate the initial pattern dimensions based on the biggest ship
        width = ship_size * 2 - 1
        height = ship_size * 2 - 1

        # Attempt to find the pattern in the map
        coordinates = search_map_for_pattern(map_game, height, width)

        # If no suitable coordinates are found, enter a loop to adjust the pattern
        if not coordinates:
            while not coordinates:

                # Try searching again with the current pattern dimensions
                coordinates = search_map_for_pattern(map_game, height, width)

                # Break the loop if coordinates are found
                if coordinates:
                    break

                # Randomly choose which dimension to reduce
                reduction = random.choice(["height", "width"])

                # Reduce the height and search again
                if reduction == "height":
                    height, width, coordinates = map_search_reduce_height(height, width, map_game)

                # Reduce the width and search again
                if reduction == "width":
                    height, width, coordinates = map_search_reduce_width(height, width, map_game)

                # Various exit conditions for the loop
                if (height < ship_size and width <= 1) or (height <= 1 and width < ship_size) or (height < 1 or width < 1):
                    break

        # Randomly choose from the found coordinates
        chosen_coordinates = random.choice(coordinates)

        # Validate the format of the chosen coordinates
        if len(chosen_coordinates) != 2:
            return None, None  # Handle error case

        # Extract the row and column from the chosen coordinates
        coord_row, coord_column = chosen_coordinates

        # Calculate the middle point of the pattern
        middle_width = (width // 2) + random.choice([1, width % 2]) - 1
        middle_height = (height // 2) + random.choice([1, height % 2]) - 1

        # Calculate the final shooting coordinates based on the middle point
        coordinate_column = coord_column + middle_width
        coordinate_row = coord_row + middle_height

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


def cpu_deploy_all_ships(map_game, fleet, gaps_on_map):
    """
    Deploy all CPU ships on the map.

    This function deploys all the CPU's ships on a given game map based on the fleet
    configuration. It uses various helper functions to find suitable locations and alignments
    for each ship.

    Args:
        map_game (list): 2D map for the CPU.
        fleet (dict): Contains the CPU's fleet information.
        gaps_on_map (bool): If True, adds gaps between ships.


    Global Variables:
        DEFAULT_SYMBOL (str): Default symbol for empty cells.
        SHIP_SYMBOLS (dict): Dictionary containing ship symbols.

    Returns:
        tuple: Updated map_game and fleet with the ship coordinates.
    """

    # Declare global variables for function access
    global DEFAULT_SYMBOL, SHIP_SYMBOLS

    # Initialize the map with default symbols if not already done

    # Creating empty list for ship coordinates, which will be appended to fleet later
    ship_coordinates = []
    result = ""
    # Iterate through each ship type in the fleet configuration
    for ship_name, ship_info in fleet.items():
        quantity = ship_info["Quantity"]  # Number of ships of this type
        size = ship_info["Size"]  # Size of this type of ship

        # Deploy the required number of each ship type
        for _ in range(quantity):
            # Variables to keep track of the ship's location and alignment
            location = ""

            # Handle single-cell ships
            if size == 1:
                alignment = "Single"
                result = search_map_for_pattern(map_game, 1, 1)
                if not result:
                    return False  # Abort if no suitable location is found

            else:
                # Randomly choose alignment for multi-cell ships
                alignment = random.choice(["Horizontal", "Vertical"])

                # Find a suitable location based on the alignment
                # Try vertical alignment first
                if alignment == "Vertical":
                    result = search_map_for_pattern(map_game, size, 1)
                    if not result:  # If not found, try horizontal
                        alignment = "Horizontal"
                        result = search_map_for_pattern(map_game, 1, size)
                        if not result:
                            return False  # Abort if no suitable location is found

                # Try horizontal alignment
                elif alignment == "Horizontal":
                    result = search_map_for_pattern(map_game, 1, size)
                    if not result:  # If not found, try vertical
                        alignment = "Vertical"
                        result = search_map_for_pattern(map_game, size, 1)
                        if not result:
                            return False  # Abort if no suitable location is found

            # Choose a random suitable location
            location = random.choice(result)

            if len(location) == 2:
                # Deploy the ship at the chosen location
                coordinates_list = create_coordinate_list(location[0], location[1], alignment, size)
                map_show_ship_or_symbols(map_game, coordinates_list, alignment, gaps_on_map)

                # Append ship coordinates to the fleet
                fleet[ship_name]["Coordinates"].append(coordinates_list)

            if len(location) < 2:
                return False  # Abort if no suitable location is found

    # Finalize the map by showing only the ships
    map_game = map_show_only_ships(map_game)

    return map_game, fleet  # Return the updated map and fleet




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
    action_outcome = f'{player} performed shot on coordinates {row} and {column} and it was a MISS'

    # Log the miss action into the game actions log
    game_actions_log.append([player, timer, row, column, action_outcome])

    # Update the hidden map at the given row and column to mark the miss
    # Use the symbol designated for "Miss" in the SHIP_SYMBOLS dictionary
    map_hidden[row][column] = SHIP_SYMBOLS["Miss"][0]

    # Update the display map at the given row and column to mark the miss
    # Use the symbol designated for "Miss" in the SHIP_SYMBOLS dictionary
    map_display[row][column] = SHIP_SYMBOLS["Miss"][0]

    return map_hidden, map_display




def action_perform_shoot(player, map_hidden, map_display, row, column, fleet,
                         cpu_shot_log_tmp):
    """
    Perform a shooting action on the game board.

    This function performs the action of shooting at a given coordinate on the game board.
    It uses helper functions to update the map and fleet information based on whether the
    shot hit a ship or missed.

    Args:
        player (str): The player who is performing the action.
        row (int): The row coordinate for the shot.
        column (int): The column coordinate for the shot.
        map_hidden (list): The 2D hidden map.
        map_display (list): The 2D display map.
        fleet (dict): Dictionary containing fleet information.
        cpu_shot_log_tmp (list): Temporary log for CPU shots.

    Global Variables:
        game_actions_log (list): Log of game actions.
        start_time (datetime): The start time of the game.
        SHIP_SYMBOLS (dict): Dictionary containing ship symbols.

    Returns:
        - fleet_target: Dictionary holding information about the CPU's fleet.
        - map_hidden: Hidden map here we perform search and shoot
        - map_display: Display map if shoot is success, then display hit or miss

    """

    # Declare global variables for function access
    global game_actions_log, start_time, SHIP_SYMBOLS

    # Find the ship details at the given coordinates
    ship_name, ship_size, coordinates_list, coordinates_set_id, coordinates_id = find_ship_and_coordinates(fleet, [row, column])

    try:
        # If a ship is found at the coordinates
        if ship_name:
            # Handle the logic for a hit ship
            map_hidden, map_display, fleet = handle_ship_hit(player, row, column, map_hidden, map_display, fleet,
                            ship_name, ship_size, coordinates_list, coordinates_set_id, coordinates_id, cpu_shot_log_tmp)
            return map_hidden, map_display, fleet

        else:  # If no ship was found at the coordinates
            # Handle the logic for a missed shot
            map_hidden, map_display = handle_miss(player, row, column, map_hidden, map_display)
            return map_hidden, map_display, fleet

    except Exception as e:  # Handle exceptions gracefully
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs


def handle_ship_hit(player, row, column, map_hidden, map_display, fleet,
                     ship_name, ship_size, coordinates_list, coordinates_set_id, coordinates_list_id, cpu_shot_log_tmp):
    """
    Handle the logic when a ship is hit.

    This function takes care of updating the game state when a ship is hit.
    It updates the map, checks if a ship is sunk, and logs the action.

    Args:
        player (str): The player making the shot ("CPU" or "Human").
        row (int): The row-coordinate of the shot.
        column (int): The column-coordinate of the shot.
        map_hidden (list): The hidden map that tracks shots.
        map_display (list): The displayed map that shows ships.
        fleet (dict): Information about the fleet of ships.
        ship_name (str): Name of the ship that was hit.
        ship_size (int): Size of the ship that was hit.
        coordinates_list (list): List of coordinates of the ship.
        coordinates_set_id (int): Index of the coordinate set in the fleet.
        coordinates_list_id (int): Index of the coordinate in the coordinate set.
        cpu_shot_log_tmp (list): Temporary log for CPU actions.

    Global Variables:
        game_actions_log (list): Log of game actions.
        start_time (float): The game start time for logging.
        SHIP_SYMBOLS (dict): Symbols used for different states of the ship.

    Returns:
        - fleet_target: Dictionary holding information about the CPU's fleet.
        - map_hidden: Hidden map here we perform search and shoot
        - map_display: Display map if shoot is success, then display hit or miss
    """

    # Declare global variables for logging and timing
    global game_actions_log, start_time, SHIP_SYMBOLS

    # Calculate the elapsed time since the game started
    timer = time.time() - start_time

    # Update the hidden and display maps to indicate a hit
    map_hidden[row][column] = SHIP_SYMBOLS["Hit"][0]
    map_display[row][column] = SHIP_SYMBOLS["Hit"][0]

    # Log the action in the global game actions log
    log_text = f'{player} performed shot on coordinates {row} and {column} and it was a HIT. Some Ship Damaged'
    game_actions_log.append([player, timer, row, column, log_text])

    # If the player is the CPU, append the shot to the CPU's temporary shot log
    if player == "CPU":
        cpu_shot_log_tmp.append([row, column])

    # Initialize the ship_sunk flag as False
    ship_sunk = False

    # Determine the alignment of the ship
    alignment, coordinates_index = find_first_ship_alignment(coordinates_list)

    # Check if the ship is sunk
    for coord in coordinates_list:
        r, c = coord
        if map_hidden[r][c] != SHIP_SYMBOLS["Hit"][0]:
            ship_sunk = False
            break
        ship_sunk = True

    # If the ship is sunk, handle additional logic
    if ship_sunk:
        alignment += "Sunk"
        map_hidden, map_display, fleet = handle_ship_sunk(map_hidden,
                                                          map_display, player,
                                                          fleet, ship_name, row,
                                                          column, ship_size,
                                                          alignment,
                                                          coordinates_list,
                                                          coordinates_set_id,
                                                          coordinates_list_id,
                                                          cpu_shot_log_tmp)
    return map_hidden, map_display, fleet


def handle_ship_sunk(map_hidden, map_display, player, fleet, ship_name,
                     ship_size, row, column, alignment, coordinates_list,
                     coordinates_set_id, coordinates_list_id, cpu_shot_log_tmp,
                     gaps_on_map=True):
    """
    Handle actions and updates for when a ship is sunk.

    This function updates the game state when a ship is sunk, including updating the map,
    the fleet, and various logs.

    Args:
        player (str): The player who sunk the ship ("CPU" or "Human").
        fleet (dict): The current fleet information.
        ship_name (str): The name of the ship that was sunk.
        ship_size (int): The size of the ship.
        coordinates_list (list): The list of coordinates of the ship.
        coordinates_set_id (int): The ID of the coordinate set in the fleet.
        coordinates_list_id (int): The ID of the coordinates in the coordinate set.
        map_display (list): The displayed map.
        map_hidden (list): The hidden map.
        cpu_shot_log_tmp (list): Temporary log of CPU actions.
        alignment (str): The alignment of the ship ("Horizontal" or "Vertical").
        gaps_on_map (bool): Flag to indicate if gaps are allowed on the map.


    Global Variables:
        start_time (float): Game start time for logging.
        SHIP_SYMBOLS (dict): Symbols for different ship states.
        game_actions_log (list): Log of game actions.
        game_result (str): The result of the game ("Game Over" or None).

    Returns:
        - fleet_target: Dictionary holding information about the CPU's fleet.
        - map_hidden: Hidden map here we perform search and shoot
        - map_display: Display map if shoot is success, then display hit or miss
    """
    # Declare global variables for logging and timing
    global start_time, SHIP_SYMBOLS, game_actions_log, game_result

    # Update the display and hidden maps to reflect the sunk ship
    map_show_ship_or_symbols(map_display, coordinates_list, alignment, gaps_on_map)
    map_show_ship_or_symbols(map_hidden, coordinates_list, alignment, gaps_on_map)

    # Log the action of sinking the ship
    timer = time.time() - start_time
    action_outcome = f'{player} performed shot on coordinates {row} and {column} and {ship_name} was SUNK'
    game_actions_log.append([player, timer, coordinates_list[0][0], coordinates_list[0][1], action_outcome])

    # If the player is the CPU, update its temporary shot log
    if player == "CPU":
        cpu_shot_log_tmp = update_cpu_shot_log(coordinates_list, cpu_shot_log_tmp)

    # Remove the sunk ship's coordinates from the fleet
    remove_coordinates_from_fleet(fleet, ship_name, coordinates_set_id)

    # Check for game over condition
    if not fleet:
        timer = time.time() - start_time
        game_actions_log.append([player, timer, coordinates_list[0][0], coordinates_list[0][1], "Game Over"])
        game_result = False
    return map_hidden, map_display, fleet





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

        # Remove the entire set of coordinates from the ship
        del fleet[ship_name]["Coordinates"][coordinates_list_set_id]

        # Remove any empty coordinate sets from the ship's list of coordinates
        fleet[ship_name]["Coordinates"] = [coords for coords in fleet[ship_name]["Coordinates"] if coords]

        # Reduce the quantity of this type of ship by 1
        fleet[ship_name]["Quantity"] -= 1

        # If the quantity of this type of ship reaches zero, remove it from the fleet
        if fleet[ship_name]["Quantity"] <= 0:
            del fleet[ship_name]

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
        return ('Single', 0)

    # Loop through each coordinate in the log for comparison
    for i, (row1, column1) in enumerate(coordinates_list):
        # Nested loop to compare the current coordinate with subsequent coordinates
        for j, (row2, column2) in enumerate(coordinates_list[i + 1:], start=i + 1):

            # If the rows are the same across two coordinates, it's horizontally aligned
            if row1 == row2:
                return ('Horizontal', i)
            # If the columns are the same across two coordinates, it's vertically aligned
            elif column1 == column2:
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
        for d_row, d_column in shifts:
            new_row, new_column = row + d_row, column + d_column

            # Check if the cell is within map boundaries and is untargeted
            if 0 <= new_row <= max_row and 0 <= new_column <= max_column:
                # Then check if the cell hasn't been shot at before
                if map_to_search[new_row][new_column] == DEFAULT_SYMBOL:
                    potential_shots.append([new_row, new_column])

        if len(potential_shots) > 0:
            break

    if len(potential_shots) == 0:
        shifts = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for coord in cpu_shot_log_tmp:
            row, column = coord
            for d_row, d_column in shifts:
                new_row, new_column = row + d_row, column + d_column
                # Check if the new coordinates are within map boundaries and haven't been shot at before
                if 0 <= new_row <= max_row and 0 <= new_column <= max_column:
                    # Then check if the cell hasn't been shot at before
                    if map_to_search[new_row][new_column] == DEFAULT_SYMBOL:
                        potential_shots.append([new_row, new_column])
                if len(potential_shots) > 0:
                    break
            if len(potential_shots) > 0:
                break
    # Randomly choose one of the potential shots if any are available
    if len(potential_shots) > 0:
        selected_row, selected_column = random.choice(potential_shots)
        return selected_row, selected_column

    # If no potential shots were found, return None, None
    return None, None




def cpu_move(map_hidden, map_display, fleet_target, cpu_shot_log_tmp):
    """
    Executes the CPU's move during the game.
    Args:
        - fleet_target: Dictionary holding information about the CPU's fleet.
        - map_hidden: Hidden map here we perform search and shoot
        - map_display: Display map if shoot is success, then display hit or miss
        - cpu_shot_log_tmp: Temporary log for the CPU's shots.


    Global Variables:
        - game_result: Holds the current state of the game ("Game Over" or None).

        - game_actions_log: Log for game actions.
        - start_time: Time when the game started.
        - SHIP_SYMBOLS: Dictionary holding symbols for different ship states.

    Returns:
        None
    """

    # Declare global variables accessed within the function
    global game_result
    global game_actions_log, start_time, SHIP_SYMBOLS

    # Identify the player as CPU for logging and action purposes

    player = "CPU"

    # Check if there are any damaged but not sunk ships in cpu_shot_log_tmp
    if len(cpu_shot_log_tmp) == 0:
        # If no damaged ships are found, choose coordinates based on the largest ship in the fleet
        row, column = cpu_choose_shooting_coordinates_biggest_ship(fleet_target, map_hidden)
        # Perform the shooting action and update the game state
        map_hidden, map_display, fleet = action_perform_shoot(player,
                                                              map_hidden,
                                                              map_display, row,
                                                              column,
                                                              fleet_target,
                                                              cpu_shot_log_tmp)
        return map_hidden, map_display, fleet

        # Check for game over condition
    else:
        # If damaged ships are found, focus on sinking them by selecting the best shot based on ship alignment
        row, column = select_best_shot_based_on_alignment(map_hidden, cpu_shot_log_tmp)
        # Perform the shooting action and update the game state
        map_hidden, map_display, fleet = action_perform_shoot(player,
                                                              map_hidden,
                                                              map_display, row,
                                                              column,
                                                              fleet_target,
                                                              cpu_shot_log_tmp)
        return map_hidden, map_display, fleet



"""Game Start Functions
---------------------"""


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
    global cpu_shot_log_tmp, game_actions_log, DEFAULT_SYMBOL, game_result

    # Clear terminal for a clean game start (assuming the function 'clear_terminal' exists)
    clear_terminal()

    # Print ASCII art
    #print_acid_effect()

    # Initializing game instructions
    height, width, fleet, gaps_on_map = game_instructions()

    # Creating Maps for player and CPU:
    map_cpu_hidden, map_cpu_display, fleet_cpu = (
        create_initial_game_variables(height, width, symbol, fleet))
    
    map_player_hidden, map_player_display, fleet_player = (
        create_initial_game_variables(height, width, symbol, fleet))

    #Now we will ask player to Deploy all ships:
    map_player_display, fleet_player = player_deploy_all_ships(
    map_player_display,map_player_hidden, fleet_player, gaps_on_map)

    """ temporary code so cpu deploys ships for player
    map_player_display, fleet_player = (
        cpu_deploy_all_ships(map_player_display, fleet_player, gaps_on_map))
        """

    # After all player ships are deployed, we will reset hidden map, so it is blank. This map will be attacked by CPU.
    map_player_hidden = create_map(height, width, DEFAULT_SYMBOL)
    map_player_display = map_show_only_ships(map_player_display)

    # CPU time to deploy its ships
    map_cpu_display, fleet_cpu = cpu_deploy_all_ships(map_cpu_display, fleet_cpu, gaps_on_map)

    # now creating loop for this current game
    game_result = True
    game_actions_log = [["Player", "Time", "Row", "Column", ""]]

    while True:
        if not game_result:
            break
        clear_terminal()
        if len(game_actions_log) > 1:
            print(game_actions_log[-2][4])
        print(game_actions_log[-1][4])
        print_two_maps(map_cpu_hidden, map_player_display, "CPU Map", "Player Map",
                       10)
        # Player goes first
        map_cpu_hidden, map_cpu_display, fleet_cpu = player_shoot_input(
            map_cpu_hidden, map_cpu_display, fleet_cpu)
        if not game_result:
            break
        map_player_hidden, map_player_display, fleet_player = cpu_move(
            map_player_hidden, map_player_display, fleet_player, cpu_shot_log_tmp)
        print_aligned_log(game_actions_log)
    print(game_actions_log[-1][4])






battleship_game_singe(DEFAULT_MAP_HEIGHT, DEFAULT_MAP_WIDTH, DEFAULT_SYMBOL,
 DEFAULT_FLEET, start_time, game_actions_log)

def cpu_vs_cpu():
    global DEFAULT_MAP_HEIGHT, DEFAULT_MAP_WIDTH, DEFAULT_SYMBOL, \
        DEFAULT_FLEET, cpu_shot_log_tmp, game_actions_log, DEFAULT_GAPS_BETWEEN_MAPS


    map_cpu_hidden, map_cpu_display, fleet_cpu = (
        create_initial_game_variables(DEFAULT_MAP_HEIGHT, DEFAULT_MAP_WIDTH,
                                      DEFAULT_SYMBOL,
                                      DEFAULT_FLEET))

    map_cpu_display, fleet_cpu = cpu_deploy_all_ships(map_cpu_display,
                                                      fleet_cpu, True)

    game_actions_log = [["Player", "Time", "Row", "Column", ""]]
    for i in range(100):
        clear_terminal()
        print(game_actions_log[-1][4])
        print_two_maps(map_cpu_hidden, map_cpu_display, "CPU Map", "Player "
                                                                   "Map", 10)
        map_cpu_hidden, map_cpu_display, fleet_cpu = cpu_move(map_cpu_hidden,
                                                              map_cpu_display,
                                                              fleet_cpu,
                                                              cpu_shot_log_tmp)


        # Player goes first




#cpu_vs_cpu()