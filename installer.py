#!/usr/bin/python3
import os
import subprocess
import json
import argparse
import configparser
import shutil

indent=""
sshclient=None

# Get list of projects to install, either from a list of all subdirectories, or from a comma separated list 'projectList'
def getProjects(projectList, projectsFile):
    if projectsFile == None:
        projectsFile = "projects.env"
      
    plist = []
    if projectList == None:  
        plist = config.sections()
    else:
        print("Project List: "+str(projectList))
        plist = projectList.split(",")

    return plist

# Read installed versions from VERSIONS.txt
def readInstalledVersions(versionFile="VERSIONS.txt"):
    try:
        with open(versionFile, 'r') as file:
            return json.load(file)
    except:
        return {}
    
# Config parser safe get, returns None if the option doesn't exist
def safeGet(config, name, option):
    if config.has_option(name, option):
        return config.get(name, option)
    return None

# Check versions to see if we need to bother updating/reinstalling or not
# Installed versions are stored in the version file, in a dict
def checkVersion(version, newVersion):
    if version == None or version != newVersion:
        return False
    return True

def expandFile(projectDir, archive):
    if archive.endswith('.zip'):
        localCommand("unzip "+archive, projectDir)
    elif archive.endswith('.tgz') or archive.endswith('.tar.gz'):
        localCommand("tar -xzf "+archive, projectDir)
    elif archive.endswith('.tar') or archive.endswith('.bz2'):
        localCommand("tar -xf "+archive, projectDir)
    else:
        raise("Unknown archive file type: "+archive)

def defaultProvisioner(name, projectDir, projOffline):
    print("  Running default provisioner (no-op currently) for "+name+"/"+projOffline+" in "+projectDir)
    return True
    
def installProject(name, config, versions):
    global indent
    
    # 0. Check version, do we need to update?
    newVersion = safeGet(config, name, "version")
    if forceInstall == False:
        version = versions.get(name)
        already = checkVersion(version, newVersion)
        if already == True:
            print("  "+name+" already installed at version "+newVersion)
            installedProjects.append(name)
            return
        elif version is not None:
            print("  "+name+" installed with old version "+version+". Ugprading to "+newVersion)
        else:
            print("  "+name+" not installed, installing version "+newVersion)
            
    print("  Installing "+name)
    cwd = os.getcwd()

    # 1: Create the directory
    projectDir = os.path.join(targetDir, name)
 
    if projectClean and os.path.exists(projectDir):
        doClean = False
        if not autoAccept:
            ans = input("Clean existing files in "+projectDir+"? (y/n)")
            if ans == 'y' or ans == 'Y':
                print("Cleaning "+projectDir)
                doClean = True
            else:
                print("NOT cleaning "+projectDir)
        else:
            doClean = True
        
        if doClean:
            if not logOnly:
                shutil.rmtree(projectDir)
            
    os.makedirs(projectDir, exist_ok=True)


    # 2: Get the project.env to get online/offline/provision links
    projOnline=safeGet(config, name, 'online')
    projOffline=safeGet(config, name, 'offline')
    projprov=safeGet(config, name, 'provision')
    extractSubdir = safeGet(config, name, 'subdir')
    renameFrom = safeGet(config, name, 'renameFrom')
    powershell = safeGet(config, name, 'powershell')
                        
    # 3: Download either online or offline
    if onlineMode and len(projOnline) > 0 and not provisionOnly:
        # Online download
        onlineType = safeGet(config, name, 'online.type')
        cmd = ""
        extractDir = targetDir
        if onlineType == 'git':
            cmd = "git clone " + projOnline + " " + name     
        elif onlineType == 'wget':
            cmd = "wget " + projOnline
            if str(extractSubdir).upper() == "TRUE":
                extractDir = projectDir
        else:
            raise "Unknown online.type in "+name+": "+onlineType

        if not autoAccept:
            ans = input("Execute remote download command: "+cmd+": (y/n)")
            if ans == 'y' or ans == 'Y':
                localCommand(cmd, extractDir)
            else:
                raise "Aborting download of "+name+" due to user command"
        else:
            localCommand(cmd, extractDir)
    elif not provisionOnly:
        # Offline copy from downloads dir
        if len(projOffline) > 0:
            dlDir = os.path.join(cwd, "downloads")
            archive = os.path.join(dlDir, projOffline)
            extractDir = targetDir
            if str(extractSubdir).upper() == "TRUE":
                extractDir = projectDir
            if (os.path.exists(archive)):
                print("  Copying "+projOffline+" to "+extractDir)
                if not logOnly:
                    shutil.copy(archive, extractDir)
                    expandFile(extractDir, archive)
                    if renameFrom is not None and len(renameFrom) > 0:
                        renameTo = os.path.join(extractDir, name)
                        print("  Renaming "+str(renameFrom)+" to "+str(renameTo))
                        shutil.rmtree(renameTo)
                        shutil.move(os.path.join(extractDir, renameFrom), os.path.join(extractDir, name))
                    copiedArchive = os.path.join(extractDir, projOffline)
                    print("  Removing archive file from "+str(copiedArchive))
                    os.remove(copiedArchive)
            else:
                print("  Unable to find offline archive "+projOffline+" in downloads!")
                            
    # 4: Copy over all files in files subdir
    filesSubdir = os.path.join(name, "files")
    if os.path.exists(filesSubdir):
        print("    Copying over files subdirectory")
        if not logOnly:
            shutil.copytree(filesSubdir, projectDir, dirs_exist_ok=True, copy_function=shutil.copy)
            
    # 5: Run provisioner script
    ret = None
    if projprov == None or str(projprov).upper() == "DEFAULT":
        # Default provisioner
        ret = defaultProvisioner(name, projectDir, projOffline)
    elif str(projprov).upper() == "MAKE":
        ret = not localCommand("make", projectDir)
    else:
        provision = os.path.join(name, projprov) 
        print("  Looking for provisioner at "+provision)
        if os.path.exists(provision):
            pTarget = os.path.join(projectDir, projprov)
            print("  Copying over "+provision+" to "+pTarget)
            if not logOnly:
                shutil.copy(provision, pTarget)
                ret = localCommand("./"+projprov, projectDir)
        else:
            print("  Provision script not found!")

    if powershell != None:
        print("  Executing: "+powershell+" in powershell")
        ret = localCommand("powershell.exe -f "+powershell, projectDir)

    if ret == 1:
        installedProjects.append(name)
        versions[name] = newVersion
    else:
        print ("  returned value = "+str(ret))
        print ("  Provision script did not complete successfully")

