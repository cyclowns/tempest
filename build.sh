#!/bin/bash

# # # # # # # # # # # #
# tempest auto-build  #
# # # # # # # # # # # #

echo "Make sure you have pip installed and in your PATH!"
echo "tempest build.sh will take the following actions:"
echo "1) Use pyinstaller to package the source code into an executable"
echo "2) Copy all necessary files into the dist/ folder"
echo "Do you want to continue? [y/n] "

continue_build="n"
read continue_build
echo ""

if [ $continue_build == "y" ]; then
    if [ -d dist ]; then rm -rf dist; fi
    mkdir dist
    cp LICENSE dist/
    cp README.md dist/
    cp install.sh dist/
    cp templates/ dist/

    sudo pip install -r requirements.txt
    pyinstaller src/main.py --clean --onefile --distpath dist -n tempest

    rm -r build
    rm tempest.spec
    echo "Done!"
fi
