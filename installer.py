#!/usr/bin/python3
import os
import subprocess
import tarfile
import zipfile
import argparse
import configparser
import time
import shutil
import hashlib
import select

from glob import glob

indent=""
sshclient=None

# Get list of projects to install, either from a list of all subdirectories, or from a comma separated list 'projectList'
def getProjects(projectList):
    if projectList == None:
        plist = glob('*/')
    else:
        print("Project List: "+str(projectList))
        plist = projectList.split(",")

    todoList = []
    for p in plist:
        pname=p
        if pname[-1:] == '/':
            pname = p[:-1]

        # ignore base and downloads, base we already installed, downloads is special
        if pname == 'base' or pname == 'downloads':
            continue
        
        todoList.append(pname)
        
    return todoList

# Unimplemented
# TODO: Check versions to see if we need to bother updating/reinstalling or not
def checkVersion(name):
    return False

def installProject(name):
    global indent
    
    if forceInstall == False:
        already = checkVersion(name)
        if already == True:
            installedProjects.append(name)
            return
            
    print("  Installing "+name)
    cwd = os.getcwd()

    # 1: Create the directory
    projectDir = os.path.join(targetDir, name)
 
    if projectClean and os.path.exists(projectDir):
        if not autoAccept:
            ans = input("Clean existing files in "+projectDir+"? (y/n)")
            if ans == 'y' or ans == 'Y':
                print("Cleaning "+projectDir)
                shutil.rmtree(projectDir)
            else:
                print("NOT cleaning "+projectDir)

    os.makedirs(projectDir, exist_ok=True)
                            
    # 2: Copy over all files in files subdir
    filesSubdir = os.path.join(name, "files")
    if os.path.exists(filesSubdir):
        print("    Copying over files subdirectory")
        shutil.copytree(filesSubdir, projectDir, dirs_exist_ok=True)

    # 3: Read the project.env to get online/offline/provision links
    config = configparser.RawConfigParser()
    config.read(os.path.join(name, "project.env"))

    projOnline=config.get(name,'project.online')
    projOffline=config.get(name,'project.offline')
    projprov=config.get(name, 'project.provision')
                        
    # 4: Download either online or offline
    if onlineMode and len(projOnline) > 0:
        # Online download
        onlineType = config.get(name, 'project.online.type')
        cmd = ""
        if onlineType == 'git':
            cmd = "git clone " + projOnline            
        elif onlineType == 'wget':
            cmd = "wget " + projOnline
        else:
            raise "Unknown project.online.type in "+name+": "+onlineType

        if not autoAccept:
            ans = input("Execute remote download command (y/n): "+cmd)
            if ans == 'y' or ans == 'Y':
                localCommand(cmd)
            else:
                raise "Aborting download of "+name+" due to user command"
            
    else:
        # Offline copy from downloads dir
        if len(projOffline) > 0:
            dlDir = os.path.join(cwd, "downloads")
            archive = os.path.join(dlDir, projOffline)
            if (os.path.exists(archive)):
                print("  Copying "+projOffline+" to "+projectDir)
                shutil.copy(archive, projectDir)
                targetZip = os.path.join(projectDir, projOffline)
                print("  Extracting "+targetZip)
                with zipfile.ZipFile(targetZip, 'r') as zipr:
                    zipr.extractall(projectDir)
            else:
                print("  Unable to find offline archive "+projOffline+" in downloads!")

    # 5: Run provisioner script
    provision = os.path.join(name, projprov)
    ret = None
    print("Looking for provisioner at "+provision)
    if os.path.exists(provision):
        pTarget = os.path.join(projectDir, projprov)
        print("  Copying over "+provision+" to "+pTarget)
        shutil.copy(provision, pTarget)
        print("  Executing: "+projprov)
        ret = localCommand("./"+projprov, projectDir)
    else:
        print("  Provision script not found!")

    if ret == 1:
        installedProjects.append(name)
    else:
        print ("  Provision script did not complete successfully")


def localCommand(command, wdir=os.getcwd()):
    print("Executing "+command+" in "+wdir)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='utf8', bufsize=1, cwd=wdir)
    fullout = ""
    while proc.poll() is None:
        line = proc.stdout.readline()
        print("> "+line, end='')
        fullout += line
        
    proc.stdout.close();
    proc.wait()
    
    return proc.returncode

###################################################
# Main
###################################################

parser = argparse.ArgumentParser()
parser.add_argument("-d", default="/mnt/c/Dev", help="Root directory to install projects to")
# online is ignored if offline is set
parser.add_argument("-online", default=False, help="Online mode, try to clone projects from remote servers.  Use offline zips as a backup", action='store_true')
parser.add_argument("-offline", default=True, help="Offline only mode, get projects from offline zips", action='store_true')
parser.add_argument("-f", default=False, help="Force re-install", action='store_true') 
parser.add_argument("-clean", default=False, help="Clean any existing files", action='store_true')
parser.add_argument("-p", default=None, help="Projects to install in a comma separated list (e.g. scapy,ghidra).  Default is everything.")
parser.add_argument("-y", default=False, help="Auto-accept, no user confirmation of overwriting or downloading", action="store_true")

args = parser.parse_args()
targetDir = args.d
onlineMode = args.online
offlineMode = args.offline
forceInstall = args.f
projectList = args.p
autoAccept = args.y
projectClean = args.clean

print("Installing projects to root directory "+targetDir)

installedProjects = []

# Install base first always
installProject("base")
worklist = getProjects(projectList)

i=1
for proj in worklist:
    print("Handling project ("+str(i)+" of "+str(len(worklist))+"): "+proj)
    i = i + 1
    try:
        installProject(proj)
    except BaseException as err:
        print("Exception installing "+proj+": "+str(err))
    
print("Installer completed")
print("Installed: "+str(installedProjects))
