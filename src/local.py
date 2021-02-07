# cfg.py - KAS configuration

import os
import sys
from os import listdir
from shutil import copy2


# ------- collect -------
def collect(archive, repo):
    file = archive + os.sep + repo + '.txt'
    if not os.path.exists(file):
        print(f"ERROR: cannot find list of files and directories for repo: {file}")
        sys.exit(3)

    target = os.path.join(archive, repo)
    if not os.access(target, os.W_OK):
        print(f"ERROR: archive is not writable: {target}")
        sys.exit(3)

    print(f" = Reading file list: {file}")
    t = open(file, 'r')
    count = 0

    while True:
        count += 1
        src = t.readline()
        if not src:
            break

        # skip blank lines
        src = src.strip()
        if len(src) < 1:
            continue

        # skip lines beginning with comment character #
        if src.startswith("#"):
            continue

        # copy the item
        copy(src, target)

    t.close()
    print(' = Done')


# ------- copy -------
def copy(src, target):
    if os.path.exists(src):

        # files & links
        if os.path.isfile(src) or os.path.islink(src):
            folder = os.path.abspath(src)
            folder = os.path.dirname(folder)
            dest = make_directories(target, folder)
            file_copy(src, dest)

        # directories
        elif os.path.isdir(src):
            directory_copy(src, target)

        elif os.path.islink(src):
            print(f" ! LINK NOT HANDLED: {src}")

        else:
            print(f" ! UNKNOWN {src}")
    else:
        print(f" ! MISSING: {src}")


# ------- directory_copy -------
def directory_copy(src, target):
    folder = os.path.abspath(src)
    dest = make_directories(target, folder)
    print(f" D {src} => {dest} ")

    contents = listdir(folder)
    for item in contents:
        path = os.path.join(folder, item)
        if os.path.isfile(path):
            file_copy(path, dest)
        elif os.path.isdir(path):
            directory_copy(path, target)
        elif os.path.islink(path):
            print(f" ! LINK NOT HANDLED: {path}")
        else:
            print(f" ! UNKNOWN {path}")


# ------- file_copy -------
def file_copy(src, target):
    file = os.path.basename(src)
    dest = os.path.join(target, file)
    print(f" F {src} => {dest} ")
    copy2(src, dest, follow_symlinks=False)
    sa = os.stat(src, follow_symlinks=False)
    os.chown(dest, sa.st_uid, sa.st_gid)
    os.chmod(dest, sa.st_mode)


# ------- make_directories -------
def make_directories(target, folder):
    # walk each folder segment
    split = folder.split(os.sep)
    sp = ''
    tp = target
    for seg in split:
        if len(seg) < 1:
            continue

        # append source segment & get the source attributes
        sp = sp + os.sep + seg
        sa = os.stat(sp, follow_symlinks=False)

        # append target segment & create if needed
        tp = tp + os.sep + seg
        if not os.path.exists(tp):
            os.makedirs(tp)

        # set ownership & permissions
        os.chown(tp, sa.st_uid, sa.st_gid)
        os.chmod(tp, sa.st_mode)

    return tp

# end
