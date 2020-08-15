import subprocess
import os
import logging

class OTRDecoder(object):
    
    BACKUPFOLDER = ""
    BINDIRECTORY = ""
    USERNAME = ""
    PASSWORD = ""

    def __init__(self, deleteOTRFile=True):
        self.deleteOTRFile = deleteOTRFile
        self.outputFolder = '.'
        self.decoderName = 'otrdecoder'
        self.logger = logging.getLogger('pyOTR.decoder')

    def setOutputFolder(self, outputFolder):
        self.outputFolder = outputFolder
    
    def decodeOTRFile(self, fileName):
        self.logger.info("\n\t ==> Decoding file %s with %s" % (fileName, self.BINDIRECTORY+self.decoderName))
        commandStr = [self.BINDIRECTORY+self.decoderName,'-i',fileName,"-e",self.USERNAME,"-p",self.PASSWORD,"-o",self.outputFolder]
        try:
            out = subprocess.check_output(commandStr)
            self.logger.debug(out)
            self.logger.info("\t ==> Success!\n")
            ret = 0
            if self.deleteOTRFile:
                os.remove(fileName)
        except subprocess.CalledProcessError as err:
            self.logger.info("\t ==> Failed!\n")
            self.logger.error("%s" % err)
            ret = err.returncode
        # TODO:
        # move OTRkey file to BACKUPFOLDER if file successfully decoded (check if decoded file exists) or delete otrkey file
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
    def __init__(self, deleteOTRFile=False):
        super(OTRDecoderArmv7, self).__init__(deleteOTRFile)
        #os.environ['LD_LIBRARY_PATH'] = path to curl librarys #set for the time of execution
        self.decoderName = "otrArmv7Decoder"

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
        
        decoder = OTRDecoder()
        decodedFile = decoder.decodeOTRFile(self.data[self.index])
        self.index = self.index + 1
        return decodedFile