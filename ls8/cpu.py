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
            147: 'ADD',
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

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,  # store the next line in register[0]
            0b00001000,  # the number 8
            0b01000111,  # PRN R0
            0b00000000,  # print the value from register[0]
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.RAM[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.REG[reg_a] += self.REG[reg_b]
        # elif op == "SUB": etc
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

    def ldi(self):
        # next element in RAM is gives register number
        reg_num = self.ram_read(self.PC + 1)
        # get value to add to register from RAM
        val = self.ram_read(self.PC + 2)
        # set  register to value
        self.REG[reg_num] = val

    def hlt(self):
        print("HLT command encountered")
        self._running = False

    def prn(self):
        reg_num = self.ram_read(self.PC + 1)
        val = self.REG[reg_num]
        print(val)

    def run(self):
        """Run the CPU."""
        while self._running:
            # read memory address in pc
            # store result in IC(instruction register)
            self.IR = self.ram_read(self.PC)
            # execute command in IR
            # print(f'IR: {self.IR}')
            # read the opcode and execute
            op = self.operations.get(self.IR)
            if op:
                op()
            # read values of pc+1 and pc+2
            # print(f'IR: {self.IR}')
            # store in operand_a/b for future use
            # operand_a = self.ram_read(self.PC + 1)
            # operand_b = self.ram_read(self.PC + 2)
            # self.trace()
            # print(f'current pc:{self.ram_read(self.PC)}')
            # operation = self.operations[IR]
            # if IR does not advance PC, update PC to get next instruction
            self.PC += 1
