#!/usr/bin/env python
"""
Enables writting messages to one common logfile.
"""
# TODO: use log from stdlib

import sys
# suppress Biopythons PDBConstructionWarnings
import warnings
warnings.filterwarnings('ignore')


class Log:
    """
    Log messages generated by ModeRNA.
    """
    def __init__(self, file_name='moderna.log'):
        """Giving a log file name is optional."""
        self.file_name = file_name
        self.contents = []  # list or dict or ? just for keeping messages
        self.add_header()
        self.write_to_stderr = True
        self.raise_exceptions = True
        self.print_all = False

    def __del__(self):
        """
        It is called before an object of this class is destroyed.
        """
        if self.contents:
            self.write_logfile()

    def set_filename(self, name):
        """Sets the name of the log file."""
        self.file_name = name

    def write_message(self, message):
        """Adds a string message to the log."""
        self.contents.append(message + '\n')
        if self.print_all:
            print(message)

    def write_error(self):
        """Adds an Exception to the log."""
        error = sys.exc_info()[0]
        self.contents.append('\nERROR: ' + str(error) + '\n')
        # also writing errors to stderr, so they are visible
        # in the console and shell
        if self.write_to_stderr:
            sys.stderr.write(str(error) + '\n')

    def write_logfile(self):
        """Writes all log messages to a file."""
        with open(self.file_name, 'w') as f:
            f.writelines(self.contents)
        self.clear_logfile()
        self.add_header()

    def clear_logfile(self):
        """Clears all log messages."""
        self.contents = []

    def add_header(self):
        """Generates the header on top of the log file."""
        header = """\
________________________________________________________________

    ModeRNA (C) 2009 by Magdalena Rother & Kristian Rother,
                         Tomasz Puton, Janusz M. Bujnicki

    Building RNA 3D models with comparative modeling approach.

    support: lenam@amu.edu.pl
________________________________________________________________

        \n"""
        self.contents.append(header)

    def redirect_stdout(self, filename='stdout.txt'):
        """Redirects all print statements to a text file"""
        stdout = open(filename, 'w')
        sys.stdout = stdout
        print('\nModerna Test Suite\n')


log = Log()
