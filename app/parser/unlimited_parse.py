import sched
import time

from collections import Counter
from itertools import takewhile

from app.parser.parse_data import HostsConnectedTo

REPEAT_EVERY = 3600


class UnlimitedParser(object):
    """
    2. Unlimited Input Parser
    The tool should both parse previously written log files and terminate or collect input from a new log
    file while it's being written and run indefinitely.
    The script will output, once every hour:
    - a list of hostnames connected to a given (configurable) host during the last hour
    - a list of hostnames received connections from a given (configurable) host during the last hour
    - the hostname that generated most connections in the last hour
    """

    def __init__(self, file, host=None):
        self.file = file
        self.host = host
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.current_timestamp = int(time.time())  # Current unix timestamp
        self.one_hour_ago_timestamp = int(self.current_timestamp) - 3600  # Current unix timestamp - 1 hour

    def hostnames_connected_to(self, init_datetime, end_datetime):
        result = HostsConnectedTo(self.file, init_datetime, end_datetime, hostname=self.host)
        return result.parse_file()

    def hostnames_receiving_connections(self, init_datetime, end_datetime):
        result = HostsConnectedTo(self.file, init_datetime, end_datetime, hostname=self.host, received=True)

        return result.parse_file()

    def hostname_most_connections_hour(self, init_datetime, end_datetime):
        result = HostsConnectedTo(self.file, init_datetime, end_datetime)
        result = result.parse_file()
        counter = Counter(result)
        if counter:
            # First I do get the max value to compare it, just in case there is multiple hosts with same max value.
            max_value = counter.most_common(1)[0][1]
            return list(takewhile(lambda x: x[1] == max_value, counter.most_common()))

    def unlimited_parse(self, sc):
        result_host_connected_to = self.hostnames_connected_to(self.one_hour_ago_timestamp, self.current_timestamp)
        result_host_receiving_conn = self.hostnames_receiving_connections(self.one_hour_ago_timestamp, self.current_timestamp)
        result_host_most_connections = self.hostname_most_connections_hour(self.one_hour_ago_timestamp, self.current_timestamp)

        if result_host_connected_to:
            print(f'\nA list of hostnames connected to {self.host} host during the last hour'
                  f'\n{result_host_connected_to}')
        else:
            print(f'\nThere is no hosts connected to the host {self.host} during last hour')

        if result_host_receiving_conn:
            print(f'A list of hostnames received connections from {self.host} host during the last hour'
                  f'\n{result_host_receiving_conn}')
        else:
            print(f'There is no hosts that has received connections from {self.host} during last hour')

        if result_host_most_connections:
            print('The hostname that generated most connections in the last hour'
                  f'\n{result_host_most_connections}')
        else:
            print(f'No connections has been generated during last hour')

        print(f'Waiting {REPEAT_EVERY} seconds...')
        self.scheduler.enter(REPEAT_EVERY, 1, self.unlimited_parse, (sc,))

    def run(self):
        self.scheduler.enter(0, 1, self.unlimited_parse, (self.scheduler,))
        self.scheduler.run()
