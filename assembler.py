#!/usr/bin/env python
# encoding: utf-8
"""
assembler.py

Created by Yann N. Dauphin on 2008-11-11.
Copyright (c) 2008 Lambda Tree Media. All rights reserved.
"""

import sys
import getopt
import parser
import architecture

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
-o some_file                        Output the compiled code to some_file
-b                                  Output in binary
''' % __file__


class Assembler(object):
    def __init__(self):
        self.codegen = MachineCodeGenerator()
    
    def assemble(self, input_file, output_binary=False):
        tree = self.parse_program(input_file)
        tags = self.find_tags(tree)
    
        for inst in tree:
            if inst[0] == 'OP':
                machine_code = self.codegen.generate_for(inst, tags)
                if output_binary:
                    print machine_code
                else:
                    print hex(int(machine_code, 2))
    
    def parse_program(self, input_file):
        tree = []
        for line in open(input_file):
            try:
                result = parser.parse('line', line)
                if result:
                    tree.append(result)
            except UnboundLocalError, e:
                exit(-1)
        return tree

    def find_tags(self, tree):
        tags, i = {}, 0
        for e in tree:
            if e[0] == 'TAGDEF':
                tags[e[1]] = i
            else:
                i += 1
        return tags


class MachineCodeGenerator(object):
    def generate_for(self, inst, tags={}):
        machine_code = []
        tags = tags or {}
        encoding = self.get_encoding_for(inst)
        section_values = self.get_section_values_for(inst, encoding, tags)
        sections = len(architecture.INSTRUCTION_FORMAT)
        
        for section in section_values:
            if type(section) in (list, tuple) and section[0] == 'NEXT':
                # One value to put in next instruction
                values = self.fit_value(section_values[section], section[1])
                machine_code += map(lambda v: (sections + self.get_pos_of(v[0]), v[1]), values)
            elif type(section) in (list, tuple):
                # One value is put in many sections
                values = self.fit_value(section_values[section], section)
                machine_code += map(lambda v: (self.get_pos_of(v[0]), v[1]), values)
            else:
                # One value is put in one section
                value = self.int2bin(section_values[section], self.get_size_of(section))
                code = self.get_pos_of(section), value
                machine_code.append(code)
        
        # Fill empty sections
        for i in range(sections):
            if i not in dict(machine_code):
                section_position = i % (sections / len(architecture.INSTRUCTION_FORMAT))
                section = architecture.INSTRUCTION_FORMAT[section_position][0]
                value = self.int2bin(0x0, self.get_size_of(section))
                machine_code.append((i, value))
        
        machine_code.sort(lambda x,y: x[0]-y[0])
        return ''.join(map(lambda v: v[1], machine_code))
    
    def get_encoding_for(self, instruction):
        op = instruction[1].upper()
        arg_types = map(lambda a: a[0], instruction[2])
        arg_types = map(lambda a: 'ADR' if a == 'TAG' else a, arg_types) # Tags are Adresses
        inst_type = tuple([op] + arg_types)
        try:
            return architecture.INSTRUCTIONS[inst_type]
        except KeyError, e: 
            raise e
    
    def get_section_values_for(self, inst, encoding, tags=None):
        tags = tags or {}
        sections = {}
        operands = map(lambda a: a[1], inst[2])
        operand_types = map(lambda a: a[0], inst[2])
        
        for i, section in enumerate(encoding):
            if type(section) is tuple and type(section[1]) is int:
                sections[section[0]] = section[1]
            elif operand_types[i-1] == 'REG':
                sections[section] = architecture.REGISTERS[operands[i-1].upper()]
            elif operand_types[i-1] == 'TAG':
                sections[section] = tags[operands[i-1]]
            else:
                sections[section] = operands[i-1]
        return sections
    
    def get_pos_of(self, section):
        for i, s in enumerate(architecture.INSTRUCTION_FORMAT):
            if s[0] == section:
                return i
    
    def get_size_of(self, section):
        sections = dict(architecture.INSTRUCTION_FORMAT)
        if type(section) in (list, tuple):
            return reduce(lambda tot, s: sections[s] + tot, section, 0)
        else:
            return sections[section]
    
    def int2bin(self, n, size):
        return "".join([str((n>>y) & 1) for y in range(size-1, -1, -1)])
    
    def fit_value(self, value, sections):
        bin_val = self.int2bin(value, self.get_size_of(sections))
        r, i = [], 0
        for section in sections:
            part = bin_val[i:i+self.get_size_of(section)]
            r.append((section, part)) 
            i += self.get_size_of(section)
        return r


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:vb", ["help", "output=", "binary"])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        verbose, output_binary = False, False
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option in ("-b", "--binary"):
                output_binary = True
        
        Assembler().assemble(args[0], output_binary)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        return 2


if __name__ == "__main__":
    sys.exit(main())
