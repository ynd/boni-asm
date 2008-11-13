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
    ('MOV', 'REG', 'NUM') : (('OP', 0xA), 'OP1', ('OP2', 'OP3')),
    ('JMP', 'ADR') : ((('OP', 'OP1'), 0xC0), ('OP2', 'OP3')),
    ('JZ', 'ADR') : ((('OP', 'OP1'), 0xC1), ('OP2', 'OP3')),
    ('JNZ', 'ADR') : ((('OP', 'OP1'), 0xC2), ('OP2', 'OP3')),
    ('JNEG', 'ADR') : ((('OP', 'OP1'), 0xC3), ('OP2', 'OP3')),
    ('JPOS', 'ADR') : ((('OP', 'OP1'), 0xC4), ('OP2', 'OP3')),
    ('STOP',) : (('OP', 0xF),),
}