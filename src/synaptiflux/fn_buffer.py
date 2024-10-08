"""Implement a function buffer."""
# Author: Garry Morrison
# Created: 2024-10-8
# Updated: 2024-10-8

class FnBuffer:
    """Implements a function buffer."""
    def __init__(self):
        self.fn_list = []
        self.params_list = []

    def __str__(self):
        s = f"\n    {len(self.fn_list)} functions in our function buffer:\n"
        for k in range(len(self.fn_list)):
            s += f"        fn: {self.fn_list[k]}\n"
            s += f"        params: {self.params_list[k]}\n\n"
        return s

    def append(self, fn, params):
        """Append a function and associated parameters to the buffer."""
        self.fn_list.append(fn)
        self.params_list.append(params)

    def erase(self):
        """Erase the buffer."""
        self.fn_list.clear()
        self.params_list.clear()

    def invoke(self):
        """Invoke our functions in order."""
        for k in range(len(self.fn_list)):
            fn = self.fn_list[k]
            params = self.params_list[k]
            fn(**params)


