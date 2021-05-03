# This code is written by Jiali Liang to make Christians lives
# much eaiser when searching bible verses. This is part of the whole code
#
import pandas as pd
import numpy as np


# For the simplicity of search engine, 1_kings -> 1_Kings,etc.
# and Song of Songs = Song_of_Songs

# Input: A book name either in English or Chinese, abbreviated or not
# Output 1: abbreviated book name in chinese (output == 'zh')
# Output 2: Full book name in English (output == 'EN')
def CVT(element,output="zh"):
    # Make sure not to confused with other book names.
    element = " "+ element
    table = open("acronym.txt","r+")
    for line in table:
        if element in line:
            if output == "zh":
                return str.split(line)[1]
            elif output == "EN":
                return str.split(line)[2]
    return element
