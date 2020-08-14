import xml.etree.ElementTree as ET
import urllib2
import os
from shutil import move
import re


class CutlistDownloader(object):
	"""docstring for Cutlist"""
	___SERVER___ = 'http://cutlist.at/'

	def __init__(self, filename, filesize = 0):
		super(CutlistDownloader, self).__init__()
		#Strip path from filename first
		head, tail = os.path.split(filename)
		self.filename = tail
		self.filesize = filesize
	
	def search(self,mode='size'):
		if mode=='ofsb' and self.filesize > 1:
			url_str = self.___SERVER___ + 'getxml.php?version=0.9.8.0&'+mode+'='+str(self.filesize)
		else:
			url_str = self.___SERVER___ + 'getxml.php?version=0.9.8.0&'+mode+'='+self.filename
		print url_str
		file = urllib2.urlopen(url_str)
		data = file.read()
		file.close()

		if data == '':
			print 'No Cutlist found'
			self.data_cl_search = []
			return 1

		root = ET.fromstring(data)
		num_lists = len(root.findall('cutlist'))
		print str(num_lists) + ' Cutlist(s) found.'

		data_cl = []
		for elem in root.findall('cutlist'):
			rating_author = elem.find('ratingbyauthor').text
			rating = elem.find('rating').text
			if rating is None:
				rating = 0
			author = elem.find('author').text
			dl_count = elem.find('downloadcount').text
			id = elem.find('id').text
			name = elem.find('name').text

			data_cl.append({'rating_author':rating_author,'rating':rating,'author':author,'dl_count':dl_count,'id':id,'name':name})

		self.data_cl_search = data_cl
		return 0

	def sort_cutlists(self):
		#print self.data_cl_search
		newlist = sorted(self.data_cl_search, key=lambda k: (float(k['rating']),float(k['rating_author']),float(k['dl_count'])),reverse=True) 
		self.sorted_list = newlist

		return newlist

	def download(self,toprated=True,saveToFile=True,folder=''):
		if toprated == True and len(self.sorted_list)>0:
			print 'Download cutlist:'
			if self.sorted_list[0]['author'] is not None:
				print 'Author:' + self.sorted_list[0]['author'].encode('utf-8','ignore')
			print 'Rating:' + str(self.sorted_list[0]['rating'])
			print 'Rating Author:' + str(self.sorted_list[0]['rating_author'])
			print 'Downloadcount:' + str(self.sorted_list[0]['dl_count'])
			response = urllib2.urlopen(self.___SERVER___+'getfile.php?id=' + self.sorted_list[0]['id'])
			cutlist = response.read()
			self.cutlist = cutlist

			if saveToFile:
				with open(self.filename + '.cutlist','wb') as output:
					output.write(cutlist)
				if os.path.isdir(folder):
					move(self.filename + '.cutlist', folder + self.filename + '.cutlist')
					print 'Moved file to ' + folder + self.filename + '.cutlist'
				else:
					print folder + ' does not exist!'
			return 0
		else:
			return 1


class CutlistReader(object):
	def __init__(self, cutlist):
		self.cutlist = cutlist
		self.formatFrames = False
		self.formatTime = False
	
	def loadCutlistFile(self):
		with open(self.cutlist, 'r') as myfile:
			self.data = myfile.read()
	
	def parseCutlist(self):
		#check if input is file or string
		if self.cutlist[-8:] == '.cutlist':
			self.loadCutlistFile()
		else:
			self.data = self.cutlist

		data = self.data
		self.fps = float(re.findall("FramesPerSecond=(\d+\.*\d*)", data)[0])
		self.numCuts = int(re.findall("NoOfCuts=(\d*)", data)[0])
		self.suggestedName = re.findall("SuggestedMovieName=(.+)", data)[0]

		self.cutsTime =  re.findall("Start=(\d+\.?\d*)", data)
		self.cutsDuration = re.findall("Duration=(\d+\.?\d*)", data)
		self.cutsFrame = re.findall("StartFrame=(\d+\.?\d*)", data)
		self.cutsFrameDuration = re.findall("DurationFrames=(\d+\.?\d*)", data)

		#TODO: NEEDS SORTING (cut5 might be first cut etc)

		if (len(self.cutsTime) > 0)  and (len(self.cutsTime) == len(self.cutsDuration) ):
			self.formatTime = True

		if (len(self.cutsFrame) > 0)  and (len(self.cutsFrame) == len(self.cutsFrameDuration) ):
			self.formatFrames = True
		
		if not self.formatFrames and not self.formatTime:
			print "Error in parsing Cutlist file!"
			raise