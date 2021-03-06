# local.py - Local file and directory operations

import os
import sys
from os import listdir
from shutil import copy2


#======= commands ==========================================

# ------- collect -------
def collect(archive, repo):
    file = archive + os.sep + repo + os.sep + "README.md"
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
        collect_item(src, target)

    t.close()
    print(' = Done')


# ------- distribute -------
def distribute(archive, repo):
    source = os.path.join(archive, repo)
    if not os.path.exists(source):
        print(f"ERROR: archive not found: {source}")
        sys.exit(3)

    # process root of archive here; subdirectories are handled by distribute_directory()
    print(f" = Reading archive: {source}")
    contents = listdir(source)
    for item in contents:
        if item == 'README.md' or item == '.git':  # only in root of archive
            continue

        src = os.path.join(source, item)
        dest = f"{os.sep}{item}"
        if os.path.isfile(src) or os.path.islink(src):
            distribute_file(src, dest)
        elif os.path.isdir(src):
            distribute_directory(src, dest)
        else:
            print(f" ! UNKNOWN {src}")

    print(' = Done')


# ======= functions ==========================================

# ------- collect_item -------
def collect_item(src, target):
    if os.path.exists(src):

        # files & links
        if os.path.isfile(src) or os.path.islink(src):
            folder = os.path.abspath(src)
            folder = os.path.dirname(folder)
            dest = make_archive_subdirectories(target, folder)
            collect_file(src, dest)

        # directories
        elif os.path.isdir(src):
            collect_directory(src, target)

        elif os.path.islink(src):  # todo remove this after links are tested
            print(f" ! LINK NOT HANDLED: {src}")

        else:
            print(f" ! UNKNOWN {src}")
    else:
        print(f" ! MISSING: {src}")


# ------- collect_directory -------
def collect_directory(src, target):
    folder = os.path.abspath(src)
    dest = make_archive_subdirectories(target, folder)
    print(f" D {src} => {dest} ")

    contents = listdir(folder)
    for item in contents:
        path = os.path.join(folder, item)
        if os.path.isfile(path):
            collect_file(path, dest)
        elif os.path.isdir(path):
            collect_directory(path, target)
        elif os.path.islink(path):
            print(f" ! LINK NOT HANDLED: {path}")
        else:
            print(f" ! UNKNOWN {path}")


# ------- collect_file -------
def collect_file(src, target):
    file = os.path.basename(src)
    dest = os.path.join(target, file)
    print(f" F {src} => {dest} ")
    copy2(src, dest, follow_symlinks=False)
    sa = os.stat(src, follow_symlinks=False)
    os.chown(dest, sa.st_uid, sa.st_gid)
    os.chmod(dest, sa.st_mode)


# ------- distribute_directory -------
def distribute_directory(src, dest):
    dest = make_target_subdirectory(src, dest)
    print(f" D {src} => {dest} ")

    contents = listdir(src)
    for item in contents:
        path = os.path.join(src, item)
        if os.path.isfile(path):
            target = dest + os.sep + item
            distribute_file(path, target)
        elif os.path.isdir(path):
            target = dest + os.sep + item
            distribute_directory(path, target)
        elif os.path.islink(path):
            print(f" ! LINK NOT HANDLED: {path}")
        else:
            print(f" ! UNKNOWN {path}")


# ------- distribute_file -------
def distribute_file(src, dest):
    print(f" F {src} => {dest} ")
    copy2(src, dest, follow_symlinks=False)
    sa = os.stat(src, follow_symlinks=False)
    os.chown(dest, sa.st_uid, sa.st_gid)
    os.chmod(dest, sa.st_mode)


# ------- make_archive_subdirectories -------
def make_archive_subdirectories(target, folder):
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

        # always (re)set ownership & permissions
        os.chown(tp, sa.st_uid, sa.st_gid)
        os.chmod(tp, sa.st_mode)

    return tp


# ------- make_target_subdirectory -------
def make_target_subdirectory(source, target):
    sa = os.stat(source, follow_symlinks=False)

    if not os.path.exists(target):
        os.makedirs(target)

        # only set ownership & permissions if created
        print(f"SETTING PERMISSIONS, on {target} mode {sa.st_mode}")
        os.chown(target, sa.st_uid, sa.st_gid)
        os.chmod(target, sa.st_mode)

    return target


# end
