#coding=utf8
from time import ctime,sleep
import os 
import sys
from run_server import get_info

arglist=sys.argv
plat=get_info.get_plat()

if "-h" in arglist:
  outstr='''
    how to use it
    -h   help
    -s   the testsuite or testcase path
    -t   taglist,likes "tag1,tag2", split by ,
    -o   the device os.likes ios,android
    -p   server port
    -sp  second server port
    -n   the num of start server
    -d   the number of the device which is the start one to autotest
  '''
  
  print outstr
  sys.exit(0)

if "-s" in arglist:
  testsuite=arglist[arglist.index('-s')+1]
else:
  print "you should select the testsuite!"
  sys.exit(0)

if "-t" in  arglist:
  tags=arglist[arglist.index('-t')+1]
else:
  print "if you want to run test by mutil,you can input like this : -t node1,node2"
  sys.exit(0)

if "-n" in arglist:
    num=arglist[arglist.index('-n')+1]
else:
    num=0

if "-o" in  arglist:
  testos=arglist[arglist.index('-o')+1]
else:
  print "you should input the true args likes: -o ios"
  sys.exit(0)

if "-d" in  arglist:
  startd=arglist[arglist.index('-d')+1]
else:
  startd=1

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
if plat in ["Mac"]:
  if testos in ["iOS","ios"]:
    run_server="python run_server.py -o {0} -p {1} -sp {2} -n {3}".format(testos,iport,wport,num)
    run_test="python robot_mutil_test.py -s {0} -t {1} -o {2} -p {3} -sp {4} -d {5}".format(testsuite,tags,testos,iport,wport,startd)
  else:
    run_server="python run_server.py -o {0} -p {1} -sp {2} -n {3}".format(testos,aport,bport,num)
    run_test="python robot_mutil_test.py -s {0} -t {1} -o {2} -p {3} -sp {4} -d {5}".format(testsuite,tags,testos,aport,bport,startd)

else:
    run_server="python run_server.py -o {0} -p {1} -sp {2} -n {3}".format(testos,aport,bport,num)
    run_test="python robot_mutil_test.py -s {0} -t {1} -o {2} -p {3} -sp {4} -d {5}".format(testsuite,tags,testos,aport,bport,startd)

os.system(run_server)
sleep(5)
os.system(run_test)
