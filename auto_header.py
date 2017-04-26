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
import datetime
import glob

configFile = os.path.expanduser("~") + "/bin/autoHeader/general.conf"
globalFolder = os.path.expanduser("~") + "/bin/autoHeader/"
localConfFile = "auto_head.conf"
version = "0.6.0"
pathnames = []

# Regexes
regFunPtrProto = "[A-Za-z0-9_]+[ \t\*]+\((\*)*[A-Za-z0-9_]+\)\((([A-Za-z0-9_]*[ ]*)?[A-Za-z0-9_]*[ \*]*[A-Za-z0-9_\[\]]*,[ \*\n\t]*)*(([A-Za-z0-9_]*[ ]*)?[A-Za-z0-9_]*[ \*]*[A-Za-z0-9_\[\]]*)?\)"
regFunFull = "^[A-Za-z0-9_]+[ \t\*]+[A-Za-z0-9_]+\(((([A-Za-z0-9_]*[ ]*)?[A-Za-z0-9_]*[ \*]*[A-Za-z0-9_\[\]]*,[ \*\n\t]*)|(" + regFunPtrProto + "))*((([A-Za-z0-9_]*[ ]*)?[A-Za-z0-9_]*[ \*]*[A-Za-z0-9_\[\]]*)|(" + regFunPtrProto + "))?\)$"
regFunCalled = "[A-Za-z0-9_]+\("
regFunPtrName = "\((\*)*[A-Za-z0-9_]+\)"
regFunCalledPtr = "(\.[A-Za-z0-9_]+\()|(->[A-Za-z0-9_]+\()"
regMacro = "[^A-Za-z0-9_][A-Z0-9_]*[A-Z]+[A-Z0-9_]*[^A-Za-z0-9_]"
regVariable = "(struct )?[A-Za-z0-9_]+\**[ \t]+\**[A-Za-z0-9_]+|\((struct )?[A-Za-z0-9_]* *\**\)[A-Za-z0-9]"
regWord = "[A-Za-z0-9_]+"
cregArgNameComma = re.compile("[ ]*[A-Za-z0-9_]+,")
cregArgNamePar = re.compile("[ ]*[A-Za-z0-9_]+\)")
cregSpaces = re.compile("[ \n\t]+")
cregSpace = re.compile(" ")
cregExceptions = re.compile("(\"(.*?)\")|(\'(.*?)\')|(\/\*(.*?)(\*\/))", re.M|re.S)
cregFunFullNp = re.compile("^[A-Za-z0-9_]+[ \t\*]+[A-Za-z0-9_]+\((([A-Za-z0-9_]*[ ]*)?[A-Za-z0-9_]*[ \*]*[A-Za-z0-9_\[\]]*,[ \*\n\t]*)*(([A-Za-z0-9_]*[ ]*)?[A-Za-z0-9_]*[ \*]*[A-Za-z0-9_\[\]]*)?\)$")
# /Regexes

# Config
output = "include/"
objDir = "objs/"
includeDir = os.path.expanduser("~") + "/bin/autoHeader/includes/"
binaryName = "a.out"
bLetArgNames = 0
bIncludeHeader = 1
bDoMakefile = 1
lineHeader = 10
# /Config

# Flags
quiet = 0
verbose = 0
onefile = ""
libs = ""
recur = False
cfiles = []
createHeader = ""
# /Flags

# Infos
author = "Fantin Bibas"
authorMail = "fantin@bib.as"
company = "Epitech"
date = str(datetime.date.today())
# /Infos

# Arrays
flags = []
functions = []
functionNames = []
usedFuncsMacsPerFile = {}
wordsPerFile = {}
includes = {}
# /Arrays

headerHeader = """/*********************************************\\
|*   Header created by AutoHeader v. """ + version + """   *|
|* https://github.com/FantinBibas/autoHeader *|
\\*********************************************/

"""

makefileHeader = """## /*********************************************\\
## |*  Makefile created by AutoHeader v. """ + version + """  *|
## |* https://github.com/FantinBibas/autoHeader *|
## \\*********************************************/

"""

class colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[34m"
    CYAN = "\033[96m"
    PINK = "\033[95m"
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
    if quiet == 0:
        if verbose == 0:
            print (colors.GREEN + " -> Ok" + colors.DEFAULT)

def showError():
    if quiet == 0:
        print (colors.YELLOW + " -> Error" + colors.DEFAULT)

def printRed(text):
    print (colors.RED + text + colors.DEFAULT)

def printGreen(text):
    print (colors.GREEN + text + colors.DEFAULT)

def printBlue(text):
    print (colors.BLUE + text + colors.DEFAULT)

def printYellow(text):
    print (colors.YELLOW + text + colors.DEFAULT)

def printPink(text):
    print (colors.PINK + text + colors.DEFAULT)

def replaceHeaderFlags(text):
    text = text.replace("#version#", version)
    text = text.replace("#output#", output)
    text = text.replace("#binary#", binaryName)
    text = text.replace("#date#", date)
    text = text.replace("#author#", author)
    text = text.replace("#mail#", authorMail)
    text = text.replace("#company#", company)
    return (text)

def loadHeaderMak():
    fileName = globalFolder + "makefileHeader"
    global makefileHeader
    if os.path.isfile(fileName):
        file = open(fileName, "r")
        makefileHeader = file.read() + "\n"
        file.close()
        makefileHeader = replaceHeaderFlags(makefileHeader)

def loadHeaderHea():
    fileName = globalFolder + "headerHeader"
    global headerHeader
    if os.path.isfile(fileName):
        file = open(fileName, "r")
        headerHeader = file.read() + "\n"
        file.close()
        headerHeader = replaceHeaderFlags(headerHeader)

def addHeader(file):
    file.write(headerHeader)

def addMakefileHeader(file):
    file.write(makefileHeader)

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
    print ("                        #############                        \n")

def analyseFlag(flag):
    global quiet
    global verbose
    global bDoMakefile
    global output
    global binaryName
    global libs
    global onefile
    global objDir
    global recur
    global pathnames
    flag = flag.split(":")
    global createHeader
    if flag[0] == "q":
        quiet = 1
    elif flag[0] == "v":
        verbose = 1
    elif flag[0] == "M":
        bDoMakefile = 1
    elif flag[0] == "m":
        bDoMakefile = 0
    elif flag[0] == "r":
        recur = True
    elif flag[0] == "o" and len(flag) == 2:
        output = flag[1]
    elif flag[0] == "b" and len(flag) == 2:
        binaryName = flag[1]
    elif flag[0] == "l" and len(flag) == 2:
        libs = flag[1]
    elif flag[0] == "files" and len(flag) == 2:
        pathnames.extend(flag[1].split(" "))
    elif flag[0] == "obj" and len(flag) == 2:
        objDir = flag[1]
    elif flag[0] == "onefile" and len(flag) == 2:
        onefile = flag[1]
    elif flag[0] == "h" and len(flag) == 2:
        createHeader = flag[1]

    else:
        printRed("Unrecognised flag \"" + flag[0] + "\"")
        print(flag)
        sys.exit(84)
    if quiet == 1:
        verbose = 0

def analyseLocal(data):
    data = data.replace("\n", "")
    data = data.split(";")
    for flag in data:
        if flag != "":
            analyseFlag(flag)

def openConfFile(confFile, local):
    if quiet == 0:
        print ("Opening \"" + colors.CYAN + confFile + colors.DEFAULT + "\"", end="")
        if verbose == 1:
            print()
    try:
        config = open(confFile, "r")
        data = config.read()
        config.close()
        if local == 1:
            data = data.split("==")
            if len(data) == 2:
                analyseLocal(data[0])
                data = data[1]
        data = cregSpaces.sub("", data)
        sepInc = data.split("-")
        for inc in sepInc:
            inc = inc.split(":")
            if verbose == 1:
                printPink("\tFound \"" + inc[0] + "\"")
            if inc[0] in includes:
                includes[inc[0]] += inc[1]
            else:
                includes[inc[0]] = inc[1]
        showOk()
    except:
        showError()

def createMakefile():
    try:
        makefile = open("Makefile", "w")
        addMakefileHeader(makefile)
        makefile.write("CC\t=\tgcc\n\n")
        makefile.write("RM\t=\trm -f\n\n")
        makefile.write("FLAGS\t+=\t-Wextra -Wall " + libs + "\n\n")
        makefile.write("CPPFLAGS\t+=\t-I " + output + "\n\n")
        makefile.write("NAME\t=\t" + binaryName + "\n\n")
        makefile.write("SRCS\t=\t")
        for fileName in sorted(usedFuncsMacsPerFile.keys())[:-1]:
            makefile.write(fileName + "\t\\\n\t\t")
        makefile.write(sorted(usedFuncsMacsPerFile.keys())[-1] + "\n\n")
        makefile.write("OBJDIR\t=\t" + objDir + "\n\n")
        if (objDir != ""):
            makefile.write("OBJS\t=\t$(SRCS:%.c=$(OBJDIR)/%.o)\n\n")
        else:
            makefile.write("OBJS\t=\t$(SRCS:.c=.o)\n\n")
        makefile.write("$(OBJDIR)/%.o:\t%.c\n\tmkdir -p $(OBJDIR)\n\tmkdir -p $(@D)\n\t$(CC) -c $< -o $@ $(CPPFLAGS)\n\n")
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
    global includeDir
    global macroFile
    global typeFile
    global bIncludeHeader
    global lineHeader
    global bDoMakefile
    global binaryName
    global bLetArgNames
    global libs
    global author
    global authorMail
    global company
    global objDir
    try:
        config = open(configFile, "r")
        data = config.read()
        config.close()
        data = cregSpaces.sub("", data)
        sepInc = data.split(";")
        for inc in sepInc:
            inc = inc.split(":")
            if len(inc) == 2:
                if inc[0] == "output":
                    output = inc[1]
                elif inc[0] == "globalIncludeFolder":
                    includeDir = inc[1].replace("~", os.path.expanduser("~"))
                elif inc[0] == "include":
                    bIncludeHeader = int(inc[1])
                elif inc[0] == "includeLine":
                    lineHeader = int(inc[1])
                elif inc[0] == "makefile":
                    bDoMakefile = int(inc[1])
                elif inc[0] == "binary":
                    binaryName = inc[1]
                elif inc[0] == "argNames":
                    bLetArgNames = int(inc[1])
                elif inc[0] == "author":
                    author = inc[1]
                elif inc[0] == "mail":
                    authorMail = inc[1]
                elif inc[0] == "company":
                    company = inc[1]
                elif inc[0] == "objdir":
                    objDir = inc[1]
    except:
        try:
            config = open(configFile, "w")
            config.write("output:" + output + ";\n")
            config.write("globalIncludeFolder:" + includeDir + ";\n")
            config.write("include:" + str(bIncludeHeader) + ";\n")
            config.write("includeLine:" + str(lineHeader) + ";\n")
            config.write("makefile:" + str(bDoMakefile) + ";\n")
            config.write("binary:" + str(binaryName) + ";\n")
            config.write("argNames:" + str(bLetArgNames) + ";\n")
            config.close()
        except:
            print (colors.YELLOW + "Warning couldn't create the config file." + colors.DEFAULT)

##THE CAKE IS A LIE!!!!!##

def addFunction(function): # Add the function to the dictionnary array of known functions
    if bLetArgNames == 0 and cregFunFullNp.match(function):
        function = cregArgNameComma.sub(",", function)
        function = cregArgNamePar.sub(")", function)
    function = cregSpaces.sub(" ", function)
    functions.append(function)
    name = function.split(" ")[1].split("(")[0].replace("*", "")
    if verbose == 1:
        printPink("\t\tFound function declaration: " + name)
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
    if quiet == 0:
        print ("\tAnalysing \"" + colors.CYAN + fileName + colors.DEFAULT + "\"", end="")
    try:
        file = open(fileName, "r")
        data = file.read()
        file.close()
    except:
        showError()
        return
    data = cregExceptions.sub("", data)
    if verbose == 1:
        print ()
    localDefinedFuncs = []
    localDefinedFuncsFull = []
    for function in re.finditer(regFunFull, data, re.M):
        localDefinedFuncs.append(addFunction(function.group()))
        localDefinedFuncsFull.append(function.group())
    localUsedFuncs = []
    for function in re.finditer(regFunCalled, data, re.M):
        name = function.group().replace("(", "")
        if not name in localUsedFuncs:
            if verbose == 1:
                printPink("\t\tFound used function: " + name)
            localUsedFuncs.append(name)
    for function in re.finditer(regFunCalledPtr, data, re.M):
        name = function.group().replace("(", "")
        name = name.replace(".", "")
        name = name.replace("->", "")
        if name in localUsedFuncs:
            if verbose == 1:
                printPink("\t\tFunction: " + name + " is an alias (I think)")
            localUsedFuncs.remove(name)
    for macro in re.finditer(regMacro, data, re.M): # Macro handling (yes I know i need to clean this)
        macro = macro.group()[1:-1]
        if not macro in localUsedFuncs:
            if verbose == 1:
                printPink("\t\tFound used macro: " + macro)
            localUsedFuncs.append(macro)
    for variable in re.finditer(regVariable, data, re.M): # Variable type handling (same as ^^^^)
        variable = variable.group().split(" ")[0].split("\t")[0]
        variable = variable.split(")")[0];
        if (variable[:1] == "("):
            variable = variable[1:]
        if not variable in localUsedFuncs:
            if verbose == 1:
                printPink("\t\tFound used variable type: " + variable)
            localUsedFuncs.append(variable)
    localWords = []
    for word in re.finditer(regWord, data, re.M):
        name = word.group()
        if not name in localWords:
            localWords.append(name)
    localWords = list(set(localWords))
    localUsedFuncs = list(set(localUsedFuncs))
    for function in localDefinedFuncs:
        if function in localUsedFuncs:
            localUsedFuncs.remove(function)
        if function in localWords:
            localWords.remove(function)
    for function in localDefinedFuncsFull:
        for viciousFuncName in re.finditer(regFunPtrName, function, re.M):
            name = viciousFuncName.group().replace("*", "").replace("(", "").replace(")", "")
            if name in localUsedFuncs:
                localUsedFuncs.remove(name)
            if name in localWords:
                localWords.remove(name)
    usedFuncsMacsPerFile[fileName] = (localUsedFuncs, localWords)
    if bIncludeHeader == 1:
        try:
            file = open(fileName, "r")
            data = file.readlines()
            file.close()
            if onefile == "":
                name = "#include \"" + fileName.split("/")[-1].replace(".c", ".h\"\n")
            else:
                name = "#include \"" + onefile + "\"\n"
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

def createHeaderFile(name, includeArray, functionArray):
    file = open(name, "w")
    addHeader(file)
    addDblIncSec(file, name)
    for inc in includeArray:
        if inc[0] != '!':
            file.write("#  include <" + inc + ">\n")
            if verbose == 1:
                printPink("\t\tIncluding \"" + inc + "\"")
    for inc in includeArray:
        if inc[0] == '!':
            file.write("#  include \"" + inc[1:] + "\"\n")
            if verbose == 1:
                printPink("\t\tIncluding \"" + inc[1:] + "\"")
    if includeArray:
        file.write("\n")
    for func in functionArray:
        if func in functionNames:
            file.write(functions[functionNames.index(func)] + ";\n")
            if verbose == 1:
                printPink("\t\tPrototyping \"" + func + "\"")
    file.write("\n#endif")
    file.close()

if __name__ == '__main__': # Main
    readConfig()
    args = sys.argv[1:]
    tempArgs = list(args)
    for arg in tempArgs:
        if arg[0] == '-':
            flags.append(arg[1:])
            args.remove(arg) # Parse arguments

    for flag in flags: # Flags handler
        analyseFlag(flag)

    if quiet == 0:
        showHeader() # Header

    pathnames.extend(args)

    for root, dirs, files in os.walk(includeDir): # Load global config files
        for file in files:
            openConfFile(os.path.join(root, file), 0)

    if os.path.isfile(localConfFile):
        openConfFile(localConfFile, 1) # Load local config file

    if createHeader != "":
        createHeaderFile(createHeader, [], [])
        sys.exit(0)

    if len(pathnames) < 1 and not recur:
        error_args()

    if quiet == 0:
        print (colors.BLUE + "\n-----------------------")
        print ("---Start of analyzis---")
        print ("-----------------------\n" + colors.DEFAULT)

    if len(pathnames) == 0:
        pathnames.append(".")

    for fileName in pathnames:
        if recur:
            if fileName.endswith("/"):
                fileName += "**/*"
            elif fileName.endswith("."):
                fileName += "/**/*"
        for cfile in glob.glob(fileName, recursive=recur):
            #print("Debug: " + cfile + " recursive: " + str(recur))
            if (cfile.endswith(".c")):
                cfiles.append(cfile)

    for cfile in cfiles:
        analizeFile(cfile)

    if quiet == 0:
        print (colors.BLUE + "\n-----------------------")
        print ("--- End of analyzis ---")
        print ("-----------------------\n" + colors.DEFAULT)


    if quiet == 0:
        print (colors.BLUE + "\n---------------------------------------")
        print ("--- Searching for function pointers ---")
        print ("---------------------------------------\n" + colors.DEFAULT)
    for fileName, pair in usedFuncsMacsPerFile.items():
        funcs = pair[0]
        words = pair[1]
        if quiet == 0:
            print ("\tSearching in \"" + colors.CYAN + fileName + colors.DEFAULT + "\"", end="")
        if verbose == 1:
            print()
        if words:
            for word in words:
                if word in functionNames and not word in funcs:
                    funcs.append(word)
                    if verbose == 1:
                        printPink("\t\tPossible function pointer: " + word)
        showOk()

    if quiet == 0:
        print (colors.BLUE + "\n-----------------------")
        print ("--- End of research ---")
        print ("-----------------------\n" + colors.DEFAULT)

    alignFunctions()
    if quiet == 0:
        print ("Creating the output folder", end="")
    if not os.path.exists(output):
        os.makedirs(output)
        if verbose == 1:
            printPink("\n\tOutput folder \"" + output + "\" created")
    else:
        if verbose == 1:
            printPink("\n\tOutput folder \"" + output + "\" existing already")
    showOk()

    loadHeaderMak()
    loadHeaderHea()

    if quiet == 0: # Start of header
        print (colors.BLUE + "\n------------------------------")
        print ("---Start of header creation---")
        print ("------------------------------\n" + colors.DEFAULT)

    if onefile == "": # Create one header for each c file
        for fileName, pair in usedFuncsMacsPerFile.items():
            funcs = pair[0]
            if funcs:
                tempName = output + fileName.split("/")[-1].replace(".c", ".h")
                if quiet == 0:
                    print ("\tCreating \"" + colors.CYAN + tempName + colors.DEFAULT + "\"", end="")
                    if verbose == 1:
                        print()
                try:
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
                                if quiet == 0:
                                    print (colors.YELLOW + "\n\t\t-> Warning: \"" + colors.RED  + func + colors.YELLOW + "\" not found in the config file nor in others c files" + colors.DEFAULT)
                    neededIncludes = list(set(neededIncludes))
                    createHeaderFile(tempName, neededIncludes, funcs)
                    showOk()
                except:
                    showError()
    else: # Create only one header for all c files
        neededIncludes = []
        try:
            if quiet == 0:
                print ("\tCreating \"" + colors.CYAN + onefile + colors.DEFAULT + "\"", end="")
                if verbose == 1:
                    print()
            for fileName, pair in usedFuncsMacsPerFile.items():
                funcs = pair[0]
                if funcs:
                    for func in funcs:
                        if not func in functionNames:
                            found = 0
                            for key, value in includes.items():
                                if func in value.split(";"):
                                    found = 1
                                    if key != "void":
                                        neededIncludes.append(key)
                            if found == 0:
                                if quiet == 0:
                                    print (colors.YELLOW + "\n\t\t-> Warning: \"" + colors.RED  + func + colors.YELLOW + "\" not found in the config file nor in others c files" + colors.DEFAULT)
            neededIncludes = list(set(neededIncludes))
            createHeaderFile(output + onefile, neededIncludes, functionNames)
            showOk()
        except:
            showError()

    if quiet == 0: # End of header
        print (colors.BLUE + "\n------------------------------")
        print ("--- End of header creation ---")
        print ("------------------------------\n" + colors.DEFAULT)

    if bDoMakefile == 1: # Creation of Makefile
        if quiet == 0:
            print ("Creating the Makefile", end="")
            if verbose == 1:
                print ()
        createMakefile()

    if quiet == 0: # Done
        print (colors.GREEN)
        print ("--------")
        print ("- DONE -")
        print ("--------")
        print (colors.DEFAULT)
