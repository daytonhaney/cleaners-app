#!/usr/bin/env python3
"""Cleaning service text/ascii"""

import os
import shutil

_txt_ = shutil.get_terminal_size().columns
cols, rows = shutil.get_terminal_size()


def centered_text(txt):
    """prints types to center termianl"""

    cols = shutil.get_terminal_size().columns
    print(txt.center(cols))


def return_centered_input(name):
    """returns any input() type to center terminal"""

    cols = shutil.get_terminal_size().columns
    name = input()
    return name.center(cols), name


def centered_input(prompt):
    """gets input() from centered terminal"""

    twidth = shutil.get_terminal_size().columns
    prompt_destination = (twidth - len(prompt)) // 2
    print(" " * prompt_destination + prompt, end="", flush=True)
    user_input = input()
    return user_input


def center_daily_info(txt):
    """center daily info"""

    twidth, _ = shutil.get_terminal_size()
    pad_left = (twidth - len(txt)) // 2
    print(" " * pad_left + txt)


def center_cash_earned(final_total: str):
    """left center total cash earned"""

    twidth, _ = shutil.get_terminal_size()
    pad_left = (twidth - len(final_total)) // 2 + 36
    print(" " * pad_left + final_total)


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
