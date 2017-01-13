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
regFunCalled = "[A-Za-z0-9_]+\("
cregArgNameComma = re.compile("[ ]*[A-Za-z0-9_]+,")
cregArgNamePar = re.compile("[ ]*[A-Za-z0-9_]+\)")
cregSpaces = re.compile("[ \n\t]+")
cregSpace = re.compile(" ")

functions = []
functionNames = []
usedFuncsPerFile = {}

def addFunction(function):
    function = cregArgNameComma.sub(",", function)
    function = cregArgNamePar.sub(")", function)
    function = cregSpaces.sub(" ", function)
    functions.append(function)
    name = function.split(" ")[1].split("(")[0].replace("*", "")
    functionNames.append(name)
    return (name)

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

def analizeFile(fileName):
    print ("Analysing \"" + fileName + "\"")
    try:
        file = open(fileName, 'r')
        data = file.read()
    except:
        error_file(fileName)
        return
    localDefinedFuncs = []
    for function in re.finditer(regFunFull, data, re.M):
        localDefinedFuncs.append(addFunction(function.group()))
    localUsedFuncs = []
    for function in re.finditer(regFunCalled, data, re.M):
        localUsedFuncs.append(function.group().replace("(", ""))
    localUsedFuncs = list(set(localUsedFuncs))
    for function in localDefinedFuncs:
        localUsedFuncs.remove(function)
    usedFuncsPerFile[fileName] = localUsedFuncs


fileNames = iter(sys.argv)
next(fileNames)
for fileName in fileNames:
    if (fileName.endswith(".c")):
        analizeFile(fileName)

print ("Aligning the functions")
alignFunctions()
print ("Done")
print ("\nPrototypes:\n")
print ('\n'.join(functions))
print ("\nNames:\n")
print ('\n'.join(functionNames))
print ("\nDefinition of needs for each file:")
for file, funcs in usedFuncsPerFile.items():
    print ("\n");
    print (file + ":");
    for func in funcs:
        if func in functionNames:
            print ("Defined:\t" + functions[functionNames.index(func)])
        else:
            print ("Not defined:\t" + func)
