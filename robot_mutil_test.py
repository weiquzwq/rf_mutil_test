#coding=utf-8
import multiprocessing
from time import ctime,sleep
import os 
import sys
from run_server import get_info,mange_server
reload(sys)
sys.setdefaultencoding('utf-8')

def run(arg):
   os.system(str(arg))

lprocess = []
ipaddr=get_info.get_ip()
wdhost="http://{0}:".format(ipaddr)
osplat=get_info.get_plat()

arglist=sys.argv

if "-h" in arglist:
  outstr='''
    how to use it
    -h   help
    -s   the testsuite or testcase path
    -t   taglist,likes "tag1,tag2", split by ,
    -o   the device os.likes ios,android
    -r   the remoteurl,use for gird
    -p   server port
    -sp  second server port
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
  tags=[]

if "-o" in  arglist:
  testos=arglist[arglist.index('-o')+1]
else:
  print "you should input the true args likes: -o ios"
  sys.exit(0)

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

if "-r" in  arglist:
  remoteurl=arglist[arglist.index('-r')+1]
else:
  remoteurl='None'         


taglist=tags.split(',')

#if len(tags)==0:
#   cmd='pybot -o .\\resultDir\\output.xml -l .\\resultDir\\log.html -r .\\resultDir\\report.html --variable remote_url:{1} {0}'.format(testsuite,remoteurl)
#   p=multiprocessing.Process(target=run,args=(cmd,))
#   lprocess.append(p)

if testos in ["iOS","ios"]:
    i=0
    divlist=get_info.get_devices("iOS")
    for tag in taglist:
      wdport=wdhost+str(iport)+"/wd/hub"
      #print wdport
      booll=mange_server.check(ipaddr,iport)
      if booll==0:
        print "the appium server by {0} is not start,please check it".format(wdport)
        sys.exit(0)
      cmd='pybot -i {0} -o ./resultDir_ios/output-{0}.xml -l ./resultDir_ios/log-{0}.html -r ./resultDir_ios/report-{0}.html --variable remote_url:{2} --variable udid:{3} {1}'.format(tag,testsuite,wdport,divlist[i])
      p=multiprocessing.Process(target=run,args=(cmd,))
      lprocess.append(p)
      iport=iport+1
      i=i+1

elif testos in ["Android","android"]:
        i=0
        divlist=get_info.get_devices("Android")
        for tag in taglist:
          wdport=wdhost+str(aport)+"/wd/hub"
          #print wdport
          booll = mange_server.check(ipaddr, aport)
          if booll == 0:
              print "the appium server by {0} is not start,please check it".format(wdport)
              sys.exit(0)
          if osplat!="Windows":
            cmd='pybot -i {0} -o ./resultDir_ad/output-{0}.xml -l ./resultDir_ad/log-{0}.html -r ./resultDir_ad/report-{0}.html --variable remote_url:{2} --variable udid:{3} {1}'.format(tag,testsuite,wdport,divlist[i])
          else:
            cmd='pybot -i {0} -o .\\resultDir_ad\\output-{0}.xml -l .\\resultDir_ad\\log-{0}.html -r .\\resultDir_ad\\report-{0}.html --variable remote_url:{2} --variable udid:{3} {1}'.format(tag,testsuite,wdport,divlist[i])
          p=multiprocessing.Process(target=run,args=(cmd,))
          lprocess.append(p)
          aport=aport+1
          i=i+1

elif testos in ["Web","web"]:
  if remoteurl=='None':
      print "if you want to run web mutil test by the tool,print input the sele-grid url!"
      sys.exit(0)

  else:
    for tag in taglist:
      if osplat!="Windows":
        cmd='pybot -i {0} -o ./resultDir_web/output-{0}.xml -l ./resultDir_web/log-{0}.html -r ./resultDir_web/report-{0}.html --variable remote_url:{2}  {1}'.format(tag,testsuite,remoteurl)
      else:
        cmd='pybot -i {0} -o .\\resultDir_web\\output-{0}.xml -l .\\resultDir_web\\log-{0}.html -r .\\resultDir_web\\report-{0}.html --variable remote_url:{2} {1}'.format(tag,testsuite,remoteurl)
      p=multiprocessing.Process(target=run,args=(cmd,))
      lprocess.append(p)
         

else:   
   print "please input true args!"
   sys.exit(0)

if __name__ == '__main__':
    if osplat!="Windows":

      if testos in ["iOS","ios"]:
        os.system('rm -rf resultDir_ios/*')
      elif testos in ["Android","android"]:
        os.system('rm -rf resultDir_ad/*')
      else:
        os.system('rm -rf resultDir/*')

    else:
      if testos in ["Android","android"]:
        os.system('del /f/s/q/a .\\resultDir_ad\\*')
      else:
        os.system('del /f/s/q/a .\\resultDir\\*')  
    for p in lprocess:
        p.daemon = True
        p.start()
        
    for p in lprocess:
        p.join()

    if osplat!="Windows":
        sleep(2)
        if testos in ["iOS","ios"]:
          os.system(u"rebot --output ./resultDir_ios/output.xml  -l ./resultDir_ios/log.html -r ./resultDir_ios/report.html --merge ./resultDir_ios/output-*.xml")
        elif testos in ["Android","android"]:
          os.system(u"rebot --output ./resultDir_ad/output.xml  -l ./resultDir_ad/log.html -r ./resultDir_ad/report.html --merge ./resultDir_ad/output-*.xml")
        else:
           os.system(u"rebot --output ./resultDir_web/output.xml  -l ./resultDir_web/log.html -r ./resultDir_web/report.html --merge ./resultDir_web/output-*.xml")
    else:
        sleep(2)
        if testos in ["Android","android"]:
          os.system(u"rebot --output .\\resultDir_ad\\output.xml  -l .\\resultDir_ad\\log.html -r .\\resultDir_ad\\report.html --merge .\\resultDir_ad\\output-*.xml")
        else:  
          os.system(u"rebot --output .\\resultDir_web\\output.xml  -l .\\resultDir_web\\log.html -r .\\resultDir_web\\report.html --merge .\\resultDir_web\\output-*.xml")
    sleep(2)
    print "Test Finish"
