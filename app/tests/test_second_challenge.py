import os
import unittest
import time

from app.parser.unlimited_parse import UnlimitedParser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSecondChallenge(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.file_test = f'{CURRENT_DIR}/files/input-file-10000.txt'
        self.current_timestamp = int(time.time())  # Current unix timestamp
        self.one_hour_ago_timestamp = int(self.current_timestamp) - 3600  # Current unix timestamp - 1 hour

    def add_dummy_data(self):
        """ We add some dummy data to the top of the file so we can have a few connections during last hour """
        new_lines_to_add = f'{self.current_timestamp - 1800} William Rebeca\n{self.current_timestamp - 1800} Sarah Nathan\n{self.current_timestamp - 1740} William Holden\n{self.current_timestamp - 60} John Patricia'
        with open(self.file_test, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(new_lines_to_add + '\n' + content)

    def remove_dummy_data(self):
        """ Removing the first 4 dummy log lines that we added """
        with open(self.file_test) as f1:
            lines = f1.readlines()
        with open(self.file_test, 'w') as f2:
            f2.writelines(lines[4::])

    def test_hostnames_connected_to(self):
        hostname = 'Nathan'
        test_object = UnlimitedParser(self.file_test, hostname)

        self.add_dummy_data()

        result = test_object.hostnames_connected_to(self.one_hour_ago_timestamp, self.current_timestamp)
        expected = [[str(self.current_timestamp - 1800), 'Sarah', 'Nathan']]

        self.assertEqual(result, expected, 'A list of hostnames connected to a given (configurable) host during the last hour')

        self.remove_dummy_data()

    def test_hostnames_receiving_connections(self):
        hostname = 'Sarah'
        test_object = UnlimitedParser(self.file_test, hostname)

        self.add_dummy_data()

        result = test_object.hostnames_receiving_connections(self.one_hour_ago_timestamp, self.current_timestamp)
        expected = [[str(self.current_timestamp - 1800), 'Sarah', 'Nathan']]

        self.assertEqual(result, expected, 'A list of hostnames received connections from a given (configurable) host during the last hour')

        self.remove_dummy_data()

    def test_hostname_most_connections_hour(self):
        test_object = UnlimitedParser(self.file_test)

        self.add_dummy_data()

        result = test_object.hostname_most_connections_hour(self.one_hour_ago_timestamp, self.current_timestamp)
        expected = [('William', 2)]

        self.assertEqual(result, expected, 'The hostname that generated most connections in the last hour')

        self.remove_dummy_data()


if __name__ == '__main__':
    unittest.main()