# Run a local command with subprocess.Popen, such as git or wget, or a provisioner script
def localCommand(command, wdir=os.getcwd()):
    print("  Executing "+command+" in "+wdir)
    if logOnly:
        return 1
    
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='utf8', bufsize=1, cwd=wdir)
    fullout = ""
    while proc.poll() is None:
        line = proc.stdout.readline()
        print("> "+line, end='')
        fullout += line
        
    proc.stdout.close();
    proc.wait()
    
    return proc.returncode

# Main
parser = argparse.ArgumentParser()
parser.add_argument("-d", default="/mnt/c/Dev/tools", help="Root directory to install projects to")
# online is ignored if offline is set
parser.add_argument("-online", default=False, help="Online mode, try to clone projects from remote servers.  Use offline zips as a backup", action='store_true')
parser.add_argument("-offline", default=True, help="Offline only mode, get projects from offline zips", action='store_true')
parser.add_argument("-f", default=False, help="Force re-install", action='store_true') 
parser.add_argument("-clean", default=False, help="Clean any existing files", action='store_true')
parser.add_argument("-file", default="projects.env", help="projects.env file to load to find projects")
parser.add_argument("-p", default=None, help="Projects to install in a comma separated list (e.g. scapy,ghidra).  Default is everything.")
parser.add_argument("-pv", default=False, help="Provision only", action="store_true")
parser.add_argument("-y", default=False, help="Auto-accept, no user confirmation of overwriting or downloading", action="store_true")
parser.add_argument("-l", default=False, help="Log only, don't actually do anything", action='store_true')
parser.add_argument("-vf", default="VERSIONS.txt", help="Installed versions json dictionary file")

# TODO: Auto check git repos for updates, update versions

args = parser.parse_args()
targetDir = args.d
onlineMode = args.online
offlineMode = args.offline
forceInstall = args.f
projectList = args.p
autoAccept = args.y
projectClean = args.clean
projectsFile = args.file
logOnly = args.l
versionFile = args.vf
provisionOnly = args.pv

print("Installing projects to root directory "+targetDir)
print("  Loading projects file: "+projectsFile)

# Read the project.env to get online/offline/provision links
config = configparser.RawConfigParser()
config.read(os.path.join(projectsFile))

installedProjects = []
worklist = getProjects(projectList, projectsFile)
print("Projects to install: "+str(worklist))

# Get already installed versions
versions = readInstalledVersions(versionFile)
print("Installed Versions: "+str(versions))

i=1
for proj in worklist:
    print(os.linesep+"Handling project ("+str(i)+" of "+str(len(worklist))+"): "+proj)
    i = i + 1
    try:
        installProject(proj, config, versions)
    except BaseException as err:
        print("Exception installing "+proj+": "+str(err))
    
print(os.linesep+"Installer completed")
print("Installed: "+str(installedProjects))

with open(versionFile, 'w') as file:
    file.write(json.dumps(versions))

print("Saved installed versions to "+versionFile)


