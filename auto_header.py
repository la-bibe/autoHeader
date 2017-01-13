#!/usr/bin/python3

import sys
import re

def error_args():
    print("Incorrect number of arguments")
    sys.exit(84)

def error_file(name):
    print("Error while opening the file: \"" + name + "\"")

# Check arguments
if len(sys.argv) < 2:
    error_args()

# Try to open the file

# Regexes
regFunFull = "^[A-Za-z0-9_]+[ \t\*]+[A-Za-z0-9_]+\(([A-Za-z0-9_]*[ \*]*[A-Za-z0-9_]*,[ \*\n\t]*)*([A-Za-z0-9_]*[ \*]*[A-Za-z0-9_]*)?\)$"
cregArgNameComma = re.compile("[ ]*[A-Za-z0-9_]+,")
cregArgNamePar = re.compile("[ ]*[A-Za-z0-9_]+\)")
cregSpaces = re.compile("[ \n\t]+")
cregSpace = re.compile(" ")

functions = []

def addFunction(function):
    function = cregArgNameComma.sub(",", function)
    function = cregArgNamePar.sub(")", function)
    function = cregSpaces.sub(" ", function)
    functions.append(function)

def alignFunctions():
    maxLen = 0
    for func in functions:
        length = len(func.split(" ")[0])
        if length > maxLen:
            maxLen = length
    maxLen += 1
    for (i, func) in enumerate(functions):
        length = len(func.split(" ")[0])
        functions[i] = cregSpace.sub(" " * (maxLen - length), func, 1)

fileNames = iter(sys.argv)
next(fileNames)
for fileName in fileNames:
    try:
        file = open(fileName, 'r')
        data = file.read()
        print ("Analysing \"" + fileName + "\"")
        for test in re.finditer(regFunFull, data, re.M):
            addFunction(test.group())
    except:
        error_file(fileName)

print ("Aligning the functions")
alignFunctions()
print ("\nDone :")
print ('\n'.join(functions))
