#!/usr/bin/env python
#coding:utf-8
# make_target_ota.py
# python ${simg2imgTool}/simg2imgTool.py ${product_chip} ${product_name} ${osapp_zip_name}  ${ANDROID_HOME_dir} ${SIGN_KEY}
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
    global appversion
    global productdir
    global outotatargetrepkg_dir
    global simg2imgtooldir
    global ota_from_target_filestool
    global mt_ota_from_target_filestool
    global SIGN_KEY
    global input_sign_key
    global apkmodules
    global SIGN_KEYTOOL
    global APKSIGN_KEYDIR
    global lib
    global CHIP
    global APKreSIGN
    global out_osapp_zip_dir
    global osapp_zip_name
    global target_file_name
    global outzipfile
    global ANDROID_out_host_linux
    global ANDROID_ROMCODE
    global ANDROID_HOME_dir
    global PRODUCTotapackage_target_file
    replaced_app=[]
    ANDROID_HOME_dir=sys.argv[4]
    ANDROID_ROMCODE='/work/OSTeam/simg2img/ROMCODE'
    ANDROID_HOME_dir=ANDROID_ROMCODE+'/'+ANDROID_HOME_dir
    osapp_zip_name=sys.argv[3]
    target_file_name = ''
    productdir='/work/OSTeam/simg2img/package_dir'
    lib = 'lib'
    APKreSIGN=True
    apkmodules={}
    input_sign_key = None
    #SCRIPT_PATH = os.getcwd()
    SCRIPT_PATH = '/work/workspace/jenkins/proj/simg2imgTool'
    date_utc_str = subprocess.Popen('date +%s',stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True).communicate()[0].rstrip()
    date_str = subprocess.Popen('date',stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True).communicate()[0].rstrip()
    file_time = time.strftime("%Y%m%d%H",time.localtime(time.time()))
    SIGN_KEY = 'releasekey'
    if sys.argv[5] =='releasekey' or sys.argv[5] =='testkey' or sys.argv[5] =='shared' or sys.argv[5] =='media':
        SIGN_KEY=sys.argv[5]
    CHIP=sys.argv[1]
    PRODUCTNAME=sys.argv[2]
    APP_CONFIG_DIR=SCRIPT_PATH+'/config/'+PRODUCTNAME
    simg2imgtooldir=SCRIPT_PATH+'/tools/'
    outotatargetrepkg_dir='/work/OSTeam/simg2img/out_ota/'+PRODUCTNAME
    out_osapp_zip_dir='/work/OSTeam/simg2img/out_osapp_zip_dir'
    PRODUCTotapackage_target_file='/work/OSTeam/simg2img/otapackage_target_file/'+PRODUCTNAME
    if not os.path.exists(PRODUCTotapackage_target_file):
        os.system('mkdir -p '+PRODUCTotapackage_target_file)
    print ('CHIP:'+str(CHIP))
    print ('ANDROID_HOME_dir:'+str(ANDROID_HOME_dir))
    print ('PRODUCTNAME:'+str(PRODUCTNAME))
    print ('osapp_zip_name:'+str(osapp_zip_name))
    osapp_zip_name=str(osapp_zip_name)
    osapp_zip_name=out_osapp_zip_dir+'/'+PRODUCTNAME+'/'+osapp_zip_name
    print ('osapp_zip_name:'+str(osapp_zip_name))
    appversion='1.1.1.0'
    ANDROID_out_host_linux=ANDROID_HOME_dir+'/out/host/linux-x86/'
    if os.path.exists(osapp_zip_name):
        appversion=os.path.basename(osapp_zip_name)
        appversion=str(osapp_zip_name).split('-')[2].replace(' ','')+'-'+str(osapp_zip_name).split('-')[3].replace(' ','').replace('.zip','')
    print ('appversion:'+str(appversion))
    if not os.path.exists(outotatargetrepkg_dir):
        os.system('mkdir -p '+outotatargetrepkg_dir)
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
    extract_repack_otatarget_zip() #备份target包，生成OTA包

def get_apps_config():
    if os.path.exists(APP_CONFIG_DIR+'/talpa_apps.config'):
        cf = open(APP_CONFIG_DIR +"/talpa_apps.config")
        lines = cf.readlines()
        cf.close
        for row in lines:
            if not row: continue
            row = row.strip()
            value = row.split('=')
            print value
            if 'null' != value[0].strip():
                replaced_app.append(value[0].strip())
    return len(replaced_app)

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

def ex_zip(zipfile):
    outzipfilepath=str(os.path.abspath(zipfile)).replace('.zip','')
    print ('outzipfilepath:'+str(outzipfilepath))
    os.system('sudo unzip -o -q '+zipfile+' -d '+outzipfilepath)
    return outzipfilepath

