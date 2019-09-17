#!/usr/bin/python

import os, time, socket
import smtplib
from email.mime.text import MIMEText

distro = 'mkarimi@beachbody.com'
walk_dir = '/home'

bodyOfMail = """
The following files are older than 30 minutes in server {0}


""".format(socket.gethostname())

filesFound = False

def getFileAge(root, files):
    global filesFound
    global bodyOfMail
    for file in files:
        if not file.startswith("."):
            filePath = os.path.join(root, file)
            createdTime = time.ctime(os.path.getctime(filePath))
            st = os.stat(filePath)
            ageInSec = (time.time()-st.st_mtime)

            if ageInSec > 3600: #if older than 60 minutes
                filesFound = True
                bodyOfMail += filePath + " --- was created: " + createdTime + '\n\n'

def sendMail():
    global bodyOfMail
    global filesFound
    if filesFound:
        s = smtplib.SMTP('smtprelay.beachbody.local')
        msg = MIMEText(bodyOfMail)
        sender = 'no-reply@%s' %(socket.gethostname())
        recipients = ['soasupport@beachbody.com','soateam@beachbody.com','netops@beachbody.com']
        msg['Subject'] = "NOTICE: old files in %s" % (socket.gethostname())
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        s.sendmail(sender, recipients, msg.as_string())

def getFiles(walk_dir):
    global bodyOfMail
    exclusion_dir = []
    with open('/usr/sbin/scripts/scan.list', 'r') as f:
        for line in f:
            exclusion_dir.append(line.rstrip('\n'))

    for root, subdirs, files in os.walk(walk_dir):
        if any(substring in root for substring in exclusion_dir):
            None
        else:
            getFileAge(root,files)

if __name__ == "__main__":
    getFiles(walk_dir)
    sendMail()