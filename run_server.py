import os
import time
import sys
#import check_port
from run_server import get_info
import threading
from run_server import mange_server
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
    -p   server port
    -sp  second server port
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

if "-p" in arglist:
    aport=int(arglist[arglist.index('-p')+1])
    iport=int(arglist[arglist.index('-p')+1])
else:
    aport=4723
    iport=14723

if "-sp" in arglist:
    bport=int(arglist[arglist.index('-sp')+1])
    wport=int(arglist[arglist.index('-sp')+1])
else:
    bport=5723
    wport=8101    

divlist=get_info.get_devices(plat)
#print divlist

def start_server():
        global aport
        global bport
        global wport
        global iport
        global ip
        global plat

        if plat in ["iOS","ios","Android","android"]:
            if osplat in ["Mac"]:
                if plat in ["iOS","ios"]:
                    result=mange_server.kill_port(iport)
                    mange_server.kill_port(wport)
                    run_app="xterm -e /bin/bash -c 'sh ./run_server/run_appium_ios.sh {0} {1} {2} ' &".format(iport,wport,ip)
                    iport=iport+1
                    wport=wport+1              
                else:
                    result=mange_server.kill_port(aport)
                    mange_server.kill_port(bport)
                    run_app="xterm -e /bin/bash -c 'sh ./run_server/run_appium_ad.sh {0} {1} {2}' &".format(aport,bport,ip)
                    aport=aport+1
                    bport=bport+1
            else:
                result=mange_server.kill_port(aport)
                mange_server.kill_port(bport)
                run_app="start .\\run_server\\run_appium.bat {0} {1} {2}".format(aport,bport,ip)
                aport=aport+1
                bport=bport+1

            if result==1:
                os.system(run_app)
            else:
                pass

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
