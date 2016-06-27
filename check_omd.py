#!/usr/bin/python

# check_omd.py - a script for checking a particular
# OMD site status
#
# 2016 By Christian Stankowic
# <info at stankowic hyphen development dot net>
# https://github.com/stdevel
#

from optparse import OptionParser
import subprocess
import io



def getSiteStatus():
	#get username
	proc = subprocess.Popen("whoami", stdout=subprocess.PIPE)
	site = proc.stdout.read().rstrip()
	if options.debug: print "DEBUG: It seems like I'm OMD site '{0}'".format(site)
	
	#get OMD site status
	cmd = ['omd', 'status', '-b']
	if options.debug: print "DEBUG: running command '{0}'".format(cmd)
	proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	res, err = proc.communicate()
	
	if err:
		if "no such site" in err:
			print "UNKNOWN: unable to check site: '{0}' - did you miss running this plugin as OMD site user?".format(err.rstrip())
		else:
			print "UNKNOWN: unable to check site: '{0}'".format(err.rstrip())
		exit(3)
	if res:
		#try to find out whether omd was executed as root
		if res.count("OVERALL") > 1:
			print "UNKOWN: unable to check site, it seems this plugin is executed as root (use OMD site context!)"
			exit(3)
		
		#check all services
		fail_srvs=[]
		warn_srvs=[]
		if options.debug: print "DEBUG: Got result '{0}'".format(res)
		for line in io.StringIO(res.decode('utf-8')):
			service = line.rstrip().split(" ")[0]
			status = line.rstrip().split(" ")[1]
			if service not in options.exclude:
				#check service
				if status != "0":
					if service in options.warning:
						if options.debug: print "{0} service marked for warning has failed state ({1})".format(service, status)
						warn_srvs.append(service)
					else:
						fail_srvs.append(service)
						if options.debug: print "{0} service has failed state ({1})".format(service, status)
			else:
				if options.debug: print "Ignoring '{0}' as it's blacklisted...".format(service)
		if len(fail_srvs) == 0 and len(warn_srvs) == 0:
			print "OK: OMD site '{0}' services are running.".format(site)
			exit(0)
		elif len(fail_srvs) > 0:
			print "CRITICAL: OMD site '{0}' has failed service(s): '{1}'".format(site, ' '.join(fail_srvs))
			exit(2)
		else:
			print "WARNING: OMD site '{0}' has service(s) in warning state: '{1}'".format(site, ' '.join(warn_srvs))
			exit(1)



if __name__ == "__main__":
	#define description, version and load parser
	desc='''%prog is used to check a particular OMD site status. By default, the script only checks a site's overall status. It is also possible to exclude particular services and only check the remaining services (e.g. rrdcached, npcd, icinga, apache, crontab).
	
	Checkout the GitHub page for updates: https://github.com/stdevel/check_omd'''
	parser = OptionParser(description=desc,version="%prog version 1.1.0")
	
	#-d / --debug
	parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="enable debugging outputs")
	
	#-e / --exclude
	parser.add_option("-x", "--exclude", dest="exclude", default=["OVERALL"], action="append", metavar="SERVICE", help="defines one or more services that should be excluded")
	
	#-w / --warning
	parser.add_option("-w", "--warning", dest="warning", default=[""], action="append", metavar="SERVICE", help="defines one or more services that only should throw a warning if not running (useful for fragile stuff like npcd)")
	
	#parse arguments
	(options, args) = parser.parse_args()
	
	#debug outputs
	if options.debug: print "OPTIONS: {0}".format(options)
	
	#check site status
	getSiteStatus()
