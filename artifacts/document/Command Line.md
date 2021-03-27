KAS is a command-line tool with several commands, each with their own options.

For the versioning option command-line git must be available.

## Command Line Options

The options for short- and long-versions are case-sensitive.

### KAS Commands

 * collect [-r|--repo repo]
      
   Collect local files based on those listed in -r|--repo repo/README.md and
   copy them to the archive directory. Otionally specify the repo name, default: user_platform, e.g. billy_linux

 * commit [-r|--repo repo]
      
   Add all archive files in -r|--repo repo and commit them to the git/GitHub.
   Optionally specify the repo name, default: user_platform, e.g. billy_linux

 * create [-g|--git|-h|--github] [-p|--private] [-t|--token token] [-u|--url url]
      [-n|--name username] [-r|--repo repo]
      
   Create a repo in the archive directory.
     * optionally create the repo for -g|--git or -h|--github.
     * optionally make the git/GitHub repo -p|--private, default: public.
     * optionally set the -t|--token to access git/GitHub repo, default: prompt
     * for git/GitHub specify the -u|--url to git/GitHub.
     * for git/GitHub specify the -n|--name username.
     * optionally specify the repo name, default: user_platform, e.g. billy_linux

 * distribute [-r|--repo repo]
      
   Distribute archive files in -r|--repo repo copy files to the system.
   Optionally specify the repo name, default: user_platform, e.g. billy_linux

 * setup -a|--archive directory
      
   Set up a ~/.kas file with the directory as the KAS -a|--archive directory.

 * update [-r|--repo repo]
      
      Update -r|--repo repo from git/GitHub.
      Optionally specify the repo name, default: user_platform, e.g. billy_linux
      
