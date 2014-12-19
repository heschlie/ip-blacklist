#!/usr/local/bin/python3.4
# This script will check the /var/log/secure file for IP
# addreses that are trying to access the machine and failing
# 
# There is no real intelligence in place yes to check for valid attempts
# where someone just fat fingered their attempt to login, so you can add IPs
# to the whitelist for the moment.

import subprocess

whitelist = ["12.221.225.162"]

def main():
    newIps = getNewIps()
    oldIps = getIpset()
    missingIps = findNewIps(oldIps, newIps)
    addToIpset(missingIps)

def getNewIps():
    """Return the list of potentially new IPs to block"""
    newIps = subprocess.check_output(["/root/bin/get-evil-ips.sh"])
    newIps = convertToList(newIps)
    return newIps

def getIpset():
    """Grabs the list of already blocked IPs"""
    oldIps = subprocess.check_output(["ipset", "list", "evil_ips"])
    oldIps = convertToList(oldIps)
    # Trim ff the header lines from the ipset
    oldIps = oldIps[6:]
    return oldIps

def addToIpset(ipList):
    """Adds the list of IPs to the evil_ips ipset"""
    log = ["Added the following IPs:"]
    for ip in ipList:
        output = subprocess.check_output(["ipset", "add", "evil_ips", ip])
        log.append(ip)
    for l in log:
        print(l)

def findNewIps(old, new):
    missingIps = []
    for ip in new:
        if ip not in old && ip not in whitelist:
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

if __name__ == "__main__":
    main()
