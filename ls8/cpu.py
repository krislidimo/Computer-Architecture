"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0] * 8

    def load(self, file):
        """Load a program into memory."""

        address = 0

        with open(file) as f:
            for line in f:
                comments = line.split("#")
                num = comments[0].strip()

                try: 
                    val = int(f'{num}'[2:],2)
                except ValueError:
                    continue
                    
                self.ram[address] = val
                address += 1 

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        NOP = 0
        HLT = 1
        LDI = 2
        PRN = 7
        MUL = 34
        pc = 0

        while True:
            ir = self.ram_read(pc) # Instruction Register, currently executing instruction
            print(f'ir: {ir}')
            if ir == HLT:
                pc +=1
                break

            elif ir == LDI:
                regAddress = self.ram_read(pc+1)
                integer = self.ram_read(pc+2)
                self.reg[regAddress] = integer
                pc +=3

            elif ir == PRN:
                print(self.reg[self.ram_read(pc+1)])
                pc +=2

            elif ir == MUL:
                regAddressA = self.ram_read(pc+1)
                regAddressB = self.ram_read(pc+2)
                intA = self.reg[regAddressA]
                intB = self.reg[regAddressB]
                self.reg[regAddressA] =intA*intB
                pc +=3

            else:
                print(f"Unknown instruction: {ir}")
                break

    # accepts the address to read and return the value stored there.
    # MAR = Memory Address Register, address that is being read or written to
    def ram_read(self, MAR):
        return self.ram[MAR]

    # accepts a value to write, and the address to write it to.
    # MAR = Memory Address Register, address that is being read or written to
    # MDR = Memory Data Register, address that is being read or written to
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR