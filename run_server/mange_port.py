#coding="utf-8"
import os
import get_info
import socket

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
                os.popen("kill -9 {0}".format(plists[0]))
                print "kill proess:{0} succuess which is used port:{1}".format(plists[0],port)
                print "port:{0} was not use,start server by this port!".format(port)
            except:
                print "kill proess fail"
        else:
            cmd="netstat -ano|findstr 0.0.0.0:{0}".format(port)
            plist=os.popen(cmd).readlines()
            plisttmp=plist[0].split(" ")
            #print plisttmp
            plists=plisttmp[-1].split("\n")
            #print plists[0]
            try:
                os.popen("taskkill /pid {0} -t -f".format(plists[0]))
                print "kill proess:{0} succuess which is used port:{1}".format(plists[0],port)
                print "port:{0} was not use,start server by this port!".format(port)
            except:
                print "kill proess fail"

    else:
        print "port:{0} was not use,start server by this port!".format(port)


if __name__=="__main__":
    kill_port(1234)
