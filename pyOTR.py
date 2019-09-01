import os
import subprocess
from Src.cutlists import CutlistDownloader, CutlistReader
from Src.decoder import OTRDecoder, OTRDecoderArmv7
from Src.system import SystemInfo 
from Src.videoTools import VideoTool, Cut, AVCut
import config

class pyOTR(object):

    DOWNLOADDIR = "" # class variable shared by all instances
    DECODIR = ""  # class variable shared by all instances
    WORKDIR = os.getcwd() + '/'

    def __init__(self, useFolder=False, useFile=False, fileName = ''):
        # something 
        self.system = SystemInfo()
        self.system.printSystemInfos()
        print "\n"
        print "Working directory:\t" + self.WORKDIR
        print "Donwload directory:\t" + self.DOWNLOADDIR
        print "Decode Directory:\t" + self.DECODIR
        print "Log Directory:\t\t" + self.DECODIR + 'Log/'
        #out = subprocess.check_output(["path/ffmpeg","-version"])
        #print "ffmpeg: Version"

        # Check for file or folder usage:
        if useFolder and useFile:
            print "Either use pyOTR on a file or on a folder."
            raise
        elif useFolder and not(useFile):
            self.useFolder = True
            self.useFile = False
        elif not(useFolder) and useFile:
            self.useFile = True
            self.useFolder = False
            if fileName != '':
                self.fileName = fileName
            else:
                print "FileName not given"
                raise
        else:
            print "Specify if a file or folder shall be evaulated."
            raise
        
        ## Set Bin paths
        if self.system.systemOS == "Darwin":
            VideoTool.BinDirectory = "Bin/Mac/"
            OTRDecoder.BINDIRECTORY = "Bin/Mac/"
        elif self.system.systemOS == "Linux" and self.system.machine == 'armv7':
            VideoTool.BinDirectory = "Bin/armv7/"

    
    def decode(self):
        # something
        if self.system.systemOS == "Linux":
            self.decoder = OTRDecoderArmv7()
        elif self.system.systemOS == "Darwin":
            self.decoder = OTRDecoder()
        else:
            print "Error: No decoder matches your system: %s." % self.system.systemOS

        if self.useFolder:
            self.decoder.setOutputFolder(self.DOWNLOADDIR)
            self.decoder.decodeOTRFolder(self.DOWNLOADDIR)
        if self.useFile:
            self.decoder.decodeOTRFile(self.fileName)


    def cut(self, download=True, cutlistFile=""):
        if download:
            #Load Cutlist
            c = CutlistDownloader(self.fileName)
            ret = c.search(mode='name')
            if ret == 1:
                # No cutlists found
                return
            c.sort_cutlists()
            ret = c.download(toprated=True, saveToFile=False)

            self.cutList = CutlistReader(c.cutlist)
        else:
            self.cutList = CutlistReader(cutlistFile)

        self.cutList.parseCutlist()

        self.cutter = AVCut(self.fileName, self.cutList)
        self.cutter.convertCutTimes()
        self.cutter.cut()

    
    def organizeFiles(self):
        print "Do something"


    def test(self):
        test = CutlistReader("Src/flash.cutlist")
        test.parseCutlist()
        print test.formatFrames
        print test.formatTime
        print test.fps

        Cut.frameOffset = 1 #static variable
        cutter = AVCut("somefile.Avi",test)
        cutter.convertCutTimes()
        cutter.cut()



if __name__ == "__main__":
    pyOTR.DOWNLOADDIR = config.DOWNLOADDIR
    pyOTR.DECODIR = config.DECODIR
    Cut.frameOffset = config.frameOffset
    Cut.CUTDIR = config.CUTDIR
    #VideoTool.BinDirectory = "Bin/Mac/"

    # Only cut single already decoded file
    #otr = pyOTR(useFile=True, fileName='The_100__The_Blood_of_Sanctum_19.08.06_21-00_uswpix_60_TVOON_DE.mpg.HQ.avi')
    #otr.cut()

    # Cut Folder
    #otr = pyOTR(useFolder=True)
    #otr.decode()
    #otr.cut()

    # Cut with cutfile
    cutfile = "Marvel_s_Agents_of_S_H_I_E_L_D___The_Sign_New_Life_19.08.02_20-00_uswabc_121_TVOON_DE.mpg.HQ.avi.cutlist"
    otr =  pyOTR(useFile=True, fileName='Marvel_s_Agents_of_S_H_I_E_L_D___The_Sign_New_Life_19.08.02_20-00_uswabc_121_TVOON_DE.mpg.HQ.avi')
    otr.cut(download=False, cutlistFile=cutfile)


    # TODO: Command options
    # pyOTR w/o paraemter - look in DownloadDir, deocde all, cut all, sort all
    # --single file FILE  - deocde, cut and sort single file
    # --deocde-only  -only decoding, no cut, no sort
    # --cut-only  -only cutting, cutlist is automatically downloaded
    # --download-cutlist -stores the cutlist used for cutting the video file 


    

#test = CutlistReader("Src/flash.cutlist")
#test.parseCutlist()
#print test.formatFrames
#print test.formatTime
#print test.fps

#Cut.frameOffset = 1 #static variable
#cutter = AVCut("somefile.Avi",test)
#cutter.convertCutTimes()
#cutter.cut()

#pyOTR("test.avi").checkForNewFiles().cutFile()
#pyOTR.DOWNLOADDIR = '/Downloads/'
#pyOTR.DECODIR = '/decoded/'
#VideoTool.BinDirectory = 'Bin/Mac/'
#Cut.frameOffset = 1

#otr = pyOTR(useFolder=True)
#print otr.DOWNLOADDIR
#print otr.DECODIR
#otr.test()

#Idea :Single File
#otr = pyOTR(file="test.avi") #constructor checks system, sets internal variables
#otr.decode() #the right decode is automatically chosen
#otr.cut(deleteFiles=True)
#otr.rename()

#Idea: Folder
#otr = pyOtr(folder="/")
#otr.decode()
#otr.cut()
#otr.rename()