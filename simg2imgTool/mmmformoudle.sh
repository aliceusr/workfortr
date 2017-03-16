#!/bin/bash

#PACKAGE_NAME = $3
#PACKAGE_DIR = $2
#ALPS = $1

echo 'ALPS: '$1
echo 'MOUDLE: '$2


cd $1
echo 'Enter alps..'

source  'build/envsetup.sh'
echo 'source build/envsetup.sh'
lunch 28
echo 'Lunch Project 28: sp7731c_1h10_native userdebug '
#cd $2
#echo 'Enter Package dir'
echo 'mmm  :'$2
mmm $2

