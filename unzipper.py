import zipfile
from shutil import copyfile
import os
import datetime
import logging
import time
import shutil

curDate = datetime.datetime.now()
zipFile = 'uploads/CommunityData.zip'
date_based_name = curDate.strftime('%Y_%m_%d')
extracted_folder = date_based_name + '_DATA'

#SETUP BASIC DIRECTORY STRUCTURE
if not os.path.exists('uploads/Logs'):
    os.mkdir('uploads/Logs')
if not os.path.exists('uploads/Data'):
    os.mkdir('uploads/Data')
if not os.path.exists('uploads/Archived_Data'):
    os.mkdir('uploads/Archived_Data')

#CONFIGURE LOGGING
logging.basicConfig(level = logging.INFO, filename = 'uploads/Logs/ForsyFuturesDigest.log', format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')

#MAKE SURE WE HAVE A .ZIP FILE TO EXTRACT
if os.path.exists(zipFile) & zipfile.is_zipfile(zipFile):
    if not os.path.exists('uploads/Data/'+extracted_folder):
        # UNZIP THE FILE INTO A NEW FOLDER BASED OFF DATE
        logging.info('Unzipping files')
        with zipfile.ZipFile(zipFile,"r") as zip_ref:
            zip_ref.extractall('uploads/Data/'+extracted_folder)
        # ARCHIVE THE ORIGINAL ZIP FILE FOR BACKUP
        logging.info('Moving ' + zipFile + ' to uploads/Archived_Data/CommunityData_' + date_based_name + '.zip')
        copyfile(zipFile,'uploads/Archived_Data/CommunityData_' + date_based_name + '.zip')
        os.remove(zipFile)
        logging.info('Completed successfully')
    else:
        logging.error('Extracted folder already exists (uploads/Data/' + extracted_folder + ')')
else:
    logging.error('No Zip File Found')

#DELETE OLDER DIRECTORIES AND FILES
directory_path = "/var/sftp/uploads/Data/"
current_date = datetime.datetime.now()

logging.info('Deleting old archived files...')
for dir_name in os.listdir(directory_path):
    dir_path = os.path.join(directory_path, dir_name)

    if os.path.isdir(dir_path):
        dir_date = datetime.datetime.fromtimestamp(os.path.getmtime(dir_path))
        if current_date - dir_date > datetime.timedelta(days=365) and dir_date.month != 12:
            logging.info('Deleting directory: ' + dir_path)
            shutil.rmtree(dir_path, ignore_errors=True)