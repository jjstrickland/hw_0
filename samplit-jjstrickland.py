# HW1: Jessica Strickland
# Sampling Script

import random
import sys

# RESOLVED MERGE CONFLICTS
with open(filename, "r") as file:

filename1 = sys.argv[1] # stores filename

with open(filename1, "r") as file:
    for line in file: # read file line by line
        if random.random() < 0.01: # output each line with a 1% probability
            print(line, end="") # prints sampled lines to standard output
