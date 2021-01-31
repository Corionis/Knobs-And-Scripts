# KAS : Knobs And Scripts

from datetime import datetime
import getopt
import getpass
import os
import sys

import cfg

# Globals
global archive  # directory of repo(s), where it is all kept
global base  # directory of this executable
global flavor  # type of vcs, if any
global index  # sys.argv index
global repo  # the specific fileset location, with or without a vcs
global url # the url of the optional vcs
global version  # this executable version
global versioned  # is a vcs being used, True/False


# ------- banner -------
def banner():
    print(f"KAS: Knobs And Scripts, version {version}")


# ------- create -------
# kas create [-g|--git|-h|--github] [-p|--private] [-u|--url url] [-n|--name username] [-t|--token token] [-r repo]
def create():
    global archive, flavor, index, repo, url, versioned

    print('action: create')
    is_git = False
    is_github = False
    is_private = False
    url = ''
    name = ''
    token = ''
    repo = ''
    vcs = None

    try:
        #noinspection SpellCheckingInspection
        options = 'ghpu:n:t:r:'
        long_opts = ['git', 'github', 'private', 'url=', 'name=', 'token=', 'repo=']
        opts, args = getopt.getopt(sys.argv[index:], options, long_opts)
    except getopt.GetoptError:
        msg = getopt.error
        print(f"ERROR: {msg}")
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-g', '--git'):
            flavor = 'git'
            is_git = True
        if opt in ('-h', '--github'):
            flavor = 'github'
            is_github = True
        if opt in ('-p', '--private'):
            is_private = True
        if opt in ('-u', '--url'):
            url = arg
        if opt in ('-n', '--name'):
            name = arg
        if opt in ('-t', '--token'):
            token = arg
        if opt in ('-r', '--repo'):
            repo = arg

    # sanity checks
    if is_git and is_github:
        print("ERROR: can only use --git or --github")
        sys.exit(2)
    if is_git or is_github:
        if len(url) == 0:
            print("ERROR: --url required")
            sys.exit(2)
        if len(name) == 0:
            print("ERROR: --name required")
            sys.exit(2)
        if len(token) == 0:
            print("ERROR: --token required")
            sys.exit(2)
        import vcs_github as vcs
        versioned = True
    if is_private and not is_github:
        print("ERROR: --private is only used wit --github")
        sys.exit(2)
    if len(repo) == 0:
        repo = getpass.getuser() + '_' + sys.platform
        print(f" ! repo name not specified, using default: {repo}")

    # create the archive + repo directory
    archive = archive + os.sep + repo
    if not os.path.exists(archive):
        # os.makedirs(archive, exist_ok=True)
        print(f" + created archive directory: {archive}")
    else:
        print(f" = archive directory exists: {archive}")

    # create the git or github repo
    if versioned:
        print(f" = vcs type: {flavor}")
        vcs.create(archive, repo, flavor, url, name, token, is_private)

    # create the metadata file
    # now = datetime.now()
    # stamp = now.strftime("%d %M %y %H:%M:%S")
    # meta = f"# KAS repo {repo}" \
    #        f"# Created: {stamp} by {getpass.getuser()}" \
    #        f"repo = {repo}" \
    #        f"flavor = {flavor}" \
    #        f"url = {url}" \
    #        f"user = {name}" \
    #        f"token = {token}" \
    #        f"private = {is_private}"
    #
    # keep = archive + os.sep + repo + '.yaml'
    # with open(keep, 'w') as o:
    #     o.writelines(meta)


# ------- collect -------
def collect():
    print('action: collect')


# ------- commit -------
def commit():
    print('action: commit')


# ------- distribute -------
def distribute():
    print('action: distribute')


# ------- pull -------
def pull():
    print('action: pull')


# ------- push -------
def push():
    print('action: push')


# ------- setup -------
def setup():
    global index

    print('action: setup')
    if len(sys.argv) > index:
        arc = sys.argv[index]
        index += 1
    else:
        arc = os.path.expanduser('~') + os.sep + 'kas-archive'
        print(f" ! archive directory not specified, using default: {arc}")

    if len(archive) > 0:
        answer = input(f"archive {archive} is already setup. Do you want to change it (y/N)? ")
        answer = answer.lower()
        if not answer == 'y':
            return

    cfg.setup(arc)


# ------- usage -------
def usage():
    print()
    print("usage")
    sys.exit(1)


# ------- main --------------------------------------------------------------
if __name__ == '__main__':

    # initialize
    archive = ''
    index = 1
    flavor = 'none'
    version = 1.0
    versioned = False

    # get the base executable directory
    base = os.path.dirname(__file__)
    base = os.path.dirname(base)
    base = os.path.abspath(base)

    banner()
    print(f" = base: {base}")

    cmd = '-'
    if len(sys.argv) > index:

        # get the command
        cmd = sys.argv[index]
        index += 1

        # read the configuration
        file = cfg.find(base)
        if len(file) > 0:
            kas = cfg.get(file)
            archive = kas.get('archive')
            if len(archive) == 0:
                print(f"ERROR: configuration file {file} has an empty archive definition")
                sys.exit(1)
            print(f" = archive directory: {archive}")
        else:
            if not cmd == 'setup':
                print("ERROR: configuration file .kas cannot be found. Use setup command")
                sys.exit(1)

        # vcs commands -------
        print()
        if cmd == 'create':
            create()
        elif cmd == 'pull':
            pull()
        elif cmd == 'commit':
            commit()
        elif cmd == 'push':
            push()
        # kas commands -------
        elif cmd == 'collect':
            collect()
        elif cmd == 'distribute':
            distribute()
        elif cmd == 'setup':
            setup()
        else:
            print(f"ERROR: unknown action: {cmd}")
            usage()
    else:
        usage()

print()
# end
