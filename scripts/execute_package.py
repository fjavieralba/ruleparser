#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import sys


def usage():
    print """
        execute_package.py [options]

options:

--help  Show help
"""


def main(argv):
    # Command line arguments
    try:
        optlist, args = getopt.getopt(argv, '', ['help'])
        for opt, value in optlist:
            if opt == '--help':
                usage()
                sys.exit()
    except getopt.GetoptError, err:
        print '\n' + str(err)
        usage()
        sys.exit(2)



if __name__ == '__main__':
    main(sys.argv[1:])
