#!/usr/bin/python3

import sys
import os
import re

output = "output/"

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
        file.close()
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

def addDblIncSec(file, name):
    name = name.split("/")[-1].upper().replace(".", "_") + "_"
    file.write("#ifndef " + name + "\n" + "#  define " + name + "\n\n")

fileNames = iter(sys.argv)
next(fileNames)
for fileName in fileNames:
    if (fileName.endswith(".c")):
        analizeFile(fileName)

print ("Aligning the functions")
alignFunctions()
print ("Done")
print ("Creating the output folder")
if not os.path.exists(output):
    os.makedirs(output)
print ("Creating the files")
for fileName, funcs in usedFuncsPerFile.items():
    if funcs:
        tempName = output + fileName.split("/")[-1].replace(".c", ".h")
        print ("Creating \"" + tempName + "\"")
        file = open(tempName, "w")
        addDblIncSec(file, tempName)
        for func in funcs:
            if func in functionNames:
                file.write(functions[functionNames.index(func)] + ";\n")
        file.write("\n#endif")
        file.close()
