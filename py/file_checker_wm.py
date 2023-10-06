import time
import sys
from ENV_git import *

#Getting current date
curr_day = date.today()
today = curr_day.weekday()
#use the below command to install the python package from GitHub to your machine
#os.system('pip install git+https://github.com/ANPD-Data-Analytics/PythonScript.git')
#use the below command to un install the python package to your machine
#pip uninstall py
from py import connections
b = connections

#Assign variable for the Files with current date
fnCal = 'WMCalendar_'+str(date.today())+'.csv.gz'
fnFact = 'WMFact_'+str(date.today())+'.csv.gz'
fnItem = 'WMItem_'+str(date.today())+'.csv.gz'
fnStore = 'WMStore_'+str(date.today())+'.csv.gz'
target_filenames = [fnCal,fnFact,fnItem,fnStore]

#Setting Log File properties
logging.basicConfig(filename='log/WMLog_'+str(date.today())+'.log',
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger.info("Start of the Script")
while target_filenames:
    # List all files in the source container
    files = source_container_client.list_blobs()
    counter = 0
   
    for file in files:
    #Loop for all 4 available files.    
        file_name = file.name
        if file_name in target_filenames:
            #List the files in Source and Destination directory
            source_blob_client = source_container_client.get_blob_client(file_name) 
            destination_blob_client = destination_container_client.get_blob_client(file_name)            
            source_blob_properties = source_blob_client.get_blob_properties()
            # Copy the matching file to the destination container
            destination_blob_client.start_copy_from_url(source_blob_client.url, metadata=source_blob_properties.metadata)
            print(f"File {file_name} copied to the destination container.")
            logger.info(f"Successfully {file_name} copied to the destination container.")
            # Remove the file from the list of target filenames
            target_filenames.remove(file_name)
            #Once all 4 files are transferred, delete the files from Source, Walmart's Container
            time.sleep(180)
            source_blob_client.delete_blob()
            
    
    if target_filenames:
        if today == 6:
            # Sleep for a while before checking again
            print("Sunday Run: Not all files found.")
            logger.info(f"No Retries on Sunday. The Sunday job triggers at 6 PM")
            send_email()
            sys.exit(0)

        else:
            for i in range(0,5):
                i+=1
                print("Not all files found. Sleeping for 1 hour and retrying...")
                logger.info(f"Retrying after 1 hour,Not all files found. No of Attempts: {i}. Total Attempts: 3")
                time.sleep(3600)
                print(i)
                if i>=5:
                    logger.info("Didn't received all Walmart Files, Sending email to the team to validate and escalate...")
                    send_email()
                    logger.error("Shutting down this Program. All attempts failed")
                    sys.exit(0)
    else:
        logger.info("All Source files found and copied to the destination container...")
        logger.info("Sleeping for 5 min.")
        time.sleep(180)
        trigger_file = 'trigger.txt'
        file_content = ''
        #Creating a trigger.txt file 
        logger.info("Creating Trigger file.")
        blob_trigger_file = destination_container_client.get_blob_client(trigger_file)
        blob_trigger_file.upload_blob(file_content,overwrite=True)
        print("Trigger File Successfully Created in Extract directory.")
        logger.info("Trigger File Successfully Created in Extract directory...")
        logger.info("Program completed successfully, Exiting...")
        sys.exit(0)
    logger.info("End of the Script")
