# TODO Licensing
#      Get users preferred license from list (agpl, apache, etc)
#      Get desired name of file
# TODO Getting templates
#      Allow users to create templates based on directory?
#      "[name]/[repo]" format allows to pull from GitHub/GitLab
#      "[template]" format pulls from base template list
#           Created from user-made templates/default templates (npm, rust, etc)
# TODO Creating template Make sure cant have "/" in name--would conflict with regex tempest.yml config file?  This config file should act like a .gitignore as well as include all
#      info as to which files should be acted upon with respect to macros
# TODO Creation
#      Make sure a git repo URL is asked for (and set remote origin to it)
#      Go down checklist--README.md, license, necessary config files (i.e. cargo.toml)
#      Create git repo
#      Prompt name/description of project--these are put into directory name/
#      README.md respectively
#      !!! Macros? i.e. putting {NAME} in a file causes it to be replaced with the project name
# TODO Macros
#      Tempest config file specifies files to replace
#      {NAME}, {DESCRIPTION}, {LICENSE}, {VERSION} etc. Maybe a diff format?
# TODO QOL
# TODO Support
#      Windows support!!!

import os
import argparse
import subprocess
import requests

from shutil import copytree, rmtree
from git import Repo

PARSER = argparse.ArgumentParser(description="Creates a source-controlled directory \
                                 given a template, or allows for creation of templates.")
COMMANDS = PARSER.add_mutually_exclusive_group(required=True)
COMMANDS.add_argument("-n", "--new", dest="template",
                      help="Creates a directory from a template")
COMMANDS.add_argument("-t", "--template", dest="directory",
                      help="Creates a new template given a directory")

def handle_creation(template):
    """Handles creation of a source-controlled directory given a template (either a github repo, default template, or user-created template)"""
    project_name = input("Name of project?\n")
    if "/" in project_name:
        print("Name cannot have a '/' character!")
        return
    desc = input("\nBrief description of project?\n")
    license_name = input("\nDesired license? [e.g. gpl-3.0, mit, unlicense]\n")
    license_text = get_license_text(license_name)

    # check what format template is in
    repo_url = None
    base_template = None
    if "/" in template: # git repository format e.g. 'cyclowns/tempest'
        print(f"\nTreating {template} as git repository.")

        git_choice = None
        print("Use Github or Gitlab for cloning?")
        while True:
            git_choice = int(input("1) Github\n2) Gitlab\n3) Neither (standalone git repository)\n"))
            if git_choice in [1, 2, 3]:
                break
        if git_choice == 1:
            repo_url = f"https://github.com/{template}"
        elif git_choice == 2:
            repo_url = f"https://gitlab.com/{template}"
        else:
            repo_url = template # assumed that the user will provide a full link to their remote repo
    else: # use a template in ~/.config/tempest
        print(f"\nTreating {template} as preinstalled template.")
        templates_folder = os.path.expanduser("~/.config/tempest/")
        if not os.path.isdir(templates_folder):
            print("tempest templates folder not found at ~/.config/tempest!")
            return
        elif not template in os.listdir(templates_folder):
            print(f"template {template} not found in ~/.config/tempest!")
            return
        else:
            base_template = os.path.join(templates_folder, template)

    # we can now start actually creating the new project
    print(f"\nCreating project named {project_name}...")
    if os.path.isdir(project_name):
        print(f"Directory {project_name} already exists!")
        return
    if repo_url: # clone from git repo to create base folder
        try:
            Repo.clone_from(repo_url, project_name)
        except:
            print(f"Repository {repo_url} is not valid!")
            return
    elif base_template:
        copytree(base_template, project_name)
    print(f"Created folder {project_name} from template {template}!")

    os.chdir(project_name)
    if os.path.isdir(".git"): # delete git history if it exists
        rmtree(".git")
    print("\nCreating empty git repo...")
    subprocess.run(["git", "init", "."])

    print("\nCreating README and license...")
    overwrite = None
    if os.path.exists("README.md") or os.path.exists("LICENSE"):
        while True:
            overwrite = input("README or LICENSE file already exist. Overwrite? (y/n) ")
            if overwrite.lower() in ["y", "n"]:
                break
    if overwrite == "y":
        os.remove("README.md")
        os.remove("LICENSE")
    with open("README.md", "w") as file:
        file.write(f"# {project_name}\n\n{desc}")
    with open("LICENSE", "w") as file:
        file.write(license_text)
    print("\nDone!")

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
            res = requests.get(f"https://api.github.com/licenses/{licenses[k]}") # TODO maybe make sure this is a more permanent link
            if res and res.status_code == 200:
                return res.json()["body"]
            else:
                print("Couldn't retrieve license!")
                quit()

def handle_templating(directory):
    """Handles creating a template given a directory to base the template off"""

if __name__ == "__main__":
    ARGS = PARSER.parse_args()
    if ARGS.template:
        handle_creation(ARGS.template)
    elif ARGS.directory:
        handle_templating(ARGS.directory)
