#!/bin/bash

# # # # # # # # # # #
# tempest installer #
# # # # # # # # # # #

echo "This file should only be run if you downloaded this from the 'Releases' section on github, or if you built tempest yourself and are in the dist/ directory."
echo "tempest installer will take these actions: "
echo "1) Copy 'tempest' executable into /usr/bin "
echo "2) Copy default templates and configs into ~/.local/share and ~/.config"
echo "Continue? [y/n] "

continue_install="n"
read continue_install
echo ""

if [ $continue_install == "y" ]; then
    sudo cp tempest /usr/bin
    cp -r templates/ ~/.config/tempest
    # copy configs here
fi

