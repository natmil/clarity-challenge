import os

from app.parser.parse_data import HostsConnectedTo
from app.parser.unlimited_parse import UnlimitedParser

FILE = ''  # For example => 'app/tests/files/input-file-10000.txt'


class Menu(object):
    def __init__(self):
        self.init_datetime = 1
        self.end_datetime = 1
        self.hostname = ''

    @staticmethod
    def get_option(options):
        print('\n'.join((f'{str(i)}. {name}' for i, name in options.items())))

        opt_input = input('Please, select an option: ')
        while not opt_input or not opt_input.isdigit() or opt_input.isspace() or int(opt_input) not in options.keys():
            opt_input = input('[Incorrect] Please, select an option: ')

        return int(opt_input)

    @staticmethod
    def get_timestamp(name):
        timestamp = input(f'[{name}]: ')
        while not timestamp or not timestamp.isdigit() or timestamp.isspace() or int(timestamp) < 1:
            timestamp = input(f'[{name}] incorrect: ')

        return int(timestamp)

    @staticmethod
    def get_username():
        hostname = input('[hostname]: ')
        while not hostname or hostname.isspace():
            hostname = input('[hostname] incorrect: ')

        return hostname

    def parse_data_init_end_time(self):
        print("### Parse the data with a time_init, time_end ###")

        self.init_datetime = self.get_timestamp('time_init')
        self.end_datetime = self.get_timestamp('time_end')

        self.hostname = self.get_username()

        result = HostsConnectedTo(FILE, self.init_datetime, self.end_datetime, hostname=self.hostname)
        result.run()

    def unlimited_input_parser(self):
        print("### Unlimited Input Parser ###")

        self.hostname = self.get_username()

        result = UnlimitedParser(FILE, self.hostname)
        result.run()

    def select_option(self):
        options = {
            1: 'Parse the data with a time_init, time_end',
            2: 'Unlimited Input Parser'
        }

        func_options = [
            self.parse_data_init_end_time,
            self.unlimited_input_parser
        ]

        print(f'FILE: {FILE}')
        result = self.get_option(options)

        func_options[result - 1]()


if __name__ == '__main__':
    if os.path.isfile(FILE):
        clarity = Menu()
        clarity.select_option()
    else:
        print('File does not exists.')
