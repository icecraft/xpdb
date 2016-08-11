# -*- coding: utf-8 -*-
import sys
import os
import traceback
from .xpdb import XPdb, Restart


def main():
    print sys.argv
    if not sys.argv[1:] or sys.argv[1] in ("--help", "-h"):
        print "usage: xpdb.py scriptfile [arg] ..."
        sys.exit(2)

    mainpyfile = sys.argv[1]     # Get script filename
    if not os.path.exists(mainpyfile):
        print 'Error:', mainpyfile, 'does not exist'
        sys.exit(1)


    # Replace xpdb's dir with script's dir in front of module search path.
    sys.path[0] = os.path.dirname(mainpyfile)

    # Note on saving/restoring sys.argv: it's a good idea when sys.argv was
    # modified by the script being debugged. It's a bad idea when it was
    # changed by the user from the command line. There is a "restart" command
    # which allows explicit specification of command line arguments.
    xpdb = XPdb()
    while True:
        try:
            xpdb._runscript(mainpyfile)
            if xpdb._user_requested_quit:
                break
            print "The program finished and will be restarted"
        except Restart:
            print "Restarting", mainpyfile, "with arguments:"
            print "\t" + " ".join(sys.argv[1:])
        except SystemExit:
            # In most cases SystemExit does not warrant a post-mortem session.
            print "The program exited via sys.exit(). Exit status: ",
            print sys.exc_info()[1]
        except:
            traceback.print_exc()
            print "Uncaught exception. Entering post mortem debugging"
            print "Running 'cont' or 'step' will restart the program"
            t = sys.exc_info()[2]
            xpdb.interaction(None, t)
            print "Post mortem debugger finished. The " + mainpyfile + \
                  " will be restarted"

            
