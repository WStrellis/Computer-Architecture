import unittest
import unittest.mock
import sys
from io import StringIO
from ls8.cpu import CPU


class TestCase(unittest.TestCase):
    def setUp(self):
        self.capturedOutput = StringIO()
        sys.stdout = self.capturedOutput

    def tearDown(self):
        sys.stdout = sys.__stdout__
        self.capturedOutput = None

    def test_load(self):
        """ should initalize the memory in the CPU with the contents from test.txt"""
        cpu = CPU()

        program_file = './tests/test.txt'
        cpu.load(program_file)
        self.assertEqual(cpu.RAM[0], '00000001')
        self.assertEqual(cpu.RAM[1], '00000010')
        self.assertEqual(cpu.RAM[2], '00000011')
        self.assertEqual(cpu.RAM[3], '00000100')

    def test_advance_pc(self):
        """ should advance PC correctly"""
        cpu = CPU()

        self.assertEqual(cpu.PC, 0, f'Expected {cpu.PC} to eq 0')
        cpu.advance_pc('0000')
        self.assertEqual(cpu.PC, 1, f'Expected {cpu.PC} to eq 1')
        cpu.advance_pc('0100')
        self.assertEqual(cpu.PC, 3, f'Expected {cpu.PC} to eq 3')
        cpu.advance_pc('1000')
        self.assertEqual(cpu.PC, 6, f'Expected {cpu.PC} to eq 6')

    def test_ret(self):
        """should set PC and SP"""
        cpu = CPU()

        cpu.RAM[240] = 10
        cpu.SP = 240
        cpu.ret()
        self.assertEqual(cpu.PC, 10)
        self.assertEqual(cpu.SP, 241)

    def test_call(self):
        """should push next instruction onto stack and then set PC"""
        cpu = CPU()

        cpu.RAM[1] = '00000001'
        cpu.RAM[2] = '00001111'
        cpu.REG[1] = 4
        cpu.call()
        self.assertEqual(cpu.SP, 243)
        self.assertEqual(cpu.PC, 4)

    def test_print8(self):
        """should print the number 8 to the console"""
        cpu = CPU()

        program_file = './ls8/examples/print8.ls8'
        cpu.load(program_file)
        cpu.run()
        result = self.capturedOutput.getvalue().strip()
        self.assertEqual(result, '8')

    def test_mult(self):
        """should print the number 72 to the console"""
        cpu = CPU()

        program_file = './ls8/examples/mult.ls8'
        cpu.load(program_file)
        cpu.run()
        result = self.capturedOutput.getvalue().strip()
        self.assertEqual(result, '72', f'Expected 72 but got {result}')

    def test_stack(self):
        """should print the numbers 2,4,1  to the console"""
        cpu = CPU()

        program_file = './ls8/examples/stack.ls8'
        cpu.load(program_file)
        cpu.run()
        expected = '2\n4\n1'
        result = self.capturedOutput.getvalue().strip()
        self.assertEqual(result, expected,
                         f'Expected {expected} but got {result}')

    def test_subroutines(self):
        """should print the numbers 20,30,36,60  to the console"""
        cpu = CPU()

        program_file = './ls8/examples/call.ls8'
        cpu.load(program_file)
        cpu.run()
        expected = '20\n30\n36\n60'
        result = self.capturedOutput.getvalue().strip()
        self.assertEqual(result, expected,
                         f'Expected {expected} but got {result}')


if __name__ == '__main__':
    unittest.main()
