#coding=utf-8
import os 
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

if __name__=="__main__":
    booll=check("127.0.0.1",4723)
    if booll==0:
        print "the appium server is not start,please check it"
    else:
        print "appium server is started by ip:{0},port:{1}".format("127.0.0.1",4723)
