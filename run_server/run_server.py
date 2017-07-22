import os
import time
import sys
#import check_port
import get_info
import threading
import mange_port
reload(sys)
sys.setdefaultencoding('utf-8')

ip=get_info.get_ip()
osplat=get_info.get_plat()
arglist=sys.argv

if "-h" in arglist:
  outstr='''
    how to use it
    -h   help
    -o   the device os.likes ios,android
    -n   the num of starting appium server
  '''
  print outstr
  sys.exit(0)

if "-o" in arglist:
  plat=arglist[arglist.index('-o')+1]
else:
  print "you should input the true args likes: -o ios"
  sys.exit(0)

if "-n" in arglist:
    num=arglist[arglist.index('-n')+1]
else:
    num=0  

divlist=get_info.get_devices(plat)
#print divlist
aport=4723
bport=5723
wport=8101
iport=14723
conf="..\\conf\\appium_cf.json"
conf_mac="conf/appium_cf.json"

def start_server():
        global aport
        global bport
        global wport
        global iport
        global conf
        global conf_mac
        global ip
        global plat

        if plat in ["iOS","ios","Android","android"]:
            if osplat in ["Mac"]:
                if plat in ["iOS","ios"]:
                    mange_port.kill_port(wport)
                    mange_port.kill_port(iport)
                    run_app="xterm -e /bin/bash -c 'sh run_appium_ios.sh {0} {1} {2} ' &".format(iport,wport,ip)
                    iport=iport+1
                    wport=wport+1              
                else:
                    mange_port.kill_port(aport)
                    mange_port.kill_port(bport)
                    run_app="xterm -e /bin/bash -c 'sh run_appium_ad.sh {0} {1} {2}' &".format(aport,bport,ip)
                    aport=aport+1
                    bport=bport+1
            else:
                mange_port.kill_port(aport)
                mange_port.kill_port(bport)
                run_app="start run_appium.bat {0} {1} {2}".format(aport,bport,ip)
                aport=aport+1
                bport=bport+1
            os.system(run_app)
            
            
        elif plat in ["grid","Grid"]:
            mange_port.kill_port(bport)
            if osplat in ["Mac"]:
                run_app="xterm -e /bin/bash -c 'sh run_appium_grid.sh {0} {1} {2} {3} {4}' &".format(ip,aport,bport,div,conf_mac)
            else:
                run_app='start run_appium_grid.bat {0} {1} {2} {3} {4}'.format(ip,aport,bport,div,conf)
            os.system(run_app)     
            aport=aport+1
            bport=bport+1


        else:
            print "Not support this os device!"

if divlist==[]:
    if int(num)==0:
        if plat in ["iOS","ios"]:
            print "No iOS Device Connect The PC!"
        elif plat in ["android","Android"]:
            print "NO Android Device Connect The PC!"
        else:
            print "Not support this os device!"
    else:
        t=0
        for t in range (int(num)):
            start_server()
               

else:
    if len(divlist)>=int(num):
        for div in divlist:
            start_server()
    else:
        t2=0
        for t2 in range (int(num)):
            start_server()      


time.sleep(3)
