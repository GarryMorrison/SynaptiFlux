"""Implement a string buffer."""
# Author: Garry Morrison
# Created: 2024-9-29
# Updated: 2024-9-29

class Buffer:
    """Implements a string buffer."""
    def __init__(self, s1):
        self.s = s1

    def __str__(self):
        return self.s

    def append(self, s2):
        """Append a string to the buffer."""
        self.s += s2

    def unappend(self, s2):
        """Unappend a string to the end of the buffer if it has that suffix."""
        if self.s.endswith(s2):
            self.s = self.s[:-len(s2)]

    def erase(self):
        """Erase the buffer."""
        self.s = ""
