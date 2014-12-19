#!/usr/local/bin/python3.4
# This script will check the /var/log/secure file for IP
# addreses that are trying to access the machine and failing
# 
# There is no real intelligence in place yes to check for valid attempts
# where someone just fat fingered their attempt to login, so you can add IPs
# to the whitelist.txt for the moment.

import subprocess
import sys, os
import time
import logging, logging.handlers

LOGFILE = "blacklist_log"

try:
    whitelist = open("whitelist.txt").read().splitlines()
except FileNotFoundError:
    pass

# Steup logging
logger = logging.getLogger('blacklist_log')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(LOGFILE, 
                                               maxBytes=1000000,
                                               backupCount=5)
logger.addHandler(handler)

def main():
    newIps = getNewIps()
    oldIps = getIpset()
    missingIps = findNewIps(oldIps, newIps)
    addToIpset(missingIps)

def getNewIps():
    """Return the list of potentially new IPs to block"""
    getEvilIps = getPath() + "/get-evil-ips.sh"
    newIps = subprocess.check_output([getEvilIps])
    newIps = convertToList(newIps)
    return newIps

def getIpset():
    """Grabs the list of already blocked IPs"""
    oldIps = subprocess.check_output(["ipset", "list", "evil_ips"])
    oldIps = convertToList(oldIps)
    # Trim ff the header lines from the ipset list command
    oldIps = oldIps[6:]
    return oldIps

def addToIpset(ipList):
    """Adds the list of IPs to the evil_ips ipset"""
    date = time.strftime("%c")
    added = []
    for ip in ipList:
        output = subprocess.check_output(["ipset", "add", "evil_ips", ip])
        added.append(ip)

    numIps = len(added)
    logger.info(date + "\n" + "Added " + str(numIps) + ":\n")
    for ip in added:
        logger.info(ip)

def findNewIps(old, new):
    missingIps = []
    for ip in new:
        if ip not in old and ip not in whitelist:
            missingIps.append(ip)
    return missingIps

def convertToList(bytestring):
    """
    Convert the bytestring into a normal String object
    and then break it up into a list of strings containing
    the IP addresses, and pop the empty line off the end.
    """
    newList = bytestring.decode("utf-8").split("\n")
    newList.pop()
    return newList

def getPath():
    pathName = os.path.dirname(sys.argv[0])
    return os.path.abspath(pathName)

if __name__ == "__main__":
    main()
