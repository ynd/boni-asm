"""
Created by Yann N. Dauphin on 2008-11-11.
Copyright (c) 2008 Lambda Tree Media. All rights reserved.

You only need to modify this file to add or remove instructions.

This file defines:
- The Assembly Language that is supported
- The machine code that is generated

So the compiler is easily retargetable.
"""


# Decompopes an instructions into multiple named parts
# Format: ('name', length)
INSTRUCTION_FORMAT = (
    ('OP', 4),
    ('OP1', 4),
    ('OP2', 4),
    ('OP3', 4),
)

# List of available registers
REGISTERS = {
    'R0': 0x0,
    'R1': 0x1,
    'R2': 0x2,
    'R3': 0x3,
    'R4': 0x4,
    'R5': 0x5,
    'R6': 0x6,
    'R7': 0x7,
    'R8': 0x8,
    'R9': 0x9,
    'R10': 0xA,
    'R11': 0xB,
    'R12': 0xC,
    'R13': 0xD,
    'R14': 0xE,
    'R15': 0xF,
}

# List and Format of available instructions
INSTRUCTIONS = {
    ('ADD', 'REG', 'REG', 'REG') : (('OP', 0x0), 'OP1', 'OP2', 'OP3'),
    ('SUB', 'REG', 'REG', 'REG') : (('OP', 0x1), 'OP1', 'OP2', 'OP3'),
    ('SHR', 'REG', 'REG', 'REG') : (('OP', 0x2), 'OP1', 'OP2', 'OP3'),
    ('SHL', 'REG', 'REG', 'REG') : (('OP', 0x3), 'OP1', 'OP2', 'OP3'),
    ('NOT', 'REG', 'REG') : (('OP', 0x4), 'OP1', 'OP2'),
    ('AND', 'REG', 'REG', 'REG') : (('OP', 0x5), 'OP1', 'OP2', 'OP3'),
    ('OR', 'REG', 'REG', 'REG') : (('OP', 0x6), 'OP1', 'OP2', 'OP3'),
    ('MOV', 'REG', 'REG') : (('OP', 0x7), 'OP1', 'OP2'),
    ('MOV', 'REG', 'ADR') : (('OP', 0x8), 'OP1', ('OP2', 'OP3')),
    ('MOV', 'ADR', 'REG') : (('OP', 0x9), ('OP2', 'OP3'), 'OP1'),
    ('MOV', 'REG', 'NUM') : (('OP', 0xA), 'OP1', ('NEXT', ('OP','OP1', 'OP2', 'OP3'))),
    ('JMP', 'ADR') : ((('OP', 'OP1'), 0xC0), ('OP2', 'OP3')),
    ('JZ', 'ADR') : ((('OP', 'OP1'), 0xC1), ('OP2', 'OP3')),
    ('JNZ', 'ADR') : ((('OP', 'OP1'), 0xC2), ('OP2', 'OP3')),
    ('JNEG', 'ADR') : ((('OP', 'OP1'), 0xC3), ('OP2', 'OP3')),
    ('JPOS', 'ADR') : ((('OP', 'OP1'), 0xC4), ('OP2', 'OP3')),
    ('STOP',) : (('OP', 0xF),),
}