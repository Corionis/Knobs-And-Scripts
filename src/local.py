# cfg.py - KAS configuration

import os
import sys


# ------- collect -------
def collect(archive, repo):
    file = archive + os.sep + repo + '.txt'
    if not os.path.exists(file):
        print(f"ERROR: cannot find list of files and directories for repo: {file}")
        sys.exit(3)

    print(f" = Reading file list: {file}")
    l = open(file, 'r')
    count = 0

    while True:
        count += 1
        line = l.readline()
        if not line:
            break

        # skip blank lines
        line = line.strip()
        if len(line) < 1:
            continue

        # skip lines beginning with comment character #
        if line.startswith("#"):
            continue

        print(line)

    l.close()
