#!/usr/bin/env python3
#
# crossplatform substitute for
# find . -type d -name .svn -prune -o -type f -print0 |xargs -0 ls -Tul
#
# usage: atime_dump.py [path]

import os, sys
from datetime import datetime

root = "."
if len(sys.argv) >= 2:
    root = sys.argv[1]

for path, dirs, fnames in os.walk(root):
    for fname in fnames:
        fpath = os.path.join(path, fname)
        ftime = os.path.getatime(fpath)
        print(datetime.fromtimestamp(ftime).isoformat() + "\t" + fpath)
        
    if ".svn" in dirs:
        dirs.remove(".svn")  # don't visit SVN directories
