"""
Simulador de Pipelane


Suporta as instruções:
    add
    sub 
    and
    or
    not
    lw
    st
    
"""


from pipelinx.instruction import *
import os

class Simulador:
    def __init__( self, mem_size : int) -> None:
        self.instructions = []
        self.pc = 1

        self.cout = 2
        self.line = 1
        self.mem_inst = []
       


    def initialize( self, path : str) -> None:
        with open( path, 'r') as file:
            instructions = [ line for line in file.readlines()]

        print(len(instructions))
        for i, instruction in enumerate(instructions):
            if instruction:
                self.mem_inst.append(Instruction( instruction))
        for i in range(len(self.instructions), 32):
            self.mem_inst.append(False)

    
    def run( self):
        self.instructions.append([self.mem_inst[0]])
        for i, stage in enumerate([ "BI", "DI", "EX", "MEM","ER"]):
            self.instructions[0].append(stage)

        while( self.pc < 32):
            # try:
            self.step()

            self.print()

            input()
            os.system("clear")
            # except:
                # break
        
        print(f"===================================================================================\n")
        print(f"=====================================FINALIZADO=====================================\n")
        print(f"===================================================================================\n")

    def step( self):
        current = self.mem_inst[self.pc]
        self.pc +=1
        
        self.instructions.append([current])
        for i in range( 1, self.cout):
            self.instructions[self.line].append(0)
        
        cout = 0
        

        stages = ["BI", "DI", "EX", "MEM", "ER"]
        if current:
            while(cout< 5):
                for x in range( self.line-1, -1, -1):
                   
                    #verifica as dependencias das instruções anteriores
                    inst = self.instructions[x][0]

                    if (inst.opcode == "jmp" or inst.opcode == "beq") and self.instructions[x].index("MEM") > self.cout+cout:
                        for i in range( 3):
                            self.instructions[x][0].buffer = "Criando bolhas por desvio"
                            self.instructions[self.line].append(0)
                            self.pc = inst.ads +1
                            self.cout+=1
                        break
                

                    if self.instructions[x].index(stages[cout]) == self.cout+cout:    
                        # for i in range(x):
                        #     self.instructions[i].append(0)
                        self.cout += 1

                    # Bolha para adiantar dps adiantar
                    if inst.reg_write in current.reg_read and stages[cout] == "DI":
                        index = self.instructions[x].index("MEM")
                    
                        if index > self.cout:
                            self.instructions[x][0].buffer = f"Criando bolha e adiantando da MEM para EX o reg{inst.reg_write}"
                            self.instructions[self.line].append(0)
                            self.cout +=1

                            break

                    if inst.reg_write in current.reg_read and stages[cout] == "DI":
                        index = self.instructions[x].index("EX")
                    
                        if index > self.cout:
                            # self.instructions[x][0].buffer = f"Criando bolha e adiantando da EX para EX o reg{inst.reg_write}"
                            self.instructions[self.line].append(0)
                            self.cout +=1

                            break
            
                self.instructions[self.line].append(stages[cout])
                cout +=1
            self.cout +=1
        for i in range(self.line):
            self.instructions[i].append(0)
        self.line +=1
                        
                
    def print( self):
        for l in self.instructions:
                index = l.index("BI")
                buffer = " "*16*(index-1)
                line = "_"*10 + " "*5
                edges = line * (l.index("ER")-index+1)
                
                stage_line = []
                for stage in l[index:l.index("ER")+1]:
                    if len(str(stage)) == 2:
                        stage_line.append(f"|{'   '+str(stage)+'   '}|")
                    elif len(str(stage)) == 3:
                        stage_line.append(f"|{'  '+str(stage)+'  '}|")
                    elif len(str(stage)) == 1:
                        stage_line.append(f"|{'        '}|")
                    stage_line.append("  -> ")

                stage_block = "".join(stage_line)

                print(f'{buffer}{edges}\n')
                print(f'{buffer}{stage_block[:-5]}\n')
                print(f'{buffer}|{str(l[0])}\n')
                print(f'{buffer}{"-"*(14*(l.index("ER")-index+1))}')
               

     
   