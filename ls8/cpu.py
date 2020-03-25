"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.RAM = [0] * 256
        self.PC = 0
        self.FL = [0] * 8
        self.REG = [0] * 8
        self.IR = 0
        self._running = True

        self.REG[7] = 0xF4

        self.operations = {
            147: self.alu,
            162: self.alu,
            1: self.hlt,
            130: self.ldi,
            71: self.prn
        }

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
            # line = line.split('#')[0]
            # skip empty lines and lines with only a comment
            if line == '' or line[0] == '#':
                continue
            # remove whitespace
            # line = line.strip()
            line = line[0:8]
            # convert to int
            # val = int(line, 2)
            # add to memory at address
            self.ram_write(address, line)
            # increment address
            address += 1

        program_file.close()

    def alu(self):
        """ALU operations."""
        op = self.IR
        # values from specified ram address
        reg_a = self.ram_read(self.PC + 1)
        # val_a = self.REG[reg_a]
        reg_b = self.ram_read(self.PC + 2)
        # val_b = self.REG[reg_b]

        if op == 147:  # ADD
            self.REG[reg_a] += self.REG[reg_b]
        elif op == 162:  # MUL
            self.REG[reg_a] *= self.REG[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

        self.PC += 3

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

    def ldi(self):
        # next element in RAM is gives register number
        reg_num = self.ram_read(self.PC + 1)
        # get value to add to register from RAM
        val = self.ram_read(self.PC + 2)
        # set  register to value
        self.REG[reg_num] = val
        self.PC += 3

    def hlt(self):
        self._running = False

    def prn(self):
        reg_num = self.ram_read(self.PC + 1)
        val = self.REG[reg_num]
        print(val)
        self.PC += 2

    def advance_pc(self):
        """ use first two bits of op code to determine how far
        to advance the PC"""
        op_bits = self.IR[:2]
        op_bits = int(op_bits, 2)
        self.PC += op_bits + 1

    def run(self):
        """Run the CPU."""
        while self._running:
            # read memory address in pc
            # store result in IC(instruction register)
            self.IR = self.ram_read(self.PC)
            # convert IR to decimal format
            op_code = int(self.IR, 2)
            # read the opcode and execute
            op = self.operations.get(op_code)
            op()
            # increment PC
            self.advance_pc()
