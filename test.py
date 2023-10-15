def cpu_move(fleet_target, map_hidden, map_display, cpu_shot_log_tmp):
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
        - fleet_target: Dictionary holding information about the CPU's fleet.
        - map_hidden: Hidden map here we perform search and shoot
        - map_display: Display map if shoot is success, then display hit or miss
    """

    # Declare global variables accessed within the function
    global game_actions_log, start_time, SHIP_SYMBOLS, game_result


    # Identify the player as CPU for logging and action purposes
    player = "CPU"

    # Check if there are any damaged but unsunk ships in cpu_shot_log_tmp
    if len(cpu_shot_log_tmp) == 0:
        # If no damaged ships are found, choose coordinates based on the largest ship in the fleet
        row, column = cpu_choose_shooting_coordinates_biggest_ship(fleet_target, map_hidden)
        # Perform the shooting action and update the game state
        map_hidden, map_display, fleet = action_perform_shoot(player, row, column, map_hidden, map_display, fleet_target, cpu_shot_log_tmp)
        return map_hidden, map_display, fleet

        # Check for game over condition
    else:
        # If damaged ships are found, focus on sinking them by selecting the best shot based on ship alignment
        row, column = select_best_shot_based_on_alignment(map_hidden, cpu_shot_log_tmp)
        # Perform the shooting action and update the game state
        map_hidden, map_display, fleet = action_perform_shoot(player, row, column, map_hidden, map_display, fleet_target, cpu_shot_log_tmp)
        return map_hidden, map_display, fleet