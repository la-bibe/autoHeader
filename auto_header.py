#!/usr/bin/python3

# #########################
# #      Auto Header      #
# #########################
# |Created by Fantin Bibas|
# |In 2017 Jan.           |
# |                       |
# | fantin@bib.as         |
# | www.bib.as            |
# +-----------------------+

import sys
import os
import re

configFile = "general.conf"
version = "0.4.2"

class colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[34m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    DEFAULT = "\033[0m"

def error_args():
    print (colors.RED + "Incorrect number of arguments" + colors.DEFAULT)
    print (colors.YELLOW + "Usage:\n\tauto_header.py [file.c]..." + colors.DEFAULT)
    sys.exit(84)

def error_file(name):
    print (colors.RED + "Error while opening the file: \"" + name + "\"" + colors.DEFAULT)

def showOk():
    print (colors.GREEN + " -> Ok" + colors.DEFAULT)

def showError():
    print (colors.YELLOW + " -> Error" + colors.DEFAULT)

def printRed(text):
    print (colors.RED + text + colors.DEFAULT)

def printGreen(text):
    print (colors.GREEN + text + colors.DEFAULT)

def printBlue(text):
    print (colors.BLUE + text + colors.DEFAULT)

def printYellow(text):
    print (colors.YELLOW + text + colors.DEFAULT)

def showHeader():
    os.system("clear")
    print ("  #########################################################  ")
    print (" ##" + colors.RED + "              _        _    _                _         " + colors.DEFAULT + "## ")
    print ("##" + colors.RED + "    /\        | |      | |  | |              | |         " + colors.DEFAULT + "##")
    print ("#" + colors.RED + "    /  \  _   _| |_ ___ | |__| | ___  __ _  __| | ___ _ __ " + colors.DEFAULT + "#")
    print ("#" + colors.RED + "   / /\ \| | | | __/ _ \|  __  |/ _ \/ _` |/ _` |/ _ \ '__|" + colors.DEFAULT + "#")
    print ("#" + colors.RED + "  / ____ \ |_| | || (_) | |  | |  __/ (_| | (_| |  __/ |   " + colors.DEFAULT + "#")
    print ("#" + colors.RED + " /_/    \_\__,_|\__\___/|_|  |_|\___|\__,_|\__,_|\___|_|   " + colors.DEFAULT + "#")
    print ("#                                                           #")
    print ("#############################################################")
    print ("#  " + colors.CYAN + "Created by Fantin Bibas                   fantin@bib.as" + colors.DEFAULT + "  #")
    print ("#               " + colors.CYAN + "\"Neodar\"" + colors.DEFAULT + "                                    #")
    print ("##                                                         ##")
    print (" ####                     " + colors.BLUE + "v. " + version + colors.DEFAULT + "                     #### ")
    print ("    ###########                               ###########    ")
    print ("              ###########           ###########              ")
    print ("                        #############                        ")

# Check arguments
if len(sys.argv) < 2:
    error_args()

# Regexes
regFunFull = "^[A-Za-z0-9_]+[ \t\*]+[A-Za-z0-9_]+\(([A-Za-z0-9_]*[ \*]*[A-Za-z0-9_\[\]]*,[ \*\n\t]*)*([A-Za-z0-9_]*[ \*]*[A-Za-z0-9_\[\]]*)?\)$"
regFunCalled = "[A-Za-z0-9_]+\("
regMacro = "[^A-Za-z0-9_][A-Z0-9_]*[A-Z]+[A-Z0-9_]*[^A-Za-z0-9_]"
regVariable = "[A-Za-z0-9_]+\**[ \t]+\**[A-Za-z0-9_]+"
cregArgNameComma = re.compile("[ ]*[A-Za-z0-9_]+,")
cregArgNamePar = re.compile("[ ]*[A-Za-z0-9_]+\)")
cregSpaces = re.compile("[ \n\t]+")
cregSpace = re.compile(" ")
cregExceptions = re.compile("(\"(.*?)\")|(\/\*(.*?)(\*\/))|(\/\/.*$)", re.M|re.S)

# Config
output = "include/"
includeFile = "functions.conf"
macroFile = "macros.conf"
typeFile = "types.conf"
binaryName = "a.out"
bLetArgNames = 0
bIncludeHeader = 1
bDoMakefile = 1
lineHeader = 10

# Arrays
functions = []
functionNames = []
usedFuncsMacsPerFile = {}
includes = {}
macros = {}
types = {}

def createMakefile():
    try:
        makefile = open("Makefile", "w")
        makefile.write("CC\t=\tgcc\n\n")
        makefile.write("RM\t=\trm -f\n\n")
        makefile.write("CPPFLAGS\t+=\t-I " + output + "\n\n")
        makefile.write("NAME\t=\t" + binaryName + "\n\n")
        makefile.write("SRCS\t=\t")
        for fileName in sorted(usedFuncsMacsPerFile.keys())[:-1]:
            makefile.write(fileName + "\t\\\n\t\t")
        makefile.write(sorted(usedFuncsMacsPerFile.keys())[-1] + "\n\n")
        makefile.write("OBJS\t=\t$(SRCS:.c=.o)\n\n")
        makefile.write("all:\t$(NAME)\n\n$(NAME):\t$(OBJS)\n\t$(CC) $(OBJS) -o $(NAME) $(FLAGS)\n\n")
        makefile.write("clean:\n\t$(RM) $(OBJS)\n\n")
        makefile.write("fclean:\tclean\n\t$(RM) $(NAME)\n\n")
        makefile.write("re:\tfclean all\n\n")
        makefile.write(".PHONY:\tall clean fclean re\n\n")
        makefile.close()
        showOk()
    except:
        showError()

def readConfig(): # Analyse the config file
    global output
    global includeFile
    global macroFile
    global bIncludeHeader
    global lineHeader
    global bDoMakefile
    global binaryName
    global bLetArgNames
    try:
        config = open(configFile, "r")
        data = config.read()
        config.close()
        data = cregSpaces.sub("", data)
        sepInc = data.split(";")
        for inc in sepInc:
            inc = inc.split(":")
            if inc[0] == "output":
                output = inc[1]
            elif inc[0] == "funcDictionnary":
                includeFile = inc[1]
            elif inc[0] == "macrDictionnary":
                macroFile = inc[1]
            elif inc[0] == "typeDictionnary":
                typeFile = inc[1]
            elif inc[0] == "include":
                bIncludeHeader = int(inc[1])
            elif inc[0] == "includeLine":
                lineHeader = int(inc[1])
            elif inc[0] == "makefile":
                bDoMakefile = int(inc[1])
            elif inc[0] == "binary":
                binaryName = int(inc[1])
            elif inc[0] == "argNames":
                bLetArgNames = int(inc[1])
    except:
        try:
            config = open(configFile, "w")
            config.write("output:" + output + ";\n")
            config.write("funcDictionnary:" + includeFile + ";\n")
            config.write("macrDictionnary:" + macroFile + ";\n")
            config.write("typeDictionnary:" + typeFile + ";\n")
            config.write("include:" + str(bIncludeHeader) + ";\n")
            config.write("includeLine:" + str(lineHeader) + ";\n")
            config.write("makefile:" + str(bDoMakefile) + ";\n")
            config.write("binary:" + str(binaryName) + ";\n")
            config.write("argNames:" + str(bLetArgNames) + ";\n")
            config.close()
        except:
            print (colors.YELLOW + "Warning couldn't create the config file." + colors.DEFAULT)

def addFunction(function): # Add the function to the dictionnary array of known functions
    if bLetArgNames == 0:
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
    print ("\tAnalysing \"" + fileName + "\"", end="")
    try:
        file = open(fileName, "r")
        data = file.read()
        file.close()
    except:
        showError()
        return
    data = cregExceptions.sub("", data)
    localDefinedFuncs = []
    for function in re.finditer(regFunFull, data, re.M):
        localDefinedFuncs.append(addFunction(function.group()))
    localUsedFuncs = []
    for function in re.finditer(regFunCalled, data, re.M):
        localUsedFuncs.append(function.group().replace("(", ""))
    for macro in re.finditer(regMacro, data, re.M): # Macro handling (yes I know i need to clean this)
        macro = macro.group()[1:-1]
        localUsedFuncs.append(macro)
    for variable in re.finditer(regVariable, data, re.M): # Variable type handling (same as ^^^^)
        variable = variable.group().split(" ")[0].split("\t")[0]
        localUsedFuncs.append(variable)
    localUsedFuncs = list(set(localUsedFuncs))
    for function in localDefinedFuncs:
        localUsedFuncs.remove(function)
    usedFuncsMacsPerFile[fileName] = localUsedFuncs
    if bIncludeHeader == 1:
        try:
            file = open(fileName, "r")
            data = file.readlines()
            file.close()
            name = "#include \"" + fileName.split("/")[-1].replace(".c", ".h\"\n")
            exists = 0
            for line in data:
                if line == name:
                    exists = 1
            if exists == 0:
                data.insert(lineHeader, name + "\n")
                file = open(fileName, "w")
                data = "".join(data)
                file.write(data)
                file.close()
        except:
            error_file(fileName)
    showOk()

def addDblIncSec(file, name):
    name = name.split("/")[-1].upper().replace(".", "_") + "_"
    file.write("#ifndef " + name + "\n" + "#  define " + name + "\n\n")


readConfig()

showHeader()
print (colors.GREEN + "\n-----------------------")
print ("---Start of analyzis---")
print ("-----------------------" + colors.DEFAULT)
fileNames = iter(sys.argv)
next(fileNames)
for fileName in fileNames:
    if (fileName.endswith(".c")):
        analizeFile(fileName)
print (colors.GREEN + "\n-----------------------")
print ("--- End of analyzis ---")
print ("-----------------------\n" + colors.DEFAULT)

alignFunctions()
print ("Creating the output folder", end="")
if not os.path.exists(output):
    os.makedirs(output)
showOk()

# Open conf files
print ("Opening \"" + includeFile + "\"", end="")
try:
    config = open(includeFile, "r")
    data = config.read()
    config.close()
    data = cregSpaces.sub("", data)
    sepInc = data.split("-")
    for inc in sepInc:
        inc = inc.split(":")
        includes[inc[0]] = inc[1]
    showOk()
except:
    showError()
print ("Opening \"" + macroFile + "\"", end="")
try:
    config = open(macroFile, "r")
    data = config.read()
    config.close()
    data = cregSpaces.sub("", data)
    sepInc = data.split("-")
    for inc in sepInc:
        inc = inc.split(":")
        macros[inc[0]] = inc[1]
    showOk()
except:
    showError()
print ("Opening \"" + typeFile + "\"", end="")
try:
    config = open(typeFile, "r")
    data = config.read()
    config.close()
    data = cregSpaces.sub("", data)
    sepInc = data.split("-")
    for inc in sepInc:
        inc = inc.split(":")
        types[inc[0]] = inc[1]
    showOk()
except:
    showError()

print (colors.GREEN + "\n------------------------------")
print ("---Start of header creation---")
print ("------------------------------" + colors.DEFAULT)
# Create headers
for fileName, funcs in usedFuncsMacsPerFile.items():
    if funcs:
        tempName = output + fileName.split("/")[-1].replace(".c", ".h")
        print ("\tCreating \"" + tempName + "\"", end="")
        try:
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
                    for key, value in macros.items():
                        if func in value.split(";"):
                            found = 1
                            if key != "void":
                                neededIncludes.append(key)
                    for key, value in types.items():
                        if func in value.split(";"):
                            found = 1
                            if key != "void":
                                neededIncludes.append(key)
                    if found == 0:
                        print (colors.YELLOW + "Warning: function, macro or type \"" + func + "\" not found in the config file" + colors.DEFAULT)
            neededIncludes = list(set(neededIncludes))
            for inc in neededIncludes:
                if inc[0] != '!':
                    file.write("#  include <" + inc + ">\n")
            for inc in neededIncludes:
                if inc[0] == '!':
                    file.write("#  include \"" + inc[1:] + "\"\n")
            if neededIncludes:
                file.write("\n")
            for func in funcs:
                if func in functionNames:
                    file.write(functions[functionNames.index(func)] + ";\n")
            file.write("\n#endif")
            file.close()
            showOk()
        except:
            showError()
print (colors.GREEN + "\n------------------------------")
print ("--- End of header creation ---")
print ("------------------------------\n" + colors.DEFAULT)

if bDoMakefile == 1:
    print ("Creating the Makefile", end="")
    createMakefile()

print (colors.GREEN)
print ("--------")
print ("- DONE -")
print ("--------")
print (colors.DEFAULT)
