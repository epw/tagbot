#! /usr/bin/env python

# This file is part of Tagbot

# Tagbot is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# Tagbot is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301 USA.

"""A program for editing the pickle-saved vocabularies understood by Tagbot.

Commands are list, del, add, save, and quit
"""

import getopt, pickle, re, sys

def usage():
    print "Usage: " + sys.argv[0] + " [options] file"
    print "Options (mutually exclusive):"
    print "\t-h\t--help\t\t\tView this"

def save (filename, dump):
    f = open (filename, "w")
    pickle.dump (dump, f)
    f.close()

def close (filename, dump, force=0):
    if force:
        sys.exit(0)
    
    print "\nQuit without saving? (y/N):",
    choice = raw_input()
    if choice in ('y', "yes"):
        sys.exit(0)
    save (filename, dump)
    sys.exit(0)

def main():
    saved = 0
    try:
        optlist, args = getopt.getopt (sys.argv[1:], 'h', ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    if len(args) < 1:
        usage()
        sys.exit(1)

    for o, a in optlist:
        if o in ('-h', "--help"):
            usage()
            sys.exit()

    filename = args[0]
    f = open (filename)

    vocab = pickle.load (f)
    f.close()
    while True:
        print ">",
        try:
            s = raw_input()
        except (EOFError, KeyboardInterrupt):
            close(filename, vocab, saved)
        
        if re.search ('^list', s):
            regex = re.search ('^list\s*(.*)$', s)
            if regex.group(1):
                if regex.group(1) in vocab.keys():
                    print regex.group(1) + ": " + str(vocab[regex.group(1)])
                else:
                    print "No such word in vocabulary."
            else:
                for key, value in vocab.iteritems():
                    print key + ": " + str(value)
        elif re.search ('^del', s):
            regex = re.search ('^del\s*(.*)$', s)
            if regex.group(1):
                if regex.group(1) in vocab.keys():
                    print "Deleting " + regex.group(1) + ": " + str(vocab[regex.group(1)])
                    del vocab[regex.group(1)]
                else:
                    print "No such word in vocabulary."
            else:
                print "Usage: del [key to be deleted]"
        elif re.search ('^add', s):
            regex = re.search ('^add\s*(.*)$', s)
            if regex.group(1):
                if regex.group(1) in vocab.keys():
                    print "Key " + regex.group(1) + " already exists!"
                    print regex.group(1) + ": " + str(vocab[regex.group(1)])
                else:
                    print "Value for new key " + regex.group(1) + ":",
                    try:
                        newval = input()
                    except:
                        print "Error, saving to /tmp/vocab and aborting."
                        save ("/tmp/vocab", vocab)
                        sys.exit(1)
                    vocab[regex.group(1)] = newval
            else:
                print "Usage: add [key to add]\n\tYou will be prompted for the value to use."
        elif s == 'save':
            save (filename, vocab)
            saved = 2
        elif s == 'quit':
            close (filename, vocab, saved)

        if saved:
            saved -= 1

if __name__ == "__main__":
    main()

