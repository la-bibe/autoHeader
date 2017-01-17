# AutoHeader

### Description

AutoHeader is a little Python program that helps the creation of a C project.

It can create header files adapted to every c file you pass in parameter with:
- The prototypes of the functions found in the other files by analysing which ones are used
- The header files needed by analysing what functions, macros, structs and typedef are used based on the configuration files.

It can also automatically create a Makefile.

### Table of content

- [Description](#description)
- [Table of content](#table-of-content)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration files](#configuration-files)
	- [general.conf file](#generalconf-file)
	- [auto_head.conf file](#auto_headconf-file)
	- [Other configuration files](#other-configuration-files)
	- [Syntax of the configuration files](#syntax-of-the-configuration-files)

### Installation

To install it just launch the install.sh script:

`./install.sh`

### Usage

`auto_header.py [file.c]...`

You can also use the following flags:
- "-v" : Verbose mode
- "-q" : Quiet mode (overrides verbose mode)
- "-o:include/" : Set the output folder for the headers
- "-b:a.out" : Set the name of the binary for the Makefile
- "-l:-lm" : Set the libs for the Makefile
- "-M" : Create a Makefile
- "-m" : Do not create a Makefile
- "onefile:file.h" : Create only one header file which contains the necessary includes for all files and all found prototypes

### Configuration files

### general.conf file

This file is placed by default in the ~/bin/autoHeader/ folder. You can change it by modifying the line
```
configFile = os.path.expanduser("~") + "/bin/autoHeader/general.conf"
```
in auto_header.py. It should be close to the top of the file.

- `output:include/` : This is the destination of the header files.
- `globalIncludeFolder:~/bin/autoHeader/includes/` : This is the folder where the program is going to search the global configuration files.
- `include:1` : 0 or 1, if it's 1 the program will add an `#include "filename.h"` at the *includeLine* line.
- `includeLine:10` : The line where to write the include.
- `makefile:1` : 0 or 1, if it's 1 the program will create a Makefile with the files passed as parameter and including the headers.
- `binary:a.out` : Name of the output binary for the Makefile.
- `argNames:0` : 0 or 1, if it's 0 it will remove the name of the parameters in the prototypes in the headers.

### auto_head.conf file

The file auto_head.conf should be placed in the folder where you will execute auto_header.py. It should contains all the functions, macros and types which are specific to your project. See [Syntax of the configuration files](#syntax-of-the-configuration-files) for more info on how to declare functions, macro and types in conf files.

The file auto_head.conf is separated in two parts with "==". In the first part you can put flags to not be obliged to put them every time you execute auto_header.py. There is an example :
```
b:wolf3d;
l:-lm -lcsfml-graphics -lcsfml-window;
==
!macros.h:
  PLAYER_SIZEX;
  PLAYER_SIZEY;
  CURS_SIZE;
```
Here the first line `b:wolf3d` define the name of the output file for the Makefile. For more details about the flags got take a look at the [Usage](#usage) section.

### Other configuration files

By default the program will look at all the files in the folder ~/bin/autoHeader/includes/ but this can be changed in the general.conf file.

Theorically you should put all the general functions, types and macros in the configuration files in the ~/bin/autoHeader/includes/ folder and the functions, types and macros specific to your project in the auto_header.conf file.

#### Syntax of the configuration files

```
header.h:
  functionInTheHeader;
  otherFunctionInTheHeader;
  MACRO_IN_THE_HEADER;
  t_typedefInTheHeader;
-
otherHeader.h:
  MACRO_IN_OTHERHEADER;
  functionInOtherHeader;
```

Each header name can be preceded by a '!' to include it with quotes (`#include "tardis.h"`) instead of diples (`#include <tardis.h>`).

The headers are separated by '-' and the file name is separated of the functions, macros and types with ':'. Each function, macro and type must end with ';'.

For the functions you must not include the parenthesis nor the type, only the name.

You can use void as header file to not include anything for the associated function, macro or type.



#### Enjoy ! :)
