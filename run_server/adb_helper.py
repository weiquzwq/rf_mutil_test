#-*- coding: utf-8 -*-
"""
adb help tools
get device list
get api level
get platform version

execute monkey script
start app
"""
import os
import logging
import subprocess
import re
import time

def is_windows():
    if os.name in ('nt','ce'):
        return True
    return False

#---------------------------------------------------------------------------
# 模块工具类方法
# 获取Adb对象
#---------------------------------------------------------------------------
def getAdb(name):
    pass

class AdbHelper (object):
    """
    ADB 命令行方法帮助类
    """
    def __init__(self, opts={}):
        """
        初始化方法，opts为一个map类型参数
        """
        if 'sdkRoot' in opts:
            self.sdkRoot = opts.sdkRoot
        elif "ANDROID_HOME" in os.environ:
            self.sdkRoot = os.environ['ANDROID_HOME']
        self.iswindows = is_windows()
        result,self.adb = self._checkaSdkBinarypresent('adb')
        if not result:
            raise Exception("adb tool not found")
        if 'logfile' in opts:
            self.logfile = opts.logfile
        else:
            self.logfile = os.getcwd() + os.sep + "adb.log"
        if 'log_level' in opts:
            self.log_level = opts.log_level
        else:
            self.log_level = logging.DEBUG

        self.logger = logging.getLogger("adb_log")
        self.logger.setLevel(self.log_level)
        #log to file
        log_fileHandler = logging.FileHandler(self.logfile)
        log_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        log_fileHandler.setFormatter(log_formater)
        self.logger.addHandler(log_fileHandler)
        #default argument of adb
        self.adb_defaultArgs = []
        self.devices = []
        self.binarySearchPath = []

    def _checkaSdkBinarypresent(self, binary):
        '''
        检查android工具,
        platform-tools: 平台工具,adb,dmtracedump
        tools: ddms,android,monitor,monkeyrunner,traceview,uiautomatorviewer
        build-tools: android各平台的构建工具,appt,aapt2,zipalign,
        :param binary:
        :return:
        '''
        binaryName = binary
        if self.iswindows:
            if not binaryName.endswith(".exe"):
                binaryName = binaryName + ".exe"
        if not self.sdkRoot:
            raise   Exception("%s not found", binaryName)
        self.binarySearchPath = []
        platform_tools_binary =  self.sdkRoot + os.sep + "platform-tools" + os.sep + binaryName
        tools_binary = self.sdkRoot + os.sep + "tools" + os.sep + binaryName
        build_tools_path = self.sdkRoot + os.sep + "build-tools"
        build_tools_binarys = [build_tools_path + os.sep + build_tools_dir + os.sep + binaryName for build_tools_dir in os.listdir(build_tools_path)]
        self.binarySearchPath.append(platform_tools_binary)
        self.binarySearchPath.append(tools_binary)
        self.binarySearchPath += build_tools_binarys
        for bi in self.binarySearchPath:
            if os.path.exists(bi):
                return True,bi

        raise   Exception("%s not found", binaryName)
    def shell(self, cmd, wait=True, stdout=subprocess.PIPE):
        return self.execshell("shell %s" % cmd, wait, stdout)

    def execshell(self,cmd, wait=True, stdout=subprocess.PIPE):
        if not cmd:
            raise Exception("command can't be empty")
        fullCmd = self.adb + " " +  " ".join(self.adb_defaultArgs) + " " + cmd
        #return os.popen(fullCmd).readline()
        if wait == False:
            process = subprocess.Popen(fullCmd.split(), stdout=stdout)
            return True, process
        try:
            process = subprocess.Popen(fullCmd.split(), stdin=subprocess.PIPE, stdout=stdout, stderr=subprocess.PIPE)
        except (OSError, ValueError) as err:
            self.logger.error("Run %s command Exception", fullCmd)
            raise Exception("subprocesserror")
        stdoutdata, stderrdata = process.communicate()
        self.logger.debug(fullCmd + " status " + str(process.returncode))
        if process.returncode:
            return False, stderrdata
        else:
            return True,stdoutdata
        # result = []
        # while True:
        #     output = process.stdout.readline()
        #     if output != '':
        #         result.append(output)
        #     else:
        #         break
        # return  result

    def setDeviceId(self, deviceId):
        self.currentDeviceId = deviceId
        if not "-s " + deviceId in self.adb_defaultArgs:
            self.adb_defaultArgs.append("-s " + deviceId)

    def getConnectDevices(self):
        self.logger.debug("Get connected devices")
        result,output_lines = self.execshell("devices")
        _devices = []
        for line in output_lines.split('\n'):
            if line.strip() and line.find("List of devices") == -1 and line.find("* daemon") == -1 and line.find("offline")==-1:
                lineinfo = line.split("\t")
                #print lineinfo
                _devices.append({"uuid":lineinfo[0], "state": lineinfo[1]})
        self.devices = _devices
        self.logger.debug(str(len(self.devices)) + " device(s) connected")
        return self.devices

    def reconnect(self):
        self.logger.debug("Reconnect devices")
        self.execshell("reconnect")

    def killAdbServer(self):
        """
        kill adb server by shell
        """
        return self.execshell("kill-server")

    def startAdbServer(self):
        return self.execshell("start-server")

    def checkProcess(self, processName):
        '''
        检查进程是否存在
        adb shell ps 将输出
        USER     PID   PPID  VSIZE  RSS     WCHAN    PC         NAME
        :param processName:
        :return:
        '''
        self.logger.debug("Check process %s" % processName)
        result,output = self.execshell("shell ps")
        for line in output.split("\r\n"):
            line = line.strip().split()
            if not line:
                continue
            _t = line[len(line)-1]
            if _t and _t.find(processName) !=-1:
                self.logger.debug("Find process %s from %s" % (processName, _t) )
                return True

        self.logger.debug("Canot find process %s" % processName)
        return False

    def push(self, localPath, remotePah):
        return self.execshell("push %s %s  " % (localPath,remotePah) )

    def pull(self, remotePath, localPath):
        return self.execshell("pull %s %s\r\n" % (remotePath, localPath) )

    def forwardPort(self, systemPort, devicePort):
        '''
        adb forward <local> <remote> - forward socket connections
                                 forward specs are one of:
                                   tcp:<port>
                                   localabstract:<unix domain socket name>
                                   localreserved:<unix domain socket name>
                                   localfilesystem:<unix domain socket name>
                                   dev:<character device name>
                                   jdwp:<process pid> (remote only)
        :param systemPort:  PC机的端口号
        :param devicePort:  设备(手机、模拟器)端口号
        :return:
        '''
        return self.execshell("forward tcp: %s tcp: %s" % (systemPort, devicePort))

    def isDeviceConnected(self):
        devices = self.getConnectDevices()
        if len(devices) > 0:
            return True
        else:
            return False

    def getPIDByName(self, name):
        #command = " shell ps '%s'" % name
        command = " shell ps | grep %s " % name
        result, output = self.execshell(command)
        pids = []
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
            m = re.match("[^\t ]+[\t ]+([0-9]+)", line)
            if m is not None:
                pids.append(m.group(1))
        return pids

    def killProcessByPID(self, pid):
        '''
        需要root权限
        :param pid:
        :return:
        '''
        return self.shell("kill  %s" % pid)

    def killProcessByName(self, name):
        pids = self.getPIDByName(name)
        for pid in pids:
            self.logger.debug('kill process %s' % pid)
            self.killProcessByPID(pid)

    def uiautomator_dump(self, path):
        self.shell("uiautomator dump /sdcard/window_dump.xml")
        return self.pull("/sdcard/window_dump.xml", path)

    def clear(self, pkg):
        return self.shell("pm clear %s " % pkg)

    def forceStop(self, pkg):
        return self.shell("am force-stop %s " % (pkg,))

    def install(self, apk, replace=True):
        '''
        用adb install安装应用包
        :param apk:
        :param replace:
        :return:
        '''
        cmd = 'install'
        if replace:
            cmd +=  ' -r '
        cmd += '"%s"' % apk
        return self.execshell(cmd)

    def uninstall(self, pkg):
        self.forceStop(pkg)
        result = self.execshell("uninstall %s " % (pkg,))
        if result.find("Success") == -1:
            self.logger.debug("App was not uninstalled")
        else:
            self.logger.debug("App was uninstalled")

    def mkdir(self, path):
        return self.shell('mkdir -p %s' % (path))
    def remove(self, path):
        return self.shell("rm -rf %s" % (path))

    def screenshot(self, despath):
        '''
        截屏
        :param despath:
        :return:
        '''
        path = '/sdcard/%s.png' % (time.time(),)
        self.shell("screencap -p %s" % (path,))
        self.pull(path, despath)
        self.remove(path)

    def exescript(self, path):
        '''
        执行本地脚本
        push script file to /data/local/tmp/
        增加执行权限
        chmod 0777 /data/local/tmp/file
        执行脚本
        /data/local/tmp/file
        :param path:
        :return:
        '''
        destFile = "/data/local/tmp/" + str(time.time()) + ".sh"
        result,_ = self.push(path,destFile)
        if not result:
            return False,'push file (%s) to device failed' % path
        cmd = "chmod 0777 %s" % destFile
        result,_ = self.shell(cmd)
        if not result:
            return False, 'change file (%s) mod failed' % destFile
        self.logger.debug("exec script: %s" % destFile)
        return self.shell(destFile, False)

    def getstarttime(self, pkg):
        _,result = self.shell("am start -S -W %s | grep TotalTime" % pkg)
        if result:
            return result.split(":")[-1].strip()
        return  ''

    def getmeminfo(self, type=None):
        '''
        获取内存信息,android.os.Process readProcLines
        /proc/meminfo 文件包含内存所有信息
        MemTotal:        2015044 kB
        MemFree:           92984 kB
        Buffers:           47724 kB
        Cached:           239408 kB
        ...
        :return:
        '''
        result,meminfo = self.shell("cat /proc/meminfo")
        if not result:
            return False,'get meminfo failed'

        if not type:
            return True, meminfo.split('\r\n')

        meminfos = meminfo.split('\r\n')
        if type == 'total':
            return True, meminfos[0].split(":")[-1].strip()
        elif type == 'free':
            return True, meminfos[1].split(":")[-1].strip()
        elif type == 'buffer':
            return True, meminfos[2].split(":")[-1].strip()

    def getMemTotal(self):
        return self.getmeminfo('total')

    def getMemFree(self):
        return self.getmeminfo('free')

    def getMemFuffers(self):
        return self.getmeminfo('buffer')

    def getDumpmeminfo(self, package='', find='TOTAL'):
        '''
        根据应用包名查看内存信息,默认返回TOTAL信息
        使用dumpsys meminfo
        例如：
        Applications Memory Usage (kB):
        Uptime: 1257823060 Realtime: 1500084325

        ** MEMINFO in pid 14891 [com.mi.global.shop] **
                        Pss      Private  Private  Swapped     Heap     Heap     Heap
                        Total    Dirty    Clean    Dirty     Size    Alloc     Free
                        ------   ------   ------   ------   ------   ------   ------
          Native Heap        0        0        0        0    19884    15058     4157
          Dalvik Heap    46824    46684        0    18824    81336    68169    13167
         Dalvik Other     5087     4932       28      572
                Stack      768      768        0        8
               Ashmem      134       76        0        0
            Other dev      196      188        8        0
             .so mmap    11548     2680     3580     1312
            .apk mmap      488        0      156        0
            .ttf mmap      151        0      104        0
            .dex mmap     5646      112     4424       52
           Other mmap     1062        4      932        0
              Unknown    14625    14604        0      116
                TOTAL    86529    70048     9232    20884   101220    83227    17324

         Objects
                       Views:      855         ViewRootImpl:        2
                 AppContexts:        5           Activities:        2
                      Assets:        5        AssetManagers:        5
               Local Binders:       22        Proxy Binders:       29
            Death Recipients:        1
             OpenSSL Sockets:       15

         SQL
                 MEMORY_USED:      727
          PAGECACHE_OVERFLOW:      635          MALLOC_SIZE:       85

         DATABASES
              pgsz     dbsz   Lookaside(b)          cache  Dbname
                 4      604            103       66/50/15  /data/data/com.mi.global.shop/databases/google_analytics_v4.db
        :param package:
        :return:
        '''
        result, meminfo = self.shell("dumpsys meminfo %s" % package)
        if not result:
            return False, 'dumpsys meminfo failed'

        if "No process found for:" in meminfo:
            return False, "Not process found for %s" % package

        for line in meminfo.split("\r\n"):
            if find in line:
                return True, line

    def getProcessCpuInfo(self, pid):
        result,cpuinfo = self.shell("cat /proc/%s/stat" % pid)
        if not result:
            return False,cpuinfo
        return True, cpuinfo.split()

    def getProcessCpuUsage(self, pkg):
        '''
        获取某个PID的CPU信息: /proc/pid/stat
        pid   command  state parentid groupid  sessionid tty_nr tpgidb flags minflt cminflt majflt cmajflt utime stime...
        计算公式(http://stackoverflow.com/questions/1420426/how-to-calculate-the-cpu-usage-of-a-process-by-pid-in-linux-from-c#answer-1424556)：
        1. pidtotal = utime + cutime
        2. total = /proc/stat total
        usage = pidtotal_diff/total_diff
        :return:
        '''
        pids = self.getPIDByName(pkg)
        if len(pids)<=0:
            return False, "No process found for %s " % pkg
        pid = pids[0]
        result,cpuinfo_pid = self.getProcessCpuInfo(pid)
        if not result:
            return False, "Get process %s cpu info failed " % pid
        utime1 = int(cpuinfo_pid[13])
        stime1 = int(cpuinfo_pid[14])
        pid_cpu_total1 = utime1 + stime1
        result, cpuinfo_total = self.getCpuInfo()
        if not result:
            return False, "Get Cpu info  %s  failed "
        total1 = sum(int(i) for i in cpuinfo_total[1:])
        #时间片
        time.sleep(1)#sleep for 0.5 second

        result, cpuinfo_pid = self.getProcessCpuInfo(pid)
        utime2 = int(cpuinfo_pid[13])
        stime2 = int(cpuinfo_pid[14])
        pid_cpu_total2 = utime2 + stime2
        result, cpuinfo_total2 = self.getCpuInfo()
        total2 = sum(int(i) for i in cpuinfo_total2[1:])
        cpu_usage = 0.0
        if total2-total1 >0:
            cpu_usage = 100 * (pid_cpu_total2-pid_cpu_total1) / ((total2-total1) * 1.0)
        return True, cpu_usage

    def getCpuInfo(self):
        '''
         获取CPU的信息: cat /proc/stat
             user nice system idle iowait  irq  softirq steal guest guest_nice
        cpu  4705 356  584    3699   23    23     0       0     0          0
              用户态运行时间 nice值为负（高优先级）进程占用CPU时间，核心态时间，除iowait外的等待时间，iowait时间，硬中断时间,软中断时间,丢失时间(被其他虚拟CPU抢占)
        :return:
        '''
        result, statinfo = self.shell("cat /proc/stat")
        if not result:
            return False, statinfo
        cpu_line = statinfo.split("\r\n")[0]
        cpu_info = cpu_line.split()
        return True, cpu_info

    def getCpuUsage(self):
        '''
        CPU时间占用率计算公式：(一段时间内的cpu占用率 (1-idle)/total)
            total = total2 - total1
            idle = idle2 - idle1
            cpu_usage = (total - idle)/total * 100
        :return:
        '''
        result, cpu_info = self.getCpuInfo()
        if not result:
            return False, cpu_info
        idle1 = int(cpu_info[4]) + int(cpu_info[5])
        total1 = sum(int(i) for i in cpu_info[1:])
        #diff时间为0.5s
        time.sleep(0.5)
        result, cpu_info2 = self.getCpuInfo()
        idle2 = int(cpu_info2[4]) + int(cpu_info2[5])
        total2 = sum(int(j) for j in cpu_info2[1:])
        cpu_usage = 100- 100*(idle2 - idle1)/((total2-total1)*1.0)
        return True, cpu_usage

    def getBatteryInfo(self, search=None):
        '''
        获取电量值: dumpsys battery
        :return:
        '''
        result,battery_info = self.shell("dumpsys battery")
        if not result:
            return False, "dumpsys battery failed"
        if search is None:
            return True, battery_info.split("\r\r\n")
        info = battery_info.split("\r\r\n")
        for list in info:
            pos = list.find(search)
            if pos>=0:
                return list[pos+len(search):]

    def getBatteryLevel(self):
        return self.getBatteryInfo('level:')

    def getBatteryHealthStatus(self):
        '''
        获取电池健康状态
        1: BATTERY_HEALTH_UNKNOWN 未知
        2: BATTERY_HEALTH_GOOD 状态良好
        3：BATTERY_HEALTH_OVERHEAT 电池过热
        4: BATTERY_HEALTH_DEAD 没有电了
        5： BATTERY_HEALTH_OVER_VOLTAGE 电池电压过高
        6：BATTERY_HEALTH_UNSPECIFIED_FAILURE
        :return:
        '''
        return self.getBatteryInfo('health:')

    def getBatteryStatus(self):
        '''
        获取电池健康状态
        1: BATTERY_STATUS_UNKNOWN 未知
        2: BATTERY_STATUS_CHARGING 充电中
        3：BATTERY_STATUS_DISCHARGING 放电中
        4: BATTERY_STATUS_NOT_CHARGING 未充电
        5： BATTERY_STATUS_FULL 已充满
        :return:
        '''
        return self.getBatteryInfo('status:')

    def getFPSInfo(self):
        '''
        !!!需要root权限
        https://android.googlesource.com/platform/frameworks/native/+/f67623632a545bd9ca1d8afefc3dd0789eaba6b3/services/surfaceflinger/SurfaceFlinger.cpp#2508
        service call SurfaceFlinger 1013
        计算公式
        surface_after-surface_before/time_diff
        :return:
        '''
        result, fps_info = self.shell("service call SurfaceFlinger 1013")
        assert result==True
        match = re.search('^Result: Parcel\((\w+)', fps_info[0])
        cur_surface = 0
        if not match:
            raise Exception(fps_info)
        cur_surface = int(match.group(1), 16)
        return {
            'page_flip_count': cur_surface,
            'timestamp': time.time()
        }

    def getFPS(self):
        '''
        计算FPS
        :return:
        '''
        surface_before = self.getFPSInfo()
        time.sleep(1)
        surface_after = self.getFPSInfo()
        return (surface_after['page_flip_count'] - surface_before['page_flip_count'])/1.0


if __name__ == "__main__":
    adb=AdbHelper()
    b = adb.getConnectDevices()
    print b