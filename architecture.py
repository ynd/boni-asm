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
REGISTERS = (
    ('r0', 0x0),
    ('r1', 0x1),
    ('r2', 0x2),
    ('r3', 0x3),
    ('r4', 0x4),
    ('r5', 0x5),
    ('r6', 0x6),
    ('r7', 0x7),
    ('r8', 0x8),
    ('r9', 0x9),
    ('ra', 0xA),
    ('rb', 0xB),
    ('rc', 0xC),
    ('rd', 0xD),
    ('re', 0xE),
    ('rf', 0xF),
)

# List and Format of available instructions
INSTRUCTIONS = (
    ('ADD', ('OP', 0x0), ('OP1', 'REG'), ('OP2', 'REG'), ('OP3', 'REG')),
    ('SUB', ('OP', 0x1), ('OP1', 'REG'), ('OP2', 'REG'), ('OP3', 'REG')),
    ('SHR', ('OP', 0x2), ('OP1', 'REG'), ('OP2', 'REG')),
    ('SHL', ('OP', 0x3), ('OP1', 'REG'), ('OP2', 'REG')),
    ('NOT', ('OP', 0x4), ('OP1', 'REG'), ('OP2', 'REG')),
    ('AND', ('OP', 0x5), ('OP1', 'REG'), ('OP2', 'REG'), ('OP3', 'REG')),
    ('OR', ('OP', 0x6), ('OP1', 'REG'), ('OP2', 'REG'), ('OP3', 'REG')),
    ('MOV', ('OP', 0x7), ('OP1', 'REG'), ('OP2', 'REG')),
    ('MOV', ('OP', 0x8), ('OP1', 'REG'), (('OP2', 'OP1'), 'ADR')),
    ('MOV', ('OP', 0x9), (('OP2', 'OP1'), 'ADR'), ('OP1', 'REG')),
    ('MOV', ('OP', 0xA), ('OP1', 'REG'), (('OP2', 'OP1'), 'NUM')),
    ('JMP', (('OP', 'OP1'), 0xC0), ('OP2', 'ADR')),
    ('STOP', ('OP', 0xF)),
)