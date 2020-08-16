import subprocess
import os
import logging
from shutil import move

class VideoTool(object):
	BinDirectory = 'Bin/'
	LibDirectory = 'Lib/'

class Cut(VideoTool):

	frameOffset = 0
	CUTDIR = ''

	def __init__(self, filename, cutReaderObject):
		self.filename = filename
		self.cutReaderObject = cutReaderObject
		self.cutTimes = [] #array for each cutting timestamp
		self.logger = logging.getLogger('pyOTR.Cut')
	
	#@abstractmethod
	
	def cut(self):
		return


class AVCut(Cut):

	# Start cutting with avcut
	def cut(self):
		#command = "avcut" + self.timeString + ' -'
		self.logger.info("Cut file %s with FrameOffset %d" % (self.filename, self.frameOffset))
		if len(self.cutTimes) == 0:
			self.logger.error("AVCut Error: No cuts found. Run convertCutTimes first!")
			return
		path, fileName = os.path.split(self.filename)
		fileNameCut, extension = os.path.splitext(fileName)
		fileNameCut = fileNameCut + '-cut' + extension
		#todo: check for avcut version. Version 0.2 does not support -i and -o, but just avcut inputfile outputfile cuts!
		commandStr = [self.BinDirectory+'avcut','-i',self.filename,'-o',self.CUTDIR+fileNameCut]
		for cutTime in self.cutTimes:
			commandStr.append("%.3f" % cutTime)
		commandStr.append('-')
		self.logger.info("Calling " + ' '.join(commandStr))
		ret = subprocess.call(commandStr)
		self.logger.info("AVCut exits with code %d\n" % ret)
		if (ret==0):
			if not(os.path.isdir(self.CUTDIR + '#recycle/')):
				os.mkdir(self.CUTDIR + '#recycle')
			move(self.filename, self.CUTDIR + '#recycle')


	# Convert the times from the cutlists so that they can be used with avcut
	# Mode is either "Time" or "Frames"
	def convertCutTimes(self, mode="Time"):
		times = [0]
		if mode=="Time":
			framediff = 1/self.cutReaderObject.fps #time difference of one frame
			for (cut,duration) in zip(self.cutReaderObject.cutsTime, self.cutReaderObject.cutsDuration):
				newStartTime = float(cut) + self.frameOffset*framediff
				times.append(newStartTime)
				newEndTime = float(duration) + newStartTime + self.frameOffset*framediff
				#print "%.3f" % newTimesEnde
				times.append(newEndTime)

		if mode=="Frames":
			fps = self.cutReaderObject.fps

			for (cut,duration) in zip(self.cutReaderObject.cutsFrame,self.cutReaderObject.cutsFrameDuration):
				newTimeStart = (float(cut)+self.frameOffset)/fps
				times.append(newTimeStart)
				newTimesEnde = (float(duration)+float(cut)+self.frameOffset)/fps
				times.append(newTimesEnde)
		
		self.cutTimes = times


	

