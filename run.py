# battleship.py test.py - this code is for testing CPU vs CPU game

# Import required libraries
import random  # For generating random numbers
import copy  # For creating deep copies of data structures
import os  # For clearing the terminal screen
import time  # For time-related functionalities
from typing import List, Tuple  # For type hinting


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



