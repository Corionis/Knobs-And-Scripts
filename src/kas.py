# KAS : Knobs And Scripts

import getpass
import os
import sys

import cfg

# Globals
global archive
global base
global flavor
global index
global location
global version
global versioned


# ------- banner -------
def banner():
    print(f"KAS: Knobs And Scripts, version {version}")


# ------- create -------
def create():
    global archive, index, location

    print('action: create')
    if len(sys.argv) > index:
        name = sys.argv[index]
        index += 1
    else:
        name = sys.platform + '_' + getpass.getuser()
        print(f" ! no archive name specified, using default: {name}")

    archive = location + os.sep + name
    if not os.path.exists(archive):
        os.makedirs(archive, exist_ok=True)
        print(f" + created archive directory: {archive}")
    else:
        print(f" = archive directory exists: {archive}")

    if versioned:
        print(f" = vcs type: {flavor}")
        vcs.create(archive, name)


# ------- collect -------
def collect():
    print('action: collect')


# ------- usage -------
def usage():
    print()
    print("usage")
    sys.exit(1)


# ------- main --------------------------------------------------------------
if __name__ == '__main__':

    # initialize
    index = 1
    flavor = 'none'
    version = 1.0
    versioned = False

    # get the base executable directory
    base = os.path.dirname(__file__)
    base = os.path.dirname(base)
    base = os.path.abspath(base)

    banner()
    print('start:')
    print(f" = runtime: {base}")

    # Add init command that creates .kas.yaml with location only
    # Change create to use parameters for username, token, etc. and create an [archive].yaml
    # in the location directory for the archive subdirectory.
    # This allows different archives to use different vcs

    # read the configuration
    file = cfg.find(base)
    cfg = cfg.get(file)

    location = cfg.get('archive')
    print(f" = archive directory: {location}")

    cmd = '-'
    if len(sys.argv) > index:
        # get the command
        cmd = sys.argv[index]
        index += 1

        # see if there is a vcs option
        if len(sys.argv) > index and sys.argv[index] == '-github':
            index += 1
            flavor = 'github'
            versioned = True
            import vcs_github as vcs

        # process the command
        if cmd == 'create':
            create()
        elif cmd == 'pull':
            print('pull')
        elif cmd == 'commit':
            print('comment')
        elif cmd == 'push':
            print('push')
        elif cmd == 'collect':
            print('collect')
        elif cmd == 'distribute':
            print('distribute')
        else:
            print(f"ERROR: unknown action: {cmd}")
            usage()
    else:
        usage()

print()
# end
