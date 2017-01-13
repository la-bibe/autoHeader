#!/usr/bin/python3

import sys
import os
import re

output = "include/"
includeFile = "includes.config"

class colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    DEFAULT = "\033[0m"

def error_args():
    print(colors.RED + "Incorrect number of arguments" + colors.DEFAULT)
    sys.exit(84)

def error_file(name):
    print(colors.RED + "Error while opening the file: \"" + name + "\"" + colors.DEFAULT)

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
includes = {}

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
        file = open(fileName, "r")
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
print ("Creating the output folder")
if not os.path.exists(output):
    os.makedirs(output)
print ("Opening the " + includeFile + " file")
try:
    config = open(includeFile, "r")
    data = config.read()
    config.close()
    data = cregSpaces.sub("", data)
    sepInc = data.split("-")
    for inc in sepInc:
        inc = inc.split(":")
        includes[inc[0]] = inc[1]
except:
    print (colors.YELLOW + "Warning: no config file found, you should add one" + colors.DEFAULT)
print ("Creating the files")
for fileName, funcs in usedFuncsPerFile.items():
    if funcs:
        tempName = output + fileName.split("/")[-1].replace(".c", ".h")
        print ("Creating \"" + tempName + "\"")
        file = open(tempName, "w")
        addDblIncSec(file, tempName)
        neededIncludes = []
        for func in funcs:
            if not func in functionNames:
                found = 0
                for key, value in includes.items():
                    if func in value.split(";"):
                        found = 1
                        if key != "void":
                            neededIncludes.append(key)
                if found == 0:
                    print (colors.YELLOW + "Warning: function \"" + func + "\" not found in the config file" + colors.DEFAULT)
        neededIncludes = list(set(neededIncludes))
        for inc in neededIncludes:
            file.write("#  include <" + inc + ">\n")
        if neededIncludes:
            file.write("\n")
        for func in funcs:
            if func in functionNames:
                file.write(functions[functionNames.index(func)] + ";\n")

        file.write("\n#endif")
        file.close()
print ("Done")
