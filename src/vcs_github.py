# vcs_github.py - Version Control methods for GitHub

import os
import subprocess
import sys
from github import Github

# for GitHub
githubApi = 'https://api.github.com/'
githubUser = 'Corionis'
githubToken = '403bcc6e36124089eaed056b4cfe15b1a7609605'
githubPrivate = 'true'

# ------- create -------
def create(archive, name):
    os.chdir(archive)

    g = Github("403bcc6e36124089eaed056b4cfe15b1a7609605")

    # print("  ", end='', flush=True)
    # subprocess.run(["git", "init"])

    # curl -u USER https://api.github.com/user/repos -d '{"name":"NEW_REPO_NAME","private":false}'
    #gitCmd = githubApi + r"user/repos -d '\{\"name\":\"" + name + "\",\"private\":" + githubPrivate + "}'"
    gitCmd = "githubapi"
    print(f"gitCmd: {gitCmd} {name}")
    # subprocess.run("curl", f"-u {githubUser}:{githubToken} {gitCmd}")
