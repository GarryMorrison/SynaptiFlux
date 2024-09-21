"""Define some sources."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

def source_off():
    """Always return 0."""
    while True:
        yield 0

def source_on():
    """Always return 1."""
    while True:
        yield 1

def source_init():
    """Initial spike, then 0's after."""
    yield 1
    while True:
        yield 0

def source_init_N(N):
    """Initially 0 for N steps, then a spike, then 0's after."""
    for _ in range(N):
        yield 0
    yield 1
    while True:
        yield 0

def source_alt_2():
    """Alternate between 1 and 0."""
    n = 0
    while True:
        yield 1 if n % 2 == 0 else 0
        n += 1

def source_alt_N(N):
    """Alternate between 1 and 0 with mod N."""
    n = 0
    while True:
        yield 1 if n % N == 0 else 0
        n += 1


