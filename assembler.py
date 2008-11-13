#!/usr/bin/env python
# encoding: utf-8
"""
assembler.py

Created by Yann N. Dauphin on 2008-11-11.
Copyright (c) 2008 Lambda Tree Media. All rights reserved.
"""

import sys
import getopt


help_message = '''
88888888ba     ,ad8888ba,    888b      88  88  
88      "8b   d8"'    `"8b   8888b     88  88  
88      ,8P  d8'        `8b  88 `8b    88  88  
88aaaaaa8P'  88          88  88  `8b   88  88  
88""""""8b,  88          88  88   `8b  88  88  
88      `8b  Y8,        ,8P  88    `8b 88  88  
88      a8P   Y8a.    .a8P   88     `8888  88  
88888888P"     `"Y8888Y"'    88      `888  88  
Created by Yann N. Dauphin on 2008-11-11.
Copyright (c) 2008 Lambda Tree Media. All rights reserved.

Boni is a retargetable assembler that can compile Turing Complete Assembly.
Boni was originally created for the machine defined in the fifth TP of the course INF3500.
Boni makes it easy to add support for more architectures.

Usage:
python %s yourfile.s

Options:
-o some_file: Output the compiled code to some_file
''' % __file__


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        return 2


if __name__ == "__main__":
    sys.exit(main())
