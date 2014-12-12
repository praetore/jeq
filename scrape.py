#!/usr/bin/env python3
__author__ = 'darryl'

import fileinput
with fileinput.input() as f_input:
    for line in f_input:
        print(line, end='')