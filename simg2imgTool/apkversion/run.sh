#!/bin/bash
WORKSPACE=$WORKSPACE
GITtalpa_appsREPOURL=$GITtalpa_appsREPOURL
JENKINSWORKSPACE=$JENKINSWORKSPACE
JOB_NAME=$JOB_NAME
APKVERSION='V0.0.0'
APKVERSIONTEM='V0.0.1'
echo "WORKSPACE:"$WORKSPACE
echo "JENKINSWORKSPACE:"$JENKINSWORKSPACE
echo "GITtalpa_appsREPOURL:"$GITtalpa_appsREPOURL
BUILD='False'
if [ ! -d "$JENKINSWORKSPACE/talpa_apps" ];then
	mkdir -p $JENKINSWORKSPACE/talpa_apps
	cd $JENKINSWORKSPACE/talpa_apps
	git clone $GITtalpa_appsREPOURL;
	cd -
fi
if [ ! -d "$WORKSPACE" ];then
	echo "You project file not exist! Please commit  file by Yourselfe!"
	exit 1
else
	APKVERSION=$(find $WORKSPACE/code/$JOB_NAME/ -name AndroidManifest.xml -exec grep "android:versionName=*" {} \;)
	APKVERSION=${APKVERSION##*=}
	APKVERSION=$(echo $APKVERSION |sed 's/\"//g')
	APKVERSION=$(echo $APKVERSION |sed 's/[\>]//g')
	APKVERSION=$(echo $APKVERSION |sed 's/[[:space:]]//g')
       echo "APKVERSIONs:"$APKVERSION
       APKVERSION=$(echo $APKVERSION |sed 's/[a-zA-Z]//g')
	echo "APKVERSION:"$APKVERSION
	if [ ! -d "/work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERSION/" ];then
		mkdir -p /work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERSION/
		find $WORKSPACE/code/$JOB_NAME/ -name '*.apk' -exec cp {} /work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERSION/$JOB_NAME''_''$APKVERSION''.apk \;
		cp -raf $WORKSPACE/code/$JOB_NAME/Android.mk /work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERSION/
		if [ -d "$WORKSPACE/code/lib" ];then
			cp -raf $WORKSPACE/code/lib /work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERSION/
		fi
        if [  -f "$WORKSPACE/code/$JOB_NAME/fm.conf" ]; then  
            cp -raf $WORKSPACE/code/$JOB_NAME/fm.conf /work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERSION/
        fi
		cd /work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERSION/
		apkname=$JOB_NAME''_''$APKVERSION''.apk
		sed -i 's/LOCAL_SRC_FILES     := [A-Za-z0-9_]*.*/LOCAL_SRC_FILES     := '$apkname'/g' Android.mk
		cd -
	fi
fi

if [ -f "$WORKSPACE/Readme.txt" ];then
	BUILD='True'
fi
echo "BUILD:"$BUILD
if [ $BUILD == 'True' ];then
	APKVERcheckSION='demo'
	firstline='Readmefirstline'
	checktag='CodeGittag'
	firstline=`head -1 $WORKSPACE/Readme.txt |grep -o "[^ ]\+\( \+[^ ]\+\)*"`
	firstline=${firstline##*=}
	firstline=$(echo $firstline |sed 's/\"//g')
	firstline=$(echo $firstline |sed 's/" ﻿0"/"0"/g')
        echo "firstlines:"$firstline
        firstline=$(echo $firstline |sed 's/[a-zA-Z]//g')
	cd $WORKSPACE
	checktag=`git ls-remote --tags origin |grep $firstline |grep -o "[^ ]\+\( \+[^ ]\+\)*"`
        echo "checktag1: " $checktag
        checktag=$(echo $checktag|cut -d "/" -f 3)
        echo "checktag2:" $checktag
        checktag=$(echo $checktag|cut -d " " -f 1)
        echo "checktag3:" $checktag
	checktag=${checktag##*=}
	checktag=$(echo $checktag |sed 's/\"//g')
    echo "checktags:"$checktag
    gittag=$checktag
    gittagend=$(echo $checktag|cut -d "." -f 3)
    echo "gittagend:"$gittagend
    gittagend1=$(echo $gittagend |sed 's/\(.*\)\(.\)$/\2/')
    gittagend2=$(echo ${gittagend:length-2:length-1})
    echo "gittagend1:"$gittagend1
    echo "gittagend2:"$gittagend2
    if [ "$gittagend1" == "P" -a "$gittagend2" == "2" ]; then
        echo "=============================================="
        echo "YourProject is for Product!!!"
        echo "=============================================="
    elif [ "$gittagend1" == "D" -a "$gittagend2" == "0" ]; then
        echo "=============================================="
        echo "YourProject is for Debug!!!"
        echo "=============================================="
    elif [ "$gittagend1" == "M" -a "$gittagend2" == "1" ]; then
        echo "=============================================="
        echo "YourProject is for master!!!"
        echo "=============================================="
    else
        echo "========================================================"
        echo 'Your tag is: '$gittag
        echo "Your tag is wrong,Please modify such as: x.xxx.YYMMDDHH00D"
        echo "                                         x.xxx.YYMMDDHH01M"
        echo "                                         x.xxx.YYMMDDHH02P"
        echo " The last two mean:                      2P :  product"
        echo "                                         1M :  master"
        echo "                                         0D :  debug"
        echo "========================================================"
        exit 1
    fi
    checktag=$(echo $checktag |sed 's/[a-zA-Z]//g')
	echo 'gittag:'$gittag
	echo 'firstline:'$firstline
	if [ "$checktag"!="" -a "$firstline"!="" ];then
		if [ $firstline == $checktag ];
		then
			if [ ! -d "$JENKINSWORKSPACE/talpa_apps/$JOB_NAME/" ];then
				mkdir -p $JENKINSWORKSPACE/talpa_apps/$JOB_NAME/
			fi
			if [ ! -d "$JENKINSWORKSPACE/talpa_apps/$JOB_NAME/$firstline/" ];then
				mkdir -p $JENKINSWORKSPACE/talpa_apps/$JOB_NAME/$firstline/
			fi
			cp -raf $WORKSPACE/Readme.txt $JENKINSWORKSPACE/talpa_apps/$JOB_NAME/$firstline/
			git reset --hard;
			git clean -fdx;
			git pull
			git checkout $gittag;
			APKVERcheckSION=$(find $WORKSPACE/code/$JOB_NAME/ -name AndroidManifest.xml -exec grep "android:versionName=*" {} \;)
			APKVERcheckSION=${APKVERcheckSION##*=}
			APKVERcheckSION=$(echo $APKVERcheckSION |sed 's/\"//g')
			APKVERcheckSION=$(echo $APKVERcheckSION |sed 's/[\>]//g')
			APKVERcheckSION=$(echo $APKVERcheckSION |sed 's/[[:space:]]//g')
                        echo "APKVERcheckSIONs:"$APKVERcheckSION
                        APKVERcheckSION=$(echo $APKVERcheckSION |sed 's/[a-zA-Z]//g')
			APKVERSIONCODE=$(find $WORKSPACE/code/$JOB_NAME/ -name AndroidManifest.xml -exec grep "android:versionCode=*" {} \;)
			APKVERSIONCODE=${APKVERSIONCODE##*=}
			APKVERSIONCODE=$(echo $APKVERSIONCODE |sed 's/\"//g')
			APKVERSIONCODE=$(echo $APKVERSIONCODE |sed 's/[\>]//g')
			APKVERSIONCODE=$(echo $APKVERSIONCODE |sed 's/[[:space:]]//g')
			demook=$(echo $APKVERcheckSION|cut -d "." -f 3)
			echo "APKVERSIONCODE:"$APKVERSIONCODE
			echo 'APKVERcheckSION:'$APKVERcheckSION
			echo "demook:"$demook
			if [ $APKVERSIONCODE != $demook ];then
				echo "You project APKVERSIONCODE != APKVERcheckSIONNAME,Please Check YourProject's AndroidManifest.xml"
				exit 0
			fi
			if [ $APKVERcheckSION == $firstline ];then
				mkdir -p $JENKINSWORKSPACE/talpa_apps/$JOB_NAME/$APKVERcheckSION/
				cp -raf /work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERcheckSION/$JOB_NAME''_''$APKVERcheckSION''.apk $JENKINSWORKSPACE/talpa_apps/$JOB_NAME/$APKVERcheckSION/
				cp -raf /work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERcheckSION/Android.mk $JENKINSWORKSPACE/talpa_apps/$JOB_NAME/$APKVERcheckSION/
				cd $JENKINSWORKSPACE/talpa_apps/$JOB_NAME/$APKVERcheckSION/
				APKVERSIONTEM=$(find $JENKINSWORKSPACE/talpa_apps/$JOB_NAME/$APKVERcheckSION/ -name Android.mk -exec grep "LOCAL_SRC_FILES" {} \;)
				APKVERSIONTEM=${APKVERSIONTEM##*:=}
				if [ ! $APKVERSIONTEM == "$JOB_NAME''_''$APKVERcheckSION''.apk" ];then
					apkname=$JOB_NAME''_''$APKVERcheckSION''.apk
					sed -i 's/LOCAL_SRC_FILES     := [A-Za-z0-9_]*.*/LOCAL_SRC_FILES     := '$apkname'/g' Android.mk
				fi
				if [ -d "/work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERcheckSION/lib" ];then
					cp -raf /work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERcheckSION/lib $JENKINSWORKSPACE/talpa_apps/$JOB_NAME/$APKVERcheckSION/
				fi
                if [  -f "/work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERcheckSION/fm.conf" ]; then  
                    cp -raf /work/OSTeam/simg2img/talpa_apps_backup/$JOB_NAME/$APKVERcheckSION/fm.conf $JENKINSWORKSPACE/talpa_apps/$JOB_NAME/$APKVERcheckSION/
                fi
				cd $JENKINSWORKSPACE/talpa_apps/
				git checkout master
				git config --global user.email "3033798168@qq.com";
				git config --global user.name "ostest";
				git add --all;
				git commit -s -m "add $JOB_NAME'_'$APKVERcheckSION'_'Apk ";
				git push origin master
			fi
		else
			exit 1
		fi
	else
		exit 1
	fi
fi
