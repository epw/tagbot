#! /usr/bin/env python

import sys, tagbot, time, urllib

tag = tagbot.Tagbot()

def tagboard (message=None):
    if message is None:
        post = urllib.urlopen ("http://www2.cbox.ws/box/index.php?boxid=1076239&boxtag=5732&sec=submit")
    else:
        data = urllib.urlencode ((('nme', tag.name),
                                  ('cstr', message)))
        post = urllib.urlopen ("http://www2.cbox.ws/box/index.php?boxid=1076239&boxtag=5732&sec=submit", data)

    text = post.read ()
    post.close ()
    return text

while True:
    time.sleep (10)
    try:
        text = tagboard ()
        
