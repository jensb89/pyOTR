from __future__ import print_function
import platform
import re
import subprocess
import os
import logging


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
        self.logger = logging.getLogger('pyOTR.system')
    
    def printSystemInfos(self):
        self.logger.info("User:\t\t%s" % self.user)
        self.logger.info("System OS:\t%s" % self.systemOS)
        self.logger.info("Name:\t\t%s" % self.node)
        self.logger.info("Machine:\t%s" % self.machine)
        self.logger.info("Version:\t%s" % self.version)
        self.logger.info("RAM:")
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
        
        self.logger.info(indentTabs*"\t" + 'Total Memory:\t\t%s MB' % total)
        self.logger.info(indentTabs*"\t" + 'Used Memory:\t\t%s MB' % used)
        self.logger.info(indentTabs*"\t" + 'Free Memory:\t\t%s MB' % free)
        self.logger.info(indentTabs*"\t" + 'Shared Memory:\t\t%s MB' % shared)
        self.logger.info(indentTabs*"\t" + 'Availabe Memory:\t%s MB' % availabe)

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

        self.logger.info(indentTabs*"\t" + 'Wired Memory:\t\t%d MB' % ( vmStats["Pages wired down"]/1024/1024 ))
        self.logger.info(indentTabs*"\t" + 'Active Memory:\t\t%d MB' % ( vmStats["Pages active"]/1024/1024 ))
        self.logger.info(indentTabs*"\t" + 'Inactive Memory:\t%d MB' % ( vmStats["Pages inactive"]/1024/1024 ))
        self.logger.info(indentTabs*"\t" + 'Free Memory:\t\t%d MB' % ( vmStats["Pages free"]/1024/1024 ))
        self.logger.info(indentTabs*"\t" + 'Real Mem Total (ps):\t%.3f MB' % ( rssTotal/1024/1024 ))

#test = SystemInfo()
#test.printSystemInfos()
