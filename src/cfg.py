# cfg.py - KAS configuration

import os

import yaml


# ------- find -------
def find(base):
    # is it with the executable?
    cfg = base + os.sep + ".kas"
    if os.path.exists(cfg):
        return cfg

    # is it in the user home directory?
    cfg = os.path.expanduser('~') + os.sep + ".kas"
    if os.path.exists(cfg):
        return cfg

    # no configuration found
    return ''


# ------- get -------
def get(file):
    with open(file) as h:
        cfg = yaml.load(h, Loader=yaml.FullLoader)
        return cfg


# ------- setup -------
def setup(loc):
    config = f"# KAS - Knobs And Scripts configuration\n" \
             f"\n" \
             f"# location of kas archive directory to hold repositories\n" \
             f"archive: {loc}\n" \
             f"\n"

    file = os.path.expanduser('~') + os.sep + '.kas'
    with open(file, 'w') as o:
        o.writelines(config)

    print(f" + created new configuration file: {file} with archive location: {loc}")
    return file


# end
