import subprocess
import os

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
	
	#@abstractmethod
	
	def cut(self):
		return


class AVCut(Cut):

	# Start cutting with avcut
	def cut(self):
		#command = "avcut" + self.timeString + ' -'
		print "Cut file %s with FrameOffset %d" % (self.filename, self.frameOffset)
		if len(self.cutTimes) == 0:
			print "AVCut Error: No cuts found. Run convertCutTimes first!"
			raise
		path, fileName = os.path.split(self.filename)
		fileNameCut, extension = os.path.splitext(fileName)
		fileNameCut = fileNameCut + '-cut' + extension
		commandStr = [self.BinDirectory+'avcut','-i',self.filename,'-o',self.CUTDIR+fileNameCut]
		for cutTime in self.cutTimes:
			commandStr.append("%.3f" % cutTime)
		commandStr.append('-')
		print "Calling " + ' '.join(commandStr)
		ret = subprocess.call(commandStr)
		print "AVCut exits with code %d" % ret

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


	

