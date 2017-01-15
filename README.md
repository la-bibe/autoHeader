# AutoHeader

### Description

AutoHeader is a little Python program that helps the creation of a C project.

It can create header files adapted to every c file you pass in parameter with:
- The prototypes of the functions found in the other files by analysing which ones are used
- The header files needed by analysing what functions, macros, structs and typedef are used based on the configuration files.

It can also automatically create a Makefile.

### Table of content

- [AutoHeader](#)
		- [Description](#)
    - [Table of content](#)
    - [Installation](#)
		- [Usage](#)
		- [general.conf file](#)
		- [Other configuration files](#)
			- [Syntax of the configuration files](#)

### Installation

To install it just launch the install.sh script:

```
./install.sh
```

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

### general.conf file

This file is placed by default in the ~/bin/settings folder. You can change it by modifying the line
```
configFile = os.path.expanduser("~") + "/bin/settings/general.conf"
```
in auto_header.py. It should be near to the top of the file.

- `output:include/` : This is the destination of the header files.
- `funcDictionnary:~/bin/settings/functions.conf` : This is the file which contains the headers associated with their functions.
- `macrDictionnary:~/bin/settings/macros.conf` : This is the file which contains the headers associated with their macros.
- `typeDictionnary:~/bin/settings/types.conf` : This is the file which contains the headers associated with their types.
- `include:1` : 0 or 1, if it's 1 the program will add an `#include "filename.h"` at the *includeLine* line.
- `includeLine:10` : The line where to write the include.
- `makefile:1` : 0 or 1, if it's 1 the program will create a Makefile with the files passed as parameter and including the headers.
- `binary:a.out` : Name of the output binary for the Makefile.
- `argNames:0` : 0 or 1, if it's 0 it will remove the name of the parameters in the prototypes in the headers.

### Other configuration files

By default the program will look at the three files function.conf, macros.conf and types.conf in the folder ~/bin/settings but this can be changed in the general.conf file. The program will also check if there is a file auto_header.conf in the folder where it is executed, if so it will load it as well.

Theorically you should put all the general functions, types and macros in the configuration files in the ~/bin/settings folder and the functions, types and macros specific to your project in the auto_header.conf file.

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
