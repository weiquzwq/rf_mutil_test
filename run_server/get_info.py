#coding=utf-8
import threading
from time import ctime,sleep
import os 
import sys
import adb_helper
import socket
import platform
reload(sys)
sys.setdefaultencoding('utf-8')


def get_devices(auto=None):
    #run_grid="adb kill-server "
    #os.system(run_grid)
    ADB=adb_helper.AdbHelper()
    devices=[]
    if auto in ["iOS","ios"]:
    	output=os.popen("idevice_id -l").readlines()
    	for idevice in output:
        	idev=idevice.split('\n')[0]
        	devices.append(idev)
    	return devices

    output=ADB.getConnectDevices()
    #print output
    for line in output:
        if line['state'] in ["device","device\r"]:
            dev=line['uuid']
            devices.append(dev)
    return devices


def get_ip():
	iplist=[]
	iplist = socket.gethostbyname_ex(socket.gethostname())
	ip=iplist[2][0]
	return ip

def get_plat():
  sysstr = platform.system()
  if(sysstr =="Windows"):
    #print ("Call Windows tasks")
    return "Windows"
  elif(sysstr == "Linux"):
    #print ("Call Linux tasks")
    return "Linux"
  else:
    return "Mac"    

if __name__ == "__main__":
        auto=sys.argv[1]
        b = get_devices(auto)
        print b
