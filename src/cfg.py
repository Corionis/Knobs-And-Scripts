# cfg.py - KAS configuration

import os

import yaml


# ------- find -------
def find(base):
    # is it with the executable?
    cfg = base + os.sep + ".kas.yaml"
    if os.path.exists(cfg):
        return cfg

    # is it in the user home directory?
    cfg = os.path.expanduser('~') + os.sep + ".kas.yaml"
    if os.path.exists(cfg):
        return cfg

    # no configuration found
    return make()


# ------- get -------
def get(file):
    with open(file) as h:
        cfg = yaml.load(h, Loader=yaml.FullLoader)
        return cfg


# ------- make -------
def make():
    # default to the user home directory
    loc = os.path.expanduser('~') + os.sep

    config = f"# KAS - Knobs And Scripts configuration\n" \
             f"\n" \
             f"# location of archive to hold repositories\n" \
             f"archive: {loc}.kas-archive\n" \
             f"\n" \
             f"# parameters for the create -github option\n" \
             f"# uncomment the following github lines then\n" \
             f"# set username and token to valid values\n" \
             f"#githubApi: https://api.github.com/\n" \
             f"#githubUser: username\n" \
             f"#githubToken: token\n" \
             f"#githubPrivate: true\n"

    loc += '.kas.yaml'
    with open(loc, 'w') as o:
        o.writelines(config)

    print(f" + created new configuration file: {loc}")
    return loc
