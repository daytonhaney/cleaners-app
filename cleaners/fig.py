#!/usr/bin/env python3
import os
import shutil


def centered_text(txt):
    """prints any type to the center of terminal"""

    cols = shutil.get_terminal_size().columns
    print(txt.center(cols))
    # return text.center(cols)


def return_centered_input(user_input):
    """returns any input() type to center terminal"""

    cols = shutil.get_terminal_size().columns
    user_input = input()
    return input(user_input.center(cols))


def io_figlets(t):
    """prints welcome title"""

    cols = shutil.get_terminal_size().columns
    lines = t.split("\n")
    max_line_length = max(len(line) for line in lines)

    pad_left = (cols - max_line_length) // 2
    for line in lines:
        print(" " * pad_left + line)


io_figlets_title = """
    
     ___          ___      ___        _   
    |_ _|_ __    ( _ )    / _ \ _   _| |_ 
     | || '_ \   / _ \/\ | | | | | | | __|
     | || | | | | (_>  < | |_| | |_| | |_ 
    |___|_| |_|  \___/\/  \___/ \__,_|\__|
                                      
      ____ _                  _                ____                  
     / ___| | ___  __ _ _ __ (_)_ __   __ _   / ___|___  _ __ _ __   
    | |   | |/ _ \/ _` | '_ \| | '_ \ / _` | | |   / _ \| '__| '_ \  
    | |___| |  __/ (_| | | | | | | | | (_| | | |__| (_) | |  | |_) | 
     \____|_|\___|\__,_|_| |_|_|_| |_|\__, |  \____\___/|_|  | .__(_)
                                      |___/                  |_|     
    """


io_figlets(io_figlets_title)
