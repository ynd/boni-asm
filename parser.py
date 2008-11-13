from string import *
import re
from yappsrt import *

class AssemblyScanner(Scanner):
    patterns = [
        ('","', re.compile(',')),
        ('#.*(?=$|\\n)', re.compile('#.*(?=$|\\n)')),
        ('[ \\t\\n\\r]+', re.compile('[ \\t\\n\\r]+')),
        ('NUM', re.compile('\\$(0x[a-fA-F0-9]+|[0-9]+)')),
        ('ADR', re.compile('0x[a-fA-F0-9]+|[0-9]+')),
        ('REG', re.compile('%(\\w+)')),
        ('OP', re.compile('[a-zA-Z]+')),
        ('TAG', re.compile('[a-zA-Z0-9_]+')),
        ('TAGDEF', re.compile('[a-zA-Z0-9_]+:')),
        ('END', re.compile('$')),
    ]
    def __init__(self, str):
        Scanner.__init__(self,None,['#.*(?=$|\\n)', '[ \\t\\n\\r]+'],str)

class Assembly(Parser):
    def line(self):
        _token_ = self._peek('TAGDEF', 'END', 'OP')
        if _token_ == 'OP':
            instruction = self.instruction()
            END = self._scan('END')
            return instruction
        elif _token_ == 'TAGDEF':
            TAGDEF = self._scan('TAGDEF')
            END = self._scan('END')
            return ('TAGDEF', TAGDEF[:len(TAGDEF)-1])
        else:# == 'END'
            END = self._scan('END')
            return []

    def instruction(self):
        OP = self._scan('OP')
        result = []
        while self._peek('NUM', 'ADR', 'TAG', 'REG', 'END') != 'END':
            operand = self.operand()
            if self._peek('","', 'NUM', 'ADR', 'TAG', 'REG', 'END') == '","':
                self._scan('","')
            result.append(operand)
        return ('OP', OP, result)

    def operand(self):
        _token_ = self._peek('NUM', 'ADR', 'TAG', 'REG')
        if _token_ == 'NUM':
            NUM = self._scan('NUM')
            return ('NUM', eval(NUM[1:]))
        elif _token_ == 'ADR':
            ADR = self._scan('ADR')
            return ('ADR', eval(ADR))
        elif _token_ == 'TAG':
            TAG = self._scan('TAG')
            return ('TAG', TAG)
        else:# == 'REG'
            REG = self._scan('REG')
            return ('REG', REG[1:])


def parse(rule, text):
    P = Assembly(AssemblyScanner(text))
    return wrap_error_reporter(P, rule)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print parse(argv[1], f.read())
    else: print 'Args:  <rule> [<filename>]'
