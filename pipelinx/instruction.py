

class Instruction:
    """Instruções suportadas por nosso simulador são:
        opp $0, $2, $3; Tipo R com opp podendo ser: add, sub, mul, and, or, 
        opp $1, $4, #3; I
        opp #20;        J

        Exemplos:
            add $r0, $r2, $r3;
            add $r3, $r2, #4;
            sw $r3, #2($r5);
            lw $r0, #4($r5);
            jmp #10;
            jz $3, #10;

    """

    
    def __init__( self, instruction : str) -> None:
        self.instruction = instruction
        instruction = instruction.split(" ")

        self.opcode = instruction[0]

        self.stages = []

        self.reg_read = []
        self.reg_write = -1
        self.imme = 0
    
        self.mem_read = -1
        self.mem_write = -1
        self.buffer = ''


        self.ads= None
        
        self.__decode_operands( ''.join(instruction[1:]))


    def __decode_operands( self, instruction: str) -> list:
        if "(" in instruction:
            instruction = instruction.replace("(", ",").replace(")", "")
        
        operands = instruction.split(",")
        operands = [o.replace(" ", "") for o in operands]
        
        if len(operands) == 1:
            self.reg_read = []
            self.reg_write = []
            self.mem_read = []
            self.mem_write = []

            self.ads = int( operands[0][1:].replace(";","").replace("\n", ""))
            # J
            
        else:
            if all([ True if "$" in operand else False for operand in operands]):
                # R
            
                
                self.reg_read.append(int(operands[1][1:].replace(";","").replace("\n", "")) )
                self.reg_read.append(int(operands[2][1:].replace(";","").replace("\n", "")))
                self.reg_write = int(operands[0][1:])
                self.mem_read = None
                self.mem_write = None
                           


            elif "$" in operands[0] and "#" in operands[1] and "$" in operands[2] :
                # I
                reg_read = []
                reg_write = -1
                mem_read = -1
                mem_write = -1

                ads = None

                if self.opcode == "lw":
                    reg_read = [ int(operands[2][1:].replace(";","").replace("\n", ""))]
                    mem_read = int(operands[1][1:].replace(";","").replace("\n", "")) 
                    reg_write = int(operands[0][1:].replace(";","").replace("\n", "")) 

                elif self.opcode == "sw":
                    mem_write = int(operands[1][1:])
                    reg_read.append(int(operands[1][1:].replace(";","").replace("\n", "")) )
                    reg_read.append( int(operands[2][1:].replace(";","").replace("\n", "")))
                    # { "desvio" : int(operands[2][1:].replace(";","").replace("\n", "")
                    
                
                elif self.opcode == "beq":
                    reg_read = [int(operands[1][1:].replace(";","").replace("\n", "")) ]
                    ads = int(operands[2][1:].replace(";","").replace("\n", ""))

                else:
                    reg_write = int(operands[0][1:].replace(";","").replace("\n", "")) 
                    reg_read = [ int(operands[1][1:].replace(";","").replace("\n", ""))]
                    self.imme = int(operands[2][1:].replace(";","").replace("\n", ""))

                self.reg_read = reg_read
                self.reg_write = reg_write
                self.mem_read = mem_read
                self.mem_write = mem_write
                self.ads = ads
            
    def _to_dict(self):
        dictionary = {
            self.instruction : {
                'reg_read' : self.reg_read,
                'reg_write' : self.reg_write,
                'mem_read' : self.mem_read,
                'mem_write' : self.mem_write,
                'adress' : self.ads
            }
        }

        return dictionary

    def __str__(self) -> str:
        
        return self.instruction[:-1]+self.buffer 
    