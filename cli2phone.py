#!/usr/bin/env python

"""cli2phone pushes messages from the command line to your android phone.
Requires Android 2.2 or newer, and the chrometophone application installed.
See: http://code.google.com/p/chrometophone/

Usage: cli2phone URL
"""

import sys
import getopt
from auth import Auth

apiVersion = '5'
baseUrl = 'https://chrometophone.appspot.com/send?ver=' + apiVersion


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])

    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    if len(args) == 0:
        print __doc__

    else:
        for arg in args:
            send_url(arg)


def send_url(url):
    """Sends a URL to the phone"""

    params = {'url': url,
              'title': '',
              'sel': '',
              'type': '',
              'deviceType': 'ac2dm'}
    auth = Auth()
    auth.request(baseUrl, params)

if __name__ == "__main__":
    sys.exit(main())
