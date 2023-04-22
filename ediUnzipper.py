import zipfile
from shutil import copyfile
import os
import datetime
import logging
import time
import glob, os

curDate = datetime.datetime.now()
date_based_name = curDate.strftime('%Y_%m_%d')
workingDir = '/var/sftp/sn_billing'

#SETUP BASIC DIRECTORY STRUCTURE
if not os.path.exists(workingDir + '/Logs'):
    os.mkdir(workingDir + '/Logs')
if not os.path.exists(workingDir + '/Archived_Data'):
    os.mkdir(workingDir + '/Archived_Data')

#CONFIGURE LOGGING
logging.basicConfig(level = logging.INFO, filename = workingDir + '/Logs/unzipper.log', format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')

#EXTRACT ALL THE .ZIP FILES
os.chdir(workingDir)
for zipFile in glob.glob('*.zip'):
    #print(zipFile)
     with zipfile.ZipFile(zipFile,"r") as zip_ref:
            zip_ref.extractall(workingDir)
            # ARCHIVE THE ORIGINAL ZIP FILE FOR BACKUP
            logging.info('Moving ' + zipFile + ' to Archived_Data/' + zipFile)
            copyfile(zipFile,workingDir + '/Archived_Data/' + zipFile)
            os.remove(zipFile)
            logging.info('Completed successfully')

logging.info('Finished job execution')