def readAndroidmk(Androidpath,splitarg,filearg):
    apkfile_object = open(os.path.join(Androidpath))
    for mkline in apkfile_object:
        if mkline.split(splitarg)[0].replace(' ','')==filearg:
            strg=''
            strg=mkline.split(splitarg)[1].replace('\n','').replace('\r','').replace('\t','').replace(' ','')
            return strg

def readrmapkAndroidmk(Androidpath,splitarg,filearg):
    apkfile_object = open(os.path.join(Androidpath))
    for mkline in apkfile_object:
        if mkline.split(splitarg)[0].replace(' ','')==filearg:
            strg=mkline.split(splitarg)[1].replace('\n','').replace('\r','').replace('\t','').strip()
            print (len(strg.split(' ')))
            print (strg.split(' '))
            return strg.split(' ')

def replac_app(package_dir,appversionzip):
    apkmodule=[]
    rmapks=[]
    PRODUCT_COPY_FILES=[]
    PROD_COPY=False
    if os.path.exists(appversionzip) and appversionzip.endswith('.zip'):
        outzipfile=ex_zip(appversionzip)
        if os.path.exists(outzipfile) and os.path.exists(outzipfile+'/talpa.mk'):
            if get_apps_config()>0:
                for f in replaced_app:
                    if os.path.exists(package_dir+'/priv-app/'+f):
                        print ('rm:'+str(f))
                        os.system('sudo rm -rf '+package_dir+'/priv-app/'+f)
                    elif os.path.exists(package_dir+'/app/'+f):
                        print ('rm:' + str(f))
                        os.system('sudo rm -rf '+package_dir +'/app/'+f)
            file_object = open(os.path.join(outzipfile,'talpa.mk'))
            print ('file_object:'+str(file_object))
            for line in file_object:
                apk=''
                apk=line.split(' \\')[0].replace('\n','').replace('\r','').replace('\t','').replace(' ','')
                print ('apk:'+str(apk))
                apkmodule.append(apk)
            print ('apkmodule:'+str(apkmodule))
            for pline in apkmodule:
                if 'PRODUCT_COPY_FILES' in pline:
                    PROD_COPY=True
                    print ('PROD_COPY:'+str(PROD_COPY))
                    break
            for pline in apkmodule:
                if 'copy_files' in pline and PROD_COPY and ':' in pline:
                    print ('5556:')
                    PRODUCT_COPY=''
                    PRODUCT_COPY=pline.split(':')[1]
                    PRODUCT_COPY_FILES.append(PRODUCT_COPY)
            print ('PRODUCT_COPY_FILES:'+str(PRODUCT_COPY_FILES))
            print ('outzipfile:'+str(outzipfile))
            removeflag = True
            for PRODUCT_COPY_FILE in PRODUCT_COPY_FILES:
                print (str(outzipfile+'/copy_files/'+PRODUCT_COPY_FILE)+':'+str(os.path.exists(outzipfile+'/copy_files/'+PRODUCT_COPY_FILE)))
                if os.path.exists(outzipfile+'/copy_files/'+PRODUCT_COPY_FILE):
                    PRODUCT_COPY_FILEdir=str(PRODUCT_COPY_FILE).replace('system/','').split('/')[0]
                    PRODUCT_COPY_FILE_full_dir=str(PRODUCT_COPY_FILE).replace('system/','')
                    print ('PRODUCT_COPY_FILEdir_sencond:'+PRODUCT_COPY_FILEdir)
                    print ('PRODUCT_COPY_FILEdir_full:'+PRODUCT_COPY_FILE_full_dir)
                    print ('PRODUCT_COPY_FILE_NAMES:'+PRODUCT_COPY_FILE_full_dir.split('/')[-1])
                    PRODUCT_COPY_FILE_NAMES=PRODUCT_COPY_FILE_full_dir.split('/')[-1]
                    print ('PRODUCT_COPY_FILEdir_for_files:'+PRODUCT_COPY_FILE_full_dir.replace(PRODUCT_COPY_FILE_NAMES,''))
                    if removeflag == True:
                        if PRODUCT_COPY_FILE_full_dir.replace(PRODUCT_COPY_FILE_NAMES,'') == 'vendor/overlay/' :
                            print ('remove vendor/overlay/ ')
                            os.system('sudo chmod 777 '+package_dir+ PRODUCT_COPY_FILE_full_dir.replace(PRODUCT_COPY_FILE_NAMES,''))
                            os.system('sudo rm -rf '+package_dir+ PRODUCT_COPY_FILE_full_dir.replace(PRODUCT_COPY_FILE_NAMES,''))
                            removeflag = False
                    PRODUCT_COPY_FILE_full_dir=PRODUCT_COPY_FILE_full_dir.replace(PRODUCT_COPY_FILE_NAMES,'')
                    if not os.path.exists(package_dir+ PRODUCT_COPY_FILE_full_dir):
                        os.system('sudo mkdir -p '+ package_dir+ PRODUCT_COPY_FILE_full_dir)
                        os.system('sudo chmod 0755 '+ package_dir+ PRODUCT_COPY_FILE_full_dir)
                    if PRODUCT_COPY_FILEdir == 'media':
                        print ('chb: PRODUCT_COPY_FILE0-'+package_dir+PRODUCT_COPY_FILE)
                        os.system('sudo chmod 777 '+ package_dir+ PRODUCT_COPY_FILEdir)
                        os.system('sudo rm -rf '+package_dir+PRODUCT_COPY_FILE)
                    print ('----chb: in files:----'+outzipfile+'/copy_files/'+PRODUCT_COPY_FILE)
                    print ('----chb: out files:----'+package_dir+ PRODUCT_COPY_FILE_full_dir)
                    os.system('sudo cp -rauf ' + outzipfile+'/copy_files/'+PRODUCT_COPY_FILE+'  '+ package_dir+ PRODUCT_COPY_FILE_full_dir)
                   
            for apk in apkmodule:
                if os.path.exists(outzipfile+'/'+apk) and os.path.exists(outzipfile+'/'+apk+'/'+'Android.mk'):
                    print ('apk:'+str(apk))
                    apkm=''
                    apkm=readAndroidmk(outzipfile+'/'+apk+'/'+'Android.mk',':=','LOCAL_MODULE')
                    print ('apkm_LOCAL_MODULE:'+str(apkm)+'  apkm==apk:'+str(apkm==apk))
                    if apkm==apk:
                        apk_src_files=''
                        apk_src_files=readAndroidmk(outzipfile+'/'+apk+'/'+'Android.mk',':=','LOCAL_SRC_FILES')
                        print ('apkm:'+str(apk)+' apk_src_files:'+str(apk_src_files))
                        if os.path.exists(outzipfile+'/'+apkm+'/'+apk_src_files):
                            if APKreSIGN == True:
                                certificate=''
                                certificate=readAndroidmk(outzipfile+'/'+apk+'/'+'Android.mk',':=','LOCAL_CERTIFICATE')
                                print ('apkm:'+str(apk)+' certificate:'+str(certificate))
                                cmd = 'sudo java -jar ' + SCRIPT_PATH+'/tools/signapk.jar '+APKSIGN_KEYDIR + '/'+certificate+'.x509.pem '+APKSIGN_KEYDIR + '/'+certificate+'.pk8 '+outzipfile+'/'+apk+'/'+apk_src_files+'  '+outzipfile+'/'+apk+'/'+apkm+'.apk'
                                print ('cmd:'+str(cmd))
                                p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
                                if input_sign_key == None:
                                    key = os.getenv("TALPA_KEY",None)
                                    if key != None:
                                        p.communicate(key)
                                        p.wait()
                                    else:
                                        p.communicate()
                                else:
                                    p.communicate(input_sign_key)
                                    p.wait()
                            rmapk=[]
                            rmapk=readrmapkAndroidmk(outzipfile+'/'+apk+'/'+'Android.mk',':=','LOCAL_OVERRIDES_PACKAGES')
                            print ('rmapk:'+str(rmapk))
                            if rmapk !=None:
                                for rms in rmapk:
                                    print ('rms:'+str(rms))
                                    if rms != None and os.path.exists(package_dir + '/priv-app/'+rms):
                                        os.system('sudo rm -rf '+package_dir + '/priv-app/'+rms)
                                    if rms != None and os.path.exists(package_dir + '/app/'+rms):
                                        os.system('sudo rm -rf '+package_dir + '/app/'+rms)
                            if os.path.exists(outzipfile+'/'+apk+'/'+apkm+'.apk'):
                                paths=''
                                paths=readAndroidmk(outzipfile+'/'+apk+'/'+'Android.mk',':=','LOCAL_MODULE_PATH')
                                print ('paths:'+str(paths))
                                if "TARGET_OUT_APPS_PRIVILEGED" in paths:
                                    if not os.path.exists(package_dir + '/priv-app/'+apk):
                                        os.system('sudo mkdir -p '+package_dir + '/priv-app/'+apk+'/')
                                    else:
                                        os.system('sudo rm -rf '+package_dir + '/priv-app/'+apk)
                                        os.system('sudo mkdir -p '+package_dir + '/priv-app/'+apk+'/')
                                    os.system('sudo chmod 0755 '+package_dir + '/priv-app/'+apk)
                                    os.system('sudo cp -rauf '+outzipfile+'/'+apk+'/'+apkm+'.apk'+' '+package_dir + '/priv-app/'+apk+'/'+apk+'.apk')
                                    
                                    print ('apkmodule:'+str(outzipfile+'/'+apk+'/'+apkm+'.apk'))
                                    if os.path.exists(outzipfile+'/'+apk+'/'+lib):
                                        os.system('sudo cp -rauf '+outzipfile+'/'+apk+'/'+lib+' '+package_dir + '/priv-app/'+apk+'/')
                                        os.system('sudo chmod 0755 '+package_dir + '/priv-app/'+apk+'/'+lib)
                                        
                                    if os.path.exists(outzipfile+'/'+apk+'/'+'fm.conf'):
                                        os.system('sudo cp -rauf '+outzipfile+'/'+apk+'/'+'fm.conf'+' '+package_dir + '/priv-app/'+apk+'/')
                                        os.system('sudo chmod 0755 '+package_dir + '/priv-app/'+apk+'/'+'fm.conf')
                                        
                                else:
                                    if not os.path.exists(package_dir + '/app/'+apk):
                                        os.system('sudo mkdir -p '+ package_dir + '/app/'+apk+'/')
                                    else:
                                        os.system('sudo rm -rf '+ package_dir + '/app/'+apk)
                                        os.system('sudo mkdir -p '+ package_dir + '/app/'+apk+'/')
                                    os.system('sudo chmod 0755 '+package_dir + '/app/'+apk)
                                    os.system('sudo cp -rauf '+outzipfile+'/'+apk+'/'+apkm+'.apk'+' '+ package_dir + '/app/'+apk+'/'+apkm+'.apk')
                                    print ('apkmodule:'+str(outzipfile+'/'+apk+'/'+apkm+'.apk'))
                                   
                                    if os.path.exists(outzipfile+'/'+apk+'/'+lib):
                                        os.system('sudo cp -rauf '+outzipfile+'/'+apk+'/'+lib+' '+package_dir + '/app/'+apk+'/')
                                        os.system('sudo chmod 0755 '+package_dir + '/app/'+apk+'/'+lib)
                                        #APKSIZE=getfilesize(outzipfile+'/'+apk+'/'+lib)+APKSIZE
                                    if os.path.exists(outzipfile+'/'+apk+'/'+'fm.conf'):
                                        os.system('sudo cp -rauf '+outzipfile+'/'+apk+'/'+'fm.conf'+' '+package_dir + '/app/'+apk+'/')
                                        os.system('sudo chmod 0755 '+package_dir + '/app/'+apk+'/'+'fm.conf')
                                       
                                apkmodules[apkm]=apk_src_files
        print ('apkmodules:'+str(apkmodules))
        
        if os.path.exists(outzipfile):
            os.system('sudo rm -rf '+outzipfile)

def getpropstring(filename,arg):
    if os.path.exists(filename):
        file_object = open(os.path.join(filename))
        for line in file_object:
            if line.split('=')[0].replace(' ','')==arg:
                prop=line.split('=')[1].replace(' ','').replace('\n','').replace('\r','').replace('\t','')
                print ('prop:'+prop)
                return prop

def extract_repack_otatarget_zip():
    otatarget_zipdir=productdir+'/target_zip/'+PRODUCTNAME
    ver_name=appversion
    otaoutname=PRODUCTNAME+'-'+ ver_name
    if not os.path.exists(otatarget_zipdir):
        os.system('sudo mkdir -p '+otatarget_zipdir)
        os.system('sudo chmod 777 '+otatarget_zipdir)
    os.system('rm -rf '+'/tmp/tmp*')
    os.system('rm -rf '+'/tmp/targetfile*')
    os.system('rm -rf '+'/tmp/imgdiff*')
    if os.path.exists(otatarget_zipdir+'/target'):
        os.system('sudo rm -rf '+otatarget_zipdir+'target')
    delet_nouse_file(otatarget_zipdir,True)
    files=glob.glob(otatarget_zipdir + '/*.zip')
    if files.__len__() < 1:
        print ('ota target.zip is not exists!')
        return False
    fctimes={}
    ctimes=[]
    for file in files:
        fileinfo=os.stat(file)
        time=(fileinfo.st_ctime)
        fctimes[time]=(file)
        ctimes.append(time)
    print (str(fctimes))
    ctimes=max(ctimes)
    target_file_name = str(fctimes[ctimes])
    print ('max ota target.zip file :'+str(fctimes[ctimes])+' time:'+str(ctimes))
    if os.path.exists(str(fctimes[ctimes])):
        os.system('sudo chown -R jenkins:jenkins '+otatarget_zipdir)
        os.system('mkdir -p '+otatarget_zipdir+'/target')
        os.system('unzip -o -q '+str(fctimes[ctimes])+' -d '+otatarget_zipdir+'/target')
        print (str('unzip -o -q '+str(fctimes[ctimes])+' -d '+otatarget_zipdir+'/target'))
    os.system('sudo sed -i "s/ro.build.display.id=.*/ro.build.display.id='+PRODUCTNAME+'-'+ appversion+'/g" '+otatarget_zipdir + '/target/SYSTEM/build.prop')
    if CHIP == 'MTK':
        os.system('sudo sed -i "s/ro.itel.version.release=.*/ro.itel.version.release='+PRODUCTNAME+'-'+ appversion+'/g" '+otatarget_zipdir + '/target/SYSTEM/build.prop')
    else:
        os.system('sudo sed -i "s/ro.build.display.spid.customer=.*/ro.build.display.spid.customer='+PRODUCTNAME+'-'+ appversion+'/g" '+otatarget_zipdir + '/target/SYSTEM/build.prop')
    #os.system('sed -i "s/ro.build.date.utc=[A-Za-z0-9_-.]*/ro.build.date.utc='+date_utc_str+'/g" '+otatarget_zipdir + '/target/SYSTEM/build.prop')
    #os.system('sed -i "s/ro.build.date=.*/ro.build.date='+date_str+'/g" '+otatarget_zipdir + '/target/SYSTEM/build.prop')
    replac_app(otatarget_zipdir+'/target/SYSTEM/',osapp_zip_name)
    os.system('sudo chown -R jenkins:jenkins '+otatarget_zipdir)
    print ('start make ota package')
    os.chdir(otatarget_zipdir+'/target')
    cmd='zip -r -y '+outotatargetrepkg_dir+'/'+'tmp.zip '+'./'
    print ('cmd:'+str(cmd))
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    outs=p.communicate()
    #print('outs:'+str(outs))
    print ('start make ota tmp.zip')
    os.system('mv '+outotatargetrepkg_dir+'/'+'tmp.zip '+PRODUCTotapackage_target_file+'/'+otaoutname+'_update.zip')
    os.system('sudo chmod 777 '+ota_from_target_filestool)
    os.chdir(ANDROID_HOME_dir)
    if CHIP==('MTK'):
        cmd = ota_from_target_filestool + ' -v -p '+ANDROID_out_host_linux+' -k '+SIGN_KEYTOOL+SIGN_KEY+' -s '+mt_ota_from_target_filestool+' '+PRODUCTotapackage_target_file+'/'+otaoutname+'_update.zip '+outotatargetrepkg_dir+'/'+otaoutname+'_FULL_OTA' +'.zip'
    else:
        cmd = ota_from_target_filestool + ' -v -p '+ANDROID_out_host_linux+' -k '+SIGN_KEYTOOL+SIGN_KEY+' '+PRODUCTotapackage_target_file+'/'+otaoutname+'_update.zip '+outotatargetrepkg_dir+'/'+otaoutname+'_FULL_OTA' +'.zip'
    print ('cmd:'+str(cmd))
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    if input_sign_key != None:
        p.communicate(input_sign_key)
        p.wait()
    else:
        outs=p.communicate()
    print ('stop make ota package...succeed')
    print ('......remove tmp file......')
    os.system('sudo rm -rf '+outotatargetrepkg_dir+'/tmp.zip')
    os.system('sudo rm -rf '+otatarget_zipdir+'/target')
    os.system('rm -rf '+'/tmp/tmp*')
    os.system('rm -rf '+'/tmp/targetfile*')
    os.system('rm -rf '+'/tmp/imgdiff*')
    print ('\n##############################################################')
    print ('product_chip: '+str(CHIP))
    print ('product_name: '+str(PRODUCTNAME))
    print ('osapp_zip_name: '+str(sys.argv[3]))
    print ('target_file_name: '+str(target_file_name))
    print ('backup_target_path: '+str(PRODUCTotapackage_target_file+'/'+otaoutname+'_update.zip'))
    print ('out_ota_path: '+str(outotatargetrepkg_dir+'/'+otaoutname+'_FULL_OTA'+'.zip'))
    print ('##############################################################')

if __name__ == '__main__':
    set_dev_info()