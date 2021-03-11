# vcs_github.py - Version control functions for GitHub

import os
import shutil
import subprocess
import sys

import yaml

from github import Github


# ------- create -------
def create(archive, repo, flavor, url, name, token, is_private):
    target = archive + os.sep + repo

    # make sure git is available
    path = shutil.which('git')
    if len(path) < 1:
        print('ERROR: cannot find git')
        sys.exit(1)

    # change to the kas target root directory
    os.chdir(target)

    # init the git repo if it does not exist
    created = False
    if not os.path.exists(target + os.sep + ".git"):
        print(" + ", end='', flush=True)
        result = subprocess.run(["git", "init"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"ERROR: {result.stdout}")
            sys.exit(3)
        created = True
    else:
        print(f" = local repo {repo} already exists")

    # add README.md
    print(' = Attempting to add README.md')
    path = target + os.sep + "README.md"
    result = subprocess.run(["git", "add", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"ERROR: {result.stdout}")
        sys.exit(3)

    # commit
    print(' = Attempting to commit')
    if created:
        text = "KAS initial commit"
    else:
        text = "KAS commit"
    subprocess.run(["git", "commit", "-m", text])  # ignore any errors

    # set the branch name to default main
    print(' = Attempting to set branch name to main')
    result = subprocess.run(["git", "branch", "-M", "main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"ERROR: {result.stdout}")
        sys.exit(3)

    # create the new repo on GitHub
    if flavor == 'github':
        print(' = Existing GitHub repos:')
        g = Github(token)
        for there in g.get_user().get_repos():
            print("     " + there.name)
            if there.name == repo:
                print(f"ERROR: GitHub repo {repo} already exists")
                sys.exit(2)

        print(f"Attempting to create repo '{repo}' on GitHub")
        user = g.get_user()
        added = user.create_repo(repo, 'KAS repository', '', is_private)
        origin = added.clone_url
    else:
        if url[len(url - 1):] != "/":
            url += '/'
        origin = url + name

    # set the origin
    print(' = Attempting to set the remote origin')
    result = subprocess.run(["git", "remote", "add", "origin", origin], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        text = result.stdout
        if text != 'None':
            print(f"ERROR: {text}")
        sys.exit(3)

    source = 'https://' + token + '@github.com/' + name + '/' + repo + '.git'

    # push set upstream branch
    print(' = Attempting to push')
    result = subprocess.run(["git", "push", "--set-upstream", source, "main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"ERROR: {result.stdout}")
        sys.exit(3)

    print(' = Done')


# ------- commit -------
def commit(target):
    # make sure git is available
    path = shutil.which('git')
    if len(path) < 1:
        print('ERROR: cannot find git')
        sys.exit(1)

    # change to the kas target root directory
    os.chdir(target)

    print(' = Attempting to add files')
    result = subprocess.run(["git", "add", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"ERROR: {result.stdout}")
        sys.exit(3)

    print(' = Attempting to commit')
    result = subprocess.run(["git", "commit", "-m", "KAS commit", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        o = str(result.stdout)
        if o.count('nothing to commit') == 0:
            print(f"ERROR: {result.stdout}")
            sys.exit(3)

    print(' = Attempting to push')
    result = subprocess.run(["git", "push"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"ERROR: {result.stdout}")
        sys.exit(3)

    print(' = Done')


# ------- dumb_meta -------
def dumb_meta(archive, repo):
    file = archive + os.sep + repo + '.yaml'
    if not os.path.exists(file):
        print(f"ERROR: cannot find repo metadata file: {file}")
        sys.exit(3)

    print(f" = Reading metadata: {file}")
    with open(file) as m:
        meta = yaml.load(m, Loader=yaml.FullLoader)

    print(meta.get('flavor'))
    print(meta.get('url'))
    print(meta.get('repo'))
    print(meta.get('name'))
    print(meta.get('token'))
    print(meta.get('private'))


# ------- prompt_token -------
def prompt_token():
    print(" ? Enter git/GitHub access token:")
    answer = input(' : ')
    return answer


# ------- update -------
def update(target):
    # make sure git is available
    path = shutil.which('git')
    if len(path) < 1:
        print('ERROR: cannot find git')
        sys.exit(1)

    # change to the kas target root directory
    os.chdir(target)

    print(' = Attempting to update files')
    result = subprocess.run(["git", "pull", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"ERROR: {result.stdout}")
        sys.exit(3)

    print(' = Done')

# end
