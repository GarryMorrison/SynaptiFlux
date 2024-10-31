"""Implement a simple counter."""
# Author: Garry Morrison
# Created: 2024-10-31
# Updated: 2024-10-31

class Counter:
    """Implements a simple counter."""
    def __init__(self):
        self.counter = 0

    def get(self):
        """Get the value of the counter."""
        return self.counter

    def set(self, n):
        """Set the value of the counter."""
        self.counter = n

    def reset(self):
        """Reset the counter to zero."""
        self.counter = 0

    def increment(self):
        """Increment the counter by one."""
        self.counter += 1


