#!/bin/bash

#PACKAGE_NAME = $3
#PACKAGE_DIR = $2
#ALPS = $1

echo 'ALPS: '$1
echo 'PACKAGE_DIR: '$2
echo 'PACKAGE_NAME: '$3

cd $1
echo 'Enter alps..'

source  'build/envsetup.sh'
echo 'source build/envsetup.sh'
lunch 39
echo 'Lunch Project'
cd $2
echo 'Enter Package dir'
mmm $3
echo 'mmm  success'
