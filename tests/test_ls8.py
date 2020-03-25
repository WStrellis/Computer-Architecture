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


if __name__ == '__main__':
    unittest.main()
