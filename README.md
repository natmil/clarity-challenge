# Clarity AI -  Backend Code Challenge

A log file contains newline-terminated, space-separated text formatted like:

`<unix_timestamp> <hostname> <hostname>`

For example:

```
1366815793 quark garak
1366815795 brunt quark
1366815811 lilac garak
```

Each line represents connection from a host (left) to another host (right) at a given time. The lines are
roughly sorted by timestamp. They might be out of order by maximum 5 minutes.
Implement a tool that parse log files like these, we provide you a input Data Example.

Requirements
----

You'll only need Python3, **3.8.5** to be precise.

How to run
----

There's no need to create virtual environment, as there is no external libraries required. Just pure Python.

Edit the main.py script, to add the file that you want to work with. For example:

```
FILE = 'app/tests/files/input-file-10000.txt'
```

Execute the script.

```
$ python3 main.py
```

You'll see this menu, just select the options you want.

```
1. Parse the data with a time_init, time_end
2. Unlimited Input Parser
Please, select an option:
```

First Challenge
---

**1. Parse the data with a time_init, time_end**

Build a tool, that given the name of a file (with the format described above), an init_datetime, an end_datetime, and a Hostname, returns:

  - a list of hostnames connected to the given host during the given period

> With this one I created this class called 'HostsConnectedTo', where I have a function called parse_file.
>
> This function will open the file, then read line by line till the timestamp is lower or equal than the current end_time, or we reached the end of the file.
>
> Then, it will filter the data using a comprehension list, to check if the value meets the requirements.

Second Challenge
---

> I couldn't make it to collect input from a new log file while it's being written and run indefinitely.
>
> BUT: It will parse the previously written log file and terminate, and then is gonna wait till one hour passes to run again.

**2. Unlimited Input Parser**

The tool should both parse previously written log files and terminate or collect input from a new log file while it's being written and run indefinitely.

The script will output, once every hour:
  - a list of hostnames connected to a given (configurable) host during the last hour
  > I recycled the function from the first challenge. But this time, I use for the arguments the current unix timestamp and the same one minus 3600, which is 1 hour in seconds.
  - a list of hostnames received connections from a given (configurable) host during the last hour
  > Same as before, I did use the same function. But this time, I pass and extra argument called 'received' as True, to switch the index of the host.
  - the hostname that generated most connections in the last hour
  > I did use the same function. Same current timestamp and one-hour ago timestamp. No host and 'received' for arguments. So it will only return the name of the host or hosts who has had connected in the last hour. Then it will check who host or hosts  — I have assumed that MAYBE there is more than one host generating the most connections. — has the most connections.



Tests
---

Just run this commend to execute the tests.

```
$ python3 -m unittest discover app/tests/
```

TODOs
---
  - I really want to make it so it can collect input from a new log file while it's being written, I have to do more research on how to do it without any external libraries.
  - I would like to implement this library — already built in Python — called mmap. It seems to be a great option for reading really big files faster, as it will map the file into memory.
  - Write MORE tests.

Feedback
---

Any feedback would be VERY appreciated. As I'm just a junior dev, and anything that can be improved is going to help me a lot.

Thank you! :)