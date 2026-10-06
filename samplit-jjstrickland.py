# HW1: Jessica Strickland
# Sampling Script

import random
import sys

# INSERTED RANDOM CHANGES

<<<<<<< HEAD
#TRIVIAL CHANGES ADDED OMG!
trivalchanges = hellothere

with open(filename, "r") as file:
=======
branch = hw_1b
filename1 = sys.argv[1] # stores filename

with open(filename1, "r") as file:
>>>>>>> hw_1b
    for line in file: # read file line by line
        if random.random() < 0.01: # output each line with a 1% probability
            print(line, end="") # prints sampled lines to standard output
