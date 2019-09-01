from cutlists import Cutlist

class Test(object):
    
    def __init__(self):
        self.cutlist = Cutlist("some_movie.avi",0)


t = Test()
print t.cutlist.filename