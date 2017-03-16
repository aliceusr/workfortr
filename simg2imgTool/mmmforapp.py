#!/usr/bin/env python
import os
import sys
import subprocess

def mmm():
    global PACKAGE_NAME
    global 	PACKAGE_DIR
    global ALPS
    
    ALPS = sys.argv[1]
    print ('alps: ')+ALPS
    PACKAGE_DIR = sys.argv[2]
    print ('PACKAGE_DIR: ')+PACKAGE_DIR
    PACKAGE_NAME = sys.argv[3]
    print ('PACKAGE_NAME: ')+PACKAGE_NAME
    
    os.chdir(ALPS)
    #os.system('source build/envsetup.sh')
    #os.system('lunch 39')
    cmd = 'source '+ ALPS+'build/envsetup.sh'
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    outs=p.communicate()
    
    cmd1 = 'lunch 39'
    p = subprocess.Popen(cmd1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    outs=p.communicate()
    
    
    os.chdir(PACKAGE_DIR)
    
    cmd2 = 'mmm '+PACKAGE_NAME
    p = subprocess.Popen(cmd2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    outs=p.communicate()
    
    #os.system('mmm'+' '+PACKAGE_NAME)
    
    

if __name__ == '__main__':
    mmm()