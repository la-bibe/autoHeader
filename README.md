# AutoHeader

### Description

AutoHeader is a little Python program that helps the creation of a C project.

It can create header files adapted to every c file you pass in parameter with:
- The prototypes of the functions found in the other files by analysing which ones are used
- The header files needed found associated with their functions in the functions.conf file (by default)
- The header files needed for the macros in macros.conf (by default)

It can also automatically create a Makefile.

### Usage
`auto_header.py [file.c]...`

### general.conf file
- `output:include/` : This is the destination of the header files.
- `funcDictionnary:functions.conf` : This is the file which contains the headers associated with their functions.
- `macrDictionnary:macros.conf` : This is the file which contains the headers associated with their macros.
- `include:1` : 0 or 1, if it's 1 the programm will add an `#include "filename.h"` at the *includeLine* line.
- `includeLine:10` : The line where to write the include.
- `makefile:1` : 0 or 1, if it's 1 the programm will create a Makefile with the files passed as parameter and including the headers.
- `binary:a.out` : Name of the output binary for the Makefile.
- `argNames:0` : 0 or 1, if it's 0 it will remove the name of the parameters in the prototypes in the headers.

### functions.conf file
Each header name can be preceded by a '!' to include it with quotes (`#include "tardis.h"`) instead of diples (`#include <tardis.h>`).

The headers are separated by '-' and the file name is separated for the functions with ':'. Each function must end with ';'.

You don't need to write the parenthesis, just the name of the function.

### macros.conf file
Same as the functions.conf file.

### types.conf file
Same as the functions.conf file.
