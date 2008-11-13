parser Assembly:
    ignore:       r'#.*(?=$|\n)'    # line comment
    ignore:       r'[ \t\n\r]+'
    token NUM:    r'\$(0x[a-fA-F0-9]+|[0-9]+)'
    token ADR:    r'0x[a-fA-F0-9]+|[0-9]+'
    token REG:    r'%(\w+)'
    token OP:     r'[a-zA-Z]+'
    token TAG:    r'[a-zA-Z0-9_]+'
    token TAGDEF: r'[a-zA-Z0-9_]+:'
    token END:    r'$'
    
    rule line: instruction END    {{ return instruction }}
             | TAGDEF END         {{ return ('TAGDEF', TAGDEF) }}
             | END                {{ return [] }}

    rule instruction: OP                    {{ result = [] }}
                         (                   
                           operand [","]    {{ result.append(operand) }}
                         )*                  
                                            {{ return ('OP', OP, result) }}
    
    rule operand: NUM          {{ return ('NUM', eval(NUM[1:])) }}
                | ADR          {{ return ('ADR', eval(ADR)) }}
                | TAG          {{ return ('TAG', TAG) }}
                | REG          {{ return ('REG', REG) }}