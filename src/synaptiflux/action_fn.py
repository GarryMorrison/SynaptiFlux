"""Define some toy actions."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-29

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

def action_print_to_buffer(value, buffer, s):
    """Append the given string to the given buffer, if value > 0."""
    if value > 0:
        buffer.append(s)

def action_print_to_buffer_flush(value, buffer, s):
    """Append the given string to the given buffer, then print the buffer, if value > 0."""
    if value > 0:
        buffer.append(s)
        print(buffer)
        buffer.erase()


