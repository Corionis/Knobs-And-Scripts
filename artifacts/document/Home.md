Knobs And Scripts is a utility to save, restore, and optionally 
version Linux settings (knobs) and scripts. Originally written to 
make rebuilding a system and sharing configurations easier KAS may 
be used at the system or user level.

## How KAS Works

KAS uses a local directory, the "*archive directory*", to store one 
or more "*repos*" of files and/or directories along with their paths
and permissions. The repo directory may optionally be versioned to 
a git or GitHub repository. Multiple named repositories are supported
within the archive directory.

The list of specific files and directories is up to the administrator or
user. The list is kept in a README.md file located in the root of the 
specified repo directory. An initial README.md is created when the 
repo is created. A matching YAML file is created in the archive directory
with the metadata needed.

For example, archve directory kas-archive with a repo named JackHome:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Archive directory example](https://github.com/Corionis/Knobs-And-Scripts/blob/main/artifacts/images/tree.png)

Note the README.md file is *not* copied to the system during the distribute command.

### Setup Commands

 * setup - Required first step to create a ~/.kas file defining the
   location of the archive directory.
   
 * create - Create a named repo within the archive directory and 
   optional matching git or GitHub repository.

### Local Commands

 * collect - Collects the files and directories defined in the README.md
   of a repo including the paths and permissions into the repo directory.
   
 * distribute - Distribute the files and directories from the repo 
   directory to their matching locations on the systerm including permissions.

### Repository Commands

 * commit - Commit and push the content of a repo directory to a git or GitHub
   repository.
   
 * update - Update a repo directory from the associated git or GitHub
   repository.

## Initial Setup

KAS can either create a new repo directory, and optionally a git or GitHub
repository or use an existing archive directory or repository.

 1. `kas setup --archive-directory [directory path]` create a ~/.kas file to define the location
    of the archive directory for subsequent commands.

### Using an Existing Repository

To use an existing git or GitHub repository:

 1. `mkdir [directory path]` the same directory specified during initial setup.
 2. `cd [directory path]` change to the new directory
 3. `git clone [repository url]`  clone the repository into the archive directory

### Using an Existing KAS Archive

If the KAS archive directory already exists or has been copied from 
another computer then be sure the `[directory path]` used with the
*setup* command matches that location.

Note the permissions of the existing items are used during the
*distribute* command. To move or copy a KAS archive directory to
another system use *tar* to capture the ownership and permissions.

### Creating a New Archive Directory

Use the *create* command to establish a new named repo inside the
KAS archive directory. A git or GitHub repo may also be created at
the same time. GitHub repos may be public or private.

Note: KAS depends on git being installed on the local system for 
some operations.

Example of creating a KAS repo named MyKAS that is also a private
GitHub repo owned by user JackFrost. The local and remote repositories 
are initialized and committed.

kas create --github --private --url `https://github.com` --name JackFrost --repo MyKAS

You will be prompted for the GitHub access token.

