import unittest, os, io
import unittest.mock
import sys
current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(current))
from mars_rover.Position import Position
from mars_rover.Plateau import Plateau
from mars_rover.Rover import Rover
from mars_rover.Config import Config
from driver import process_input

class TestPosition(unittest.TestCase):
    def testConstructor(self):
        # Create position instance with default values
        position = Position()
        self.assertEqual(position.x, 0)
        self.assertEqual(position.y, 0)

        # Create position instance with values
        position = Position(1, 2)
        self.assertEqual(position.x, 1)
        self.assertEqual(position.y, 2)


class TestPlateau(unittest.TestCase):
    def testConstructor(self):
        plateau = Plateau(7, 10)

        self.assertEqual(plateau.width, 7)
        self.assertEqual(plateau.height, 10)


class TestRover(unittest.TestCase):
    def testConstructor(self):
        plateau = Plateau(7, 7)
        position = Position(0, 0)

        rover = Rover('Rover1', plateau, position, Config.DIRECTIONS['W'])

        self.assertEqual(Position(0, 0), rover.position)
        self.assertEqual(plateau, rover.plateau)


class TestMarsRover(unittest.TestCase):
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def testMRover(self, mock_stdout):
        files = [
            f'{current}/test_data/data1.txt',
            f'{current}/test_data/data2.txt'
        ]
        
        expected = [
            'Invalid command D',
            "Rover1:3 7 N\nRover2:1 1 S\n"
        ]
        
        for i, fil in enumerate(files):
            if i == 0:
                with self.assertRaises(Exception) as context:
                    process_input(fil)

                self.assertTrue(expected[i] in str(context.exception))
            else:
                process_input(fil)
                self.assertEqual(mock_stdout.getvalue(), expected[i])

        
if __name__ == '__main__':
    unittest.main()