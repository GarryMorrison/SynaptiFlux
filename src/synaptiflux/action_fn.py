"""Define some toy actions."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

def action_null(value):
    """Do nothing action."""
    return

def action_println(value, s):
    """Print string action, with new line, if value > 0."""
    if value > 0:
        print(s)

def action_print(value, s):
    """Print string action, without new line, if value > 0."""
    if value > 0:
        print(s, end='')


