                                        oooooooooo.    .oooooo.   ooooo      ooo ooooo 
                                        `888'   `Y8b  d8P'  `Y8b  `888b.     `8' `888' 
                                         888     888 888      888  8 `88b.    8   888  
                                         888oooo888' 888      888  8   `88b.  8   888  
                                         888    `88b 888      888  8     `88b.8   888  
                                         888    .88P `88b    d88'  8       `888   888  
                                        o888bood8P'   `Y8bood8P'  o8o        `8  o888o 


Boni is an easily retargetable assembler
========================================

It should take a few hours to add support for new architectures. You just have to edit [architecture.py](/ynd/boni-asm/tree/master/architecture.py "architecture.py").


I wrote it for one of my courses so I had to finish it pretty quickly. It is well written though(Pythonic).

It only supports one architecture for now. A general purpose micro-processor made in our course. I am confident it can support x86 with minimal effort.

I hope someone can build from this.

**Usage:**

`python assembler.py yourfile.s`

`python assembler.py examples/example1.s`

**Options:**

`-b                                  Output in binary`