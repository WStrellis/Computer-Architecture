"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.RAM = [0] * 256
        self.PC = 0
        self.REG = [0] * 8
        self.FL = [0] * 8
        self.IR = 0
        self._running = True
        self.SP = 0xf4

        self.REG[7] = 0xF4

        self.operations = {
            162: lambda x: self.alu(x),
            160: lambda x: self.alu(x),
            1: lambda x: self.hlt(),
            130: lambda x: self.ldi(),
            71: lambda x: self.prn(),
            70: lambda x: self.pop(),
            69: lambda x: self.push(),
            80: lambda x: self.call(),
            17: lambda x: self.ret(),
            167: lambda x: self.alu(x),  # CMP
            84: lambda x: self.jmp(),
            85: lambda x: self.jeq(),
            86: lambda x: self.jne(),
        }

    def push(self):
        """take value from register and add  to the stack"""
        # decrement SP
        self.SP -= 1
        # get value in register
        reg_num = int(self.ram_read(self.PC + 1), 2)
        val = self.REG[reg_num]
        # store value in stack
        self.ram_write(self.SP, val)

    def pop(self):
        """ remove an item from the stack and add to register"""

        # get register number from ram
        reg_num = int(self.ram_read(self.PC + 1), 2)
        # get value from stack
        val = self.ram_read(self.SP)
        # store value in register
        self.REG[reg_num] = val
        # increment SP
        self.SP += 1

    def ram_read(self, mar):
        """Read and return the value at the specified address in memory"""
        return self.RAM[mar]

    def ram_write(self, mar, mdr):
        """writes data to ram at the specified address"""
        self.RAM[mar] = mdr

    def load(self, file):
        """Load a program into memory."""

        address = 0
        program_file = open(file, 'r')
        for line in program_file:
            line = line.strip()
            # remove comments
            # skip empty lines and lines with only a comment
            if line == '' or line[0] == '#':
                continue
            # remove whitespace
            line = line[0:8]
            # add to memory at address
            self.ram_write(address, line)
            # increment address
            address += 1

        program_file.close()

    def alu(self, ir):
        """ALU operations."""
        ir = int(ir, 2)

        op_a = int(self.ram_read(self.PC + 1), 2)
        op_b = int(self.ram_read(self.PC + 2), 2)

        if ir == 160:  # ADD
            self.REG[op_a] += self.REG[op_b]
        elif ir == 162:  # MUL
            self.REG[op_a] *= self.REG[op_b]

        elif ir == 167:  # CMP
            if self.REG[op_a] == self.REG[op_b]:
                self.FL[7] = 1
            else:
                self.FL[7] = 0
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.REG[i], end='')

        print()

    def jmp(self):
        """set PC to address at given register"""
        reg_num = int(self.ram_read(self.PC + 1), 2)
        self.PC = self.REG[reg_num]

    def jeq(self):
        """if FL[7] is True set PC to value at given register"""
        if self.FL[7] == 1:
            reg_num = int(self.ram_read(self.PC + 1), 2)
            self.PC = self.REG[reg_num]
        else:
            self.PC += 2

    def jne(self):
        """ if FL[7] is False set PC to value at given register"""
        if self.FL[7] == 0:
            reg_num = int(self.ram_read(self.PC + 1), 2)
            self.PC = self.REG[reg_num]
        else:
            self.PC += 2

    def ldi(self):
        reg_num = int(self.ram_read(self.PC + 1), 2)
        val = int(self.ram_read(self.PC + 2), 2)
        # set  register to value
        self.REG[reg_num] = val

    def hlt(self):
        self._running = False

    def prn(self):
        loc = int(self.ram_read(self.PC + 1), 2)
        val = self.REG[loc]
        print(val)

    def call(self):
        """ can call saved functions"""
        # push next instruction onto stack
        self.SP -= 1
        self.ram_write(self.SP, self.PC + 2)
        # set PC to given reg#
        reg_num = int(self.ram_read(self.PC + 1), 2)
        self.PC = self.REG[reg_num]

    def ret(self):
        """pop value from top of stack and store in PC"""
        self.PC = self.ram_read(self.SP)
        self.SP += 1

    def advance_pc(self, ir):
        """ reads instruction register and determines how far to advance the PC
            uses fourth bit of op code to determine whether or not to advance the PC
         use first two bits of op code to determine how far
        to advance the PC"""
        if ir[3] == '0':
            op_bits = ir[:2]
            op_bits = int(op_bits, 2)
            self.PC += op_bits + 1

    def run(self):
        """Run the CPU."""
        while self._running:
            # read memory address in pc
            # store result in IC(instruction register)
            IR = self.ram_read(self.PC)
            # convert to decimal
            op_code = int(IR, 2)

            # read the opcode and execute
            self.operations[op_code](IR)

            # advance PC
            self.advance_pc(IR)
