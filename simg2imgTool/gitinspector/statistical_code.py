#!/usr/bin/python
# -*- encoding: utf-8 -*-
# python ${simg2imgTool}/gitinspector/statistical_code.py  ${Gerrit_Project}

import sys
import os
import re
import time
import commands   
import subprocess

global gerrit_project
global branch 
global Branch_List
global Report_list
Branch_List = []
Report_list = []
gerrit_project = sys.argv[1]
#branch = sys.argv[2]
Project = "/work/workspace/jenkins/proj/"+gerrit_project   # code dir
HtmlTarget = "/var/www/html/gitinspector"  # http://10.250.119.10/gitinspector/[project]/result.html
ViewURL = "http://10.250.119.10/gitinspector"  #dir£º /var/www/html/gitinspector  
CreateDate = time.strftime("%Y%m%d%H%M")
HtmlTarget_dir = HtmlTarget+'/'+gerrit_project
if not os.path.exists(HtmlTarget_dir):
    os.system('mkdir -p '+HtmlTarget_dir)
#branch_list = commands.getstatusoutput('git ls-remote -h ssh://ostest@10.250.119.10:29418/'+gerrit_project)
p = subprocess.Popen('git ls-remote -h ssh://ostest@10.250.119.10:29418/'+gerrit_project,shell=True,stdout=subprocess.PIPE)  
out,err = p.communicate()  
for line in out.splitlines():  
    #print (line.split()[1].replace('refs/heads/', ''))
    branch_new = line.split()[1].replace('refs/heads/', '')
    Branch_List.append(branch_new)
Branch_List_len = len(Branch_List)

print "\n######################################################"
print ('gerrit_project_name: '+str(gerrit_project))
print ('Branch_List_len: '+str(Branch_List_len))
print ('Branch_List: '+str(Branch_List))
print ('gerrit_project_dir: '+Project)
print ('gerrit_project_report_dir: '+HtmlTarget_dir)  
print ('now time: '+CreateDate)   
print "######################################################"
print "\n============%s Projetc Code Report START============" % gerrit_project

def delFile(PATH):
    os.chdir(PATH)
    S, R = commands.getstatusoutput("find . -type f -ctime +30 | xargs rm -f")
    if S == 0:
        print "\nStart delete html file A month ago..."
    else:
        print "Delete file failed"

def historyHtml(PATH, project):
    print "\n###########################"
    print "#    History report list  #"
    print "###########################"
    for file in os.listdir(PATH):
        print os.path.join(ViewURL+'/'+gerrit_project, file)
    print "============%s Projetc Code Report END============" % project
    print ""
count = 0   
 
for branch_current in Branch_List:
    branch = branch_current
    if branch == "release" :
        continue
    print ('\nThe current branch is: %s'%branch)
    ProjectList = []
    ProjectList.append(Project)
    for projectPATH in ProjectList:
        os.chdir(projectPATH)
        item = projectPATH.split('/')[5]
        gitreset = commands.getstatusoutput("git reset --hard")
        gitbranch = commands.getstatusoutput("git checkout %s" %branch)
        gitStatus, gitResult = commands.getstatusoutput("git pull")
        #print ('gitStatus&gitResult: '+str(gitResult))
        if gitStatus == 0:
            print "============Update Project %s Code============" % item
            print "Code update complete. %s" %gitResult
            try:
                simpleStatus, simpleResult = commands.getstatusoutput("gitinspector -wTHL %s" % projectPATH)
            except Exception as e:
                count += 1
                print (e)
            else:
                if simpleStatus == 0:
                    simpleStatus == 0
                else:
                    count += 1
                    #print (str(simpleStatus))
            try:
                if not os.path.exists(HtmlTarget_dir):
                    os.system('mkdir -p '+HtmlTarget_dir)
                viewStatus, viewResult = commands.getstatusoutput("gitinspector --format=html --timeline --localize-output -w %s > %s/%s_CodeReport_%s_for_%s.html" % (projectPATH,HtmlTarget_dir,item,CreateDate,branch))                                           
                report_list = ViewURL+'/'+item+'/'+item+'_CodeReport_'+CreateDate+'_for_'+branch+'.html'
                Report_list.append(report_list)
                #print (str(viewStatus))
                #print "Access the following URL to view details: "
                #print "%s/%s/%s_%s_CodeReport_%s_for_%s.html \n" % (ViewURL, item, item,CreateDate,branch)
                #print (str(report_list))

            except Exception as e:
                count += 1
                print (e)
        else:
            print "============Update Project %s Code============" % item
            time.sleep(2)
            print "Code update failed."
            print ""
            sys.exit(5)
print "\nAccess the following URL to view details: "
for report in Report_list:
    print (str(report))

delFile("%s/%s" % (HtmlTarget, gerrit_project))
historyHtml(HtmlTarget_dir, gerrit_project)

if count == 0:
    sys.exit()
else:
    sys.exit(126)
    



