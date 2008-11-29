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


class Assembler(object):
    def __init__(self):
        self.codegen = MachineCodeGenerator()
    
    def assemble(self, input_file, mode='HEX'):
        f = open(input_file).read()
        tree = self.parse_program(f)
        tags = self.find_tags(tree)
        if mode == 'VHDL':
            program = []
            
        for inst in tree:
            if inst[0] == 'OP':
                machine_code = self.codegen.generate_for(inst, tags)
                if mode == 'BIN':
                    print machine_code
                elif mode == 'VHDL':
                    program.extend(self.codegen.split_machine_code(machine_code))
                elif mode == 'COMMENT':
                    print hex(int(machine_code, 2)).ljust(32, ' '), '#', inst
                else:
                    print hex(int(machine_code, 2))
        
        if mode == 'VHDL':
            print '(',
            for word in program:
                print 'x"%s",' % hex(int(word, 2))[2:].rjust(self.codegen.get_instruction_size()/4,"0"),
            print "others => (others => '1') )"
    
    def parse_program(self, input):
        tree = []
        for line in input.splitlines():
            try:
                result = parser.parse('line', line)
                if type(result) is list:
                    for e in result:
                        tree.append(e)
                elif result:
                    tree.append(result)
            except UnboundLocalError, e:
                print >> sys.stderr, 'A syntax error was found.'
                exit(-1)
        return tree

    def find_tags(self, tree):
        # Initialize dict
        tags = {}
        for e in tree:
            if e[0] == 'TAGDEF':
                tags[e[1]] = 0
        # Find correspondence
        i = 0
        for inst in tree:
            if inst[0] == 'TAGDEF':
                tags[inst[1]] = i
            elif inst[0] == 'OP':
                machine_code = self.codegen.generate_for(inst, tags)
                i += len(machine_code) / self.codegen.get_instruction_size()
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
            print >> sys.stderr, 'This type of instruction is not supported:', inst_type
            print >> sys.stderr, 'You wrote:', instruction[1:]
            print >> sys.stderr, 'Please consult architecture.py for a list of supported instructions.'
            exit(-1)
    
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
    
    def get_instruction_size(self):
        return reduce(lambda tot, t: t[1] + tot, architecture.INSTRUCTION_FORMAT, 0)
    
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
    
    def split_machine_code(self, machine_code):
        r = []
        instruction_size = self.get_instruction_size()
        for part in range(0, len(machine_code), instruction_size):
            r.append(machine_code[part:part+instruction_size])
        return r


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:vbm", ["help", "output=", "binary", "mode="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        verbose, mode = False, 'HEX'
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(open("USAGE").read())
            if option in ("-o", "--output"):
                output = value
            if option in ("-b", "--binary"):
                mode = 'BIN'
            if option in ("-m", "--mode"):
                mode = value.upper()
        
        Assembler().assemble(args[0], mode)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": "
        print str(err.msg)
        return 2


if __name__ == "__main__":
    sys.exit(main())
