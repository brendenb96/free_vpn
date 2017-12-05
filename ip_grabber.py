#! /usr/bin/env python
#
# Created by: Brenden Bickner
# checks if public IP has changed then posts to slack channel
# vars file should have an IP in it before first run

import sys
import urllib2
import subprocess
from optparse import OptionParser
from slacker import Slacker



def main():

    #### COLOURS ####
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    VARS_FILEPATH = '/home/brenden/.ipgrabber.vars'
    SLACK_API_TOKEN = 'xoxb-282920378854-fo83cWTlYsXXjhFXR9Zqu8Xe'


    #### OPTION MENU ####
    usage = "./ip_grabber.py [options]"
    parser = OptionParser(usage=usage)


    slack = Slacker(SLACK_API_TOKEN)
    current_ip = urllib2.urlopen('http://ip.42.pl/raw').read()

    try:
        vars_file = open(VARS_FILEPATH,'r')
        the_vars = vars_file.read().split('\n')
        old_ip = the_vars[0]
    except IOError:
        print "ERROR READING FROM VARS FILE"

    if current_ip != old_ip:
        print "SENDING SLACK MESSAGE"
        slack.chat.post_message("#ip_addresses", current_ip, as_user=True)
        try:
            subprocess.Popen(
                "> " + VARS_FILEPATH,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True).communicate()

            vars_file = open(VARS_FILEPATH,'w')
            vars_file.write("%s\n" %current_ip)
            vars_file.close()
        except IOError:
            print "ERROR WRITING TO VARS FILE"
            return 1

        
    print("Current IP Address:  %s" %current_ip)
    print("Previous IP Address: %s" %old_ip)
 


    return 0


#############################
if __name__ == "__main__":
    sys.exit(main())
#############################