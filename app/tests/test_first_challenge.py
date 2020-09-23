import unittest
import os

from app.parser.parse_data import HostsConnectedTo

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestFirstChallenge(unittest.TestCase):

    def test_first_exercise(self):
        test_file = f'{CURRENT_DIR}/files/input-file-10000.txt'
        init_datetime = 1565647204351
        end_datetime = 1565650799255
        hostname = 'Alyaa'

        result = HostsConnectedTo(test_file, init_datetime, end_datetime, hostname=hostname)
        result = result.parse_file()

        expected = [['1565647368307', 'Mehkai', 'Alyaa'], ['1565650799255', 'Donnis', 'Alyaa']]

        self.assertEqual(list(result), expected)


if __name__ == '__main__':
    unittest.main()
