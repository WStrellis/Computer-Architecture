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

    def test_load(self):
        """ should inialize the memory in the CPU with the contents from test.txt"""
        cpu = CPU()

        program_file = './tests/test.txt'
        cpu.load(program_file)
        self.assertEqual(cpu.RAM[0], 1)
        self.assertEqual(cpu.RAM[1], 2)
        self.assertEqual(cpu.RAM[2], 3)
        self.assertEqual(cpu.RAM[3], 4)

    # @unittest.mock.patch('sys.stdout',new_callable=StringIO )

    def test_print8(self):
        """should print the number 8 to the console"""
        cpu = CPU()

        program_file = './ls8/examples/print8.ls8'
        cpu.load(program_file)
        cpu.run()
        result = self.capturedOutput.getvalue().strip()
        self.assertEqual(result, '8')


if __name__ == '__main__':
    unittest.main()
