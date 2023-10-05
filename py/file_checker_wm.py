from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import smtplib
from smtplib import SMTPException   
from email.mime.text import MIMEText
import logging
from datetime import date
#import the variables from connections file available in python package
from py import connections
b = connections

# Source Connection details
account_name = b.shi_name
account_key = b.shi_key
source_container_name = "abbottwmextract"
blob_service_client_source = BlobServiceClient(account_name, credential=account_key)

# Define Azure Storage account connection string-CDP
connection_string = b.cdp_con
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
destination_container_name = "anpd-mida-file-system\Raw_Data\Walmart_Retail\Extract"

# Assign source and destination containers to variables
source_container_client = blob_service_client_source.get_container_client(source_container_name)
destination_container_client = blob_service_client.get_container_client(destination_container_name)

#Email function - Send email to Data Analytics group
def send_email():
    sender = 'data.analytics@abbott.com'
    message = """This is a test message - Walmart Files."""
    text_subtype = 'plain'
    msg = MIMEText(message, text_subtype)
    msg['Subject']= 'Walmart files Not yet received. Please check'
    msg['From']   = sender 
    msg['To']   = 'data.analytics@abbott.com' #,daniel.shields@abbott.com, carly.goodman@abbott.com' 

    try:
        smtpObj = smtplib.SMTP('mail.abbott.com',25)
        smtpObj.sendmail(sender, ['data.analytics@abbott.com'], msg.as_string())         
        print("Successfully sent email")
    except SMTPException:
        pass

#Logging Configuration
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
