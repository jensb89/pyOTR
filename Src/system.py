from __future__ import print_function
import platform
import re
import subprocess
import os


class SystemInfo(object):
    def __init__(self):
        (system, node, release, version, machine, processor) = platform.uname()
        self.systemOS = system
        self.node = node
        self.release = release
        self.version = version
        self.machine = machine
        self.processor = processor
        self.user = os.getlogin()
    
    def printSystemInfos(self):
        print("User:\t\t%s" % self.user)
        print("System OS:\t%s" % self.systemOS)
        print("Name:\t\t%s" % self.node)
        print("Machine:\t%s" % self.machine)
        print("Version:\t%s" % self.version)
        print("RAM:")
        self.printRam()


    def printRam(self):
        if self.systemOS == "Darwin":
            self.printRamDarwin()
        elif self.systemOS == "Linux":
            self.printRamLinux()

    def printRamLinux(self,indentTabs=2):
        output = subprocess.check_output(["free", "-m"])
        p = re.compile('Mem:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')
        (total,used,free,shared,buff,availabe) = p.findall(output)[0]
        
        print(indentTabs*"\t" + 'Total Memory:\t\t%s MB' % total)
        print(indentTabs*"\t" + 'Used Memory:\t\t%s MB' % used)
        print(indentTabs*"\t" + 'Free Memory:\t\t%s MB' % free)
        print(indentTabs*"\t" + 'Shared Memory:\t\t%s MB' % shared)
        print(indentTabs*"\t" + 'Availabe Memory:\t%s MB' % availabe)

    def printRamDarwin(self,indentTabs=2):
        # Ram under MacOS
        # https://apple.stackexchange.com/questions/4286/is-there-a-mac-os-x-terminal-version-of-the-free-command-in-linux-systems
        # Get process info
        ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0].decode()
        vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode()

        # Iterate processes
        processLines = ps.split('\n')
        sep = re.compile('[\s]+')
        rssTotal = 0 # kB
        for row in range(1,len(processLines)):
            rowText = processLines[row].strip()
            rowElements = sep.split(rowText)
            try:
                rss = float(rowElements[0]) * 1024
            except:
                rss = 0 # ignore...
            rssTotal += rss

        # Process vm_stat
        vmLines = vm.split('\n')
        sep = re.compile(':[\s]+')
        vmStats = {}
        for row in range(1,len(vmLines)-2):
            rowText = vmLines[row].strip()
            rowElements = sep.split(rowText)
            vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

        print(indentTabs*"\t" + 'Wired Memory:\t\t%d MB' % ( vmStats["Pages wired down"]/1024/1024 ))
        print(indentTabs*"\t" + 'Active Memory:\t\t%d MB' % ( vmStats["Pages active"]/1024/1024 ))
        print(indentTabs*"\t" + 'Inactive Memory:\t%d MB' % ( vmStats["Pages inactive"]/1024/1024 ))
        print(indentTabs*"\t" + 'Free Memory:\t\t%d MB' % ( vmStats["Pages free"]/1024/1024 ))
        print(indentTabs*"\t" + 'Real Mem Total (ps):\t%.3f MB' % ( rssTotal/1024/1024 ))

#test = SystemInfo()
#test.printSystemInfos()
