#!/usr/bin/env python
#coding:utf-8
# python ${simg2imgTool}/make_ota_Test.py ${product_chip} ${product_name}  ${new_version} ${old_version} ${ANDROID_HOME_dir} ${SIGN_KEY}
                                                      
import os
import sys
import zipfile
import glob
import time
import subprocess
import hashlib

def set_dev_info():
    global PRODUCTNAME
    global SCRIPT_PATH
    global APP_CONFIG_DIR
    global replaced_app
    global date_str
    global date_utc_str
    global file_time
    global simg2imgtooldir
    global ota_from_target_filestool
    global mt_ota_from_target_filestool
    global SIGN_KEY
    global input_sign_key
    global SIGN_KEYTOOL
    global APKSIGN_KEYDIR
    global CHIP
    global outzipfile
    global ANDROID_out_host_linux
    global ANDROID_ROMCODE
    global ANDROID_HOME_dir
    global new_version_file
    global old_version_file
    global PRODUCTotapackage_target_file
    global PRODUCTotapackage_target_file_diff
    ANDROID_HOME_dir=sys.argv[5]
    ANDROID_ROMCODE='/work/OSTeam/simg2img/ROMCODE'
    ANDROID_HOME_dir=ANDROID_ROMCODE+'/'+ANDROID_HOME_dir
    input_sign_key = None
    #SCRIPT_PATH = os.getcwd()
    SCRIPT_PATH = '/work/workspace/jenkins/proj/simg2imgTool'
    date_utc_str = subprocess.Popen('date +%s',stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True).communicate()[0].rstrip()
    date_str = subprocess.Popen('date',stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True).communicate()[0].rstrip()
    file_time = time.strftime("%Y%m%d%H",time.localtime(time.time()))
    SIGN_KEY = 'releasekey'
    if sys.argv[6] =='releasekey' or sys.argv[6] =='testkey' or sys.argv[6] =='shared' or sys.argv[6] =='media':
        SIGN_KEY=sys.argv[6]
    CHIP=sys.argv[1]
    PRODUCTNAME=sys.argv[2]
    APP_CONFIG_DIR=SCRIPT_PATH+'/config/'+PRODUCTNAME
    simg2imgtooldir=SCRIPT_PATH+'/tools/'
    PRODUCTotapackage_target_file='/work/OSTeam/simg2img/otapackage_target_file/'+PRODUCTNAME
    PRODUCTotapackage_target_file_diff='/work/OSTeam/simg2img/otapackage_target_file/'+PRODUCTNAME+'_diff'
    if not os.path.exists(PRODUCTotapackage_target_file):
        os.system('mkdir -p '+PRODUCTotapackage_target_file)
    if not os.path.exists(PRODUCTotapackage_target_file_diff):
        os.system('mkdir -p '+PRODUCTotapackage_target_file_diff)
    new_version_file = PRODUCTotapackage_target_file+'/'+sys.argv[3]
    old_version_file = PRODUCTotapackage_target_file+'/'+sys.argv[4]
    print ('new_version_file:'+str(new_version_file))
    print ('old_version_file:'+str(old_version_file))
    print ('CHIP:'+str(CHIP))
    print ('ANDROID_HOME_dir:'+str(ANDROID_HOME_dir))
    print ('PRODUCTNAME:'+str(PRODUCTNAME))
    ANDROID_out_host_linux=ANDROID_HOME_dir+'/out/host/linux-x86/'
    SIGN_KEYTOOL=ANDROID_HOME_dir+'/build/target/product/security/'
    APKSIGN_KEYDIR=SCRIPT_PATH+'/tools/'+CHIP+'/'+'/security'
    if not os.path.exists(SCRIPT_PATH+'/tools/'+CHIP+'/'+PRODUCTNAME+'/security/'):
        SIGN_KEYTOOL=SCRIPT_PATH+'/tools/'+CHIP+'/security/'
        APKSIGN_KEYDIR=SCRIPT_PATH+'/tools/'+CHIP+'/'+'/security'
    else:
        SIGN_KEYTOOL=SCRIPT_PATH+'/tools/'+CHIP+'/'+PRODUCTNAME+'/security/'
        APKSIGN_KEYDIR=SCRIPT_PATH+'/tools/'+CHIP+'/'+PRODUCTNAME+'/security'
    print ('SIGN_KEYTOOL:'+str(SIGN_KEYTOOL))
    print ('APKSIGN_KEYDIR:'+str(APKSIGN_KEYDIR))
    mt_ota_from_target_filestool='demo'
    if CHIP==('MTK'):
        mt_ota_from_target_filestool=ANDROID_HOME_dir+'/device/mediatek/build/releasetools/mt_ota_from_target_files'
    os.system('sudo  cp -rf '+SCRIPT_PATH+'/tools/'+CHIP+'/'+PRODUCTNAME+'/talpa_ota_update '+ANDROID_HOME_dir+'/build/tools/releasetools/talpa_ota_update')
    ota_from_target_filestool=ANDROID_HOME_dir+'/build/tools/releasetools/talpa_ota_update'
    os.chdir(ANDROID_HOME_dir)
    os.system('pwd')
    make_ota_diff(new_version_file,old_version_file,PRODUCTotapackage_target_file_diff)
    


def delet_nouse_file(dirpath,zip):
    s=os.listdir(dirpath)
    print ('...files '+str(s))
    for zf in s:
        if not zf.endswith('.zip') and zip:
            print ('delet_nouse_file:'+dirpath+'/'+str(zf))
            os.system('sudo rm -rf '+dirpath+'/'+zf)
        else:
            if not zf.endswith('.img') and zip==False:
                print ('delet_nouse_file:'+dirpath+'/'+str(zf))
                os.system('sudo rm -rf '+dirpath+'/'+zf)


#传入两个差异版本的tagert文件名称
def make_ota_diff(file1,file2,PRODUCTotapackage_target_file_diff):
    #time1 = os.path.basename(file1).split('-')[1]
    time2 = str(os.path.basename(file2).split('-')[1])+'-'+str(os.path.basename(file2).split('-')[2].replace('_update.zip',''))
    os.system('sudo chmod 777 ' + ota_from_target_filestool)
    if CHIP==('MTK'):
        cmd = ota_from_target_filestool + ' -k '+SIGN_KEYTOOL+SIGN_KEY+' -s '+mt_ota_from_target_filestool+' -i ' + file2 + ' ' + file1 + ' ' + PRODUCTotapackage_target_file_diff + '/' + os.path.basename(file1)[:-4] + '_' + time2 + '.zip'
    else:
        cmd = ota_from_target_filestool + ' -k '+SIGN_KEYTOOL+SIGN_KEY+' -i ' + file2 + ' ' + file1 + ' ' + PRODUCTotapackage_target_file_diff + '/' + os.path.basename(file1)[:-4] + '_' + time2 + '.zip'
    print ('cmd:'+str(cmd))
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    if input_sign_key != None:
        p.communicate(input_sign_key)
        p.wait()
    else:
        p.communicate()

if __name__ == '__main__':
    set_dev_info()