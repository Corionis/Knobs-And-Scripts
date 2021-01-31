# vcs_github.py - KAS version control functions for GitHub

import os

from github import Github

# for GitHub
githubApi = 'https://api.github.com/'
githubUser = 'Corionis'
githubToken = '403bcc6e36124089eaed056b4cfe15b1a7609605'
githubPrivate = 'true'

# ------- create -------
def create(archive, repo, flavor, url, name, token, is_private):
    os.chdir(archive)

    txt = f"archive = {archive} " \
    f"repo = {repo} " \
    f"flavor = {flavor} " \
    f"url = {url} " \
    f"user = {name} " \
    f"token = {token} " \
    f"private = {is_private}"
    print(txt)

    #g = Github("403bcc6e36124089eaed056b4cfe15b1a7609605")

    # print("  ", end='', flush=True)
    # subprocess.run(["git", "init"])

    # curl -u USER https://api.github.com/user/repos -d '{"name":"NEW_REPO_NAME","private":false}'
    #gitCmd = githubApi + r"user/repos -d '\{\"name\":\"" + name + "\",\"private\":" + githubPrivate + "}'"
    # subprocess.run("curl", f"-u {githubUser}:{githubToken} {gitCmd}")
