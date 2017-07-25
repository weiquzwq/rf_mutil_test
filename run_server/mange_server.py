#coding="utf-8"
import os
import get_info
import socket
import sys
import requests
import time 


def check(ip,port):
    flag=1
    ct=0
    while(flag and ct<10):
        try:
            r = requests.get(url='http://{0}:{1}/favicon.ico'.format(ip,port))
            if r.status_code==200:
                print "the appium respone code is {0}".format(r.status_code)
                flag=0
                return 1
            else:
                ct=ct+1
                print "the appium respone code is {0}".format(r.status_code)
                print "the code is not equels 200 ,it would something wrong,please check it,,time:{0} ".format(ct)            
                time.sleep(3)
        except:
            ct=ct+1
            print "appium server is not start by port:{0},try to check again now ,time:{1}".format(port,ct)
            time.sleep(3)
            
    if ct==10:
         return 0

def check_running(ip,port):
        try:
            r = requests.get(url='http://{0}:{1}/favicon.ico'.format(ip,port))
            if r.status_code==200:
                return 1
            else:
                print "the appium respone code is {0}".format(r.status_code)         
                return 0
        except:
            return 0

def IsOpen(ip,port):  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
    try:  
        s.connect((ip,int(port)))  
        s.shutdown(2)  
        return True  
    except:  
        return False

def kill_port(port):
    ip = get_info.get_ip()
    plat=get_info.get_plat()
    if IsOpen(ip, port) == True:
        if plat!="Windows":
            cmd="lsof -i :{0}".format(port)
            plist=os.popen(cmd).readlines()
            plisttmp=plist[1].split("    ")
            plists=plisttmp[1].split(" ")
            #print plists[0]
            try:
                if check_running(ip,port)==0:
                    os.popen("kill -9 {0}".format(plists[0]))
                    print "kill proess:{0} succuess which is used port:{1}".format(plists[0],port)
                    return 1
                else:
                    print "the appium server by port:{0} still run,skip".format(port)
                    return 0   
            except:
                print "kill proess fail"
                return 0
        else:
            cmd="netstat -ano|findstr 0.0.0.0:{0}".format(port)
            plist=os.popen(cmd).readlines()
            plisttmp=plist[0].split(" ")
            #print plisttmp
            plists=plisttmp[-1].split("\n")
            #print plists[0]
            try:
                if check_running(ip,port)==0:
                    os.popen("taskkill /pid {0} -t -f".format(plists[0]))
                    print "kill proess:{0} succuess which is used port:{1}".format(plists[0],port)
                    return 1
                else:
                    print "the appium server by port:{0} still run,skip".format(port)
                    return 0 
            except:
                print "kill proess fail"
                return 0

    else:
        print "port:{0} was not use".format(port)
        return 1





if __name__=="__main__":
    booll=check_running("192.168.1.104",14723)
    if booll==0:
        print "the appium server is not start,please check it"
    else:
        print "appium server is started by ip:{0},port:{1}".format("127.0.0.1",4723)
