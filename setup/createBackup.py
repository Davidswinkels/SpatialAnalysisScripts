#!/usr/bin/env python2
## Document information
__author__ = "David Swinkels"
__github__ = "davidswinkels"
__purpose__ = "Part of MSc thesis Geo-Information Science at Wageningen University"
__status__ = "Production"

## Import functions here
import os, os.path
import zipfile
from datetime import datetime

## This function check current date and its add to filename
dateTime = str(datetime.now())
filenameScripts = "E:\BackupReportsScripts\Scripts\\" + dateTime[:10]+ "Scripts.zip"
filenameReports = "E:\BackupReportsScripts\Reports\\" + dateTime[:10] + "Reports.zip"

## This function zips the workspace
def zip_dir(dirpath, zippath):
    fzip = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED, allowZip64 = True)
    basedir = os.path.dirname(dirpath) + '/' 
    for root, dirs, files in os.walk(dirpath):
        if os.path.basename(root)[0] == '.':
            continue #skip hidden directories        
        dirname = root.replace(basedir, '')
        for f in files:
            if f[-1] == '~' or (f[0] == '.' and f != '.htaccess'):
                #skip backup files and all hidden files except .htaccess
                continue
            fzip.write(root + '/' + f, dirname + '/' + f)
    fzip.close()

## Zip the scripts and reports from workspaces to backup USB drive
zip_dir(dirpath = 'D:\Workspace\Scripts', zippath = filenameScripts)
zip_dir(dirpath = 'M:\Thesis\Reports', zippath = filenameReports)
