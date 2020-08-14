import subprocess
import os

class OTRDecoder(object):
    
    BACKUPFOLDER = ""
    BINDIRECTORY = ""
    USERNAME = ""
    PASSWORD = ""

    def __init__(self, deleteOTRFile=False):
        self.deleteOTRFile = deleteOTRFile
        self.outputFolder = '.'

    def setOutputFolder(self, outputFolder):
        self.outputFolder = outputFolder
    
    def decodeOTRFile(self, fileName):
        commandStr = [self.BINDIRECTORY+'otrdecoder','-i',fileName,"-e",self.USERNAME,"-p",self.PASSWORD,"-o",self.outputFolder]
        #print "Calling " + ' '.join(commandStr)
        ret = subprocess.check_output(commandStr)
        print ret
        # TODO:
        # move OTR file to BACKUPFOLDER if file successfully decoded (check if decoded file exists) // should be moved by the -o tag
        # move decoded OTR file to DECODIR
        return ret
    
    def decodeOTRFolder(self, folder):
        # go trhough all files in folder
        ret = -1
        for filename in os.listdir(folder):
            if filename.endswith(".otrkey"):
                ret = self.decodeOTRFile(folder + filename)
                continue
            else:
                continue
        return ret

class OTRDecoderArmv7(OTRDecoder):
    def __init__():
        super(OTRDecoder, self).__init__()
        #os.environ['LD_LIBRARY_PATH'] = path to curl librarys #set for the time of execution
        self.decoder = "otrArmv7Decoder"

class OTRDecoderBatch(object):
    # Takes list of files, returns string of decoded file in iteration
    def __init__(self, files):
        self.data = files
        self.numFiles = len(files)
        self.index = 0

    def __iter__(self):
        return self
    
    def next(self):
        if self.index == self.numFiles:
            raise StopIteration
        
        decodedFile = OTRDecoder(self.data[self.index]).decodeOTRFile()
        self.index = self.index + 1
        return decodedFile