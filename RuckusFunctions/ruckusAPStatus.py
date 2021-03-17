#!/usr/local/bin/python3.9

import os,sys
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


if len(sys.argv) == 1:
	raise Exception('AP MAC Must be passed')
	
if len(sys.argv) > 2:
	raise Exception('too many parameters passed')

strAPMac = sys.argv[1].strip().lower()

print ('AP Mac ' + strAPMac)

import csv
import sdkRND_API
import re

import datetime
reportline = list()
report = list()

#create an object containing the ND API Functions from Class
apiND = sdkRND_API.clsSdkRndAPI()

resp = apiND.getAPStatus(strAPMac)
print(resp)
