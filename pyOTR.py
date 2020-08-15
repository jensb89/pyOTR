import os
import subprocess
from Src.cutlists import CutlistDownloader, CutlistReader
from Src.decoder import OTRDecoder, OTRDecoderArmv7
from Src.system import SystemInfo 
from Src.videoTools import VideoTool, Cut, AVCut
import config
import argparse
from Utils.OtrRenameForTvShows.otr_rename import OTR_Rename
import sys
import logging
from datetime import datetime

## LOGGING
# create logger
mainlogger = logging.getLogger('pyOTR')
mainlogger.setLevel(logging.INFO)

# create file handler which logs even debug messages
if config.enableFileLogging:
    fh = logging.FileHandler(config.LOGDIR + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") +'.log')
    fh.setLevel(logging.INFO)

    # add the handlers to the logger
    mainlogger.addHandler(fh)

class pyOTR(object):

    DOWNLOADDIR = "" # class variable shared by all instances
    DECODIR = ""    # class variable shared by all instances
    WORKDIR = os.getcwd() + '/'

    def __init__(self, useFolder=False, useFile=False, fileName = ''):
        # Init process. Print system infos and initialize folders and settings
        self.logger = logging.getLogger('pyOTR')
        self.logger.debug('Logging started.')

        self.system = SystemInfo()
        self.system.printSystemInfos()
        self.logger.info("\n")
        self.logger.info("Working directory:\t" + self.WORKDIR)
        self.logger.info("Donwload directory:\t" + self.DOWNLOADDIR)
        self.logger.info("Decode Directory:\t" + self.DECODIR)
        self.logger.info("Log Directory:\t\t\n" + self.DECODIR + 'Log/')
        self.logger.info("FFMPEG Info:\n")
        try:
            out = subprocess.check_output(["ffmpeg","-version"])
            self.logger.info(out)
        except OSError:
            self.logger.warn("ffmpeg was not found! Make sure ffmpeg is installed in order to cut videos!")
        
        self.logger.info("FFProbe Info:\n")
        try:
            out = subprocess.check_output(["ffprobe","-version"])
            self.logger.info(out)
        except OSError:
            self.logger.warn("ffprobe was not found! Some features might not work.")

        # Check for file or folder usage:
        if useFolder and useFile:
            self.logger.error("Either use pyOTR on a file or on a folder.")
            return
        elif useFolder and not(useFile):
            self.useFolder = True
            self.useFile = False
        elif not(useFolder) and useFile:
            self.useFile = True
            self.useFolder = False
            if fileName != '':
                self.fileName = fileName
            else:
                self.logger.error("FileName not given!")
                return
        else:
            self.logger.error("Specify if a file or folder shall be evaulated.")
            return
        
        ## Set Bin paths
        if self.system.systemOS == "Darwin":
            VideoTool.BinDirectory = "Bin/Mac/"
            OTRDecoder.BINDIRECTORY = "Bin/Mac/"
        elif self.system.systemOS == "Linux" and self.system.machine == 'armv7':
            VideoTool.BinDirectory = "Bin/armv7/"

    def decode(self):
        # decode the otrkey files
        if self.system.systemOS == "Linux":
            self.decoder = OTRDecoderArmv7()
        elif self.system.systemOS == "Darwin":
            self.decoder = OTRDecoder()
        else:
            self.logger.error("Error: No decoder matches your system: %s." % self.system.systemOS)

        if self.useFolder:
            self.logger.debug("decode folder...\n")
            self.decoder.setOutputFolder(self.DECODIR)
            self.decoder.decodeOTRFolder(self.DOWNLOADDIR)
        if self.useFile:
            self.logger.debug("decode file...\n")
            self.decoder.decodeOTRFile(self.fileName)

    def cutSingleFile(self, fileName, download=True, cutlistFile="", saveCutlist=False):
        #cut a decoded video file
        if download:
            #Load Cutlist
            c = CutlistDownloader(fileName)
            ret = c.search(mode='name')
            if ret == 1:
                # No cutlists found
                return
            c.sort_cutlists()
            ret = c.download(toprated=True, saveToFile=saveCutlist)

            self.cutList = CutlistReader(c.cutlist)
        else:
            self.cutList = CutlistReader(cutlistFile)

        self.cutList.parseCutlist()

        self.cutter = AVCut(fileName, self.cutList)
        self.cutter.convertCutTimes()
        self.cutter.cut()

    def cut(self, download=True, cutlistFile="", saveCutlist=False):
        # cut the decoded video file
        if self.useFile:
            self.cutSingleFile(self.fileName, download=download, cutlistFile=cutlistFile, saveCutlist=saveCutlist)

        if self.useFolder:
            #loop through folder
            for filename in os.listdir(self.DECODIR):
                if filename.endswith(".avi"):
                    self.cutSingleFile(self.DECODIR + filename, download=download, cutlistFile=cutlistFile, saveCutlist=saveCutlist)
                    continue
                else:
                    continue

    def renameFiles(self):
        # Batch renaming decoded otr video files in the format SeriesName.S01E02.EpisodeName.avi
        self.logger.info("Renaming decoded otr video files in the format SeriesName.S01E02.EpisodeName.avi:\n")

        files = [f for f in os.listdir(Cut.CUTDIR) if f.endswith('.avi')]

        for filename in files:
            print filename
            tv_show = OTR_Rename(os.path.join(Cut.CUTDIR,filename))
            tv_show.copy_and_sort()

if __name__ == "__main__":
    pyOTR.DOWNLOADDIR = config.DOWNLOADDIR
    pyOTR.DECODIR = config.DECODIR
    Cut.frameOffset = config.frameOffset
    Cut.CUTDIR = config.CUTDIR
    OTRDecoder.USERNAME = config.OTRMAIL
    OTRDecoder.PASSWORD = config.OTRPW
    #VideoTool.BinDirectory = "Bin/Mac/"

    ### Argument parser ###
    parser = argparse.ArgumentParser(prog="pyOtr", description='Process and decoded otrkey files and cut the decoded video files.')
    parser.add_argument('--single-file', metavar="fileName", help="deocde, cut and sort single file")
    parser.add_argument('--decode-only', help="only decoding, no cut, no sort", action='store_true')
    parser.add_argument('--cut-only', help="only cutting, cutlist is automatically downloaded", action='store_true')
    parser.add_argument('--save-cutlist', help="-stores the cutlist used for cutting the video file", action='store_true')
    parser.add_argument('--cutlist-file', metavar="cutlistFile", help="If this option is used, a manual cutlist file can be used. Otherwise the best cutlist available from cutlist.at will be used instead.")
    parser.add_argument('--no-file-rename', help="do not try to rename the file with the season and episode information", action='store_true')
    args = parser.parse_args()

    if args.single_file == None:
        otr = pyOTR(useFolder=True)
    else:
        otr = pyOTR(useFile=True, fileName=args.single_file)

    if not args.cut_only:
        otr.logger.debug("decoding...\n") 
        otr.decode()

    if args.cutlist_file == None:
        cutFile = ""
        useCutfile = False
    else:
        cutFile = args.cutlist_file
        useCutfile = True
    
    if not args.decode_only:
        otr.cut(download=not(useCutfile), cutlistFile=cutFile, saveCutlist=args.save_cutlist)

    if not args.no_file_rename:
        otr.renameFiles()