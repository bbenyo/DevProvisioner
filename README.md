# Dev Provisioner
Provisioner to load development tools either from online repositories or local zip, install and perform any additional local setup

# Steps
For each project, we create a [project] subdirectory under the target directory  Create /opt/scapy

1. Verify: Check to see if it's already installed
  a. If so, and the update flag is set, check versions and potentially update

2. Download
  a. If the online flag is set, either clone a remote repo, or download from a remote site.
  b. If offline is set, copy an archive from the zips directory
  c. Copy over anything in the files subdirectory over to 

3. Install
  a. Run the provisioner script defined in the project info file

## Example

target=/opt
project=scapy

1. Verify checks that /opt/scapy exists, and eventually checks versions.
  For now, if it doesn't exist or if it exists and -f (force update) is set, install, else move on
2. From project.json in scapy, we get the online download link (clone from github), or the offline zip (from downloads)
   Either clone inth /opt/scapy, or unzip into /opt/scapy, creating /opt/scapy/scapy-master
   Then copy over scapy/files to /opt/scapy, creating /opt/scapy/cheatsheet.txt and /opt/scapy/tools
3. Run provision.sh in /opt/scapy


## Subdirectories
Each subdirectory contains a single project.
Each project must contain a project info file (project.env), this gives the location to download, version number or date, link to provisioner script
Project directories can also contain additional files to copy over in the files subdirectory


