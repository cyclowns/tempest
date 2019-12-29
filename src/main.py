# TODO Licensing
#      Get users preferred license from list (agpl, apache, etc)
#      Get desired name of file
# TODO Getting templates
#      Allow users to create templates based on directory?
#      '[name]/[repo]' format allows to pull from GitHub/GitLab
#      '[template]' format pulls from base template list
#           Created from user-made templates/default templates (npm, rust, etc)
# TODO Creating template
#      Make sure cant have '/' in name--would conflict with regex
# TODO Creation
#      Go down checklist--README.md, license, necessary config files (i.e. cargo.toml)
#      Create git repo
#      Prompt name/description of project--these are put into directory name/
#      README.md respectively
#      Macros? i.e. putting {NAME} in a file causes it to be replaced with the project name
# TODO QOL
#      Better --help (argparse?)

import argparse
import subprocess
import requests
import os

parser = argparse.ArgumentParser(description='Creates a source-controlled directory given a template, or allows for creation of templates.')
commands = parser.add_mutually_exclusive_group(required=True)
commands.add_argument('-n', '--new', dest='template',
                    help='Creates a directory from a template')
commands.add_argument('-t', '--template', dest='directory',
                    help='Creates a new template given a directory')

def handle_creation(template):
    """Handles creation of a source-controlled directory given a template (either a github repo, default template, or user-created template)"""
    name = input("Name of project?\n")
    desc = input("Brief description of project?\n")
    license_name = input("Desired license? [e.g. gpl-3.0, mit, unlicense]\n")
    license_text = get_license_text(license_name)

def get_license_text(name):
    """Returns text of a certain license given its name"""
    # https://developer.github.com/v3/licenses/#list-commonly-used-licenses
    licenses = { "mit": "mit",
                 "lgpl": "lgpl-3.0",
                 "mpl": "mpl-2.0",
                 "agpl": "agpl-3.0",
                 "unlicense": "unlicense",
                 "apache": "apache-2.0",
                 "gpl": "gpl-3.0"
               }

    for k in licenses:
        if k in name: # e.g. typing "apachev2" instead of "apache-2.0" still works
            res = requests.get(f"https://api.github.com/licenses/{licenses[k]}")
            if res and res.status_code == 200:
                return res.json()["body"]
            else:
                print("Couldn't retrieve license!")
                quit()

def handle_templating(directory):
    """Handles creating a template given a directory to base the template off of"""
    pass

if __name__ == "__main__":
    args = parser.parse_args()
    if args.template:
        handle_creation(args.template)
    elif args.directory:
        handle_templating(args.directory)
