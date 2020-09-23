import os.path


class HostsConnectedTo(object):
    """
    1. Parse the data with a time_init, time_end
    Build a tool, that given the name of a file (with the format described above), an init_datetime, an
    end_datetime, and a Hostname, returns: a list of hostnames connected to the given host during the given period
    """

    def __init__(self, file, init_datetime, end_datetime, **kwargs):
        self.file = file
        self.init_datetime = init_datetime
        self.end_datetime = end_datetime
        self.hostname = kwargs.get('hostname')
        # If 'received' is True, it will set the index to 1 to check received connections, if not it will be index 2
        # to check given connections
        self.received = 1 if kwargs.get('received') is not None else 2

    def parse_file(self):
        # 'With' block will automatically close the file once it reach the end of the 'with' block.
        # So there's no need to close the file at the end. I mention it just in case.
        with open(self.file) as f:
            query = []
            # Will keep reading the file if the next line has content, and if the timestamp is <= than the current
            # end_time, just because the logfile is sorted and we don't want to keep reading lines that are not
            # useful to us. Just to be efficient.
            line = f.readline().split()
            while line and int(line[0]) <= self.end_datetime:
                query.append(line)
                line = f.readline().split()

            if self.hostname is not None:
                # This comprehension list will iterate over our query to check if the value meets the requirements
                result = [x for x in query
                          if self.init_datetime <= int(x[0]) <= self.end_datetime
                          and self.hostname == x[self.received]]
            else:
                result = [x[1] for x in query if self.init_datetime <= int(x[0]) <= self.end_datetime]

            return result

    def run(self):
        if os.path.isfile(self.file):
            parsed_result = self.parse_file()
            if parsed_result:
                print('List of hostnames connected to the host {} during the period between {} and {}\n{}'.format(
                    self.hostname, self.init_datetime, self.end_datetime, parsed_result))
            else:
                print('There is no hosts connected to the host {} during the period between {} and {}'.format(
                    self.hostname, self.init_datetime, self.end_datetime))
        else:
            print('File does not exists.')
