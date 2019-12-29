# TODO Licensing
#      Get users preferred license from list (agpl, apache, etc)
#      Get desired name of file
# TODO Getting templates
#      Allow users to create templates based on directory?
#      '[name]/[repo]' format allows to pull from GitHub/GitLab
#      '[template]' format pulls from base template list
#           Created from user-made templates/default templates (npm, rust, etc)
# TODO Creation
#      Go down checklist--README.md, license, necessary config files (i.e. cargo.toml)
#      Create git repo
#      Prompt name/description of project--these are put into directory name/
#      README.md respectively
#      Macros? i.e. putting {NAME} in a file causes it to be replaced with the project name
# TODO QOL
#      Better --help (argparse?)

import argparse

parser = argparse.ArgumentParser(description='Creates a source-controlled directory given a template, or allows for creation of templates.')
commands = parser.add_mutually_exclusive_group(required=True)
commands.add_argument('-n', '--new', dest='template',
                    help='Creates a directory from a template')
commands.add_argument('-t', '--template', dest='directory',
                    help='Creates a new template given a directory')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)

def handle_creation():
    """Handles creation of a source-controlled directory given"""
    pass

def handle_templating():
    """Handles creating a template given a directory to base the template off of"""
    pass
