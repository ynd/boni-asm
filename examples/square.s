# Take a number N in memory and square it
    
    # Initialization - The return value will be %r0
    MOV %r0, $0x0            # $0x0 is the constant number 0x0
    
    # We decide the parameter of the function will be at address 0x0
    MOV %r1, 0x0             # Adresses are numbers without a preceding $
    MOV %r2, 0x0

# This is a tag definition
loop_header:
    ADD %r0, %r1, %r0
    
    # Branch condition
    MOV %r3, $1              # $1 is the same as $0x1 but in decimal
    SUB %r2, %r2, %r3
    JNZ loop_header
    
    STOP
    
    
    